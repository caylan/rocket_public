import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

from flask.ext.sqlalchemy import SQLAlchemy

import rocket_models

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Do a login, might be different if we use flask-login
        pass
    else:
        # Render login form
        pass
    return "This will be the login page"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Process the form and return user to login page
        pass
    else:
        # Render a user registration form
        pass
    return "This will be a registration form"

@app.route('/jobs')
def show_jobs():
    """
    Renders a list of jobs that the currently logged in user qualifies for.
    """
    # All this code is scratch, dependent on the sqlaclhemy yet do be written
    user = flask.ext.login.current_user
    # How do we filter the jobs, all job tags must be fulfilled by user?
    jobs = Job.query.filter_by(tags=user.tags)

    return "This will show the user a list of jobs, based on their qualifications"

@app.route('/details/<int:jid>')
def display_job_details(jid):
    job = Job.query.get(jid)
    return "Job with id: " + jid + ", name: " + job.name + "location: " \
            + ", deadline: " + job.deadline + ", description: " + job.description

if __name__ == '__main__':
    app.run(host='0.0.0.0')