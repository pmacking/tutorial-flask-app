"""
This module contains routing for the flask app
"""

import secrets, os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required

from yahtzee import app, connexion_app, db, bcrypt, mail
from yahtzee.models import User
from yahtzee.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                           RequestResetForm, ResetPasswordForm)
from flask_mail import Message

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
    """
    # check if user is already authenticated before presenting registration
    if current_user.is_authenticated:
        return redirect(url_for('home'))

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
    """
    # check if user is already authenticated before presenting registration
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()

    # add validate on submit to alert user if form submission successful
    if form.validate_on_submit():

        # check if user.email exists in the db, or set user as None
        user = User.query.filter_by(email=form.email.data).first()

        # check if user and that form password matches hashed password
        if user and bcrypt.check_password_hash(user.password,
                                               form.password.data):

            # login the user with login_user method from flask_login
            login_user(user, remember=form.remember.data)

            next_page = request.args.get('next')

            return redirect(next_page) if next_page \
                else redirect(url_for('home'))
        else:
            flash(
                'Login unsuccessful. Please use correct email and password',
                'danger'
                )

    return render_template("login.html", title='Login', form=form)


@connexion_app.route("/logout")
def logout():
    """
    This function responds to the browser URL localhost:5000/logout
    """
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    """
    This function renames a form field picture with a unique path.
    It then saves new filename to filesystem.

    :return picture_filename: The new unique filename with basename 8 byte hex.
    """
    # create a new unique path for the form_picture to prevent collisions
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + file_ext
    picture_path = os.path.join(
                        app.root_path,
                        'static/profile_pics',
                        picture_filename
                        )

    # resize to maximum image size
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    # use the save method on the resized i picture at the unique picture_path
    i.save(picture_path)

    return picture_filename


@connexion_app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    """
    This function responds to the browser URL localhost:5000/account
    """
    # create form from class
    form = UpdateAccountForm()

    # if valid form submission, update current_user attributes and flash msg
    if form.validate_on_submit():

        # log current_user data
        logger.info(f"current_user({current_user.first_name}, "
                    f"{current_user.last_name}, {current_user.username}, "
                    f"{current_user.email}, {current_user.image_file})")

        # if update form field pic, rename/save pic, and update db image_file
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
            logger.info(f"Updated {current_user.username} "
                        f"picture: {picture_file}")

        # update current_user with form field data, and commit to db
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        db.session.commit()

        # log updated current_user data
        logger.info(f"current_user({current_user.first_name}, "
                    f"{current_user.last_name}, {current_user.username}, "
                    f"{current_user.email}, {current_user.image_file})")

        flash('Account update successful', 'success')

        # redirect user to account route avoid post/redirect/get pattern issue
        return redirect(url_for('account'))

    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
        form.username.data = current_user.username

    image_file = url_for(
                    'static',
                    filename='profile_pics/' + current_user.image_file
                    )

    return render_template("account.html", title='Account',
                           image_file=image_file, form=form)


def send_reset_email(user):
    """
    Gets a token from passed-in user and mail.send a reset password email.

    :param user: unauthenticated user
    """
    # get token for passed-in user from User model's get_reset_token() method
    token = user.get_reset_token()

    # create a Message instance
    msg = Message(
            'Password Reset Request',
            sender='noreply@demo.com',
            recipients=[user.email]
            )

    # add msg body with url_for link containing route, token and _external
    # boolean True to make link absolute url (relative works when inside app)
    msg.body = f"""To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not maket this request then ignore this email.
"""

    # send the email msg
    mail.send(msg)


@connexion_app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():  # this func is named _request vs _password in url
    """
    This route issues a password reset token for unauthorized user email
    """
    # ensure user is not authenticated in order to reset password (vs update)
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RequestResetForm()

    # if rendered form is submitted, get user from email, send reset email
    # with token, and redirect user to the login page
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Email has been sent to reset your password', 'info')
        return redirect(url_for('login'))

    return render_template("reset_request.html", title='Reset Password',
                           form=form)


@connexion_app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):  # this func is named _token, accepts token param
    """
    This route allows user to reset password with a valid token
    """
    # ensure user is not authenticated in order to reset password (vs update)
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    # get the user_id using the verify_reset_token method and token param
    user = User.verify_reset_token(token)

    # check if user was not returned due to invalid token
    if user is None:
        flash("That is an invalid or expired token", "warning")
        return redirect(url_for('reset_request'))

    # if user was valid present the reset password (reset_token) form
    form = ResetPasswordForm()

    # handle password/confirm password reset form submission
    if form.validate_on_submit():

        # hash password from reset password form submission
        hashed_password = bcrypt.generate_password_hash(
                            form.password.data).decode('utf-8')

        # try to update user password in db
        try:
            user.password = hashed_password
            db.session.commit()
            flash(f'Your password has been updated.', 'success')
            logger.info(f'User created: "{user}"')
        except Exception as e:
            logger.exception(f'{e}')

        # redirect user to login page
        return redirect(url_for('login'))  # url_for arg is route func not arg

    return render_template("reset_token.html", title='Reset Password',
                           form=form)
