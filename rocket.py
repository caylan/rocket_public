import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Load default config
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='\x83c^|\xcd\xfc\xf6\xf5E\xf3\xd1p\x8e\r\x99\\\xfc\xa6W\xd4\xd2<\xea\x9a',
    USERNAME='admin',
    PASSWORD='somethingthatisntthedefaultpassword'
))

db = SQLAlchemy(app)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login():
	return "This will be the login page"

@app.route('/jobs')
def show_jobs():
	return "This will show the user a list of jobs, based on their qualifications"

@app.route('/details/<int:jid>')
def display_details(jid):
	return "This will display details about the given job with id = " + str(jid)

if __name__ == '__main__':
    app.run(host='0.0.0.0')