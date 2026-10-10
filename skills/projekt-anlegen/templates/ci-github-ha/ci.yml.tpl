name: ci

on:
  push:
  pull_request:

jobs:
  pruefen:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v6
      - run: uv venv --python 3.14 .venv
      - run: uv pip install --python .venv/bin/python -r requirements-logik.txt
      - run: uv pip install --python .venv/bin/python -r requirements-ha.txt
      - run: .venv/bin/python -m ruff format --check .
      - run: .venv/bin/python -m ruff check .
      - run: .venv/bin/python -m pytest -q -p no:cacheprovider tests/logik
      - run: .venv/bin/python -m pytest -q -p no:cacheprovider -n auto tests/integration
