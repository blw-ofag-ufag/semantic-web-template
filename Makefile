# ==============================================================================
# CONFIG
# ==============================================================================

# Directories
BUILD_DIR        := build
RDF_DIR          := $(BUILD_DIR)/rdf
PYTHON_DIR       := src/python

# Tools and binaries
PYTHON           ?= $(shell command -v python3 || command -v python)
VENV             ?= venv
VENV_BIN         := $(VENV)/bin
VENV_PYTHON      := $(VENV_BIN)/python
VENV_PIP         := $(VENV_BIN)/pip
PYSHACL          := $(VENV_BIN)/pyshacl
PYTEST           := $(VENV_BIN)/pytest -p no:cacheprovider # suppress cache

# Inputs
ONTO             := src/rdf/ontology/model.owl.ttl
DATA             := $(wildcard src/rdf/data/*.ttl)
SHAPES           := src/rdf/shapes/model.shacl.ttl
CONFIG           := project.yml
CONFIG_SCRIPT    := src/python/utils/project_config.py
PREFIXES         := src/rdf/prefixes.ttl
RULES            := $(sort $(wildcard src/sparql/inference/*.rq))
QUERIES          := $(sort $(wildcard src/sparql/processing/*.rq))
PIPELINE_SCRIPTS := $(sort $(wildcard src/python/pipeline/*.py))

# Intermediate & Output Files
METADATA         := $(RDF_DIR)/metadata.ttl
FETCHED_DATA     := $(RDF_DIR)/00-integrated.ttl
MERGED_DATA      := $(RDF_DIR)/01-merged.ttl
INFERRED_DATA    := $(RDF_DIR)/02-inferred.ttl
PROCESSED_DATA   := $(RDF_DIR)/03-processed.ttl
SHACL_REPORT     := $(RDF_DIR)/04-shacl-report.ttl
DOCS_DIR         := docs
QUARTO_METADATA  := $(DOCS_DIR)/_project.yml

# Values of the project configuration, read when a recipe runs (the virtual
# environment does not exist yet when Make reads this file). They can be
# overridden on the command line, e.g. to publish to another endpoint.
LINDAS_GRAPH       = $$($(VENV_PYTHON) $(CONFIG_SCRIPT) get lindas.graph)
LINDAS_GRAPH_STORE = $$($(VENV_PYTHON) $(CONFIG_SCRIPT) get lindas.graph-store)

# Logs
LOG_DIR          := $(BUILD_DIR)/log
SHACL_LOG        := $(LOG_DIR)/01-shacl.log
QUARTO_LOG       := $(LOG_DIR)/02-quarto.log

# Colors for logging
RED              := \033[0;31m
GREY             := \033[0;90m
BOLD       := \033[1;37m
NC               := \033[0m

.PHONY: all help check test docs clean check-python venv install-dependencies setup build delete publish check-publication generate-shacl-docs generate-glossary-docs

# A failed recipe must not leave a half-written target behind
.DELETE_ON_ERROR:

# Default target
all: test docs ## Run the tests and build the documentation (default)

# ==============================================================================
# HELP
# ==============================================================================

# Lists every target that carries a "## description" after its rule line.
help: ## Show this help
	@printf "$(BOLD)Usage:$(NC) make <target>\n\n$(BOLD)Targets:$(NC)\n"
	@grep -hE '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "} {printf "  $(BOLD)%-24s$(NC) %s\n", $$1, $$2}'
	@printf "\nThe default target is $(BOLD)all$(NC). The project is configured in $(CONFIG). Publishing requires LINDAS_USER and LINDAS_PASSWORD in .env.\n"

# ==============================================================================
# SETUP
# ==============================================================================

# 1. Check python interpreter
check-python:
	@command -v $(PYTHON) >/dev/null 2>&1 || \
		(printf "$(RED)ERROR: Python interpreter not found.$(NC)\n"; exit 1)

# 2. Set up virtual environment
$(VENV_PYTHON):
	@command -v $(PYTHON) >/dev/null 2>&1 || \
		(printf "$(RED)ERROR: Python interpreter not found.$(NC)\n"; exit 1)
	@$(PYTHON) -m venv $(VENV)
	@printf "$(GREY)"; $(VENV_PYTHON) -m pip install --upgrade pip || { printf "$(NC)"; exit 1; }; printf "$(NC)"

venv: $(VENV_PYTHON)

# 3. Install python dependencies
$(VENV)/.requirements-installed.stamp: $(PYTHON_DIR)/requirements.txt | $(VENV_PYTHON)
	@printf "$(GREY)"; $(VENV_PIP) install -q -r $(PYTHON_DIR)/requirements.txt || { printf "$(NC)"; exit 1; }; printf "$(NC)"
	@touch $@

install-dependencies: $(VENV)/.requirements-installed.stamp

# 4. Full setup
setup: install-dependencies ## Create the virtual environment and install the Python dependencies
	@printf "$(BOLD)[*] Setup complete.$(NC)\n"

# ==============================================================================
# RDF DATA INTEGRATION, INFERENCE AND POST-PROCESSING
# ==============================================================================

# 1. Set up directories
$(RDF_DIR) $(LOG_DIR):
	@mkdir -p $@

# 2. Describe the named graph as a dataset, from the project configuration
$(METADATA): $(CONFIG) $(CONFIG_SCRIPT) $(PREFIXES) | $(RDF_DIR) $(VENV)/.requirements-installed.stamp
	@printf "$(BOLD)[*] Generating the dataset description...$(NC)\n"
	@$(VENV_PYTHON) $(CONFIG_SCRIPT) metadata -o $(METADATA) -p $(PREFIXES)

# 3. Fetch, Query, and Transform source data sequentially
$(FETCHED_DATA): $(PIPELINE_SCRIPTS) | $(RDF_DIR) $(LOG_DIR) $(VENV)/.requirements-installed.stamp
	@printf "$(BOLD)[*] Running data integration pipelines...$(NC)\n"
	@printf "$(GREY)"; \
	if [ -n "$(PIPELINE_SCRIPTS)" ]; then \
		for script in $(PIPELINE_SCRIPTS); do \
			echo "Executing $$script..."; \
			$(VENV_PYTHON) "$$script" --output $(FETCHED_DATA) || { printf "$(NC)"; exit 1; }; \
		done; \
	else \
		echo "No pipeline scripts found. Creating empty data file."; \
		touch $(FETCHED_DATA); \
	fi; \
	printf "$(NC)"

# 4. Check that all turtle files are syntactically valid
$(LOG_DIR)/syntax-check.stamp: $(DATA) $(ONTO) $(SHAPES) $(METADATA) $(PREFIXES) $(FETCHED_DATA) tests/test_syntax.py | $(LOG_DIR) $(VENV)/.requirements-installed.stamp
	@printf "$(BOLD)[*] Checking Turtle syntax...$(NC)\n"
	@printf "$(GREY)"; \
	$(PYTEST) tests/test_syntax.py -q > /dev/null 2>&1 || { printf "$(NC)\n$(RED)[ERROR] Syntax check failed:$(NC)\n"; $(PYTEST) tests/test_syntax.py -v; exit 1; }; \
	printf "$(NC)"
	@touch $@

# 5. Build the graph in one run (src/python/utils/build_graph.py), which
#    writes the result of each step to its own file for inspection:
#      - merge: ontology, shapes, dataset description, static and fetched data
#      - infer: the rules of src/sparql/inference/, until nothing new is derived
#      - update: the SPARQL updates of src/sparql/processing/, in alphabetical order
#    Then the modification date of the dataset is set and the final graph is
#    formatted with the prefixes of the project. The date is part of the build,
#    so that the graph that is tested is exactly the graph that is published.
#    It is today's date if the content differs from the graph on LINDAS (or if
#    LINDAS cannot be reached), otherwise the date found there.
$(PROCESSED_DATA): $(ONTO) $(SHAPES) $(METADATA) $(DATA) $(FETCHED_DATA) $(PREFIXES) $(RULES) $(QUERIES) $(CONFIG) $(LOG_DIR)/syntax-check.stamp $(CONFIG_SCRIPT) src/python/utils/build_graph.py src/python/utils/graph_metadata.py | $(VENV)/.requirements-installed.stamp
	@printf "$(BOLD)[*] Merging, inferring and applying SPARQL updates...$(NC)\n"
	@printf "$(GREY)"; \
	$(VENV_PYTHON) src/python/utils/build_graph.py \
		--input $(ONTO) $(SHAPES) $(METADATA) $(DATA) $(FETCHED_DATA) \
		--rules $(RULES) \
		--update $(QUERIES) \
		--prefixes $(PREFIXES) \
		--merged $(MERGED_DATA) \
		--inferred $(INFERRED_DATA) \
		--output $(PROCESSED_DATA) || { printf "$(NC)"; exit 1; }; \
	printf "$(NC)"
	@printf "$(BOLD)[*] Setting the modification date and formatting the graph...$(NC)\n"
	@printf "$(GREY)"; \
	$(VENV_PYTHON) src/python/utils/graph_metadata.py --graph $(PROCESSED_DATA) --iri "$(LINDAS_GRAPH)" --endpoint "$(LINDAS_GRAPH_STORE)" --prefixes $(PREFIXES) || { printf "$(NC)"; exit 1; }; \
	printf "$(NC)"

# 6. Trigger the whole graph build process
build: $(PROCESSED_DATA) ## Build the graph: integration, inference, SPARQL processing

# ==============================================================================
# BUILD DOCUMENTATION
# ==============================================================================

generate-shacl-docs: $(SHAPES) $(PREFIXES) $(PROCESSED_DATA) $(CONFIG) src/python/utils/generate_shacl_docs.py | $(VENV)/.requirements-installed.stamp ## Generate the data model and code list pages from the SHACL shapes and the graph
	@printf "$(BOLD)[*] Generating SHACL documentation...$(NC)\n"
	@printf "$(GREY)"; \
	$(VENV_PYTHON) src/python/utils/generate_shacl_docs.py -i $(SHAPES) -d $(DOCS_DIR) -p $(PREFIXES) -g $(PROCESSED_DATA) -c $(CONFIG) || { printf "$(NC)"; exit 1; }; \
	printf "$(NC)"

generate-glossary-docs: src/rdf/data/glossary.skos.ttl $(PREFIXES) src/python/utils/generate_glossary_docs.py | $(VENV)/.requirements-installed.stamp ## Generate the glossary pages from the SKOS glossary
	@printf "$(BOLD)[*] Generating glossary documentation...$(NC)\n"
	@printf "$(GREY)"; \
	$(VENV_PYTHON) src/python/utils/generate_glossary_docs.py -i src/rdf/data/glossary.skos.ttl -d $(DOCS_DIR) -p $(PREFIXES) || { printf "$(NC)"; exit 1; }; \
	printf "$(NC)"

# The metadata that docs/_quarto.yml includes: eCH title page, website title,
# navigation and announcement, all from the project configuration
$(QUARTO_METADATA): $(CONFIG) $(CONFIG_SCRIPT) $(DOCS_DIR)/_extensions/ech/ech_vocabulary.yml | $(VENV)/.requirements-installed.stamp
	@$(VENV_PYTHON) $(CONFIG_SCRIPT) quarto -o $(QUARTO_METADATA)

# Quarto runs the Python code chunks with the interpreter of the virtual environment
docs: $(SHACL_REPORT) $(QUARTO_METADATA) generate-shacl-docs generate-glossary-docs | $(VENV)/.requirements-installed.stamp ## Generate the data model and glossary pages and render the documentation (website, PDF)
	@printf "$(BOLD)[*] Rendering documentation with Quarto...$(NC)\n"
	@printf "$(GREY)"; \
	QUARTO_PYTHON=$(VENV_PYTHON) quarto render docs > $(QUARTO_LOG) 2>&1 || { printf "$(NC)\n$(RED)ERROR: Quarto rendering failed. See log below:$(NC)\n$(GREY)"; cat $(QUARTO_LOG); printf "$(NC)\n"; exit 1; }; \
	printf "$(NC)"

# ==============================================================================
# TESTS
# ==============================================================================

# 1. Offline checks of the sources (syntax, prefixes, configuration,
#    translations, code lists, glossary). They need neither the network
#    nor a built graph: pytest leaves out the tests marked `network` and
#    `graph` (see tests/conftest.py).
check: | $(VENV)/.requirements-installed.stamp ## Check the sources offline, without building the graph
	@printf "$(BOLD)[*] Checking the sources...$(NC)\n"
	@$(PYTEST) tests/ -q -m "not network and not graph"

# 2. SHACL validation
$(SHACL_REPORT): $(PROCESSED_DATA) $(SHAPES) | $(LOG_DIR) $(VENV)/.requirements-installed.stamp
	@printf "$(BOLD)[*] Running SHACL engine...$(NC)\n"
	@printf "$(GREY)"; \
	$(PYSHACL) -s $(SHAPES)  -a -f turtle -o $(SHACL_REPORT) $(PROCESSED_DATA) > $(SHACL_LOG) 2>&1 || true; \
	printf "$(NC)"

# 3. Run pytest (relies on written SHACL reports for all shape-related tests)
test: build $(SHACL_REPORT) | $(VENV)/.requirements-installed.stamp ## Build the graph, validate it with SHACL and run the test suite
	@printf "$(BOLD)[*] Running final test suite...$(NC)\n"
	@$(PYTEST) tests/ -v

# ==============================================================================
# PUBLICATION
# ==============================================================================

# 1. Import environment variables natively into Make. Only the credentials are
#    passed on to the recipes, as environment variables: they are read there
#    by graph_metadata.py and handed to curl on standard input, so that the
#    password never appears on a command line.
-include .env
export LINDAS_USER LINDAS_PASSWORD

# curl: fail on HTTP errors (printing the answer of the server) and read the
# credentials as a config line from standard input.
CURL             := curl --silent --show-error --fail-with-body --config -
CURL_CREDENTIALS := printf '%s:%s' "$$LINDAS_USER" "$$LINDAS_PASSWORD" | sed 's/[\\"]/\\&/g; s/.*/user = "&"/'

# 2. Check that the credentials for LINDAS are set
check-publication: | $(VENV)/.requirements-installed.stamp
	@missing=""; \
	[ -n "$$LINDAS_USER" ] || missing="$$missing LINDAS_USER"; \
	[ -n "$$LINDAS_PASSWORD" ] || missing="$$missing LINDAS_PASSWORD"; \
	if [ -n "$$missing" ]; then \
		printf "$(RED)ERROR: not set:$$missing. Add them to .env or to the environment.$(NC)\n"; exit 1; \
	fi

# 3. Delete the existing data from LINDAS
delete: check-publication ## Delete the published graph from LINDAS (needs .env)
	@printf "$(BOLD)[*] Delete existing data from LINDAS$(NC)\n"
	@printf "$(GREY)"; \
	$(CURL_CREDENTIALS) | $(CURL) -X DELETE "$(LINDAS_GRAPH_STORE)?graph=$(LINDAS_GRAPH)" \
		|| { printf "$(NC)\n$(RED)ERROR: could not delete the graph on LINDAS.$(NC)\n"; exit 1; }; \
	printf "$(NC)\n"

# 4. Publish the final graph to LINDAS. A single PUT request replaces the
#    content of the named graph: if it fails, the published graph stays as it was.
publish: check-publication test ## Test, then replace the graph on LINDAS with the newly built one (needs .env)
	@printf "$(BOLD)[*] Upload final graph to LINDAS$(NC)\n"
	@printf "$(GREY)"; \
	$(CURL_CREDENTIALS) | $(CURL) -X PUT -H "Content-Type: text/turtle" --data-binary @$(PROCESSED_DATA) "$(LINDAS_GRAPH_STORE)?graph=$(LINDAS_GRAPH)" \
		|| { printf "$(NC)\n$(RED)ERROR: the upload to LINDAS failed. The published graph was not replaced.$(NC)\n"; exit 1; }; \
	printf "$(NC)\n"

# ==============================================================================
# CLEANUP
# ==============================================================================

clean: ## Remove all build artifacts, caches, the virtual environment and generated pages
	@printf "$(BOLD)[*] Cleaning build artifacts...$(NC)\n"
	@rm -rf $(BUILD_DIR) $(VENV) docs/*/codelists.md docs/*/entities.md docs/*/glossary.md docs/*/namespaces.md $(QUARTO_METADATA) $(DOCS_DIR)/_extensions/ech/plantuml/cache
	@find . -path ./.git -prune -o \( -name __pycache__ -o -name .pytest_cache -o -name .quarto -o -name '*_files' -o -name '*_cache' -o -name '*.quarto_ipynb' \) -prune -exec rm -rf {} +