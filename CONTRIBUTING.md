
# Contributing to Cachorro

## How to Contribute

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## Code Style

Please follow the PEP 8 guidelines.
For this reason, we use `pre-commit` and `flake8` to ensure uniformity of code linting.

Install `pre-commit`:

```bash
pip install pre-commit
```

Install the Pre-Commit hook:

```bash
pre-commit install
```

## Tests

Besides code linting, we also use a precommit hook to run the unit tests before committing the repository.

### Running Tests Manually

To run the tests and generate a coverage report manually, use:

```bash
pytest
```

Alternatively, to run the tests manually, generate a report in [TESTS.md](TESTS.md) and show a badge in the [README.md](README.md), run:

```bash
./testscoverage.py
```
