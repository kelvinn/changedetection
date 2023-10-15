#!/bin/bash

# Abort the script if any command fails
set -e


# See README.md for how to get these values

TAG="0.0.$GITHUB_RUN_NUMBER" # Initially set this to "0.0.1", and then update to come from Github Actions
APP_NAME="changedetection-a32cf"

fly deploy --ha=false --strategy immediate --wait-timeout 240

sleep 5 # Wait for machine to get replaced

MACHINE_ID=$(fly machine list --json | jq -r '.[] | select(.config.metadata.fly_process_group == "worker") | .id')
fly machine update $MACHINE_ID --yes --restart on-fail --skip-health-checks --schedule=daily --metadata fly_process_group=worker
