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

# Define a function to run the main script
task_scrap_store() {
    poetry run python main.py
}

usage() {
  echo "USAGE"
  echo "scrap-store | test-project | poetry"
  echo ""
  exit 1
}

cmd=$1
shift || true
case "$cmd" in
scrap-store) task_scrap_store ;;
test-project) task_test ;;
poetry) install_poetry ;;
*) usage ;;
esac