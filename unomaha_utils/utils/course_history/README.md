**Course listing up to date as of 2015-11-08**

Searches for terms when a course was last taught.

Uses BenDoan/unomaha-course-scraper to get the list of courses.

## Example runs
```
→ ./search.py CSCI 4700
Loading courses...
Tallying...

Fall 2011
COMPILER CONSTRUCTION
Section 001 - William Mahoney (5/20)

Spring 2014
COMPILER CONSTRUCTION
Section 001 - William Mahoney (4/20)

→ ./search.py CSCI 1620
Loading courses...
Tallying...

Fall 2011
INTRODUCTN TO COMPUTER SCI II
Section 001 - Patrick M. Cavanaugh (26/30)
Section 002 - Patrick M. Cavanaugh (29/30)
Section 003 - Sandra Lynn Vlasnik  (30/30)
Section 098 - Patrick M. Cavanaugh (4/3)
Section 099 - Patrick M. Cavanaugh (2/3)
Section 850 - Sandra Lynn Vlasnik  (25/25)

...

Spring 2016
INTRO TO COMPUTER SCIENCE II
Section 001 - Patrick M. Cavanaugh (7/30)
Section 002 - Brian C Ricks        (9/30)
Section 003 - Mark Allan Pauley    (12/30)
Section 004 - Mai Ren              (0/30)
Section 005 - Brian C Ricks        (2/30)
Section 006 - Ashwathy P Ashokan   (3/30)
Section 850 - Patrick M. Cavanaugh (7/25)
```

## Usage
```
Usage:
    ./search.py <college> <course_number> [options]

Options:
    -h, --help          Prints this help message.
    -f=<f>, --file=<f>  Manually choose the courses file [default: all_courses.json].
```
