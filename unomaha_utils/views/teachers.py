import json
import os
import tempfile

from flask import (
    Blueprint,
    request,
    abort,
    render_template,
    redirect,
    url_for,
    current_app,
    make_response
)
from util import term_data, DATA_DIR

from os import path

from utils.teacher_info.teacher_info import get_teacher_info
from utils.word_cloud.gen_cloud import get_all_words, plot_cloud, clean_text

SCRIPT_DIR = path.dirname(path.realpath(__file__))

WORD_CLOUD_CACHE = path.join(SCRIPT_DIR, "..", "data", "UU_WORDCLOUDS")

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
    current_app.logger.info("Getting word cloud for %s", teacher_name)

    if not teacher_name:
        abort(400)

    cached_png = get_cached_wc(teacher_name)
    if not cached_png:
        words = get_all_words(DATA_DIR, teacher_name)
        png = plot_cloud(clean_text(words))
        cache_wc(teacher_name, png)
    else:
        png = cached_png

    response = make_response(png)
    response.headers['Content-Type'] = 'image/png'
    return response

def get_cached_wc(teacher_name):
    fname = path.join(WORD_CLOUD_CACHE, teacher_name+".png")
    if path.isfile(fname):
        with open(fname, 'rb') as f:
            return f.read()

def cache_wc(teacher_name, png):
    if not path.isdir(WORD_CLOUD_CACHE):
        os.mkdir(WORD_CLOUD_CACHE)

    fname = path.join(WORD_CLOUD_CACHE, teacher_name+".png")
    with open(fname, "wb") as f:
        f.write(png)
