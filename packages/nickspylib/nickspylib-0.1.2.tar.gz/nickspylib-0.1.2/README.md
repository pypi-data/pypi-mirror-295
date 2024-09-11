# nicks-pylib

Example of a Python library

## Start poetry shell

```bash
$ poetry shell
```

## Install Dependencies

```bash
$ poetry install
```

## Run Tests With Poetry

```bash
$ poetry run pytest
```

## Build the Package

```bash
$ poetry build
```

## Useful Poetry Commands

* poetry show —Lists the packages installed in your current project’s virtual environment. You can use `poetry show --tree` to view dependencies in a tree format to help understand the hierarchical structure of package dependencies.
* poetry add — Add new dependencies to your project. It automatically updates your pyproject.toml and poetry.lock files.
* poetry install — Reads the pyproject.toml file from the current project, resolves the dependencies, and installs them. If a poetry.lock file exists, it will use the exact versions from there instead of resolving them.
* poetry env — Shows information about the current environment or even removes virtual environments associated with the project.
poetry shell— Spawns a shell, like bash or zsh, within the virtual environment created by Poetry.
* poetry remove— Removes a package that is no longer necessary from the pyproject.toml and lock file.
poetry version minor— Bumps the minor version of your project (according to semantic versioning). Similar for MAJOR or PATCH .
* poetry publish — Publishes a project to PyPI or another configured repository.