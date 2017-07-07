import json

from flask import Blueprint, request, abort, render_template, redirect, url_for, current_app

from utils.course_history.search import get_course_instances, get_term

classes = Blueprint('classes', __name__,
                        template_folder='templates')

term_data = None
college_keys = None
course_keys = None

# get latest semester
def init_data(new_term_data):
    global college_keys
    global course_keys
    global term_data
    if term_data is None:
        term_data = new_term_data
        latest_colleges = term_data[sorted(new_term_data.keys())[-1]]

        college_keys = sorted(latest_colleges.keys())
        course_keys = list(set(sum([list(x.keys()) for x in latest_colleges.values()], [])))

@classes.route("/")
def hello():
    return redirect(url_for('classes.course_search_search'))

@classes.route('/search')
def course_search_search():
    init_data(current_app.get_term_data())
    return render_template("class_search.html", college_keys=college_keys, course_keys=course_keys)

@classes.route('/view')
def course_search_view():
    init_data(current_app.get_term_data())
    college_key = request.args.get("college")
    term_key = request.args.get("term")
    current_app.logger.info("Searching for term %s college %s", current_app.term_key_to_name[term_key], college_key)

    colleges = term_data.get(term_key)
    if not colleges:
        abort(404)

    courses = colleges.get(college_key)
    if not courses:
        abort(404)

    for _, course in courses.items():
        reversed(course['sections'].items())
    return render_template("class_view.html", college_name=college_key, courses=courses, term_key=term_key)

@classes.route('/history')
def course_history():
    init_data(current_app.get_term_data())
    college_key = request.args.get("college")
    course_key = request.args.get("course")
    current_app.logger.info("Searching for history of %s%s", college_key, course_key)

    if not college_key or not course_key:
        abort(404)

    college_key = college_key.upper()

    course_instances = get_course_instances(term_data, college_key, course_key)

    if len(course_instances) < 1:
        abort(404)

    return render_template("class_history.html", college_key=college_key,
                                                  course_key=course_key,
                                                  course_instances=course_instances)
