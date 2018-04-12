from flask import Flask, render_template, redirect, request, session
import random as rnd

app = Flask(__name__)
app.secret_key = '2f9bbdc0-18e4-424d-b322-ba3de2af5ac5'

@app.route('/')
def index():
	if "random_number" not in session:
		random_number = rnd.randrange(0, 101)
		session["random_number"] = random_number
		print "Random number set to " + str(random_number)

	if "result" in session:
		result = session["result"]
		answer = ""

		if result == 0:
			answer = session["random_number"]
			session.pop("random_number")

		session.pop("result")
		return render_template('index.html', result=result, answer=answer)

	return render_template('index.html')

@app.route('/', methods=['POST'])
def guess():
	number = request.form['guess']

	if number is not None and number.isdigit() and "random_number" in session:
		random_number = session["random_number"]

		if int(number) == random_number:
			session["result"] = 0
		elif int(number) > random_number:
			session["result"] = 1
		else:
			session["result"] = 2

	return redirect('/')

app.run(debug=True)