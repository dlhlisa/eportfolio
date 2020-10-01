# eportfolio
ePortfolio assignments for course "Build Your Professional ePortfolio in English".

https://eportfolioapp.herokuapp.com/

## Build your local app



## Deploy on Heroku (for static web app)

Prerequisites：
- Install Git
- Install gunicorn
- Install [The Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)

- `pip freeze > requirements.txt`
- Create Procfile, with "web: gunicorn app:app" in the file.
- create a Heroku account, then create new app
- use git to upload your code `git init`, `git add .`, `git commit -m 'first commit'`
- `heroku login -i` or use `heroku login` to login using the browser
- `heroku git:remote -a {your-project-name}`, this add the repository to the remote
- git push heroku master
- Your application https://{your-project-name}.herokuapp.com/

## Use addons on Heroku

I am using MySQL locally, so ClearDB on Heroku is actually the best addon choice on Heroku, but even the Ignite plan (Free) requires credit card verification, this is because on Heroku, add any add-on to the app, even if the add-on is free, requires verification. The only exceptions to this are the free plans for the Heroku Postgres and Heroku Connect add-ons. Considering this, I will use Heroku Postgres as my addon to avoid verificatio.