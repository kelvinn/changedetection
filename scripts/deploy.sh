#!/usr/bin/env bash

# Abort the script if any command fails
set -e

npm install -g serverless
sls plugin install -n serverless-python-requirements
sls deploy