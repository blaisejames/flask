from flask import Flask, render_template, redirect, request, session, flash
app = Flask(__name__)
app.secret_key = 'KeepItSecretKeepItSafe'

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    if len(request.form['name']) < 1:
        flash("Name cannot be empty!")
        return redirect('/')
    elif len(request.form['comment']) < 1 or len(request.form['comment']) > 120:
        flash("Comment cannot be empty or longer than 120 characters!")
        return redirect('/')
    else:
        return render_template('process.html', name=request.form['name'], location=request.form['location'], language=request.form['language'], comment=request.form['comment'])

app.run(debug=True)