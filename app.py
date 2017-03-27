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
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    """After each request"""
    g.db.close()
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
        return render_template(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Your email or password does not match", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user()
                flash("You've been logged in!", "success")
                return redirect(url_for('index'))
            else:
                flash("Your email or password does not match!", "error")
    return render_template('login.html', form=form)


@app.route('/')
def index():
    return 'Hey!'


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
