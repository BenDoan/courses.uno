#!/bin/bash

./update_data.sh && ./docker_build.sh && docker save unomaha_utils | gzip | ssh flainted.com docker load
