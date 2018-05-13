from flask import Flask, flash, redirect, render_template, request, url_for
import re, datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
app.secret_key = '??T<??F7????U!~'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    fields = {'email': request.form['email'], 'first_name': request.form['first_name'], 'last_name': request.form['last_name'], 'password': request.form['password'], 'confirm_password': request.form['confirm_password'], 'birthday': request.form['birthday']}
    
    while True:
        error = 0
        for k,v in fields.iteritems(): 
            if len(v) < 1:
                flash(u"{} cannot be empty".format(k), 'error')
                error +=1
        if fields['first_name'].isalpha() != True or fields['last_name'].isalpha() != True:
            flash(u'Cannot have numbers in your first or last name', 'error')
            error +=1
        elif len(fields['password']) < 8:
            flash(u'Password must be longer than 8 digits', 'error')
            error +=1
        elif not re.search(r"[\d]+", fields['password']):
            flash(u'Password must have at least 1 number', 'error')
            error +=1
        elif not re.search(r"[A-Z]+", fields['password']):
            flash(u'Password must have at least 1 upper case letter', 'error')
            error +=1
        elif not EMAIL_REGEX.match(fields['email']):
            flash(u'Invalid e-mail address', 'error')
            error +=1
        elif fields['password'] != fields['confirm_password']:
            flash(u'Passwords do not match', 'error')
            error +=1
        elif not datetime.datetime.strptime(fields['birthday'], '%Y-%m-%d') or datetime.datetime.strptime(fields['birthday'], '%Y-%m-%d') > datetime.datetime.now():
            flash(u'Not a valid birthday', 'error')
            error +=1
        if error == 0:
            break
        else:
            return redirect('/')
    
    return redirect(url_for('success'))
        
@app.route('/success')
def success():
   return 'Thanks for submitting your information.'

app.run(debug=True)