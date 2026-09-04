# ==============================================================================
# CONFIG
# ==============================================================================

# Directories
BUILD_DIR        := build
RDF_DIR          := $(BUILD_DIR)/rdf
PYTHON_DIR       := src/python

# Tools and binaries
ROBOT_VERSION    := v1.9.5
PYTHON           ?= $(shell command -v python3 || command -v python)
VENV             ?= venv
VENV_BIN         := $(VENV)/bin
VENV_PYTHON      := $(VENV_BIN)/python
VENV_PIP         := $(VENV_BIN)/pip
PYSHACL          := $(VENV_BIN)/pyshacl
PYTEST           := $(VENV_BIN)/pytest -p no:cacheprovider # suppress cache
ROBOT            := java -jar $(VENV_BIN)/robot.jar

# Inputs
ONTO             := src/rdf/ontology/model.owl.ttl
DATA             := $(wildcard src/rdf/data/*.ttl)
SHAPES           := src/rdf/shapes/model.shacl.ttl
PREFIXES         := src/rdf/prefixes.ttl
QUERIES          := $(wildcard src/sparql/processing/*.rq)
PIPELINE_SCRIPTS := $(sort $(wildcard src/python/pipeline/*.py))

# Intermediate & Output Files
FETCHED_DATA     := $(RDF_DIR)/00-integrated.ttl
MERGED_DATA      := $(RDF_DIR)/01-merged.ttl
INFERRED_DATA    := $(RDF_DIR)/02-inferred.ttl
PROCESSED_DATA   := $(RDF_DIR)/03-processed.ttl
SHACL_REPORT     := $(RDF_DIR)/04-shacl-report.ttl
DOCS_DIR         := docs

# Logs
LOG_DIR          := $(BUILD_DIR)/log
MERGE_LOG        := $(LOG_DIR)/01-merge.log
INFER_LOG        := $(LOG_DIR)/02-infer.log
QUERY_LOG        := $(LOG_DIR)/03-query.log
SHACL_LOG        := $(LOG_DIR)/04-shacl.log
QUARTO_LOG       := $(LOG_DIR)/05-quarto.log

# Colors for logging
RED              := \033[0;31m
GREY             := \033[0;90m
BOLD       := \033[1;37m
NC               := \033[0m

.PHONY: all robot test docs clean check-python venv install-dependencies setup build delete publish generate-shacl-docs generate-glossary-docs

# Default target
all: test docs

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
	@test -d $(VENV) || $(PYTHON) -m venv $(VENV)
	@printf "$(GREY)"; $(VENV_PYTHON) -m pip install --upgrade pip || { printf "$(NC)"; exit 1; }; printf "$(NC)"

venv: $(VENV_PYTHON)

# 3. Install python dependencies
$(VENV)/.requirements-installed.stamp: $(PYTHON_DIR)/requirements.txt | $(VENV_PYTHON)
	@printf "$(GREY)"; $(VENV_PIP) install -q -r $(PYTHON_DIR)/requirements.txt || { printf "$(NC)"; exit 1; }; printf "$(NC)"
	@touch $@

install-dependencies: $(VENV)/.requirements-installed.stamp

# 4. Install robot
$(VENV_BIN)/robot.jar: | $(VENV_PYTHON)
	@printf "$(GREY)"; curl -sL https://github.com/ontodev/robot/releases/download/$(ROBOT_VERSION)/robot.jar -o $(VENV_BIN)/robot.jar || { printf "$(NC)"; exit 1; }; printf "$(NC)"

robot: $(VENV_BIN)/robot.jar

# 5. Full setup
setup: install-dependencies robot
	@printf "$(BOLD)[*] Setup complete.$(NC)\n"

# ==============================================================================
# RDF DATA INTEGRATION, REASONING AND POST-PROCESSING
# ==============================================================================

# 1. Set up directories
$(RDF_DIR) $(LOG_DIR):
	@mkdir -p $@

# 2. Fetch, Query, and Transform source data sequentially
$(FETCHED_DATA): $(PIPELINE_SCRIPTS) $(PREFIXES) src/python/utils/turtle_serializer.py | $(RDF_DIR) $(LOG_DIR) $(VENV)/.requirements-installed.stamp
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
	$(VENV_PYTHON) src/python/utils/turtle_serializer.py -i $(FETCHED_DATA) -p $(PREFIXES) -o $(FETCHED_DATA) || { printf "$(NC)"; exit 1; }; \
	printf "$(NC)"

# 3. Check that all turtle files are syntactically valid
$(LOG_DIR)/syntax-check.stamp: $(DATA) $(ONTO) $(SHAPES) $(PREFIXES) $(FETCHED_DATA) tests/test_syntax.py | $(LOG_DIR) $(VENV)/.requirements-installed.stamp
	@printf "$(BOLD)[*] Checking Turtle syntax...$(NC)\n"
	@printf "$(GREY)"; \
	$(PYTEST) tests/test_syntax.py -q > /dev/null 2>&1 || { printf "$(NC)\n$(RED)[ERROR] Syntax check failed:$(NC)\n"; $(PYTEST) tests/test_syntax.py -v; exit 1; }; \
	printf "$(NC)"
	@touch $@

# 4. Merge ontology, shapes, static data, fetched data, and prefixes
$(MERGED_DATA): $(ONTO) $(SHAPES) $(DATA) $(FETCHED_DATA) $(PREFIXES) $(LOG_DIR)/syntax-check.stamp src/python/utils/turtle_serializer.py | $(LOG_DIR) $(VENV_BIN)/robot.jar $(VENV)/.requirements-installed.stamp
	@printf "$(BOLD)[*] Merging ontology, shapes and data...$(NC)\n"
	@printf "$(GREY)"; \
	$(ROBOT) merge \
		--input $(ONTO) \
		--input $(SHAPES) \
		$(foreach d,$(DATA),--input $(d)) \
		--input $(FETCHED_DATA) \
		--input $(PREFIXES) \
		--output $(MERGED_DATA) > $(MERGE_LOG) 2>&1 || { printf "$(NC)\n$(RED)ERROR: ROBOT merge failed. See log below:$(NC)\n$(GREY)"; cat $(MERGE_LOG); printf "$(NC)\n"; exit 1; }; \
	$(VENV_PYTHON) src/python/utils/turtle_serializer.py -i $(MERGED_DATA) -p $(PREFIXES) -o $(MERGED_DATA) || { printf "$(NC)"; exit 1; }; \
	printf "$(NC)"

# 5. Inference using HermiT
$(INFERRED_DATA): $(MERGED_DATA) $(PREFIXES) src/python/utils/turtle_serializer.py | $(LOG_DIR) $(VENV_BIN)/robot.jar $(VENV)/.requirements-installed.stamp
	@printf "$(BOLD)[*] Running logical inference (HermiT)...$(NC)\n"
	@printf "$(GREY)"; \
	$(ROBOT) reason \
		--input $(MERGED_DATA) \
		--reasoner HermiT \
		--axiom-generators "SubClass ClassAssertion PropertyAssertion" \
		--include-indirect true \
		--output $(INFERRED_DATA) > $(INFER_LOG) 2>&1 || { printf "$(NC)\n$(RED)ERROR: ROBOT reason failed. See log below:$(NC)\n$(GREY)"; cat $(INFER_LOG); printf "$(NC)\n"; exit 1; }; \
	$(VENV_PYTHON) src/python/utils/turtle_serializer.py -i $(INFERRED_DATA) -p $(PREFIXES) -o $(INFERRED_DATA) || { printf "$(NC)"; exit 1; }; \
	printf "$(NC)"

# 6. Model-driven processing via SPARQL
$(PROCESSED_DATA): $(INFERRED_DATA) $(QUERIES) $(PREFIXES) src/python/utils/turtle_serializer.py | $(LOG_DIR) $(VENV_BIN)/robot.jar $(VENV)/.requirements-installed.stamp
	@printf "$(BOLD)[*] Applying SPARQL updates...$(NC)\n"
	@printf "$(GREY)"; \
	if [ -z "$(QUERIES)" ]; then \
		cp $(INFERRED_DATA) $(PROCESSED_DATA); \
	else \
		$(ROBOT) query \
			--input $(INFERRED_DATA) \
			$(foreach q,$(QUERIES),--update $(q)) \
			convert --output $(PROCESSED_DATA) > $(QUERY_LOG) 2>&1 || { printf "$(NC)\n$(RED)ERROR: ROBOT query failed. See log below:$(NC)\n$(GREY)"; cat $(QUERY_LOG); printf "$(NC)\n"; exit 1; }; \
	fi; \
	$(VENV_PYTHON) src/python/utils/turtle_serializer.py -i $(PROCESSED_DATA) -p $(PREFIXES) -o $(PROCESSED_DATA) || { printf "$(NC)"; exit 1; }; \
	printf "$(NC)"

# 6. Trigger the whole graph build process
build: $(PROCESSED_DATA)

# ==============================================================================
# BUILD DOCUMENTATION
# ==============================================================================

generate-shacl-docs: $(SHAPES) $(PREFIXES) src/python/utils/generate_shacl_docs.py | $(VENV)/.requirements-installed.stamp
	@printf "$(BOLD)[*] Generating SHACL documentation...$(NC)\n"
	@printf "$(GREY)"; \
	$(VENV_PYTHON) src/python/utils/generate_shacl_docs.py -i $(SHAPES) -d $(DOCS_DIR) -p $(PREFIXES) || { printf "$(NC)"; exit 1; }; \
	printf "$(NC)"

generate-glossary-docs: src/rdf/data/glossary.skos.ttl $(PREFIXES) src/python/utils/generate_glossary_docs.py | $(VENV)/.requirements-installed.stamp
	@printf "$(BOLD)[*] Generating glossary documentation...$(NC)\n"
	@printf "$(GREY)"; \
	$(VENV_PYTHON) src/python/utils/generate_glossary_docs.py -i src/rdf/data/glossary.skos.ttl -d $(DOCS_DIR) -p $(PREFIXES) || { printf "$(NC)"; exit 1; }; \
	printf "$(NC)"

docs: $(SHACL_REPORT) generate-shacl-docs generate-glossary-docs
	@printf "$(BOLD)[*] Rendering documentation with Quarto...$(NC)\n"
	@printf "$(GREY)"; \
	quarto render docs > $(QUARTO_LOG) 2>&1 || { printf "$(NC)\n$(RED)ERROR: Quarto rendering failed. See log below:$(NC)\n$(GREY)"; cat $(QUARTO_LOG); printf "$(NC)\n"; exit 1; }; \
	printf "$(NC)"

# ==============================================================================
# TESTS
# ==============================================================================

# 1. SHACL validation
$(SHACL_REPORT): $(PROCESSED_DATA) $(SHAPES) | $(LOG_DIR) $(VENV)/.requirements-installed.stamp
	@printf "$(BOLD)[*] Running SHACL engine...$(NC)\n"
	@printf "$(GREY)"; \
	$(PYSHACL) -s $(SHAPES)  -a -f turtle -o $(SHACL_REPORT) $(PROCESSED_DATA) > $(SHACL_LOG) 2>&1 || true; \
	printf "$(NC)"

# 2. Run pytest (relies on written SHACL reports for all shape-related tests)
test: build $(SHACL_REPORT) | $(VENV)/.requirements-installed.stamp
	@printf "$(BOLD)[*] Running final test suite...$(NC)\n"
	@$(PYTEST) tests/ -v

# ==============================================================================
# PUBLICATION
# ==============================================================================

# 1. Import environment variables natively into Make
-include .env
export

# 2. Delete the existing data from LINDAS
delete:
	@printf "$(BOLD)[*] Delete existing data from LINDAS$(NC)\n"
	@printf "$(GREY)"; \
	curl \
		--user $(USER):$(PASSWORD) \
		-X DELETE \
		"$(ENDPOINT)?graph=$(GRAPH)" || { printf "$(NC)"; exit 1; }; \
	printf "$(NC)\n"

# 3. Publish final graph to LINDAS
publish: test delete
	@printf "$(BOLD)[*] Upload final graph to LINDAS$(NC)\n"
	@printf "$(GREY)"; \
	curl \
		--user $(USER):$(PASSWORD) \
		-X POST \
		-H "Content-Type: text/turtle" \
		--data-binary @$(PROCESSED_DATA) \
		"$(ENDPOINT)?graph=$(GRAPH)" || { printf "$(NC)"; exit 1; }; \
	printf "$(NC)\n"

# ==============================================================================
# CLEANUP
# ==============================================================================

clean:
	@printf "$(BOLD)[*] Cleaning build artifacts...$(NC)\n"
	@rm -rf $(BUILD_DIR) $(VENV) .quarto docs/.quarto tests/__pycache__ docs/index_files docs/*/entities.md docs/*/glossary.md