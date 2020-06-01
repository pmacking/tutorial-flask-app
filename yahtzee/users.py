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
from yahtzee.models import (
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
    # containing a user list that can be converted to JSON. This is returned
    # and converted by Connexion to JSON as the response to the REST API call
    return user_schema.dump(users).data


def create(user):
    """
    This function responds to a post request to api/v1/users and creates a new
    user in the users structure based on the passed-in user data

    :param user:        user to create in the user structure
    :return:            201 on success, 409 on user exists
    """

    username = user.get('username')
    first_name = user.get('first_name')
    last_name = user.get('last_name')
    email = user.get('email')

    existing_user = User.query \
        .filter(User.username == username) \
        .filter(User.first_name == first_name) \
        .filter(User.last_name == last_name) \
        .filter(User.email == email) \
        .one_or_none()

    # can we insert this user?
    if existing_user is None:

        # create a user instance using the schema and passed-in user
        user_schema = UserSchema()
        new_user = user_schema.load(user, session=db.session).data

        # add user to database
        db.session.add(new_user)
        db.session.commit()

        # serialize and return new user in the response
        return user_schema.dump(new_user).data, 201

    # otherwise, no user already exists
    else:
        abort(409, f'User {first_name} {last_name} already exists.')


def read_one(user_id):
    """
    This function responds to a request for api/v1/users/{user_id} with one
    matching user from users

    :param user_id:     ID of user to find
    :return:            user matching ID
    """
    # get one_or_none user requested from our data
    user = User.query \
        .filter(User.user_id == user_id) \
        .one_or_none()

    # did we find person
    if user is not None:

        # serialize data for response
        user_schema = UserSchema(many=False)
        return user_schema.dump(user).data

    # otherwise, no we didn't find user
    else:
        abort(404, f'User not found for Id: {user_id}')

def update(user_id, user):
    """
    This function responds to a PUT api/v1/users/{user_id} to update a user in
    the user structure. Throws an error if the user to update already exists.

    :param user_id:     the ID of the user we want to update
    :param user:        the user data to update with
    :return:            updated user structure
    """
    # get the user requested from the data
    update_user = User.query \
        .filter(User.user_id == user_id) \
        .one_or_none()

    # try and find an existing user with the same data as user param
    first_name = user.get("first_name")
    last_name = user.get("last_name")

    existing_user = User.query \
        .filter(User.first_name == first_name) \
        .filter(User.last_name == last_name) \
        .one_or_none()

    # are we updating a user that doesn't exist?
    if update_user is None:
        abort(404, f"User not found for Id: {user_id}")

    # does the user to update with already exist (would we create dupe)?
    elif (existing_user is not None and existing_user.user_id != user_id):
        abort(409, f"Person {first_name} {last_name} already exists")

    # otherwise update user
    else:

        # create a user instance using the schema and user param
        user_schema = UserSchema()
        update = user_schema.load(user, session=db.session)

        # set the id to the user we want to update
        update.user_id = update_user.user_id

        # merge new object into old and commit to db
        db.session.merge(update)
        db.session.commit()

        # return updated user in response
        data = user_schema.dump(update_user)

        return data, 200
