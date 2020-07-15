<h1>Tutorial Flask App</h1>

<h2>Description</h2>

<p>This repo explored building a single page web application using Flask, SQLAlchemy, SQLite, Pillow, NGINX, and Gunicorn.

Original intent was to build a yahtzee web application, but this repo pivoted to a basic application given the scope of learning fundamentals of Flask.
</p>

<h2>How to Clone and Build</h2>

<p>Download/clone repo, create/activate virtual environment for your own sanity, ensure you're on python3.8, "pip install -r requirements.txt" to install dependencies.

Set environment variables with export SECRET_KEY, EMAIL_USER, and EMAIL_PASSWORD.

Run "make db" to build db at ./data/yahtzee.db

Run "make run" to build app, access in browser at localhost:5000</p>
