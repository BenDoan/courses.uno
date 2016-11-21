import json

from collections import OrderedDict
from os import path

SCRIPT_PATH = path.dirname(path.realpath(__file__))

def get_courses():
    print "Loading course data"
    with open(path.join(SCRIPT_PATH, "all_courses.json")) as f:
        return json.load(f, object_pairs_hook=OrderedDict)
courses_dict = get_courses()
courses_meta = courses_dict['meta']
term_data = courses_dict['term_data']
