# Unomaha Utils
A collection of basic utilities useful for students and staff at UNOmaha.

A hosted version is available at [uno.flainted.com](http://uno.flainted.com)

The application currently includes:
* A instructor history search
* A course history search
* A course search
* A room schedule search

## Installation

1. Install the python packages with ```pip install -r requirements.txt```
1. Obtain the course data and place it in ```unomaha_utils/data/all_courses.json```. You can obtain this file by either of the following methods:
   * **(preferred)** Download the json file from instance I host [here](http://uno.flainted.com/static/all_courses.json) (this saves the UNO courses search from being hammered with traffic)
   * Run the scraper located in ```utils/course_scraper``` to obtain the course json manually
1. Run the server with one of the following methods:
   * Run the development server with ```python web.py```
   * Run the production server with ```gunicorn -b 0.0.0.0:5566 web:app```
   * Run the docker container with ```./docker_build.sh && docker run -p 80:5566 unomaha_utils```
