from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def greet():
    return render_template('index.html')

@app.route('/ninjas')
def ninjas():
    return render_template('ninjas.html')

@app.route('/dojos/<usertype>')
def dojos(usertype):
    return render_template('dojos.html', kind = usertype)

app.run(debug=True)