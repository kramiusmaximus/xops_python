#!/bin/bash

docker-compose -f docker-compose.yaml build --no-cache
docker-compose -f docker-compose.yaml up
