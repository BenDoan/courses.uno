FROM debian:latest

RUN apt-get update
RUN apt-get install -q -y python python-pip vim net-tools

COPY ./unomaha_utils/requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY ./unomaha_utils/ /unomaha_utils

EXPOSE 5566

WORKDIR /unomaha_utils
CMD ["/usr/local/bin/gunicorn", "-t", "120", "-w", "2", "-b", "0.0.0.0:5566", "--error-logfile", "-", "web:app"]
