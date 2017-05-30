import json

from flask import Blueprint, request, abort, render_template, redirect, url_for, current_app, make_response
from util import term_data, DATA_DIR

from utils.teacher_info.teacher_info import get_teacher_info
from utils.word_cloud.gen_cloud import get_all_words, plot_cloud, clean_text

teachers = Blueprint('teachers', __name__,
                        template_folder='templates')

@teachers.route("/")
def hello():
    return redirect(url_for('teachers.teacher_search_search'))

@teachers.route('/search')
def teacher_search_search():
    return render_template("teacher_search.html")

@teachers.route('/view')
def teacher_search_view():
    teacher_last_name = request.args.get('lastname')
    current_app.logger.info("Searching for teacher %s", teacher_last_name)

    matching_courses = get_teacher_info(term_data, teacher_last_name)

    if not matching_courses:
        abort(404)

    return render_template("teacher_view.html", matching_courses=matching_courses, name=teacher_last_name)


@teachers.route('/cloud.png')
def teacher_wordcloud():
    teacher_name = request.args.get('name')
    current_app.logger.info("Generating word cloud for %s", teacher_name)

    if not teacher_name:
        abort(400)

    words = get_all_words(DATA_DIR, teacher_name)
    png = plot_cloud(clean_text(words))

    response = make_response(png)
    response.headers['Content-Type'] = 'image/png'
    return response
