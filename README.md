# eportfolio
ePortfolio assignments for course "Build Your Professional ePortfolio in English".

https://eportfolioapp.herokuapp.com/

## Build your local app

## Deploy on Heroku

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
