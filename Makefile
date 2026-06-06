# Variables
ROBOT := java -jar build/robot.jar
PYSHACL := pyshacl
ONTO := ontology/model.owl.ttl
DATA := data/people.ttl
SHAPES := shapes/model.shacl.ttl
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

# 4. SHACL Validation
build/report.txt: build/03_processed.ttl $(SHAPES)
	$(PYSHACL) -s $(SHAPES) -m -i rdfs -a -f human -o $@ $<
	@echo "SHACL Validation Passed."

# 5. Run Pytest suite
test: build/report.txt
	pytest tests/ -v

clean:
	rm -rf build/0*.ttl build/report_shacl.txt