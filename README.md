# Semantic web project template

## Build the data model

1. Add variables to `.env`

    ``` sh
    USER=********
    PASSWORD=********
    GRAPH=********
    ENDPOINT=********
    ```

2. Start a virtual environment

    ``` sh
    python -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    ```

3. Set up dependencies

    ``` sh
    make setup
    ```

4. Run the build process

    ``` sh
    make
    ```

    Make sure you pass all tests with `pytest`.

5. Build the documentation

    ``` sh
    quarto render
    ```

## Build process overview

The `Makefile` orchestrates a multi-step data pipeline. Here is a sequence diagram explaining what happens under the hood when you run `make`:

``` mermaid
sequenceDiagram
    participant U as User
    participant M as Make
    participant PT as Pytest
    participant R as ROBOT
    participant PY as Python
    participant S as PySHACL

    U->>M: make (all)
    
    Note over M,PT: 1. Syntax Check
    M->>PT: run test_syntax.py
    PT-->>M: Syntax OK (00-syntax-ok)
    
    Note over M,R: 2. Merge Data & Ontology
    M->>R: robot merge
    R-->>M: 01-merged.ttl
    
    Note over M,R: 3. Logical Inference
    M->>R: robot reason (HermiT)
    R-->>M: 02-inferred.ttl
    
    Note over M,PY: 4. SPARQL Processing & Serialization
    M->>R: robot query (SPARQL updates)
    R-->>M: temp graph
    M->>PY: turtle-serializer.py
    PY-->>M: 03-processed.ttl
    
    Note over M,S: 5. SHACL Validation
    M->>S: pyshacl validate
    S-->>M: 04-shacl-report.ttl
    
    Note over M,PT: 6. Final Test Suite
    M->>PT: run pytest tests/
    PT-->>M: test results (including SHACL check)
    
    M-->>U: Build completed successfully
```