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
	mkdir -p build
	curl -L https://github.com/ontodev/robot/releases/latest/download/robot.jar -o build/robot.jar
	pip install -r requirements.txt

# 1. Check syntax of all turtle files first
build/00-syntax-ok: $(DATA) $(ONTO) $(SHAPES)
	mkdir -p build
	pytest tests/test_syntax.py -v
	touch $@

# 2. Merge ontology and data
build/01-merged.ttl: build/00-syntax-ok $(DATA) $(ONTO)
	$(ROBOT) merge --input $(ONTO) --input $(DATA) --output $@

# 3. Inference using HermiT
build/02-inferred.ttl: build/01-merged.ttl
	$(ROBOT) reason --input $< --reasoner HermiT --axiom-generators "SubClass ClassAssertion PropertyAssertion" --output $@

# 4. Model-driven processing via SPARQL
build/03-processed.ttl: build/02-inferred.ttl $(QUERIES)
	@if [ -z "$(QUERIES)" ]; then \
		echo "No queries found. Passing inferred graph directly."; \
		cp $< $@; \
	else \
		echo "Applying queries: $(QUERIES)"; \
		$(ROBOT) query --input $< $(foreach q,$(QUERIES),--update $(q)) --output $@; \
	fi
	python src/python/turtle-serializer.py input build/03-processed.ttl output build/03-processed.ttl

# 5. SHACL validation
build/04-shacl-report.ttl: build/03-processed.ttl $(SHAPES)
	$(PYSHACL) -s $(SHAPES) -m -i rdfs -a -f turtle -o $@ $< || true

# 6. Run full pytest suite
test: build/04-shacl-report.ttl
	pytest tests/ -v

clean:
	rm -rf build/0*.ttl