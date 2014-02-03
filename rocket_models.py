# Define the models for use in the rocket database here. 
# Use Flask-SQLAlchemy declarations, examples found here:
# http://pythonhosted.org/Flask-SQLAlchemy/models.html

from datetime import datetime

# Note: Job will not contain a reference to Organization, 
# Organization will contain a backref to Job
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
