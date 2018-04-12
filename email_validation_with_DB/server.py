from flask import Flask, render_template, redirect, flash, request
from mysqlconnection import MySQLConnector
import re

app = Flask(__name__)
app.secret_key = "a5c0a0df-e2c9-4c1a-967e-21bd44698392"
mysql = MySQLConnector(app, 'mydb')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/proceed', methods=['POST'])
def proceed():
	email = request.form['email']

	if not EMAIL_REGEX.match(email):
		flash('Invalid email!')
		return redirect('/')

	flash('The email you entered (' + email + ') is a VALID email address! Thank you!')
	mysql.query_db('INSERT INTO emails (email, created_at, updated_at) VALUES ("' + email + '", NOW(), NOW())')
	return redirect('/success')

@app.route('/delete', methods=['POST'])
def delete():
	email_id = request.form['id']
	email = request.form['email']
	flash('Email Address deleted (' + email + ')!')
	mysql.query_db('DELETE FROM emails WHERE id=' + email_id)
	return redirect('/success')
@app.route('/success')
def success():
	data = mysql.query_db('SELECT * FROM emails')

	if len(data) == 0:
		data = ['No data found! :(']

	return render_template('success.html', data=data)

app.run(debug=True)