FROM debian:latest

RUN apt-get update
RUN apt-get install -q -y python python-dev python-pip
RUN pip install -U pip
RUN pip install packaging
RUN apt-get install -q -y python python-dev python-pip libfreetype6 libfreetype6-dev libpng12-dev pkg-config libjpeg-dev python-tk

COPY ./unomaha_utils/requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY ./unomaha_utils/ /unomaha_utils

VOLUME /unomaha_utils/unomaha-utilities/data
EXPOSE 5566

WORKDIR /unomaha_utils
CMD ["/usr/local/bin/gunicorn", "-t", "120", "-w", "2", "-b", "0.0.0.0:5566", "--error-logfile", "-", "web:app"]
