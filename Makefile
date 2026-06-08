# =======================================================
# CONFIG
# =======================================================

ROBOT_VERSION := v1.9.5
ROBOT := java -jar build/robot.jar
ONTO := rdf/ontology/model.owl.ttl
DATA := rdf/data/people.ttl
SHAPES := rdf/shapes/model.shacl.ttl
QUERIES := $(wildcard src/sparql/*.rq)
PYTHON ?= $(shell command -v python3 || command -v python)
VENV ?= venv

# explicitly define paths to venv binaries
VENV_BIN := $(VENV)/bin
VENV_PYTHON := $(VENV_BIN)/python
VENV_PIP := $(VENV_BIN)/pip
PYSHACL := $(VENV_BIN)/pyshacl
PYTEST := $(VENV_BIN)/pytest

.PHONY: all robot test docs clean

# Default target
all: robot test

# =======================================================
# SETUP
# =======================================================

# 1. Check python interpreter
check-python:
	@command -v $(PYTHON) >/dev/null 2>&1 || \
		(echo "ERROR: Python interpreter not found."; exit 1)

# 2. Set up virtual environment
venv: check-python
	@test -d $(VENV) || $(PYTHON) -m venv $(VENV)
	@$(VENV_PYTHON) -m pip install --upgrade pip

# 3. Install project dependencies
install: venv
	@$(VENV_PIP) install -r requirements.txt

# 4. Install robot
robot: venv
	@mkdir -p build
	@curl -sL https://github.com/ontodev/robot/releases/download/$(ROBOT_VERSION)/robot.jar -o build/robot.jar
	@echo "Installing Python dependencies..."
	@$(VENV_PIP) install -q -r requirements.txt
	@echo "Setup complete."

# =======================================================
# RDF DATA INTEGRATION, REASONING AND POST-PROCESSING
# =======================================================

# 1. Check that all turtle files are syntactically valid
build/rdf/00-syntax-ok: $(DATA) $(ONTO) $(SHAPES)
	@mkdir -p build/rdf
	@echo "Checking Turtle syntax..."
	@$(PYTEST) tests/test_syntax.py -q > /dev/null 2>&1 || (echo "\n[ERROR] Syntax check failed:" && $(PYTEST) tests/test_syntax.py -v && exit 1)
	@touch $@

# 2. Merge ontology and data
build/rdf/01-merged.ttl: build/rdf/00-syntax-ok $(DATA) $(ONTO)
	@echo "Merging ontology and data..."
	@$(ROBOT) merge --input $(ONTO) --input $(DATA) --output $@ > build/01-merge.log 2>&1 || (cat build/01-merge.log && exit 1)

# 3. Inference using HermiT
build/rdf/02-inferred.ttl: build/rdf/01-merged.ttl
	@echo "Running logical inference (HermiT)..."
	@$(ROBOT) reason --input $< --reasoner HermiT --axiom-generators "SubClass ClassAssertion PropertyAssertion" --output $@ > build/02-infer.log 2>&1 || (cat build/02-infer.log && exit 1)

# 4. Model-driven processing via SPARQL
build/rdf/03-processed.ttl: build/rdf/02-inferred.ttl $(QUERIES)
	@echo "Applying SPARQL updates..."
	@if [ -z "$(QUERIES)" ]; then \
		cp $< $@; \
	else \
		$(ROBOT) query --input $< $(foreach q,$(QUERIES),--update $(q)) convert --output $@ > build/03-query.log 2>&1 || (cat build/03-query.log && exit 1); \
	fi
	@$(VENV_PYTHON) src/python/turtle-serializer.py build/rdf/03-processed.ttl output build/rdf/03-processed.ttl

# =======================================================
# BUILD DOCUMENTATION
# =======================================================

docs: shacl
	@echo "Rendering documentation with Quarto..."
	@quarto render > build/05-quarto.log 2>&1 || true

# =======================================================
# TESTS
# =======================================================

# 1. SHACL validation
shacl: build/rdf/03-processed.ttl $(SHAPES)
	@echo "Running SHACL engine..."
	@$(PYSHACL) -s $(SHAPES) -m -i rdfs -a -f turtle -o build/rdf/04-shacl-report.ttl $< > build/04-shacl.log 2>&1 || true

# 2. Run pytest (relies on written SHACL reports for all
#    shape-related tests)
test: shacl
	@echo "Running final test suite..."
	@$(PYTEST) tests/ -v

# =======================================================
# CLEANUP
# =======================================================

clean:
	rm -rf build venv .quarto tests/__pycache__