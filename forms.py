# Author: Naz-Al Islam
# Contributors: []
# Description: This file renders different forms for palsoncampus application
# Date: Mon April 10 2017


from flask_wtf import Form
from wtforms import (StringField, PasswordField, BooleanField, FileField, 
        SelectField, RadioField, IntegerField, DateField)
from wtforms.validators import (DataRequired, Regexp, ValidationError, Email, Length, EqualTo)

from models import User
from data_model import Profile

def name_exists(form, field):
    if User.exists(field.data):
        raise ValidationError("User with that name already exists.")

class RegisterForm(Form):
    email = StringField('Email', 
                validators=[
                        DataRequired(),
                        Email()
                    ]
            )
    nickName = StringField('Username',
                validators=[
                        DataRequired(),
                        Regexp(r'^[a-zA-Z0-9_]+$',
                        message="Username should be one word, letters numbers, and underscores only."),
                        name_exists
                    ]
            )
    password = PasswordField('Password',
                validators=[
                        DataRequired(),
                        Length(min=2),
                        EqualTo('password2', message="Password does not match!")
                    ]
            )
    password2 = PasswordField('Confirm Password',
            validators=[
                    DataRequired()
                ]
            )
    firstName = StringField('First Name',
                validators=[
                        DataRequired(),
                    ]
            )
    lastName = StringField('Last Name',
                validators=[
                        DataRequired(),
                    ]
            )
    birthDate = DateField('Birth Date',
                validators=[
                        DataRequired(),
                    ]
            )
    status = BooleanField()
    public = BooleanField()
    campus = StringField('What campus are you in?',
                validators=[
                        DataRequired(),
                    ]
            )
    pastCampus = StringField('Any past campus?',
                validators=[
                        DataRequired(),
                    ]
            )
    hometown = StringField('Hometown?',
                validators=[
                        DataRequired(),
                    ]
            )
    about = StringField('About you...',
                
            )
    profilePicture = FileField('Upload a picture')
    uploadedPictures = FileField('Other pictures')
    interests = StringField('Any interests...')
    linkedPages = StringField('Linked pages')
    campusInvolvement = StringField('Other assoicated campus...')
    gender = RadioField('Gender')
    phone = IntegerField('Enter your phone number', 
                validators=[DataRequired()])


class LoginForm(Form):
    username  = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])