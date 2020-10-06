# eportfolio

Personal website. Parts of it is for the assignments of course "Build Your Professional ePortfolio in English".

https://eportfolioapp.herokuapp.com/

## Build your local app

I am using Python [Flask framework](https://flask.palletsprojects.com/en/1.1.x/).

## Deploy on Heroku (for static web app)

Prerequisites：
- Install Git
- Install gunicorn
- Install [The Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
- After installing, Heroku CLI can be used in commandline through your windows powershell (note not the command prompt, cmd.exe).
- create a Heroku account, then create new app
- `pip freeze > requirements.txt`, this requirements.txt file is needed for later deployment to set up the python environment.
- Create Procfile, with "web: gunicorn app: app" in the file.
- use git to upload your code `git init`, `git add .`, `git commit -m 'first commit'`
- `heroku login -i` or use `heroku login` to login through the browser
- `heroku git:remote -a {your-project-name}`, this add the repository to the remote
- git push heroku master
- Your application should be available at https://{your-project-name}.herokuapp.com/ if deployed correctly.

## Use addons on Heroku

I am using MySQL locally, so ClearDB on Heroku is actually the best addon choice for deploy my local web application on Heroku, but even the Ignite plan (Free) requires credit card verification (this is because on Heroku, add any add-on to the app, even if the add-on is free, requires verification. The only exceptions to this are the free plans for the Heroku Postgres and Heroku Connect add-ons). Considering this, I will use Heroku Postgres as my addon to avoid verification.

### Install PostgreSQL on your local machine

Steps:
- [download postgresql here](https://www.postgresql.org/download/), refer to the current [documentation here](https://www.postgresql.org/docs/13/index.html).
- use addons on Heroku for your app, please [refer to here](https://elements.heroku.com/addons/heroku-postgresql).
- create your database dump file from your local postgreSQL database, please [refer to here](https://www.postgresql.org/docs/current/backup-dump.html): `pg_dump -U postgres your_databasename > your_dumpfilename.dump`, you have to provide your password
- login to your Heroku postgres database and import the data to it from your local dump file.
  - login to your Heroku: `heroku login`
  - change directory to your local project folder, which contains the previously created dump file
  - check if you have already installed the addons correctly: `heroku addons`, you will see "heroku-postgresql  hobby-dev free created" listed there
  - use the [database credentials](https://data.heroku.com/datastores/dee11dcc-6a5f-49db-9f60-0e4386968c96#administration) provided on your Heroku postgres database settings to connect to the heroku postgres database and import the data from the dump file, for mine `heroku pg:psql postgresql-aerodynamic-28324 --app eportfolioapp`, **postgresql-aerodynamic-28324** is displayed on the databases of my account, **eportfolioapp** is the application name that I want to deploy
  - You will see the command prompt: `eportfolioapp::DATABASE=>`, you are using psql, the command-line interface to PostgreSQL.
  - `\i your_dumpfilename.dump` this will build your Heroku postgres database from your dump file.
  - there seems some problem with the rebuilding of database from dump file, to be solved later.