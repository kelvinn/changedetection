#!/usr/bin/env bash

# Abort the script if any command fails
set -e

npm i -D serverless
npx sls plugin install -n serverless-python-requirements
npx sls deploy