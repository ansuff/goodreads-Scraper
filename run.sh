#!/bin/bash

# Define a function to install Poetry
install_poetry() {
    echo "Installing Poetry..."
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
    source $HOME/.poetry/env
}

# Check if Poetry is installed
if ! command -v poetry &> /dev/null
then
    install_poetry
fi

# Install dependencies
poetry install

# Define a function to run the tests
task_test() {
    poetry run pytest
}

# Define a funtion to lint the code
task_lint() {
    poetry run ruff check .
}

# Define a function to run the main script
task_scrap() {
    poetry run python main.py
}

usage() {
  echo "USAGE"
  echo "scrap | unittest | poetry | lint"
  echo ""
  exit 1
}

cmd=$1
shift || true
case "$cmd" in
scrap) task_scrap ;;
unittest) task_test ;;
poetry) install_poetry ;;
lint) task_lint ;;
*) usage ;;
esac