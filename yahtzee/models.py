"""
This module contains the models for yahtzee. It also makes use of SQLAlchemy
"Model" class and Marshmallow "SQLAlchemyAutoSchema" class inheretence.
"""

from datetime import datetime
from yahtzee import db, ma


class UsersGames(db.Model):
    """
    UsersGames model which defines attributes for a user and game within the db

    UsersGames relationships: enables one-to-many between game and users
    """
    __tablename__ = "users_games"
    users_games_id = db.Column(db.Integer, nullable=False, primary_key=True)
    ones = db.Column(db.Integer, nullable=False)
    twos = db.Column(db.Integer, nullable=False)
    threes = db.Column(db.Integer, nullable=False)
    fours = db.Column(db.Integer, nullable=False)
    fives = db.Column(db.Integer, nullable=False)
    sixes = db.Column(db.Integer, nullable=False)
    three_of_a_kind = db.Column(db.Integer, nullable=False)
    four_of_a_kind = db.Column(db.Integer, nullable=False)
    full_house = db.Column(db.Integer, nullable=False)
    small_straight = db.Column(db.Integer, nullable=False)
    large_straight = db.Column(db.Integer, nullable=False)
    yahtzee = db.Column(db.Integer, nullable=False)
    chance = db.Column(db.Integer, nullable=False)
    yahtzee_bonus = db.Column(db.Integer, nullable=False)
    top_score = db.Column(db.Integer, nullable=False)
    top_bonus_score = db.Column(db.Integer, nullable=False)
    top_bonus_score_delta = db.Column(db.Integer, nullable=False)
    total_top_score = db.Column(db.Integer, nullable=False)
    total_bottom_score = db.Column(db.Integer, nullable=False)
    grand_total_score = db.Column(db.Integer, nullable=False)
    user_id = db.Column(
        db.Integer, db.ForeignKey('user.user_id'), nullable=False
    )
    game_id = db.Column(
        db.Integer, db.ForeignKey('game.game_id'), nullable=False
    )

    def __repr__(self):
        return (
            f"UsersGames("
            f"'{self.users_games_id}', "
            f"'{self.user_id}', "
            f"'{self.game_id}', "
            f"'{self.ones}', "
            f"'{self.twos}', "
            f"'{self.threes}', "
            f"'{self.fours}', "
            f"'{self.fives}', "
            f"'{self.sixes}', "
            f"'{self.three_of_a_kind}', "
            f"'{self.four_of_a_kind}', "
            f"'{self.full_house}', "
            f"'{self.small_straight}', "
            f"'{self.large_straight}', "
            f"'{self.yahtzee}', "
            f"'{self.chance}', "
            f"'{self.yahtzee_bonus}', "
            f"'{self.top_score}', "
            f"'{self.top_bonus_score}', "
            f"'{self.top_bonus_score_delta}', "
            f"'{self.total_top_score}', "
            f"'{self.total_bottom_score}', "
            f"'{self.grand_total_score}', "
            f")"
        )


class UsersGamesSchema(ma.SQLAlchemyAutoSchema):
    """
    This UsersGames schema inherets from SQLAlchemyAutoSchema and uses the Meta
    class to find the SQLAlchemy model UsersGames and the db.session.
    """
    class Meta:
        model = UsersGames
        sqla_session = db.session


class User(db.Model):
    """
    User model which defines the user attributes and SQLite3 db table/fields.
    """
    __tablename__ = "user"
    user_id = db.Column(db.Integer, nullable=False, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    timestamp = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
        )
    users_games = db.relationship('UsersGames', backref='user', lazy=True)

    def __repr__(self):
        return (
            f"User('{self.user_id}', '{self.username}', '{self.first_name}', "
            f"'{self.last_name}', '{self.email}')"
        )


class UserSchema(ma.SQLAlchemyAutoSchema):
    """
    This user schema inherets from SQLAlchemyAutoSchema and uses the Meta
    class to find the SQLAlchemy model User and the db.session.
    """
    class Meta:
        model = User
        sqla_session = db.session


class Game(db.Model):
    """
    Game model which defines the game attributes and db table/fields.
    """
    __tablename__ = "game"
    game_id = db.Column(db.Integer, nullable=False, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    users_games = db.relationship('UsersGames', backref='game', lazy=True)

    def __repr__(self):
        return f"Game('{self.game_id}', '{self.timestamp}'"


class GameSchema(ma.SQLAlchemyAutoSchema):
    """
    This game schema inherets from SQLAlchemyAutoSchema and uses the Meta
    class to find the SQLAlchemy model Game and the db.session.
    """
    class Meta:
        model = Game
        sqla_session = db.session
