#!/usr/bin/env python
import datetime
import logging
import json
import re

from flask import Flask, render_template, current_app

from collections import OrderedDict
from os import path

from views.main import main
from views.classes import classes
from views.rooms import rooms
from views.teachers import teachers

from util import get_term_mapping
from utils.course_history.search import get_term, get_term_from_date

SCRIPT_PATH = path.dirname(path.realpath(__file__))

DATA_DIR = path.join(SCRIPT_PATH, "data")
TEST_DATA_DIR = path.join(SCRIPT_PATH, "test_data")

ALL_COURSES_FNAME = "all_courses.json"

wlog = logging.getLogger('werkzeug')
wlog.setLevel(logging.ERROR)

app = Flask(__name__)

def create_app():
    app = Flask(__name__)
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 7776000 # 3 months

    app.logger.setLevel(logging.INFO)

    app.register_blueprint(main, url_prefix='')
    app.register_blueprint(classes, url_prefix='/classes')
    app.register_blueprint(rooms, url_prefix='/rooms')
    app.register_blueprint(teachers, url_prefix='/teachers')

    app.jinja_env.globals.update(get_term=get_term, get_term_from_date=get_term_from_date)

    app.term_data = None
    def get_term_data():
        if current_app.term_data is None:
            if current_app.testing:
                current_app.DATA_DIR = TEST_DATA_DIR
            else:
                current_app.DATA_DIR = DATA_DIR
            data_path = path.join(current_app.DATA_DIR, ALL_COURSES_FNAME)

            if not path.exists(data_path):
                print("Couldn't find term data at {}, exiting".format(data_path))
                sys.exit(1)

            logging.info("Loading term data from %s...", data_path)
            with open(data_path) as f:
                courses_dict = json.load(f, object_pairs_hook=OrderedDict)
                current_app.courses_meta = courses_dict['meta']
                current_app.term_data = courses_dict['term_data']

                current_app.term_key_to_name = get_term_mapping(current_app.term_data)
                current_app.term_name_to_key = {v:k for k, v in current_app.term_key_to_name.items()}
            logging.info("Term data loaded")

        return current_app.term_data
    app.get_term_data = get_term_data

    @app.before_request
    def before_request():
        get_term_data()

    @app.context_processor
    def inject_user():
        return {
            "courses_meta": current_app.courses_meta,
            "last_updated": datetime.datetime.fromtimestamp(current_app.courses_meta['time']).strftime("%Y-%m-%d"),
            "term_key_to_name": current_app.term_key_to_name,
            "term_name_to_key": current_app.term_name_to_key
        }

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    return app

app = create_app()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5566, debug=False)
