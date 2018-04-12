from flask import Flask, render_template, session, request, redirect, flash
from mysqlconnection import MySQLConnector
from flask_bcrypt import Bcrypt
import re, time

app = Flask(__name__)
app.secret_key = "e87f4af9-faf0-431e-9628-9cc292b7ba6f"
bcrypt = Bcrypt(app)
mysql = MySQLConnector(app, 'world')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

@app.route('/')
def index():
	# ID found in session, redirecting to the dashboard
	if "id" in session:
		return redirect('/wall')

	# Else render login & registration template
	return render_template('index.html')

@app.route('/wall')
def wall():
	# When someone tries to access the page without logging in, redirect
	if "id" not in session:
		flash('You must be logged in to access this page.', 'global_warning')
		return redirect('/')

	user =  mysql.query_db('SELECT * FROM users WHERE id=' + str(session['id']))
	comments = []
	messages = []
	contents = mysql.query_db('SELECT messages.id, messages.message, comments.comment, comments.created_at AS comment_creation, messages.created_at AS message_creation, CONCAT(users.first_name, " ", users.last_name) AS comment_owner,CONCAT(users2.first_name, " ", users2.last_name) AS message_owner FROM messages LEFT JOIN comments ON comments.message_id = messages.id LEFT JOIN users ON comments.user_id = users.id LEFT JOIN users AS users2 ON messages.user_id = users2.id ORDER BY messages.created_at DESC')
	
	for content in contents:
		messages_day = content['message_creation'].day
		exists = False

		for message in messages:
			if (message['id'] == content['id']):
				exists = True

		if not exists:
			messages.append({"id": content['id'], "owner": content['message_owner'], "creation": content['message_creation'].strftime('%B ' + formatDate(messages_day) + ' %Y'), "message": content['message']})

		if content['comment'] is not None:
			comments_day = content['comment_creation'].day
			comments.append({"id": content['id'], "owner": content['comment_owner'], "comment": content['comment'], "creation": content['comment_creation'].strftime('%b ' + formatDate(comments_day) + ' %Y')})

	return render_template('/wall.html', user=user, messages=messages, comments=comments)

@app.route('/login', methods=['POST'])
def login():
	if not request.form.get('email'):
		flash('Please type a valid email.', 'login_email')
		return redirect('/')

	email = request.form['email']

	if not EMAIL_REGEX.match(email):
		flash('Please type a valid email.', 'login_email')
		return redirect('/')

	if not request.form.get('password'):
		flash('Please type a valid password.', 'login_password')
		return redirect('/')

	password = request.form['password']

	query = 'SELECT * FROM users WHERE email=:email'
	values = {
		"email": email
	}

	data = mysql.query_db(query, values)

	if len(data) == 0:
		flash('No user found with the given email! Please try again.', 'global_warning')
		return redirect('/')

	if bcrypt.check_password_hash(data[0]['password'], password):
		session['id'] = data[0]['id']
	else:
		flash('Wrong password! Please try again.', 'global_warning')

	return redirect('/')

@app.route('/register', methods=['POST'])
def register():
	if not request.form.get('first_name'):
		flash('Please type a valid first name.', 'reg_first_name')
		return redirect('/')

	first_name = request.form['first_name']

	if not request.form.get('last_name'):
		flash('Please type a valid last name.', 'reg_last_name')
		return redirect('/')

	last_name = request.form['last_name']

	if not first_name.isalpha() or len(first_name) < 2:
		flash('Name must be alphabetic and longer than 1 character.', 'reg_first_name')
		return redirect('/')

	if not last_name.isalpha() or len(last_name) < 2:
		flash('Name must be alphabetic and longer than 1 character.', 'reg_last_name')
		return redirect('/')

	if not request.form.get('email'):
		flash('Please type a valid email.', 'reg_email')
		return redirect('/')

	email = request.form['email']

	if not EMAIL_REGEX.match(email):
		flash('Please type a valid email.', 'reg_email')
		return redirect('/')

	if not request.form.get('password'):
		flash('Please type a valid password.', 'reg_password')
		return redirect('/')

	password = request.form['password']

	if len(password) < 8:
		flash('Passwords must be longer than 7 characters.', 'reg_password')
		return redirect('/')

	if not request.form.get('password_confirm'):
		flash('Password confirmation section cannot be empty.', 'reg_password_confirm')
		return redirect('/')

	password_confirm = request.form['password_confirm']

	if not password == password_confirm:
		flash('Password confirmation and password must match.', 'reg_password_confirm')
		return redirect('/')

	query = 'INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (:first_name, :last_name, :email, :password, NOW(), NOW())'
	values= {
		"first_name": request.form['first_name'], 
		"last_name": request.form['last_name'], 
		"email": email, 
		"password": bcrypt.generate_password_hash(password)
	}

	mysql.query_db(query, values)
	flash('Registration was successful, you may now log in.', 'global_info')
	return redirect('/')

@app.route('/logout', methods=['POST'])
def logout():
	session.clear()
	flash('Successfully logged out.', 'global_info')
	return redirect('/')

@app.route('/post_message', methods=['POST'])
def post_message():
	if not request.form.get('message') or len(request.form['message']) < 1:
		flash('Please type a valid message.', 'global_warning')
		return redirect('/')

	query = 'INSERT INTO messages (message, created_at, updated_at, user_id) VALUES (:message, NOW(), NOW(), :id)'
	data = {
		"message": request.form['message'],
		"id": session['id']
	}

	mysql.query_db(query, data)
	flash('Message posted. (' + request.form['message'] + ')', 'global_info')
	return redirect('/wall')

@app.route('/delete_message', methods=['POST'])
def delete_message():
	if request.form.get('message_id'):
		message_id = request.form['message_id']
		query = 'SELECT * FROM messages WHERE id=:id'
		values = {
			"id": message_id
		}

		data = mysql.query_db(query, values)[0]

		if session['id'] == data['user_id']:
			creation = time.mktime(data['created_at'].timetuple())
			now = time.time()

			if now - creation - 9000 > 1800:
				flash('You may only remove messages that was made in last 30 minutes.', 'global_warning')
				return redirect('/wall')

			comments_query = 'DELETE FROM comments WHERE message_id=:id'
			values = {
				"id": message_id
			}

			mysql.query_db(comments_query, values)

			messages_query = 'DELETE FROM messages WHERE id=:id'
			values = {
				"id": message_id
			}

			mysql.query_db(messages_query, values)
			flash('Message removed!', 'global_info')
		else:
			flash("That's not your post!", 'global_warning')

	return redirect('/wall')

@app.route('/post_comment', methods=['POST'])
def post_comment():
	if not request.form.get('message') or len(request.form['message']) < 1:
		flash('Please type a valid message.', 'global_warning')
		return redirect('/')

	message_id = request.form['message_id']
	query = 'INSERT INTO comments (comment, user_id, message_id, created_at, updated_at) VALUES (:message, :user_id, :message_id, NOW(), NOW())'
	values = {
		"message": request.form['message'], 
		"user_id": session['id'], 
		"message_id": message_id
	}

	mysql.query_db(query, values)
	flash('Comment posted. (' + request.form['message'] + ')', 'global_info')
	return redirect('/wall')

def formatDate(num):
	if num == 1:
		return str(num) + "st"
	elif num == 2:
		return str(num) +  "nd"
	elif num == 3:
		return str(num) + "rd"
	else:
		return str(num) + "th"

app.run(debug=True)