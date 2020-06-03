"""
This module contains routing for the flask app
"""

from flask import render_template
import config

# get the application instance
connexion_app = config.connexion_app

# create URL route in application for home "/"
@connexion_app.route("/")
def home():
    """
    This function responds to the browser URL localhost:5000/

    return:         the renedered template "home.html"
    """
    return render_template("home.html")
