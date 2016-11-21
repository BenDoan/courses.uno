#!/usr/env/bin python

import collections
import datetime
import json
import logging
import sys

# logging.basicConfig(level=logging.ERROR)

UNO_TIME_FMT = "%I:%M%p"
DAYS = ["M", "MW", "MR", "MF", "MTW", "MWR", "MWF", "MTR", "MTWR", "MTWF", "MWRF", "MTWRF", "T", "W", "WF", "R", "TR", "TRF", "F", "FS", "S", "TBA", "U"]


class OrderedAVDict(collections.OrderedDict):
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value

class ClassDay:
    def __init__(self, day_str):
        self.day_str = day_str

    def __lt__(self, other):
        self_idx = DAYS.index(self.day_str)
        other_idx = DAYS.index(other.day_str)
        return self_idx < other_idx

    def __hash__(self):
        return hash(self.day_str)

    def __eq__(self, other):
        return self.day_str == other.day_str

    def __ne__(self, other):
        return not(self == other)

    def __str__(self):
        return self.day_str

class TimeRange(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end

    @staticmethod
    def from_uno_str(time_range_str):
        start_s, end_s = [x.strip() for x in time_range_str.split("-")]

        start = datetime.datetime.strptime(start_s, UNO_TIME_FMT)
        end = datetime.datetime.strptime(end_s, UNO_TIME_FMT)

        return TimeRange(start, end)

    def __lt__(self, other):
        if self.start < other.start:
            return True
        elif self.start == other.start:
            return self.end < other.end
        else:
            return False

    def __str__(self):
        return "{} - {}".format(self.start.strftime(UNO_TIME_FMT),
                                self.end.strftime(UNO_TIME_FMT))

def build_room_dict(semester):
    room_dict = OrderedAVDict()
    for college, classes in semester.items():
        for course_num, course_info in classes.items():
            for section_number, section_info in course_info['sections'].items():
                room = section_info.get('Location')
                days = section_info.get('Days')
                times = section_info.get('Time')
                if all([room, days, times]):
                    try:
                        tr = TimeRange.from_uno_str(times)
                        room_dict[room][ClassDay(days)][tr] = (course_info['title'], section_info.get('Instructor', "Teacher TBA"))
                    except ValueError:
                        logging.debug("Failed to parse time str: %s", times)
                else:
                    log_str = "Failed to parse college(%s):course(%s):room(%s):days(%s):times(%s)"
                    logging.debug(log_str,
                            college,
                            course_info['title'],
                            room, days, times)

    return room_dict


def _main():
    with open("all_courses.json") as f:
        semesters = json.load(f)

    latest_sem = semesters[sorted(semesters.keys())[-1]]
    room_dict = build_room_dict(latest_sem)

    # Example: "Peter Kiewit Institute 260"
    if len(sys.argv) > 1:
        room = " ".join(sys.argv[1:])
        room_dict = {room: room_dict[room]}

    for room, days in sorted(room_dict.items(), key=lambda x: x[0]):
        print(room)
        for day, times in sorted(days.items(), key=lambda x: DAYS.index(x[0])):
            print(" ", day)
            for t, course in sorted(times.items(), key=lambda x: x[0]):
                print("   ", t, ":", course)


if __name__ == '__main__':
    _main()
