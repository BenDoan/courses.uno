#!/usr/bin/env python
import datetime
import logging
import json
import re

from flask import Flask, render_template

from views.main import main
from views.classes import classes
from views.rooms import rooms
from views.teachers import teachers

from util import courses_meta, term_key_to_name, term_name_to_key
from utils.course_history.search import get_term, get_term_from_date

wlog = logging.getLogger('werkzeug')
wlog.setLevel(logging.ERROR)

app = Flask(__name__)

def create_app():
    app = Flask(__name__)
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 86400 # 1 day

    app.logger.setLevel(logging.INFO)

    app.register_blueprint(main, url_prefix='')
    app.register_blueprint(classes, url_prefix='/classes')
    app.register_blueprint(rooms, url_prefix='/rooms')
    app.register_blueprint(teachers, url_prefix='/teachers')

    app.jinja_env.globals.update(get_term=get_term, get_term_from_date=get_term_from_date)

    @app.context_processor
    def inject_user():
        return {
            "courses_meta": courses_meta,
            "last_updated": datetime.datetime.fromtimestamp(courses_meta['time']).strftime("%Y-%m-%d"),
            "term_key_to_name": term_key_to_name,
            "term_name_to_key": term_name_to_key
        }

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    return app

app = create_app()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5566, debug=False)
