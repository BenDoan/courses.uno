#!/bin/bash

(./update_data.sh && ./docker_build.sh && ./docker_test.sh && cd ~/flainted_compose/ && /usr/local/bin/docker-compose up -d &> /dev/null) > /dev/null
