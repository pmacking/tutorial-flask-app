"""
This module contains the models for yahtzee. It also makes use of SQLAlchemy
"Model" class and Marshmallow "SQLAlchemyAutoSchema" class inheretence.
"""

from datetime import datetime
from config import db, ma


class User(db.Model):
    """
    User model which defines the user attributes and SQLite3 db table/fields.
    """
    __tablename__ = "user"
    user_id = db.Column(db.Integer, nullable=False, primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    timestamp = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
        )


class UserSchema(ma.SQLAlchemyAutoSchema):
    """
    This user schema inherets from SQLAlchemyAutoSchema and uses the Meta
    class to find the SQLAlchemy model User and the db.session.
    """
    class Meta:
        model = User
        sqla_session = db.session
