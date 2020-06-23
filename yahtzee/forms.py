from flask_wtf import FlaskForm
# StringField enables string attributes in form classes
# Password enables password attributes in form classes
# Submit enables a submit button in form classes
from wtforms import StringField, PasswordField, SubmitField, BooleanField
# DataRequired class ensures the form field must contain data from user
# Length class validates acceptable length of data
# Email class validates data as email format
# EqualTo class validates attribute == other attribute as 'arg'
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from yahtzee.models import User


class RegistrationForm(FlaskForm):
    # add attributes set to imported wtforms classes
    # included args '<Titlecase>' html label
    # add args as imported wtforms.validators classes with sub args as req
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=25)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    first_name = StringField('First Name',
                             validators=[DataRequired(),
                                         Length(min=1, max=25)])
    last_name = StringField('Last Name',
                            validators=[DataRequired(),
                                        Length(min=1, max=25)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        """Validates username before add/commit user in /register route

        :param username: username of registration from.
        """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(f'Please select a unique username.')

    def validate_email(self, email):
        """Validates username before add/commit user in /register route

        :param username: username of registration from.
        """
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(f'Please select a unique email.')


class LoginForm(FlaskForm):
    # add attributes set to imported wtforms classes
    # included args '<Titlecase>' html label
    # add args as imported wtforms.validators classes with sub args as req
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
