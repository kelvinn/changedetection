
#!/usr/bin/env bash

# Abort the script if any command fails
set -e

alembic upgrade head
pytest
scrapy check
