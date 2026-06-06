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

3. Run the build process

    ``` sh
    make
    ```

    Make sure you pass all tests with `pytest`.