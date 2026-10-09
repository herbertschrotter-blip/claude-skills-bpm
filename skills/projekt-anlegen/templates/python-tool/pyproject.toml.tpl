[project]
name = "{{slug}}"
version = "0.1.0"
description = "{{name}}"
requires-python = ">=3.12"
dependencies = []

[project.optional-dependencies]
dev = [
    "pytest=={{v_pytest}}",
    "pytest-xdist=={{v_pytest_xdist}}",
    "ruff=={{v_ruff}}",
]

[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[tool.setuptools]
packages = ["{{package}}"]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-n auto"

[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP"]
