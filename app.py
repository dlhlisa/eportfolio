from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

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



@app.route('/headline')
def headline():
    return render_template('headline.html') 
    
    
@app.route('/caption')
def caption():
    return render_template('caption.html') 


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