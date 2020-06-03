"""
Main module of the server file.
"""

import config
from yahtzee import routes

# get the application instance
connexion_app = config.connexion_app

# use swagger file to configure connexion endpoints
connexion_app.add_api("swagger.yml")

if __name__ == "__main__":
    connexion_app.run(debug=True)
