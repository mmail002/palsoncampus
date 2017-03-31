from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Regexp, ValidationError, Email, Length, EqualTo

from models import User

def name_exists(form, field):
    if User.exists(field.data):
        raise ValidationError("User with that name already exists.")

class RegisterForm(Form):
    username = StringField('Username',
                validators=[
                        DataRequired(),
                        Regexp(r'^[a-zA-Z0-9_]+$',
                        message="Username should be one word, letters numbers, and underscores only."),
                        name_exists
                    ]
            )
    email = StringField('Email', 
                validators=[
                        DataRequired(),
                        Email()
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


class LoginForm(Form):
    username  = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
