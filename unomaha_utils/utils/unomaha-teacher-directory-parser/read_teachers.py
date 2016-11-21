#!/usr/bin/env python2

from parse import search
import random
import string

with open("teachers.txt") as f:
    for line in f.readlines():
        res = search(line.strip())
        for teacher, email in res:
            password = "".join((random.choice(string.ascii_lowercase) for x in range(7)))
            username = email.split("@")[0]
            print(teacher + ":" + email + ":" + password)
            requests.post("http://bdo.pw:5000/user/add", data={"name": teacher, "username": username, "password": password, "token": "acmsecret", "bracket": "teacher"})
