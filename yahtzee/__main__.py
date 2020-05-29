"""
Main module of the server file.
"""

from flask import render_template
import config

# get the application instance
connexion_app = config.connexion_app

# use swagger file to configure connexion endpoints
connexion_app.add_api("swagger.yml")

# create URL route in application for home "/"
@connexion_app.route("/")
def home():
    """
    This function responds to the browser URL localhost:5000/

    return:         the renedered template "home.html"
    """
    return render_template("home.html")


if __name__ == "__main__":
    connexion_app.run(debug=True)
