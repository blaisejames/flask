from flask import Flask, render_template, redirect, request, session
import random
app = Flask(__name__)
app.secret_key = "my very very very secret key"

@app.route('/')
def index():
    if 'number' in session:
        session.pop('number')
    return render_template('index.html')

@app.route('/guess', methods=['POST'])
def guess():
    if 'number' not in session:
        session['number'] = random.randrange(0, 101)
    guess = request.form['guess']
    color = "red"
    if guess == session['number']:
        color = "green"
        response = "You're right!"
    elif guess > session['number']:
        response = "Too high!"
    elif guess < session['number']:
        response = "Too low!"
    elif session['number'] >= 100 or session['number'] <= 0:
        response = "Error!"
    return render_template('guess.html', number = session['number'], guess = guess, color = color, response = response)
@app.route('/again')
def again():
    session.clear()
    return redirect('/')

app.run(debug=True)
