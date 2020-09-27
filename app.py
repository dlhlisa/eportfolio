from flask import Flask, render_template, request, jsonify
from mlmodels import *
from wtforms import Form, TextAreaField, StringField, validators
from flask_mysqldb import MySQL

app = Flask(__name__)

# config mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = os.environ['DB_PASS']
app.config['MYSQL_DB'] = 'mlflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# init MYSQL
mysql = MySQL(app)


@app.route('/')
def index():
    # return "<h1>Welcome to our server !!</h1>"
    return render_template('home.html')


@app.route('/resume')
def resume():
    return render_template('resume.html')  


@app.route('/skill')
def skill():
    return render_template('skill.html') 


@app.route('/blog')
def blog():
    return render_template('blog.html') 


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
    app.run(threaded=True, port=5000, debug=True)