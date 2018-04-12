from flask import Flask, render_template, redirect, request

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
	name = request.form['name']
	location = request.form['location']
	language = request.form['language']
	comment = request.form['comment']
	# print "Name is " + name + ", Selected Location is " + location + ", Selected Language is " + language + ", Comment is " + comment
	return render_template('result.html', name=name, location=location, language=language, comment=comment)

app.run(debug=True)