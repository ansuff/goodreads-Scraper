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
task_scrape() {
    poetry run python main.py
}

usage() {
  echo "USAGE"
  echo "scrape | unittest | lint"
  echo ""
  exit 1
}

cmd=$1
shift || true
case "$cmd" in
scrape) task_scrape ;;
unittest) task_test ;;
lint) task_lint ;;
*) usage ;;
esac