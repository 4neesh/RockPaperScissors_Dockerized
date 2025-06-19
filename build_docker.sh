#!/bin/sh

DOCKER_TAG=${1:-my-app}
DOCKER_DEFAULT_PLATFORM=${2:-linux/arm64/v8}

docker build --platform $DOCKER_DEFAULT_PLATFORM -t $DOCKER_TAG .