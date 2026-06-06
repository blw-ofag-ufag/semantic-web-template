# Variables
ROBOT := java -jar build/robot.jar
PYSHACL := pyshacl
ONTO := rdf/ontology/model.owl.ttl
DATA := rdf/data/people.ttl
SHAPES := rdf/shapes/model.shacl.ttl
QUERIES := $(wildcard queries/*.rq)

# Default target
all: test

# 0. Setup: Download ROBOT
setup:
	mkdir -p build
	curl -L https://github.com/ontodev/robot/releases/latest/download/robot.jar -o build/robot.jar
	pip install -r requirements.txt

# 1. Merge ontology and data
build/01_merged.ttl: $(DATA) $(ONTO)
	mkdir -p build
	$(ROBOT) merge --input $(ONTO) --input $(DATA) --output $@

# 2. Inference using HermiT
build/02_inferred.ttl: build/01_merged.ttl
	$(ROBOT) reason --input $< --reasoner HermiT --axiom-generators "SubClass ClassAssertion PropertyAssertion" --output $@

# 3. Model-driven processing via SPARQL
build/03_processed.ttl: build/02_inferred.ttl $(QUERIES)
	@if [ -z "$(QUERIES)" ]; then \
		echo "No queries found. Passing inferred graph directly."; \
		cp $< $@; \
	else \
		echo "Applying queries: $(QUERIES)"; \
		$(ROBOT) query --input $< $(foreach q,$(QUERIES),--update $(q)) --output $@; \
	fi

# 4. Run Pytest suite
test: build/03_processed.ttl
	pytest tests/ -v

clean:
	rm -rf build/0*.ttl