import json
import re

from flask import Blueprint, request, abort, render_template, redirect, url_for, current_app
from util import term_data

from utils.classroom_schedules.find_room_schedules import build_room_dict

rooms = Blueprint('rooms', __name__,
                        template_folder='templates')

# get latest semester
colleges = term_data[sorted(term_data.keys())[-1]]

room_dict = build_room_dict(colleges)
buildings = set()
for room in room_dict.iterkeys():
    building_room_pattern = r'([^0-9]+)([0-9]+)'
    matches = re.search(building_room_pattern, room)

    if matches:
        buildings.add(matches.group(1).strip())
buildings = list(buildings)

@rooms.route("/", methods=["GET"])
def hello():
    return redirect(url_for('rooms.room_search_search'))

@rooms.route('/search')
def room_search_search():
    return render_template("room_search.html", buildings=buildings)

@rooms.route('/view')
def room_search_view():
    building = request.args.get("building")
    room_number = request.args.get("room_number")
    current_app.logger.info("Searching for schedule of %s %s", building, room_number)

    building_room = building + " " + room_number
    rooms = room_dict[building_room]

    if not rooms:
        abort(404)

    return render_template("room_view.html", building_room=building_room, rooms=rooms)
