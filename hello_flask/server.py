from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
	return render_template('index.html')

@app.route('/suc')
def success():
	return render_template('suc.html', title='Serverside Title', phrase='#1')

app.run(debug=True)