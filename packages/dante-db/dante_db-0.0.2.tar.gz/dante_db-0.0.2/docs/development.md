# Developing Dante

Goals:

* zero-setup
* sync and async
* easy to use
* simple API with no nasty surprises

Code guidelines:

* feature-parity across sync and async (with identical API where applicable)
* 100% test coverage
* 100% coverage with type hints
* explicit is better than implicit (and, really, everything from the Zen of
Python)

## Setup

TBW

## Tests

Run the tests with coverage plugin:

```shell
pytest --cov=dante
```

This will show the coverage summary. To build a detailed HTML report,
then run:

```shell
coverage html
```

The report will be saved in the `htmlcov` directory.

## Linting and formatting

We use `ruff` for formatting and linting, with the default rules. To run
the checks:

```shell
ruff check --fix
ruff format
```

## Publishing the package

To publish the package, follow these steps:

1. Run `pytest`, `ruff check`, and `ruff format` to ensure everything is in
   order.
2. Bump the version in `pyproject.toml`, commit the version bump, and create a tag for it.
3. Push the package to GitHub and wait for the tests to pass.
4. Build the package: `uvx --from build pyproject-build --installer uv`
5. Upload the package to PyPI: `uvx twine upload dist/*`

We recommend using [uv](https://github.com/astral-sh/uv), but you can also
run `build` and `twine` directly (within the virtual environment).
