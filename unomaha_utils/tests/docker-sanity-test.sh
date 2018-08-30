#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

function req(){
    code=$(curl -sI "http://localhost:5566/$1" | grep HTTP | awk '{ print $2 }')
    [[ "$code" -eq "200" ]]
}

function error(){
    echo "Error: failed to request $1" 1>&2
}
cd $SCRIPT_DIR/..

gunicorn -w 1 -b localhost:5566 --error-logfile - web:app > /dev/null 2>&1 &
APP_PID=$!

sleep 1

req ""  || error "homepage"
req "classes/search" || error "class search"
req "rooms/search" || error "room search"
req "teachers/search" || error "teachers search"

req "classes/view?term=1178&college=ACCT"  || error "course info"
req "classes/history?college=ACCT&course=2000"  || error "course history"
req "rooms/view?term=1168&building=Peter+Kiewit+Institute&room_number=260" || error "room schedule"
req "teachers/view?lastname=azadmanesh" || error "teacher history"

kill $APP_PID
sleep 2
