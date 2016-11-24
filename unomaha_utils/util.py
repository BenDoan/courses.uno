import json

from collections import OrderedDict
from os import path
import sys
import logging

logging.basicConfig(level=logging.INFO)

SCRIPT_PATH = path.dirname(path.realpath(__file__))
TERM_DATA_PATH = path.join(SCRIPT_PATH, "static", "all_courses.json")

def get_courses():
    if not path.exists(TERM_DATA_PATH):
        print "Couldn't find course data at {}".format(TERM_DATA_PATH)
        sys.exit(1)

    logging.info("Loading course data...")
    with open(TERM_DATA_PATH) as f:
        term_data = json.load(f, object_pairs_hook=OrderedDict)
    logging.info("Course data loaded")
    return term_data
courses_dict = get_courses()
courses_meta = courses_dict['meta']
term_data = courses_dict['term_data']

def get_term_from_date(date):
    term_ranges = {('aug', 'dec'): "Fall",
                ('jan', "apr"): "Spring",
                ('jan', "may"): "Spring",
                ('may', "jun"): "Summer",
                ('may', 'jul'): "Summer",
                ('may', 'aug'): "Summer",
                ('jul', 'aug'): "Summer",
                ('jun', 'aug'): "Summer"
                }

    term = "Unknown"
    for months, term_name in term_ranges.items():
        if months[0] in date.lower() and months[1] in date.lower():
            term = term_name

    year = date.split("-")[0].split(",")[-1].strip()

    if term == "Unknown":
        logging.warn("Unknown term,  date is: %s", date)

    return "{} {}".format(term, year), term != "Unknown"

def get_term_name(colleges):
    for _, courses in colleges.items():
        for _, course_info in courses.items():
            for _, section_info in course_info['sections'].items():
                potential_term_date = section_info.get('Date')
                term_str, is_good = get_term_from_date(potential_term_date)
                if is_good:
                    return term_str

def get_term_mapping(term_data):
    mapping = {}
    for term_key, colleges in term_data.items():
        term_name = get_term_name(colleges)
        mapping[term_key] = term_name
    return mapping
term_key_to_name = get_term_mapping(term_data)
term_name_to_key = {v:k for k, v in term_key_to_name.items()}
