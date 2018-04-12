from flask import Flask, render_template, redirect, request, session
import random as rnd
from time import strftime

app = Flask(__name__)
app.secret_key = '2f9bbdc0-18e4-424d-b322-ba3de2af5dcd'

@app.route('/')
def index():
	if 'balance' not in session:
		session['balance'] = 0
		session['activities'] = []

	return render_template('index.html', balance=session['balance'], activities=session['activities'])

@app.route('/process_money', methods=['POST'])
def guess():
	value = request.form['building']
	current_time = "(" + strftime("%Y/%m/%d %H:%M %p") + ")"
	amount = 0

	if value == 'farm':
		amount = rnd.randrange(10, 21)
		session['balance'] += amount
		session['activities'].append("Earned " + str(amount) + " golds from the farm! " + current_time)
	elif value == 'cave':
		amount = rnd.randrange(5, 11)
		session['balance'] += amount
		session['activities'].append("Earned " + str(amount) + " golds from the cave! " + current_time)
	elif value == 'house':
		amount = rnd.randrange(2, 6)
		session['balance'] += amount
		session['activities'].append("Earned " + str(amount) + " golds from the house! " + current_time)
	elif value == 'casino':
		amount = rnd.randrange(0, 51)
		luck = round(rnd.random())
		
		if luck == 0: 
			session['balance'] += amount
			session['activities'].append("Earned " + str(amount) + " golds from the casino! " + current_time)
		else:
			session['balance'] -= amount
			session['activities'].append("Entered a casino and lost " + str(amount) + " golds... Ouch. " + current_time)

	return redirect('/')

app.run(debug=True)