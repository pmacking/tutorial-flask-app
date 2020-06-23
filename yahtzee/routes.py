"""
This module contains routing for the flask app
"""

from flask import render_template, url_for, flash, redirect

from yahtzee import connexion_app, db, bcrypt
from yahtzee.models import User
from yahtzee.forms import RegistrationForm, LoginForm

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('yahtzee.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

# create URL route in application for home "/"
@connexion_app.route("/")
def home():
    """
    This function responds to the browser URL localhost:5000/

    return:         the rendered template "home.html"
    """
    users = User.query \
        .order_by(User.last_name) \
        .all()

    return render_template("home.html", users=users)


@connexion_app.route("/about")
def about():
    """
    This function responds to the browser URL localhost:5000/about

    return:         the renedered template "about.html"
    """
    return render_template("about.html", title='About')


@connexion_app.route("/register", methods=['GET', 'POST'])
def register():
    """
    This function responds to the browser URL localhost:5000/register

    return:         the rendered template "register.html"
    """
    form = RegistrationForm()

    # add validate on submit to alert user if form submission successful
    if form.validate_on_submit():

        # hash password and create user from register form submission
        hashed_password = bcrypt.generate_password_hash(
                            form.password.data).decode('utf-8')

        # create user object
        user = User(
                username=form.username.data,
                email=form.email.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                password=hashed_password
                )  # passed hashed_password not plaintext form.password.data

        # try to create user in db
        try:
            db.session.add(user)
            db.session.commit()
            flash(f'Account created for {form.username.data}.', 'success')
            logger.info(f'User created: "{user}"')
        except Exception as e:
            logger.exception(f'{e}')

        # redirect user to login page
        return redirect(url_for('login'))  # url_for arg is route func not arg

    return render_template("register.html", title='Register', form=form)


@connexion_app.route("/login", methods=['GET', 'POST'])
def login():
    """
    This function responds to the browser URL localhost:5000/register

    return:         the renedered template "register.html"
    """
    form = LoginForm()

    # add validate on submit to alert user if form submission successful
    if form.validate_on_submit():
        # TODO: fix submit validation after connecting login to DB
        if form.email.data == 'test@test.com' and form.password.data == 'password':
            flash('You have logged in', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please use correct username and password', 'danger')

    return render_template("login.html", title='Login', form=form)
