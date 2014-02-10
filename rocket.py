from datetime import datetime
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash
from flask.ext.login import LoginManager, current_user, login_user, \
    login_required, logout_user
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form
from wtforms import fields
from wtforms.validators import ValidationError, InputRequired, Length, Email


#####################
### Configuration ###
#####################

app = Flask(__name__)

# Load default config
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='\xb3J]3\x85t\x1fFH77!D:<\xd1\xd4+\xab\x00=OZ\xab',
    USERNAME='admin',
    PASSWORD='somethingthatisntthedefaultpassword'
))

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://caylan@localhost/caylan'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


##############
### Models ###
##############

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
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
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


#############
### Forms ###
#############

class LoginForm(Form):
    email = fields.TextField(u'email', [InputRequired()])
    password = fields.PasswordField(u'password', [InputRequired()])
    remember_me = fields.BooleanField(u'remember_me', default=False)

    def validate_email(form, field):
        user = form.get_user(field.data)
        if user is None:
            raise ValidationError(u'An account with that email was not found')

    def validate_password(form, field):
        user = form.get_user(form.email.data)
        if user is not None and user.password != field.data:
            raise ValidationError('Invalid password')

    def get_user(form, email):
        return User.query.filter_by(email=email).first()


class RegistrationForm(Form):
    email = fields.TextField(u'email', [InputRequired(),
                                        Length(min=5, max=120),
                                        Email()])
    password = fields.PasswordField(u'password', [InputRequired()])

    def validate_email(form, field):
        if User.query.filter_by(email=field.data).count() > 0:
            raise ValidationError('This email is already in use.')



#############
### Views ###
#############

@app.route('/')
def index():
    if current_user.is_authenticated():
        return redirect(url_for('show_jobs'))
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated():
        return redirect(url_for('show_jobs'))

    form = LoginForm()
    if form.validate_on_submit():
        user = form.get_user(form.email.data)
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('show_jobs'))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated():
        return redirect(url_for('show_jobs'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User()
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('show_jobs'))
    return render_template('register.html', form=form)


@app.route('/jobs')
@login_required
def show_jobs():
    """
    Renders a list of jobs that the currently logged in user qualifies for.
    """

    j1 = Job('Job 1', 'Seattle, WA', datetime.now(),
             'This is a description of the first job')
    j1.id = 1
    j2 = Job('Job 2', 'Spokane, WA', datetime.now(),
             'This is a description of the second job')
    j2.id = 2
    j3 = Job('Job 3', 'Portland, OR', datetime.now(),
             'This is a description of the third job')
    j3.id = 3

    jobs = [j1, j2, j3]

    return render_template('job_list.html', jobs=jobs)


@app.route('/details/<int:jid>')
def display_job_details(jid):
    job = Job.query.get(jid)
    return "Job with id: " + jid + ", name: " + job.name + "location: "\
        + ", deadline: " + job.deadline + ", description: " + job.description


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
