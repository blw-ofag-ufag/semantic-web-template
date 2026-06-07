# Variables
ROBOT_VERSION := v1.9.5
ROBOT := java -jar build/robot.jar
PYSHACL := pyshacl
ONTO := rdf/ontology/model.owl.ttl
DATA := rdf/data/people.ttl
SHAPES := rdf/shapes/model.shacl.ttl
QUERIES := $(wildcard src/sparql/*.rq)

# Default target
all: test

# 0. Setup: Download ROBOT
setup:
	@mkdir -p build
	@echo "Downloading ROBOT..."
	@curl -sL https://github.com/ontodev/robot/releases/download/$(ROBOT_VERSION)/robot.jar -o build/robot.jar
	@echo "Installing Python dependencies..."
	@pip install -q -r requirements.txt
	@echo "Setup complete."

# 1. Check syntax of all turtle files first
build/rdf/00-syntax-ok: $(DATA) $(ONTO) $(SHAPES)
	@mkdir -p build/rdf
	@echo "Checking Turtle syntax..."
	@pytest tests/test_syntax.py -q > /dev/null 2>&1 || (echo "\n[ERROR] Syntax check failed:" && pytest tests/test_syntax.py -v && exit 1)
	@touch $@

# 2. Merge ontology and data
build/rdf/01-merged.ttl: build/rdf/00-syntax-ok $(DATA) $(ONTO)
	@echo "Merging ontology and data..."
	@$(ROBOT) merge --input $(ONTO) --input $(DATA) --output $@ > build/rdf/01-merge.log 2>&1 || (cat build/rdf/01-merge.log && exit 1)

# 3. Inference using HermiT
build/rdf/02-inferred.ttl: build/rdf/01-merged.ttl
	@echo "Running logical inference (HermiT)..."
	@$(ROBOT) reason --input $< --reasoner HermiT --axiom-generators "SubClass ClassAssertion PropertyAssertion" --output $@ > build/rdf/02-infer.log 2>&1 || (cat build/rdf/02-infer.log && exit 1)

# 4. Model-driven processing via SPARQL
build/rdf/03-processed.ttl: build/rdf/02-inferred.ttl $(QUERIES)
	@echo "Applying SPARQL updates..."
	@if [ -z "$(QUERIES)" ]; then \
		cp $< $@; \
	else \
		$(ROBOT) query --input $< $(foreach q,$(QUERIES),--update $(q)) convert --output $@ > build/rdf/03-query.log 2>&1 || (cat build/rdf/03-query.log && exit 1); \
	fi
	@python src/python/turtle-serializer.py build/rdf/03-processed.ttl output build/rdf/03-processed.ttl

# 5. SHACL validation
build/rdf/04-shacl-report.ttl: build/rdf/03-processed.ttl $(SHAPES)
	@echo "Validating SHACL shapes..."
	@$(PYSHACL) -s $(SHAPES) -m -i rdfs -a -f turtle -o $@ $< > build/rdf/04-shacl.log 2>&1 || true

# 6. Run full pytest suite
test: build/rdf/04-shacl-report.ttl
	@echo "Running final test suite..."
	@pytest tests/ -v

clean:
	rm -rf build/rdf/0*.ttl build/rdf/*.log