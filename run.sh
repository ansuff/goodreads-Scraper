#!/bin/bash

# Check if Poetry is installed
if ! command -v poetry &> /dev/null
then
    echo "Poetry is not installed. Please install it to run this script."
    exit 1
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
  echo "add --skip-poetry to skip poetry installation"
  echo ""
  exit 1
}

cmd=$1
shift || true
case "$cmd" in
scrap) task_scrap ;;
unittest) task_test ;;
lint) task_lint ;;
*) usage ;;
esac