# NEM 12 Generator

This project takes a meter configuration and generates NEM12 files.

![Tests](https://github.com/jarshwah/nem12-generator/actions/workflows/test.yml/badge.svg)
![Lint](https://github.com/jarshwah/nem12-generator/actions/workflows/pre-commit.yml/badge.svg)


## Setup / Development

1. [Install uv package manager](https://docs.astral.sh/uv/getting-started/installation/)
2. Install python 3.11 `uv python install 3.11`
3. Create a virtualenv: `uv venv -p 3.11`
4. Install: `uv sync`


## Tests

```sh
uv run pytest tests
```


## Usage

```sh
uv run generate examples/nmi-discovery.xml out/nem12-transaction.xml
```
