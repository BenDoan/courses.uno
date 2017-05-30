#!/usr/bin/env python2
import enum
import json
import random
import re
import StringIO
import sys

from os import path

import matplotlib
matplotlib.use('Agg')

from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import numpy as np
from PIL import Image

d = path.dirname(__file__)

common_words = [
    "know", "class" "lot" "the", "teaches", "teaches",
    "help", "stuff", "office", "ll", "teacher", "people",
    "lot", "ask", "talking", "willing", "don", "class",
    "everything", "material", "test", "goes", "seems", "causes",
    "also", "text", "graded", "everyone", "time", "lecture", "lectures",
    "outside", "little", "much", "gives", "well", "always", "question", "make",
    "take", "assignment", "professor", "course", "grade", "will", "subject", "took"
    "semester", "took", "one", "two", "three", "assignments", "every", "uno", "semester",
    "final", "pretty", "quot", "going", "wants", "student", "really", "lots", "questions",
    "quizzes", "tests", "makes", "definitely", "ok", "go", "teaching", "students", "ever",
    "anything", "guy", "believes", "since", "use", "feel", "point", "thing", "even", "things",
    "need", "homework", "teach", "name", "dr", "mr", "come", "matter", "real", "semester",
    "taken", "aka", "else"
]

class ReviewTypes(enum.Enum):
    UNOU = 0
    RMP = 1


def get_teacher_reviews(reviews, review_type, teacher_name):
    possible_names = []
    for name in reviews:
        if teacher_name.lower() in name.lower():
            possible_names.append(name)

    if len(possible_names) == 0:
        print "Found no matching {} reviews".format(review_type.name)
    elif len(possible_names) > 1:
        print "Found multiple matching {} teachers: {}".format(review_type.name, possible_names)
    else:
        name = possible_names[0]
        revs = reviews[name]
        print "Found {} in {} reviews with {} reviews".format(name, review_type.name, len(revs))
        return get_words(revs, review_type)

def get_words(reviews, review_type):
    # unou
    if review_type == ReviewTypes.UNOU:
        return sum([x['improvement'].split() + x['comments'].split() for x in reviews], [])
    # rmp
    elif review_type == ReviewTypes.RMP:
        return sum([x['comments'].split() for x in reviews], [])
    else:
        print "ERROR: found unsupported review"
        sys.exit(1)

def get_unou_words(reviews, teacher_lastname):
    for name, t_reviews in reviews.items():
        if teacher_lastname.lower() in name.lower():
            return sum([x['improvement'].split() + x['comments'].split() for x in t_reviews], [])
    return []


def clean_text(words):
    final_words = []
    for word in words:
        word = word.lower()
        word = re.sub("[^A-Za-z ']", "", word)

        if word in common_words:
            continue

        final_words.append(word)

    return " ".join(final_words)

def plot_cloud(text):

    # mask, max_words = np.array(Image.open(path.join(d, "uno_mask.png"))), 200
    mask, max_words = np.array(Image.open(path.join(d, "mav_mask.png"))), 300
    stopwords = STOPWORDS.union(common_words)
    wordcloud = WordCloud(background_color="white", width=2400, height=2400, mask=mask, stopwords=stopwords, max_words=max_words).generate(text)#.recolor(color_func=grey_color_func, random_state=3)

    # Open a plot of the generated image.
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    # import IPython; IPython.embed()

    fig = plt.gcf()
    fig.set_size_inches(18.5, 10.5)
    canvas = FigureCanvas(fig)
    png_output = StringIO.StringIO()
    canvas.print_png(png_output)

    return png_output.getvalue()


def grey_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(0, 0%%, %d%%)" % random.randint(60, 100)

def load_data(data_dir):
    with open(path.join(data_dir, "rmp_reviews.json"), "rb") as f:
        rmp_reviews = json.load(f)

    with open(path.join(data_dir, "unou_reviews.json"), "rb") as f:
        unou_reviews = json.load(f)

    return rmp_reviews, unou_reviews

def get_all_words(data_dir, teacher_name):
    rmp_reviews, unou_reviews = load_data(data_dir)

    rmp_words = get_teacher_reviews(rmp_reviews, ReviewTypes.RMP, teacher_name)
    unou_words = get_teacher_reviews(unou_reviews, ReviewTypes.UNOU, teacher_name)

    words = []
    if rmp_words:
        words += rmp_words
        print "{} words from RateMyProfessor".format(len(rmp_words))
    if unou_words:
        words += unou_words
        print "{} words from UNOUnderground".format(len(unou_words))

    return words

def _main():
    if len(sys.argv) < 3:
        print "Usage: ./gen_cloud.py (filename) (teacher_name)..."
        sys.exit(1)

    fname = sys.argv[1]
    teacher_name = " ".join(sys.argv[2:])

    words = get_all_words(".", teacher_name)
    png = plot_cloud(clean_text(words))

    with open(fname, "wb") as f:
        f.write(png)

if __name__ == '__main__':
    _main()
