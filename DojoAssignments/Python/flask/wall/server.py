import re, hashlib
from flask import Flask, render_template, request, redirect, flash, session
from flask.ext.bcrypt import Bcrypt
from mysqlconnection import MySQLConnector
app = Flask(__name__)
app.secret_key = "%!_^@*F?gH(*!-)"
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
bcrypt = Bcrypt(app)
mysql = MySQLConnector(app, 'wall_db')

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
        query = "INSERT INTO `wall_db`.`users` (`first_name`, `last_name`, `email`, `password`, `created_at`, `updated_at`) VALUES (:first_name, :last_name, :email, :password, now(), now());"
        data = {
            "first_name":request.form['first_name'],
            "last_name":request.form['last_name'],
            "email":request.form['email'],
            "password":bcrypt.generate_password_hash(request.form['password'])
        }
        mysql.query_db(query, data)
        flash('Successfully registered. Please log in.')
        return redirect('/')

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
        query = "SELECT * FROM `wall_db`.`users` WHERE email = :email;"
        data = {
            "email":request.form['email']
        }
        users = mysql.query_db(query, data)
        if len(users) > 0:
            user = users[0]
            password = request.form['password']
            result = bcrypt.check_password_hash(user['password'], password)
            if result == True:
                session['user_id'] = user['id']
                return redirect('/wall')
            else:
                flash('Wrong Password')
        else:
            flash('E-mail does not exist')
    return redirect('/')

@app.route('/wall')
def wall():
    user = mysql.query_db("SELECT * FROM users WHERE id = {}".format(session['user_id']))[0]
    mess = mysql.query_db("SELECT *, messages.id as message_id FROM messages JOIN users on users.id = messages.user_id")
    comm = mysql.query_db("SELECT *, comments.id as comment_id FROM comments JOIN messages on messages.id = comments.message_id")
    return render_template('wall.html', user=user, mess=mess, comm=comm)

@app.route('/post', methods=['POST'])
def post():
    query = "INSERT INTO `wall_db`.`messages` (`user_id`, `message`, `created_at`, `updated_at`) VALUES (:user_id, :message, now(), now());"
    data = {
        "user_id":session['user_id'],
        "message":request.form['post'],
    }
    mysql.query_db(query, data)
    flash('Successfully posted.')
    return redirect('/wall')

@app.route('/comments/<message_id>', methods=['POST'])
def comment(message_id):
    query = "INSERT INTO `comments` (`user_id`, `message_id`, `comment`, `created_at`, `updated_at`) VALUES (:user_id, :message_id, :comment, now(), now());"
    data = {
        "user_id":session['user_id'],
        "message_id":message_id,
        "comment":request.form['comment']
    }
    mysql.query_db(query, data)
    flash('Successfully commented.')
    return redirect('/wall')

@app.route('/logout', methods=['GET'])
def clear():
    session.clear()
    return redirect('/')

app.run(debug=True)