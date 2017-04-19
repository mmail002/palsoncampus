# shebang line:  #!/usr/bin/env python3

# Author: Naz-Al Islam
# Contributors: [Jayant Arora]
# Description: Main module for palsoncampus application 
# Date: Apr 10, 2017

from flask import Flask, g, flash, render_template, url_for, redirect
from flask_login import (LoginManager, login_user, logout_user,
                         current_user, login_required)


import models
## UPDATE: needs rename to just profile.
from data_models import profile as data_model

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
def load_user(email):
    try:
        return data_model.Profile.get_user(email)
    except:
        return None


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        data_model.Profile.create_user(
                    email=form.email.data,
                    password=form.password.data,
                    firstName=form.firstName.data,
                    lastName=form.lastName.data,
                    campus=form.campus.data,
                    birthDate=form.birthDate.data,
                )
        return render_template('thankyou_register.html', username=form.firstName.data)
    return render_template('register.html', form=form)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    form = forms.ProfileForm()
    if form.validate_on_submit():
        data_model.Profile.create_user(
                    nickName=form.nickName.data,
                    profileStatus=form.status.data,
                    public=form.public.data,
                    campus=form.campus.data,
                    pastCampus=form.pastCampus.data,
                    hometown=form.hometown.data,
                    about=form.about.data,
                    profilePicture=form.profilePicture.data,
                    uploadedPictures=form.uploadedPictures.data,
                    interests=form.interests.data,
                    linkedPages=form.linkedPages.data,
                    campusInvolvement=form.campusInvolvement.data,
                    gender=form.gender.data,
                    phone=form.phone.data
                )
        return render_template('thankyou_register.html', username=form.username.data)
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            loginUser = data_model.Profile.login_user(email=form.email.data, password=form.password.data)

            ### Properties for login_user imported from flask ###
            if loginUser.profileStatus == True:
                loginUser.is_active = True
            loginUser.is_authenticated = True
            loginUser.is_anonymous = False
            ### end properties for login_user ###

            login_user(loginUser)
            return "You've been logged in!"
        except data_model.PasswordIncorrectError:
            return "Your email or password does not match!"
        except data_model.UserNotFoundError:
            return "user does not exist"
    else:
        return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Logged out'


#@app.route('/new_post', methods=['GET', 'POST'])
#@login_required
#def post():
#    form = forms.PostForm()
#    if form.validate_on_submit():        
#        models.Post.create_post(user=g.user._get_current_object(),
#                    content=form.content.data.strip()
#                )
#        return redirect(url_for('index'))
#    return render_template('post.html', form=form)


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
    form = forms.RegisterForm()
    return render_template('index.html', form=form)


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
