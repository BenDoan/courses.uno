#!/usr/bin/env python

"""
Usage:
    ./search.py <college> <course_number> [options]

Options:
    -h, --help          Prints this help message.
    -f=<f>, --file=<f>  Manually choose the courses file [default: all_courses.json].
"""

import json
import logging
from collections import OrderedDict

def get_term(course):
    try:
        date = next(course['sections'].itervalues())['Date']
    except AttributeError:
        date = next(iter(course['sections'].values()))['Date']

    return get_term_from_date(date)

def get_term_from_date(date):
    term_ranges = {('aug', 'dec'): "Fall",
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
    if term == "Unknown":
        print("Unknown term,  date is:", date)

    year = date.split("-")[0].split(",")[-1].strip()

    return "{} {}".format(term, year)

def get_course_instances(courses, college, course_number):
    matching_courses = []
    for term_number, term in courses.items():
        if college in term:
            if course_number in term[college]:
                matching_course = term[college][course_number]
                matching_courses.append(matching_course)
    return matching_courses

def _main():
    args = docopt(__doc__, version="1")

    print("Loading courses...")
    courses = json.load(open(args['--file']), object_pairs_hook=OrderedDict)
    college = args['<college>']
    course_number = args['<course_number>']

    for matching_course in get_course_instances(courses, college, course_number):
        print(get_term(matching_course))
        print(matching_course['title'])

        max_teach_len = max(map(len, (x['Instructor'] for x in matching_course['sections'].values() if 'Instructor' in x)))
        for section_number, section in matching_course['sections'].items():
            if 'Instructor' in section:
                print("Section {} - {:<{}s} ({}/{})"
                        .format(section_number,
                                section['Instructor'],
                                max_teach_len,
                                section['Enrolled'],
                                section['Class Max']))

        print("")

if __name__ == '__main__':
    from docopt import docopt
    _main()
