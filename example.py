from flask import Flask, request, flash, url_for, session
from flask import render_template
from random import randint
from flask import redirect
import json

# Это callable WSGI-приложение
app = Flask(__name__)
app.secret_key = 'secret_key2'



@app.route('/')
def hello_world():
    return render_template('users/main.html')

@app.route('/users/new')
def new_user():
    user = {
        'id': randint(1,1000000),
        'nickname': '',
        'email': ''
    }
    return render_template('users/new.html', user=user)

@app.post('/users')
def users_post():
    user = request.form.to_dict()
    errors = validate(user)
    if errors:
        return render_template('users/new.html', user=user, errors=errors), 422

    with open('user.json', 'w+') as f:
        f.write(json.dumps(user))
    flash("User was added successfully", "success")
    return redirect('/users', 302)

def validate(user):
    errors = {}
    if len(user['name']) < 5:
        errors['Nickname'] = 'Nickname must be grater than 4 characters'
    if not user['email']:
        errors['email'] = 'email cant be empty'
    return errors


@app.route('/users')
def user():
    with open('user.json') as file:
        user = json.loads(file.read())
    return render_template(
        'users/users.html',
        user=user
    )

@app.route('/users/delete')
def delete_school():
    with open('user.json', 'w') as f:
        f.write(' ')
    flash('User has been deleted', 'success')
    return redirect(url_for('user'))
