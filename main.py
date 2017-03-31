from flask import Flask, g, flash, render_template, url_for, redirect
from flask_login import LoginManager

import models

import forms

app = Flask(__name__)
app.secret_key = 'ADASDQWqqqr2524tWT#T!!#!#!REFsdvsd&^&%^R'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


DEBUG = True
PORT = 8000
HOST = '0.0.0.0'


@app.before_request
def before_request():
    """Before each request"""


@app.after_request
def after_request(response):
    """After each request"""
    return response


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        models.User.create_user(
                    username=form.username.data,
                    email=form.email.data,
                    password=form.password.data
                )
        return render_template('thankyou_register.html', username=form.username.data)
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.exists(username = form.username.data)
        except models.DoesNotExist:
            flash("Your email or password does not match", "error")
        else:
            if user.password == form.password.data:
                login_user()
                flash("You've been logged in!", "success")
                return redirect(url_for('index'))
            else:
                flash("Your email or password does not match!", "error")
    return render_template('login.html', form=form)


@app.route('/create', methods=['GET'])
def create():
    try:

        models.User.create_user(
                username='nazalislam',
                email='naz@subtlecoding.com',
                password='password',
                is_admin=True
            )
    except ValueError:
        raise ValueError("User already exists.")
    return 'to do create'

@app.route('/update', methods=['GET'])
def update():
    try:

        models.User.update_user(
                username='nazalislam',
                email='naz@subtlecoding.com',
                password='newpassword',
                admin=True
            )
    except ValueError:
        raise ValueError("Invalid User.")
    return 'to do update'


@app.route('/delete', methods=['GET'])
def delete():
    try:

        models.User.delete_user(
                username='nazalislam',
            )
    except ValueError:
        raise ValueError("Invalid User.")
    return 'to do delete'


@app.route('/')
def index():
    return 'Hey!'


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    return 'An internal error occurred. Better luck next time', 500

if __name__ == '__main__':
    models.initialize()
    try:
        models.User.create_user(
                username='nazalislam',
                email='naz@subtlecoding.com',
                password='password',
                admin=True
            )
    except ValueError:
        pass
    app.run(debug=DEBUG, port=PORT, host=HOST)
