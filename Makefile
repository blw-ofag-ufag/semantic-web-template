# Variables
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
	mkdir -p build/rdf
	curl -L https://github.com/ontodev/robot/releases/latest/download/robot.jar -o build/robot.jar
	pip install -r requirements.txt

# 1. Check syntax of all turtle files first
build/rdf/00-syntax-ok: $(DATA) $(ONTO) $(SHAPES)
	pytest tests/test_syntax.py -v
	touch $@

# 2. Merge ontology and data
build/rdf/01-merged.ttl: build/rdf/00-syntax-ok $(DATA) $(ONTO)
	$(ROBOT) merge --input $(ONTO) --input $(DATA) --output $@

# 3. Inference using HermiT
build/rdf/02-inferred.ttl: build/rdf/01-merged.ttl
	$(ROBOT) reason --input $< --reasoner HermiT --axiom-generators "SubClass ClassAssertion PropertyAssertion" --output $@

# 4. Model-driven processing via SPARQL
build/rdf/03-processed.ttl: build/rdf/02-inferred.ttl $(QUERIES)
	@if [ -z "$(QUERIES)" ]; then \
		echo "No queries found. Passing inferred graph directly."; \
		cp $< $@; \
	else \
		echo "Applying queries: $(QUERIES)"; \
		$(ROBOT) query --input $< $(foreach q,$(QUERIES),--update $(q)) --output $@; \
	fi
	python src/python/turtle-serializer.py input build/rdf/03-processed.ttl output build/rdf/03-processed.ttl

# 5. SHACL validation
build/rdf/04-shacl-report.ttl: build/rdf/03-processed.ttl $(SHAPES)
	$(PYSHACL) -s $(SHAPES) -m -i rdfs -a -f turtle -o $@ $< || true

# 6. Run full pytest suite
test: build/rdf/04-shacl-report.ttl
	pytest tests/ -v

clean:
	rm -rf build/rdf/0*.ttl