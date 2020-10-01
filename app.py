from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, session, logging
from mlmodels import *
from wtforms import Form, TextAreaField, StringField, PasswordField, validators
# from flask_mysqldb import MySQL

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import psycopg2, psycopg2.extras

from passlib.hash import sha256_crypt

from functools import wraps

import json


app = Flask(__name__)

# # config mysql
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = os.environ['DB_PASS']
# app.config['MYSQL_DB'] = 'mlflaskapp'
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# # init MYSQL
# mysql = MySQL(app)

# app.config['POSTGRES_USER'] = 'postgres'
# app.config['POSTGRES_PW'] = os.environ['PG_PASS']
# app.config['POSTGRES_URL'] = '127.0.0.1:5432'
# app.config['POSTGRES_DB'] = 'mlflaskapp'

# config postgresql
class Config:
    POSTGRES_USER = 'postgres'
    POSTGRES_PW = os.environ['PG_PASS']
    POSTGRES_HOST = '127.0.0.1:5432'
    POSTGRES_DB = 'mlflaskapp'

    @staticmethod
    def init_app(app):
        pass

# DB_URL = 'postgresql://{user}:{pw}@{url}/{db}'.format(user=Config.POSTGRES_USER,pw=Config.POSTGRES_PW,url=Config.POSTGRES_URL,db=Config.POSTGRES_DB)
DB_URL = 'postgresql+psycopg2://{user}:{pw}@{host}/{db}'.format(user=Config.POSTGRES_USER,pw=Config.POSTGRES_PW,host=Config.POSTGRES_HOST,db=Config.POSTGRES_DB)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning

db = SQLAlchemy(app)
# db.init_app(app)
# engine = create_engine(DB_URL)

# # connect to an existing database: conn = psycopg2.connect("dbname='mlflaskapp' user='postgres' password='password' host='localhost' port='5432'")
conn_string = "dbname='mlflaskapp' user='postgres' host='localhost' port='5432'" + ' password=' + os.environ['PG_PASS']
# conn = psycopg2.connect(conn_string)
# # open a cursor to perform database operations
# cur = conn.cursor() # ur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
# # execute a command
# cur.execute("select * from reviews")
# print(cur.fetchone())


@app.route('/')
def index():
    # return "<h1>Welcome to our server !!</h1>"
    return render_template('home.html')


# register from class
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=45)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [validators.DataRequired(), validators.EqualTo('confirm', message='Passwords do not match')])
    confirm = PasswordField('Confirm Password')


# user register
@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # create cursor/engine
        # cur = mysql.connection.cursor()
        conn = psycopg2.connect(conn_string)
        cur = conn.cursor()

        cur.execute("insert into users(name, email, username, password) values(%s, %s, %s, %s)", (name, email, username, password))
        # cur.execute("insert into users(name, email, username, password) values(%s, %s, %s, %s)", (name, email, username, password))

        # commit to DB
        # mysql.connection.commit()
        conn.commit()

        # close connection
        # cur.close()
        cur.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('login'))
    return render_template('register.html', form=form)


# user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # get form fields
        username = request.form['username']
        password_candidate = request.form['password']

        # create cursor
        # cur = mysql.connection.cursor()
        conn = psycopg2.connect(conn_string)
        cur = conn.cursor()
        # cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

        result = cur.execute("select username, password from users where username = %s", [username])
        # result = json.dumps(cur.fetchall(), indent=2)
        
        if result != '':
            # get stored hash
            # data = cur.fetchone()
            # password = data['password']
            # data = json.dumps(cur.fetchone(), indent=2)
            data = cur.fetchone()
            password = data[1] # get the password from the postgres database
            # print(data, data['username'], data['password'])

            # compare passwords
            if sha256_crypt.verify(password_candidate, password):
                # passed
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                # app.logger.info('PASSWORD MATCHED')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            # close connection
            # cur.close()
            cur.close()
        else:
            error = 'Username not found'          
            return render_template('login.html', error=error)

    return render_template('login.html')


# check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap


# log out
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are logged out', 'success')
    return redirect(url_for('login'))


# dashboard
@app.route('/dashboard')
def dashboard():
    # create cursor
    # cur = mysql.connection.cursor()

    # get articles
    # result = cur.execute("select * from blogs")

    conn = psycopg2.connect(conn_string)
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    result = cur.execute("select * from blogs")
    blogs = cur.fetchall()

    if result != '':
        return render_template('dashboard.html', blogs=blogs)
    else:
        msg = 'No Blogs Found'
        return render_template('dashboard.html', msg=msg)


# blogs from class
class BlogsForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=200)])
    body = StringField('Body', [validators.Length(min=10)])


# blogs
@app.route('/blogs')
def blogs():
    # create cursor
    # cur = mysql.connection.cursor()
    conn = psycopg2.connect(conn_string)
    # cur = conn.cursor()
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

    # get blogs
    result = cur.execute("select * from blogs")

    blogs = cur.fetchall()

    if result != '':
        return render_template('blog.html', blogs=blogs)
    else:
        msg = 'No Blogs Found'
        return render_template('blog.html', msg=msg)
    # close connection
    cur.close()
    # return render_template('blog.html', blogs = blogs)


# single blog
@app.route('/blogs/<string:id>')
def blog(id):
    # create cursor
    # cur = mysql.connection.cursor()
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

    # get blog
    result = cur.execute("select * from blogs where id = %s", [id])
    blog = cur.fetchone()

    return render_template('singleblog.html', blog=blog)


# add blog
@app.route('/add_blog', methods=['GET', 'POST']) 
@is_logged_in
def add_blog():
    form = BlogsForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data

        # create cursor
        # cur = mysql.connection.cursor()
        conn = psycopg2.connect(conn_string)
        cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

        # execute
        cur.execute("insert into blogs(title, body, author) values(%s, %s, %s)", (title, body, session['username']))

        # commit to DB
        # mysql.commit()
        conn.commit()

        # close connection
        cur.close()

        flash('Blog Created', 'success')

        return redirect(url_for('dashboard'))
    return render_template('add_blog.html', form=form)


# edit blog
@app.route('/edit_blog/<string:id>', methods=['GET', 'POST']) 
@is_logged_in
def edit_blog(id):
    # create cursor
    # cur = mysql.connection.cursor()
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

    # get blog by id
    result = cur.execute("select * from blogs where id = %s", [id])

    blog = cur.fetchone()
    cur.close()
   
    # get form
    form = BlogsForm(request.form)

    # populate blog form fields
    form.title.data = blog['title']
    form.body.data = blog['body']
    # body=request.args.get('body_value')

    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']        
        # title = form.title.data
        # body = form.body.data

        # create cursor
        # cur = mysql.connection.cursor()
        conn = psycopg2.connect(conn_string)
        cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

        # execute
        cur.execute("update blogs set title=%s, body=%s where id=%s;", (title, body, id))

        # commit to DB
        # mysql.commit()
        conn.commit()

        # close connection
        cur.close()

        flash('Blog Updated', 'success')
        return redirect(url_for('dashboard'))
    return render_template('edit_blog.html', form=form)


@app.route('/delete_blog/<string:id>', methods=['POST'])
@is_logged_in
def delete_blog(id):
    # create cursor
    # cur = mysql.connection.cursor()
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

    # execute
    cur.execute("delete from blogs where id = %s", [id])

    # commit to DB
    # mysql.connection.commit()
    conn.commit()

    # close connection
    cur.close()

    flash('Blog Deleted!', 'success')

    return redirect(url_for('dashboard'))


@app.route('/resume')
@is_logged_in
def resume():
    return render_template('resume.html')  


@app.route('/skill')
def skill():
    return render_template('skill.html') 


# @app.route('/blog')
# def blog():
#     return render_template('blog.html') 


@app.route('/about')
def about():
    return render_template('about.html') 


@app.route('/blogs/headline')
def headline():
    return render_template('/blogs/headline.html') 
    
    
@app.route('/blogs/caption')
def caption():
    return render_template('/blogs/caption.html') 


@app.route('/interests/cadd')
def cadd():
    return render_template('/interests/cadd.html') 
    

class ReviewForm(Form):
    moviereview = TextAreaField('', [validators.DataRequired(), validators.length(min=15)])
   
@app.route('/interests/mlmodels')
def mlmodels():
    return render_template('/interests/mlmodels.html') 

# ml_app
@app.route('/interests/mlmodels/msclf')
def msclf():
    form = ReviewForm(request.form)
    return render_template('/interests/mlmodels/moviesentimentclassifier.html', form=form)


@app.route('/interests/mlmodels/msclf_results', methods=['POST'])
def msclf_results():
    form = ReviewForm(request.form)
    if request.method == 'POST' and form.validate():
        review = request.form['moviereview']
        y, proba = classify(review)
        return render_template('/interests/mlmodels/results.html', content=review, prediction=y, probability=round(proba*100, 2))
    return render_template('/interests/mlmodels/moviesentimentclassifier.html', form=form)



@app.route('/interests/mlmodels/msclf_thanks', methods=['POST'])
def msclf_thanks():
    # username = request.form['username']
    feedback = request.form['feedback_button']
    review = request.form['review']
    prediction = request.form['prediction']
    inv_label = {'negative':0, 'positive':1}
    y = inv_label[prediction]
    if feedback == ' Incorrect':
        y = int(not(y))
    train(review, y)
    sqlite_entry(review, y)
    return render_template('/interests/mlmodels/thanks.html')


@app.route('/interests/dataanalysis')
def dataanalysis():
    return render_template('/interests/dataanalysis.html') 


@app.route('/interests/others')
def others():
    return render_template('/interests/others.html')


@app.route('/getmsg', methods=['GET'])
def respond():
    # retrieve the name from url parameter
    name = request.args.get('name', None)

    # for debugging
    print(f'got name {name}')

    response = {}

    # check if the user sent a name at all
    if not name:
        response['ERROR'] = 'no name found, please send a name.'
    # check if the user entered a number not a name
    elif str(name).isdigit():
        response['ERROR'] = "name can't be numeric."
    # now the user entered a valid name
    else:
        response['MESSAGE'] = f"Welcome {name} to our awesome platform!!"

    # return the response in json format
    return jsonify(response)


@app.route('/post/', methods=['POST'])
def post_something():
    param = request.form.get('name')
    print(param)
    # you can add the tests cases you made in the previous function, but in our case here you are just testing the POST functionality
    if param:
        return jsonify({
            "Message": f"Welcome {name} to our awesome platform!!",
            # add this option to distinct the POST request
            "METHOD": "POST"
        })
    else:
        return jsonify({
            "ERROR": "no name found, please send a name."
        })



if __name__=='__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.secret_key='secretkey for mlflaskapp'
    app.run(threaded=True, port=5000, debug=True)