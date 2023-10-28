#!/bin/bash

# Abort the script if any command fails
set -e


# See README.md for how to get these values

TAG="0.0.$GITHUB_RUN_NUMBER" # Initially set this to "0.0.1", and then update to come from Github Actions
APP_NAME="changedetection-a32cf"

fly deploy --ha=false --strategy immediate --wait-timeout 240

sleep 10 # Wait for deploy to finish

fly scale count 1 --yes --process-group worker

MACHINE_ID=$(fly machine list --json | jq -r -c '.[] | select(.config.metadata.fly_process_group == "worker") | .id')
STATE=$(fly machine list --json | jq -r -c '.[] | select(.config.metadata.fly_process_group == "worker") | .state')

# Sometimes a machine stays in the 'destroying' state for a while 
# and Fly's gateway times out, so we are using this little hack to
# to make sure it hs actually finished being replaced
until [[ "$STATE" == "stopped" || "$STATE" == "started" ]]
do
   sleep 10
   STATE=$(fly machine list --json | jq -r -c '.[] | select(.config.metadata.fly_process_group == "worker") | .state')
   echo "Waiting for machine" $MACHINE_ID "to enter 'stopped' state. Current state: " $STATE
done

fly machine run $MACHINE_ID --wait-timeout 600 --restart on-fail --skip-health-checks --schedule=daily --metadata fly_process_group=worker
