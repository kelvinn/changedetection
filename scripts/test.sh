
#!/usr/bin/env bash

# Abort the script if any command fails
set -e

pytest tests.py
scrapy check
