"""
Main module of the server file.
"""

from yahtzee import app
from yahtzee.users.routes import users
from yahtzee.main.routes import main
from yahtzee.users.forms import RegistrationForm, LoginForm

app.register_blueprint(users)
app.register_blueprint(main)

if __name__ == "__main__":
    app.run()
