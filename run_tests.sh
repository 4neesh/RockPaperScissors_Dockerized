#!/bin/sh

export PYTHONPATH=/app

# Discover and run all test_*.py files in the tests directory recursively
python3 -m unittest discover -s tests -p "test_*.py" "$@"
