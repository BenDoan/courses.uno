#!/bin/bash

docker run -it --rm unomaha_utils /unomaha_utils/tests/docker-sanity-test.sh
if [[ $? ]]; then
    echo "Passed sanity check"
else
    echo "Failed sanity check"
    exit 1
fi

docker run -it --rm unomaha_utils bash -c "cd /unomaha_utils && nosetests"
if [[ $? ]]; then
    echo "Passed unit tests"
else
    echo "Failed unit tests"
    exit 1
fi
