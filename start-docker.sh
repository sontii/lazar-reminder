#!/bin/bash
# start-docker.sh

# Ensure the environment is correctly set up
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# Set the full path to your project directory
PROJECT_DIR="/srv/dev-disk-by-uuid-8258f36d-2a42-4932-9e7a-54da8c8da37e/scripts/reminder-email-python/python"

# Change to the project directory
cd "$PROJECT_DIR"

# Build the Docker image
if ! BUILD_OUT=$(docker build -t reminder-email-script:latest . 2>&1); then
    echo "$(date "+%F %T") docker build failed:"
    echo "$BUILD_OUT" | tail -20
    exit 1
fi

# Run the Docker container (code is baked into the image, only config and data are mounted)
docker run -i --rm --name sendmail.py \
    -v "$PROJECT_DIR/.env":/usr/src/app/.env:ro \
    -v /etc/localtime:/etc/localtime:ro \
    -v /srv/dev-disk-by-uuid-83754a0e-1568-45ba-b5e1-a2ae0229ae80/common/Doks/emlekezteto/:/usr/src/app/xls/ \
    -v /srv/dev-disk-by-uuid-8258f36d-2a42-4932-9e7a-54da8c8da37e/scripts/reminder-email-python/logs/:/usr/src/app/logs/ \
    -w /usr/src/app reminder-email-script:latest > /dev/null
