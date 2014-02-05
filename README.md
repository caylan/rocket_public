# Development
BEFORE YOU START (EVERY TIME YOU CODE): 

	1. Sync your repo
	2. Launch your virtual environment.

On Windows:

	$ ./venv/Scripts/activate

On Linux/Mac:

	$ source ./venv/bin/activate

### Updating your dependencies

	$ pip install -r requirements.txt

Now you're ready to code!

# Deployment
Rocket is currently hosted at rocket-app.herokuapp.com

## Adding heroku as a remote to your git repo

	$ git remote add heroku git@heroku.com:rocket-app.git

## Deploying to Heroku 
Using a terminal, push to the heroku remote to automatically deploy the app.

If you've made any changes to the dependencies, run the following first: 
	
	$ pip freeze > requirements.txt

For future reference, doing this in Powershell saves requirements.txt automatically in Unicode,
which is bad. Haven't looked up a way to fix this automatically, but it's not that that hard to
just Save As and set encoding back to ANSI:
http://georgik.sinusgear.com/2012/08/20/problems-with-deploying-heroku-django-app-from-windows/

Then, push to heroku:

	$ git push heroku master