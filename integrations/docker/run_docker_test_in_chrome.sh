#!/bin/bash
set -e
# Run example test from inside Docker image
echo "Running example SeleniumBase test from Docker with headless Chrome..."
cd /SeleniumBase/examples/
/usr/bin/python3 tee-time-test.py -r
which python3
exec "$@"
