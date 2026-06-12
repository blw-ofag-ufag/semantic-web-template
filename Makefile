# ==============================================================================
# CONFIG
# ==============================================================================

# Directories
BUILD_DIR        := build
RDF_DIR          := $(BUILD_DIR)/rdf

# Tools and binaries
ROBOT_VERSION    := v1.9.5
PYTHON           ?= $(shell command -v python3 || command -v python)
VENV             ?= venv
VENV_BIN         := $(VENV)/bin
VENV_PYTHON      := $(VENV_BIN)/python
VENV_PIP         := $(VENV_BIN)/pip
PYSHACL          := $(VENV_BIN)/pyshacl
PYTEST           := $(VENV_BIN)/pytest
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

# Logs
LOG_DIR          := $(BUILD_DIR)/log/
MERGE_LOG        := $(LOG_DIR)/01-merge.log
INFER_LOG        := $(LOG_DIR)/02-infer.log
QUERY_LOG        := $(LOG_DIR)/03-query.log
SHACL_LOG        := $(LOG_DIR)/04-shacl.log
QUARTO_LOG       := $(LOG_DIR)/05-quarto.log

.PHONY: all robot test docs clean fetch-data check-python venv install-dependencies setup check-syntax merge infer post-process build shacl delete publish

# Default target
all: test docs

# ==============================================================================
# SETUP
# ==============================================================================

# 1. Check python interpreter
check-python:
	@command -v $(PYTHON) >/dev/null 2>&1 || \
		(echo "ERROR: Python interpreter not found."; exit 1)

# 2. Set up virtual environment
venv: check-python
	@test -d $(VENV) || $(PYTHON) -m venv $(VENV)
	@$(VENV_PYTHON) -m pip install --upgrade pip

# 3. Install python dependencies
install-dependencies: venv
	@$(VENV_PIP) install -q -r requirements.txt

# 4. Install robot
robot: venv
	@curl -sL https://github.com/ontodev/robot/releases/download/$(ROBOT_VERSION)/robot.jar -o $(VENV_BIN)/robot.jar

# 5. Full setup
setup: install-dependencies robot
	@echo "Setup complete."

# ==============================================================================
# RDF DATA INTEGRATION, REASONING AND POST-PROCESSING
# ==============================================================================

# 1. Set up directories
mkdir:
	@mkdir -p $(RDF_DIR)
	@mkdir -p $(LOG_DIR)

# 2. Fetch, Query, and Transform source data sequentially
fetch-data: venv mkdir
	@echo "Running data integration pipelines..."
	@if [ -n "$(PIPELINE_SCRIPTS)" ]; then \
		for script in $(PIPELINE_SCRIPTS); do \
			echo "Executing $$script..."; \
			$(VENV_PYTHON) "$$script" --output $(FETCHED_DATA); \
		done; \
	else \
		echo "No pipeline scripts found. Creating empty data file."; \
		touch $(FETCHED_DATA); \
	fi
	@$(VENV_PYTHON) src/python/utils/turtle_serializer.py -i $(FETCHED_DATA) -p $(PREFIXES) -o $(FETCHED_DATA)

# 3. Check that all turtle files are syntactically valid
check-syntax: fetch-data $(DATA) $(ONTO) $(SHAPES) $(PREFIXES)
	@echo "Checking Turtle syntax..."
	@$(PYTEST) tests/test_syntax.py -q > /dev/null 2>&1 || (echo "\n[ERROR] Syntax check failed:" && $(PYTEST) tests/test_syntax.py -v && exit 1)

# 4. Merge ontology, static data, fetched data, and prefixes
merge: check-syntax $(DATA) $(ONTO) $(FETCHED_DATA) $(PREFIXES)
	@echo "Merging ontology and data..."
	@$(ROBOT) merge \
		--input $(ONTO) \
		$(foreach d,$(DATA),--input $(d)) \
		--input $(FETCHED_DATA) \
		--input $(PREFIXES) \
		--output $(MERGED_DATA) > $(MERGE_LOG) 2>&1 || (cat $(MERGE_LOG) && exit 1)
	@$(VENV_PYTHON) src/python/utils/turtle_serializer.py -i $(MERGED_DATA) -p $(PREFIXES) -o $(MERGED_DATA)

# 5. Inference using HermiT
infer: merge
	@echo "Running logical inference (HermiT)..."
	@$(ROBOT) reason \
		--input $(MERGED_DATA) \
		--reasoner HermiT \
		--axiom-generators "SubClass ClassAssertion PropertyAssertion" \
		--include-indirect true \
		--output $(INFERRED_DATA) > $(INFER_LOG) 2>&1 || (cat $(INFER_LOG) && exit 1)
	@$(VENV_PYTHON) src/python/utils/turtle_serializer.py -i $(INFERRED_DATA) -p $(PREFIXES) -o $(INFERRED_DATA)

# 6. Model-driven processing via SPARQL
post-process: infer $(QUERIES)
	@echo "Applying SPARQL updates..."
	@if [ -z "$(QUERIES)" ]; then \
		cp $(INFERRED_DATA) $(PROCESSED_DATA); \
	else \
		$(ROBOT) query \
			--input $(INFERRED_DATA) \
			$(foreach q,$(QUERIES),--update $(q)) \
			convert --output $(PROCESSED_DATA) > $(QUERY_LOG) 2>&1 || (cat $(QUERY_LOG) && exit 1); \
	fi
	@$(VENV_PYTHON) src/python/utils/turtle_serializer.py -i $(PROCESSED_DATA) -p $(PREFIXES) -o $(PROCESSED_DATA)

# 6. Trigger the whole graph build process
build: post-process

# ==============================================================================
# BUILD DOCUMENTATION
# ==============================================================================

docs: shacl
	@echo "Rendering documentation with Quarto..."
	@quarto render > $(QUARTO_LOG) 2>&1 || true

# ==============================================================================
# TESTS
# ==============================================================================

# 1. SHACL validation
shacl: build $(SHAPES)
	@echo "Running SHACL engine..."
	@$(PYSHACL) -s $(SHAPES)  -a -f turtle -o $(SHACL_REPORT) $(PROCESSED_DATA) > $(SHACL_LOG) 2>&1 || true

# 2. Run pytest (relies on written SHACL reports for all shape-related tests)
test: build shacl
	@echo "Running final test suite..."
	@$(PYTEST) tests/ -v

# ==============================================================================
# PUBLICATION
# ==============================================================================

# 1. Import environment variables natively into Make
-include .env
export

# 2. Delete the existing data from LINDAS
delete:
	@echo "Delete existing data from LINDAS"
	@curl \
		--user $(USER):$(PASSWORD) \
		-X DELETE \
		"$(ENDPOINT)?graph=$(GRAPH)"

# 3. Publish final graph to LINDAS
publish: test delete
	@echo "Upload final graph to LINDAS"
	@curl \
		--user $(USER):$(PASSWORD) \
		-X POST \
		-H "Content-Type: text/turtle" \
		--data-binary @$(PROCESSED_DATA) \
		"$(ENDPOINT)?graph=$(GRAPH)"

# ==============================================================================
# CLEANUP
# ==============================================================================

clean:
	rm -rf $(BUILD_DIR) $(VENV) .quarto tests/__pycache__ .pytest_cache