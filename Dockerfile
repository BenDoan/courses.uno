FROM base/archlinux

RUN pacman -Syy && pacman -S --noconfirm base-devel python python-pip

COPY ./unomaha_utils/requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY ./unomaha_utils/ /unomaha_utils

VOLUME /unomaha_utils/unomaha-utilities/data
EXPOSE 5566

WORKDIR /unomaha_utils
CMD ["gunicorn", "-t", "120", "-w", "2", "-b", "0.0.0.0:5566", "--error-logfile", "-", "web:app"]
