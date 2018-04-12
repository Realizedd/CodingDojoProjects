from flask import Flask, render_template, redirect, request, flash, session

app = Flask(__name__)
app.secret_key = "randomUUID"

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
	name = request.form['name']

	if len(name) < 1:
		flash("Name cannot be empty!")
		return redirect('/')

	location = request.form['location']
	language = request.form['language']
	comment = request.form['comment']

	if len(comment) < 1:
		flash('Comments cannot be empty!')
		return redirect('/')
	elif len(comment) > 120:
		flash('Comments cannot be longer than 120!')
		return redirect('/')

	session['name'] = name
	session['location'] = location
	session['language'] = language
	session['comment'] = comment
	return redirect('/result')

@app.route('/result')
def show_result():
	name = ""
	location = ""
	language = ""
	comment = ""

	if "name" and "location" and "language" and "comment" in session:
		name = session['name']
		location = session['location']
		language = session['language']
		comment = session['comment']

	return render_template('result.html', name=name, location=location, language=language, comment=comment)

app.run(debug=True)