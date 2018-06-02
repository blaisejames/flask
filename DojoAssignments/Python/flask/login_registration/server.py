import re, hashlib
from flask import Flask, render_template, request, redirect, flash, session
from flask.ext.bcrypt import Bcrypt
from mysqlconnection import MySQLConnector
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
app.secret_key = "%!_^@*F?gH(-)"
salt = "1Ha7"
mysql = MySQLConnector(app, 'userdb')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    valid = True
    if len(request.form['first_name']) < 2 or not request.form['first_name'].isalpha():
        valid = False
        flash('First Name must contain at least one letter and no numbers')
    if len(request.form['last_name']) < 2 or not request.form['last_name'].isalpha():
        valid = False
        flash('Last Name must contain at least one letter and no numbers')
    if not email_regex.match(request.form['email']):
        valid = False
        flash('Error in E-mail')
    if len(request.form['password']) < 8:
        valid = False
        flash('Password must be at least 8 characters')
    if request.form['password_confirm'] != request.form['password']:
        valid = False
        flash('Passwords do not match')
    if valid != True:
        return redirect('/')
    else:
        query = "INSERT INTO `userdb`.`users` (`first_name`, `last_name`, `email`, `password`, `created_at`, `updated_at`) VALUES (:first_name, :last_name, :email, :password, now(), now());"
        data = {
            "first_name":request.form['first_name'],
            "last_name":request.form['last_name'],
            "email":request.form['email'],
            "password":hashlib.md5(salt + request.form['password']).hexdigest()
        }
        mysql.query_db(query, data)
        flash('Successfully registered. Please log in.')
        return redirect('/')
    return "Please Register"

@app.route('/login', methods=['POST'])
def login():
    valid = True
    if not email_regex.match(request.form['email']):
        valid = False
        flash('Error in E-mail')
    if len(request.form['password']) < 8:
        valid = False
        flash('Error in Password')
    if valid != True:
        return redirect('/')
    else:
        query = "SELECT * FROM `userdb`.`users` WHERE email = :email;"
        data = {
            "email":request.form['email']
        }
        users = mysql.query_db(query, data)
        if len(users) > 0:
            user = users[0]
            if hashlib.md5(salt + request.form['password']).hexdigest() == user['password']:
                session['user_id'] = user['id']
                return redirect('/dashboard')
            else:
                flash('Wrong Password')
        else:
            flash('E-mail does not exist')
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    user = mysql.query_db("SELECT * FROM users WHERE id = {}".format(session['user_id']))[0]
    return render_template('dashboard.html', user=user)

app.run(debug=True)