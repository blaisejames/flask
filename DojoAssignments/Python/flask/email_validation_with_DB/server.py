from flask import Flask, request, redirect, render_template, flash
from mysqlconnection import MySQLConnector
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
app.secret_key = "ThisIsSoSoSecret!"
mysql = MySQLConnector(app, 'email')

@app.route('/', methods=['GET'])
def index():                 
    return render_template('index.html')

@app.route('/validate', methods=['POST'])
def validate():
    email_address = request.form['e_mail']
    errors = []
    if len(email_address) < 1 or not EMAIL_REGEX.match(email_address):
        errors.append('Email is not valid!')
    if len(errors) == 0:
        query = "INSERT INTO `email`.`email` (`address`, `created_at`, `updated_at`) VALUES (:slot_one, now(), now());"
        data = {'slot_one': email_address}
        mysql.query_db(query, data)
        flash('The email address you entered ({}) is a VALID e-mail address! Thank You!'.format(email_address))
        return redirect('/success')
    else:
        for message in errors:
            flash(message)
        return redirect('/')

@app.route('/success', methods=['GET'])
def process():                 
    query = "SELECT * FROM email"                     
    dbemails = mysql.query_db(query)       
    return render_template('success.html', dbemails = dbemails)

@app.route('/delete_emails', methods=['POST'])
def delete():
    query = "DELETE FROM email"
    data = {'id': id}
    mysql.query_db(query, data)
    return redirect('/success')

app.run(debug=True)