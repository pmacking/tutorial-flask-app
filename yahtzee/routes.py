"""
This module contains routing for the flask app
"""

from flask import render_template, url_for, flash, redirect
import config
from config import app

# import User class to access user db/table
from yahtzee.models import User
from yahtzee.forms import RegistrationForm, LoginForm

# get the application instance
connexion_app = config.connexion_app

# create URL route in application for home "/"
@connexion_app.route("/")
def home():
    """
    This function responds to the browser URL localhost:5000/

    return:         the renedered template "home.html"
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

    return:         the renedered template "register.html"
    """
    form = RegistrationForm()

    # add validate on submit to alert user if form submission successful
    if form.validate_on_submit():
        flash(f'Account create for {form.username.data}', 'success')
        return redirect(url_for('home'))  # N/B arg is name of func not route

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
