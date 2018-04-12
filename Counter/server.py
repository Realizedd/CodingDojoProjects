from flask import Flask, render_template, redirect, request, session

app = Flask(__name__)
app.secret_key = '38400000-8cf0-11bd-b23e-10b96e4ef00d'

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/ninjas')
def ninjas():
	if session.get('counts') is None:
		session['counts'] = 0

	session['counts'] = session['counts'] + 1
	return render_template('ninjas.html')

@app.route('/hackers')
def hackers():
	if session.get('counts') is None:
		session['counts'] = 0

	session['counts'] = session['counts'] + 1
	return render_template('hackers.html')

@app.route('/ninjas', methods=['POST'])
def add_to_counter():
	session['counts'] = session['counts'] + 1
	return redirect('/ninjas')

@app.route('/hackers', methods=['POST'])
def reset_counter():
	session['counts'] = -1
	return redirect('/hackers')

app.run(debug=True)