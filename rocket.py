import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

from flask.ext.sqlalchemy import SQLAlchemy
from wtforms import Form, fields, validators
from flask.ext.login import (LoginManager, current_user, login_user, login_required)

## Config setup
app = Flask(__name__)

# Load default config
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='\x83c^|\xcd\xfc\xf6\xf5E\xf3\xd1p\x8e\r\x99\\\xfc\xa6W\xd4\xd2<\xea\x9a',
    USERNAME='admin',
    PASSWORD='somethingthatisntthedefaultpassword'
))

db = SQLAlchemy(app)


## This will be moved to a separate file, probably
from datetime import datetime
class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    location = db.Column(db.String(80))
    deadline = db.Column(db.DateTime)
    description = db.Column(db.Text)

    def __init__(self, name, location, deadline, description):
        self.name = name
        self.location = location
        self.deadline = deadline
        self.description = description

    def __repr__(self):
        return '<Job %r | %r>' % (self.name, self.id)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique = True)
    password = db.Column(db.String(64))

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % self.email

class LoginForm(Form):
    email = fields.TextField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self):
        user = self.get_user()
        if user is None:
            raise validators.ValidationError('Invalid user')

        if user.password != self.password.data:
            raise validators.ValidationError('Invalid password')
    
    def get_user(self):
        return db.session.query(User).filter_by(email=self.email.data).first()

class RegistrationForm(Form):
    email = fields.TextField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        if db.session.query(User).filter_by(email=self.email.data).count() > 0:
            raise validators.ValidationError('Duplicate email')

# Initialize flask-login
def init_login():
    login_manager = LoginManager()
    login_manager.init_app(app)

    # User loader function
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(user_id)

## Load db models
# import rocket_models

## Routing
@app.route('/')
def index():
    if not current_user.is_authenticated():
        return redirect(url_for('login'))
    return redirect(url_for('jobs'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated():
        return redirect(url_for('jobs'))

    form = LoginForm()
    if form.validate_on_submit():
        login_user(user)
        return redirect(url_for('jobs'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated():
        return redirect(url_for('jobs'))

    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        user = User()
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('jobs'))

@app.route('/jobs')
@login_required
def show_jobs():
    """
    Renders a list of jobs that the currently logged in user qualifies for.
    """
    # All this code is scratch, dependent on the sqlaclhemy yet do be written
    # user = flask.ext.login.current_user
    # How do we filter the jobs, all job tags must be fulfilled by user?
    # jobs = Job.query.filter_by(tags=user.tags)

    j1 = Job('Job 1', 'Seattle, WA', datetime.now(), 'This is a description of the first job')
    j1.id = 1
    j2 = Job('Job 2', 'Spokane, WA', datetime.now(), 'This is a description of the second job')
    j2.id = 2
    j3 = Job('Job 3', 'Portland, OR', datetime.now(), 'This is a description of the third job')
    j3.id = 3

    jobs = [j1, j2, j3]

    return render_template('job_list.html', jobs=jobs)

    # return "This will show the user a list of jobs, based on their qualifications"

@app.route('/details/<int:jid>')
def display_job_details(jid):
    job = Job.query.get(jid)
    return "Job with id: " + jid + ", name: " + job.name + "location: " \
            + ", deadline: " + job.deadline + ", description: " + job.description

init_login()

if __name__ == '__main__':
    app.run(host='0.0.0.0')