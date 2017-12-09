#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DATA_DIR=$SCRIPT_DIR/unomaha_utils/data

source ~/envs/course_scraper/bin/activate
$SCRIPT_DIR/course_scraper/scraper.py > $DATA_DIR/all_courses.json.new

if [ $? ]; then
    mv -v $DATA_DIR/all_courses.json $DATA_DIR/all_courses.json.old
    mv -v $DATA_DIR/all_courses.json.new $DATA_DIR/all_courses.json
else
    echo "Scraping failed"
fi
