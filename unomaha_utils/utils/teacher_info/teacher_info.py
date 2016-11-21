#!/usr/bin/env python
import collections

class CourseInfo(object):
    def __init__(self, term_number, college_key, course_number,
                       course_title, section_info):
        self.term_number

class OrderedAVDict(collections.OrderedDict):
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value

def name_matches(search_name, candidate_name):
    split_candidate_name = [x.lower() for x in candidate_name.replace(',', '').split(" ")]
    is_match = search_name.strip().lower() in split_candidate_name
    return is_match

def get_teacher_info(courses, teacher_name):
    matching_courses = OrderedAVDict()
    for term_number, colleges in courses.items():
        for college, classes in colleges.items():
            for course_number, course_info in classes.items():
                for section_number, section_info in course_info['sections'].items():
                    if name_matches(teacher_name, section_info.get('Instructor', '')):
                        matching_courses[college][course_number][term_number][section_number] = {
                            'course_title': course_info['title'],
                            'section_info': section_info
                        }
    return matching_courses
