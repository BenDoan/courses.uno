import json

from collections import OrderedDict
from os import path
import sys
import logging

from flask import current_app

logging.basicConfig(level=logging.INFO)

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
