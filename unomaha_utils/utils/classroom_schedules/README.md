This script uses the course output scraped with [BenDoan/unomaha-course-scraper](https://github.com/bendoan/unomaha-course-scraper) to
find the class schedule for each room at UNO (Univeristy of Nebraska, Omaha)

**Note:** This script requires a file named all_courses.json containing the output of [BenDoan/unomaha-course-scraper](https://github.com/bendoan/unomaha-course-scraper) to be in the current directory

```
Usage: ./find_room_schedules.py [classroom]
```


## Examples:
```
→ ./find_room_schedules.py Arts and Sciences Hall 188
Arts and Sciences Hall 188
  MW
    01:00PM - 02:15PM : ADVANCED PUBLIC SPEAKING
  MWF
    08:00AM - 08:50AM : PUBLIC SPEAKING FUNDS
    09:00AM - 09:50AM : SMALL GROUP
    10:00AM - 10:50AM : PUBLIC SPEAKING FUNDS
  W
    03:00PM - 07:00PM : INTERCOLLEG FORENSIC ACTVTS
  TR
    08:30AM - 09:45AM : PUBLIC SPEAKING FUNDS
    10:00AM - 11:15AM : SPCH COMM  CAPSTONE SEMINAR
    11:30AM - 12:45PM : INTERVIEWING
    01:00PM - 02:15PM : INTERPERSONAL COMMUNICATION
    02:30PM - 03:45PM : PRINCIPLES OF PR

→ ./find_room_schedules.py
Allwine Hall 108
  T
    01:00PM - 03:50PM : BIOLOGY II
  W
    01:00PM - 03:50PM : BIOLOGY II
  R
  ...
```
