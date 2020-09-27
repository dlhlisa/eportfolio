import os
import pickle

import numpy as np
# from flask_mysqldb import MySQL
from app import mysql

from vectorizer import vect


# Preparing the Classifier
cur_dir = os.path.dirname(__file__)
clf = pickle.load(open(os.path.join(cur_dir, 'movieclassifier', 'pkl_objects', 'classifier.pkl'), 'rb'))

# db = os.path.join(cur_dir, 'reviews.sqlite')

# class ReviewForm(Form):
#     moviereview = TextAreaField('', [validators.DataRequired(), validators.length(min=15)])

def classify(document):
    label = {0:'negative', 1:'positive'}
    X = vect.transform([document])
    y = clf.predict(X)[0]
    proba = np.max(clf.predict_proba(X))
    return label[y], proba


def train(document, y):
    X = vect.transform([document])
    clf.partial_fit(X, [y])


def sqlite_entry(document, y):
    # username = request.form['username']
    # create cursor
    cur = mysql.connection.cursor()

    # insert new reviews DB
    cur.execute("insert into reviews (review, sentiment) values(%s, %s)", (document, y))

    # commit DB
    mysql.connection.commit()

    # close connection
    cur.close()
