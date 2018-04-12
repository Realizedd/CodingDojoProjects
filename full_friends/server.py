from flask import Flask, render_template, redirect, request, flash
from mysqlconnection import MySQLConnector

app = Flask(__name__)
app.secret_key = "AnotherRandomUUID"
mysql = MySQLConnector(app, 'mydb')

@app.route('/')
def index():
	# Display all friends from the db
	data = mysql.query_db('SELECT * FROM friends')

	if len(data) == 0:
		data = ['You have no friends :(']

	return render_template('index.html', data=data)

@app.route('/friends', methods=['POST'])
def create():
	# Create a friend
	first_name = request.form['first_name']
	last_name = request.form['last_name']
	email = request.form['email']
	mysql.query_db('INSERT INTO friends (first_name, last_name, email, created_at) VALUES ("' + first_name + '", "' + last_name + '", "' + email + '", NOW())')
	flash('Created a new friend named ' + first_name + " " + last_name + "!")
	return redirect('/')

@app.route('/friends/<id>/edit')
def edit(id):
	# Edit friend's info
	result = mysql.query_db('SELECT * FROM friends WHERE id=' + id)

	if len(result) == 0:
		flash('No friend with given id was found.')
		return redirect('/')

	return render_template('edit.html', data=result)

@app.route('/friends/<id>', methods=['POST'])
def update(id):
	# Update friend info, connected from edit

	first_name = request.form['first_name']
	last_name = request.form['last_name']
	email = request.form['email']

	mysql.query_db('UPDATE friends SET first_name="' + first_name + '", last_name="' + last_name + '", email="' + email + '" WHERE id=' + id)
	flash('Successfully updated!')
	return redirect('/')

@app.route('/friends/<id>/delete', methods=['POST'])
def delete(id):
	# Delete a friend :^(
	full_name = request.form['full_name']
	mysql.query_db('DELETE FROM friends WHERE id=' + id)
	flash('Deleted a friend named ' + full_name + "!")
	return redirect('/')

app.run(debug=True)