"""
This module manages the configuration of the Flask app with Connexion (OpenAPI
support (aka swagger)), the SQLAlchemy ORM with an SQLite3 db, and the
Marshmallow json-parser.
"""

import os
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

BASEDIR = os.path.abspath(os.path.dirname(__file__))

# create connexion app, config from swagger.yml in specification_dir path
connexion_app = connexion.App(__name__, specification_dir=BASEDIR)

# get the underlying Flask app instance
app = connexion_app.app

# config SQLAlchemy component of Flask app instance, /// supports Windows OS
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(BASEDIR, 'data/yahtzee.db')
app.config['SQLALCHMEY_TRACK_MODIFICATIONS'] = False

# create SQLAlchemy db instance
db = SQLAlchemy(app)

# init Marshmallow
ma = Marshmallow(app)
