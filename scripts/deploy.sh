
# See README.md for how to get these values

TAG="0.0.$GITHUB_RUN_NUMBER" # Initially set this to "0.0.1", and then update to come from Github Actions
MACHINE_ID=$MACHINE_ID  # Initially hard code this to your machine ID for the first deploy, e.g. "e2865c22a34548", and then update to use whatever env var is in Github Actions
APP_NAME="changedetection-a32cf"

docker build -t registry.fly.io/$APP_NAME:deployment-$TAG . --platform linux/amd64
docker push registry.fly.io/$APP_NAME:deployment-$TAG
fly machine update $MACHINE_ID --yes --image registry.fly.io/$APP_NAME:deployment-$TAG --schedule=hourly --metadata fly_process_group=app
