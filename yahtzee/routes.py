"""
This module contains routing for the flask app
"""

from flask import render_template, url_for
import config

# import User class to access user db/table
from yahtzee.models import User

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
