#!/bin/bash
set -e
# Run example test from inside Docker image
echo "Running example SeleniumBase test from Docker with headless Chrome..."
ls
cd /SeleniumBase/examples/
ls
/usr/bin/python3 my_first_test.py
which python3
exec "$@"
