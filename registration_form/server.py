from flask import Flask, render_template, request, redirect, flash
import re

app = Flask(__name__)
app.secret_key = "RandomUUID"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
    failed = False
    email = request.form['email']

    if len(email) < 1:
        flash(u'Email cannot be empty!', 'email')
        failed = True
    elif not EMAIL_REGEX.match(email):
        flash(u"Invalid email!", 'email')
        failed = True

    first_name = request.form['first_name']

    if len(first_name) < 1:
        flash(u'First name cannot be empty!', 'first_name')
        failed = True
    elif not first_name.isalpha():
        flash(u'Names cannot contain a number!', 'first_name')
        failed = True

    last_name = request.form['last_name']

    if len(last_name) < 1:
        flash(u'Last name cannot be empty!', 'last_name')
        failed = True
    elif not last_name.isalpha():
        flash(u'Names cannot contain a number!', 'last_name')
        failed = True

    password = request.form['password']

    if len(password) <= 8:
        flash(u'Password must be longer than 8 characters!', 'password')
        failed = True

    password_confirm = request.form['password_confirmation']

    if len(password_confirm) <= 8:
        flash(u'Password must be longer than 8 characters!', 'password_confirm')
        failed = True
    elif not password == password_confirm:
        flash(u'Password and Password Confirmation must match!', 'password_confirm')
        failed = True

    if not failed:
        flash(u'Thanks for submitting your information.', 'success')

    return redirect("/")

app.run(debug=True)
