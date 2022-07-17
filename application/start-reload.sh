#! /usr/bin/env bash

# Start the service with reload
uvicorn main:app --host 0.0.0.0 --port 80 --reload