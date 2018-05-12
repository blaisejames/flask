from flask import Flask, render_template, redirect, request, session
import random, datetime
app = Flask(__name__)
app.secret_key = "my very secret key"

@app.route('/')
def index():
    if 'gold' not in session:
        session['gold'] = 0
    if 'activity' not in session:
        session['activity'] = []
    return render_template('index.html')

@app.route('/process_money', methods=['POST'])
def process():
    # establish variables
    winnings = {'casino': random.randrange(-50, 51), 'farm': random.randrange(10, 21), 'cave': random.randrange(5, 11), 'house': random.randrange(2, 6)}
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    building = request.form['building']
    action = []

    # build content to pass to template
    if building and building != 'casino':
        action = ["<p class='green'>Earned {} golds from the {}! ({})</p>".format(winnings[building], building, now)]
    elif (building == 'casino') and (winnings[building] >= 0):
       action = ["<p class='green'>Entered a casino and won {} golds! ({})</p>".format(winnings[building], now)]
    elif (building == 'casino') and (winnings[building] < 0):
        action = ["<p class='red'>Entered a casino and lost {} golds! ({})</p>".format(abs(winnings[building]), now)]
    
    # keep score and activities list
    session['gold'] = session['gold'] + winnings[building]
    session['activity'] = session['activity'] + action

    return render_template('index.html', building = building, winnings = winnings[building], now = now)

@app.route('/reset')
def reset():
    session.clear()
    return redirect('/')

app.run(debug=True)