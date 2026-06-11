# Semantic web project template

## Tech stack

- HermiT
- Pytest
- Pyshacl
- Quarto

## Build the data model

1. Add variables to `.env`

    ``` sh
    USER=********
    PASSWORD=********
    GRAPH=********
    ENDPOINT=********
    ```

2. Set up dependencies

    ``` sh
    make setup
    ```

3. Run the build process

    ``` sh
    make
    ```

    Make sure you pass all tests with `pytest`.

4. Upload the final data to [LINDAS](https://lindas.admin.ch/), the linked data service by the federal archives:

    ``` sh
    make publish
    ```

    By default, the publication process starts with by deleting any pre-existing data in the provided named graph on LINDAS.
    You can also *just* delete any published data by running:

    ```
    make delete
    ```

5. *If* you want to clean all written files:

    ``` sh
    make clean
    ```
