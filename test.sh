#!/bin/bash

docker-compose -f docker-compose-test.yaml build --no-cache
docker-compose -f docker-compose-test.yaml up -d postgres_db
docker-compose -f docker-compose-test.yaml up fastapi-backend
backend_exit_code=$?

docker-compose -f docker-compose-test.yaml stop

if [ $backend_exit_code -eq 0 ]; then
    echo "Success: Integration tests passed"
else
    echo "Failure: Encountered an error during integration tests."
fi