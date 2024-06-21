#!/bin/bash
# start-docker.sh

# Ensure the environment is correctly set up
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# Set the full path to your project directory
PROJECT_DIR="/srv/dev-disk-by-uuid-8258f36d-2a42-4932-9e7a-54da8c8da37e/scripts/reminder-email-python/python"

# Change to the project directory
cd "$PROJECT_DIR"

# Run the Docker container
docker run -i --rm --name sendmail.py \
    -v "$PROJECT_DIR":/usr/src/app \
    -v /srv/dev-disk-by-uuid-83754a0e-1568-45ba-b5e1-a2ae0229ae80/common/Doks/emlekezteto/:/usr/src/app/xls/ \
    -v /srv/dev-disk-by-uuid-8258f36d-2a42-4932-9e7a-54da8c8da37e/scripts/reminder-email-python/logs/:/usr/src/app/logs/ \
    -w /usr/src/app reminder-email-script:latest