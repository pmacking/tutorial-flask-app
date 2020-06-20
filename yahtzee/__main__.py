"""
Main module of the server file.
"""

from yahtzee import connexion_app
import yahtzee.routes

if __name__ == "__main__":
    connexion_app.run()
