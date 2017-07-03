import json
import re

from flask import Blueprint, request, abort, render_template, redirect, url_for, current_app

from utils.classroom_schedules.find_room_schedules import build_room_dict

rooms = Blueprint('rooms', __name__,
                        template_folder='templates')

term_data = None
colleges = None
buildings = None
room_dicts_by_term = None

def init_data(new_term_data):
    global term_data
    global colleges
    global buildings
    global room_dicts_by_term
    if term_data is None:
        term_data = new_term_data
        colleges = term_data[sorted(term_data.keys())[-1]]

        room_dicts_by_term = {}
        for term_key, colleges in term_data.items():
            room_dicts_by_term[term_key] = build_room_dict(colleges)

        # generate list of buildings for dropdown
        buildings = set()
        for term_key, room_dict in room_dicts_by_term.items():
            for room in room_dict.keys():
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
    init_data(current_app.get_term_data())
    return render_template("room_search.html", buildings=buildings)

@rooms.route('/view')
def room_search_view():
    init_data(current_app.get_term_data())
    term = request.args.get("term")
    building = request.args.get("building")
    room_number = request.args.get("room_number")
    current_app.logger.info("Searching for schedule of %s %s for term %s", building, room_number, term)

    room_dict = room_dicts_by_term.get(term)
    if not room_dict:
        abort(404)

    building_room = building + " " + room_number
    rooms = room_dict[building_room]

    if not rooms:
        abort(404)

    return render_template("room_view.html", building_room=building_room, rooms=rooms, term_key=term)
