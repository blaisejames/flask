from flask import Flask, render_template, redirect, request, session
app = Flask(__name__)
app.secret_key = "my super secret key"

@app.route('/')
def index():
    if 'count' not in session:
        session['count'] = 0
    session['count'] = session['count'] + 1
    return render_template('index.html', count = session['count'])

@app.route('/add2')
def add2():
    session['count'] = session['count'] + 1
    return redirect('/')

@app.route('/clear')
def clear():
    session.clear()
    return redirect('/')

app.run(debug=True)