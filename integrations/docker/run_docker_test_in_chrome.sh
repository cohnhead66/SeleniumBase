#!/bin/bash
set -e
# Run example test from inside Docker image
echo "Running example SeleniumBase test from Docker with headless Chrome..."
cd /SeleniumBase/examples/cdp_mode/
/usr/bin/python3 raw_cdp.py
which python3
exec "$@"
