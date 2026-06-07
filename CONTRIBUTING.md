# Contributing to PSMV-RDF

To ensure a smooth collaboration and maintain code quality, please adhere to the following workflow.

## Collaboration via GitHub

### Open an issue

Before writing any code, **open a GitHub Issue** to discuss the proposed change.
Whether it is a bug fix, feature request, or architectural adjustment, establish the scope in an issue first.

### Create a branch

Create a new branch for your specific task. Let GitHub autogenerate the branch name based on an issue; that way it's clear what you're trying to do on said branch.

### Submit a pull request

Once your work is ready:

1. Open a draft PR against the `main` branch.
2. Summarize your changes clearly in the description.
3. Link the PR to the issue it resolves (e.g. `Closes #42`).
4. Ensure there are no merge conflicts and all tests are passed before you change the status to a standard pull request.

## Resource naming convention

Aligning with standard Semantic Web conventions, we enforce the following casing rules for URI local names:

- **Classes and individuals** (e.g., instances of `owl:Class` and instances of these): Use **PascalCase** (a.k.a. UpperCamelCase).
- **Properties** (e.g., `owl:ObjectProperty`, `owl:DatatypeProperty`): Use **camelCase** (a.k.a. lowerCamelCase).

Ensure identifiers are semantically meaningful and descriptive to facilitate readability and improve [DX](https://en.wikipedia.org/wiki/Developer_experience).

For individuals, use a sub-namespace. For example, if the project namespace is <http://example.org/>, use <http://example.org/person/> for all people:

``` ttl
@prefix : <http://example.org/> .
@prefix person: <http://example.org/person/> .

person:1 a :Person .
person:2 a :Person .
person:3 a :Person .
```