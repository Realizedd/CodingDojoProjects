from flask import Flask, render_template, redirect, session

app = Flask(__name__)
app.secret_key = "lul"
VALID_COLORS = ["red", "blue", "orange", "purple"]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ninjas')
def ninjas():
    result = ""

    if "result" in session:
        result = session["result"]

    session.clear()
    return render_template('ninjas.html', result=result)


@app.route('/ninjas/<arg>')
def ninja(arg):
    session['result'] = arg
    return redirect('/ninjas')

app.run(debug=True)
