#! /usr/bin/env sh

# Exit in case of error
set -e

# Install backend - python dependencies
(cd ./application/ && poetry install --extras debug)