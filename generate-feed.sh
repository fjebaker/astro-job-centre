#!/bin/sh

JOB_URL='https://aas.org/jobregister?f%5B0%5D=category%3A511'
PYTHON_EXEC=/home/lilith/Developer/jobcenter/venv/bin/python3

lightpanda "$JOB_URL" --dump | "$PYTHON_EXEC" parse.py

