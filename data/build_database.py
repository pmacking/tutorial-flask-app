"""
This is a utility module to initialize, clean, and create the SQLite3 db.
"""

import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from config import db
from yahtzee.models import User

# dummy data to initialize the database with
USERS = [
    {'username': 'pmacking', 'first_name': 'Paul', 'last_name': 'Maclachlan'},
    {'username': 'tayadawne', 'first_name': 'Taya', 'last_name': 'Maclachlan'}
]

# delete database file if it already exists
if os.path.exists('yahtzee.db'):
    os.remove('yahtzee.db')

# create the database
db.create_all()

# iterate over the USERS dummy data and populate the users in the db
for user in USERS:
    u = User(
        username=user['username'],
        first_name=user['first_name'],
        last_name=user['last_name']
        )
    db.session.add(u)

db.session.commit()
