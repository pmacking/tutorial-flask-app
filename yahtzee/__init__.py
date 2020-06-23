import os
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt

BASEDIR = os.path.abspath(os.path.dirname(__file__))

# create connexion app, config from swagger.yml in specification_dir path
connexion_app = connexion.App(__name__, specification_dir=BASEDIR)

# get the underlying Flask app instance
app = connexion_app.app

# config app instance from config.py class
app.config.from_object("config.DevelopmentConfig")

# create SQLAlchemy db instance from app with configs above
db = SQLAlchemy(app)

# init Bcrypt
bcrypt = Bcrypt(app)

# init Marshmallow
ma = Marshmallow(app)

# use swagger file to configure connexion endpoints
connexion_app.add_api("../swagger.yml")
