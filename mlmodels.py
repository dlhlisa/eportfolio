import os
import pickle

import numpy as np
# from flask_mysqldb import MySQL
# from app import mysql
import psycopg2
from urllib.parse import urlparse

from vectorizer import vect

# conn_string = "dbname='mlflaskapp' user='postgres' host='localhost' port='5432'" + ' password=' + os.environ['PG_PASS']
url = urlparse(os.environ['DATABASE_URL'])
conn_string = "dbname=%s user=%s password=%s host=%s port=%s" % (url.path[1:], url.username, url.password, url.hostname, url.port)
# schema = "schema.sql"
# conn = psycopg2.connect(db)

DB_URL = url

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
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()
    # cur = mysql.connection.cursor()

    # insert new reviews DB
    cur.execute("insert into reviews (review, sentiment) values(%s, %s)", (document, y))

    # commit DB
    # mysql.connection.commit()
    conn.commit()

    # close connection
    cur.close()
