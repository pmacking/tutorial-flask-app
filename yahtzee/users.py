"""
This module contains users.CRUD operations as a handler for HTTP requests to
/api/users
"""

# import flask modules to create REST API responses
from flask import (
    make_response,
    abort,
)

from config import db

# import SQLAlchemy User and Marshmallow UserSchema classes to access user
# database table and serialize the results
from models import (
    User,
    UserSchema,
)


# create handler for read (GET) users
def read_all():
    """
    This function responds to a request for api/v1/users with the list of users

    :return:            sorted list of users
    """
    # create the list of users from our data
    users = User.query \
        .order_by(User.last_name) \
        .all()

    # serialize data for response: many=True tells UserSchema expect iterable
    user_schema = UserSchema(many=True)
    # The return result is an object having a data attribute, an object
    # containing a people list that can be converted to JSON. This is returned
    # and converted by Connexion to JSON as the response to the REST API call
    return user_schema.dump(users).data
