from flask import Flask, session, request, redirect, render_template, flash
from mysqlconnection import MySQLConnector
from flask_bcrypt import Bcrypt
import re

app = Flask(__name__)
app.secret_key = "38fc636a-cbc1-46cc-8ecf-9979412d8208"
bcrypt = Bcrypt(app)
mysql = MySQLConnector(app, 'test')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

@app.route('/')
def index():
	# Load registration & login page. If user is already logged in, redirect to dashboard.
	if "id" in session:
		return redirect('/dashboard')

	return render_template('index.html')

@app.route('/dashboard')
def dashboard():
	# If user is logged in, show dashboard. If not, flash message & redirect to index.

	if "id" in session:
		user = mysql.query_db('SELECT * FROM users WHERE id=' + str(session['id']))
		return render_template('dashboard.html', data=user)

	return redirect('/')

@app.route('/process', methods=['POST'])
def process():
	# If user info doesn't exist, redirect to index with a flash message. Else, redirect to dashboard.
	action = request.form['action']
	flashed = False

	if action:
		if action == "login":
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
			result = mysql.query_db('SELECT * FROM users WHERE email="' + email + '"')

			if len(result) == 0:
				flash('No user found with the given email! Please try again.', 'global_warning')
				return redirect('/')

			if bcrypt.check_password_hash(result[0]['password'], password):
				session['id'] = result[0]['id']
				flash('Welcome Back, ' + result[0]['first_name'] + '.', 'global_info')

			else:
				flash('Wrong password! Please try again.', 'global_warning')
		elif action == "register":
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

			query = 'INSERT INTO users (first_name, last_name, email, password, created_at) VALUES (:first_name, :last_name, :email, :password, NOW())'
			data = {"first_name": request.form['first_name'], "last_name": request.form['last_name'], "email": email, "password": bcrypt.generate_password_hash(password)}
			mysql.query_db(query, data)
			flash('Registration was successful, you may now log in.', 'global_info')

		elif action == "logout":
			session.clear()
			flash('Successfully logged out.', 'global_info')

	return redirect('/')

app.run(debug=True)