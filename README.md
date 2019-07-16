# Flask-Blog
A posting blog created using flask

This project was done with python3.6 in a virtual environment using pipenv. I recommend using pipenv to run the project,
so you can get the same versions as me for each library.
The site has a working log in/register system and a posting option for each user. Also each user can see others's profile and posts.
Before you change some code you should run and play with the site a little for a better understanding. 

Also an important thing to mention is that you have to change this with an account of gmail, otherwise the changing password mail will
not be send:\
app.config['MAIL_USERNAME'] = 'yourmail@gmail.com'\
app.config['MAIL_PASSWORD'] = 'yourpassword'

Future work:
- shortcuts on sidebar
- friends list system
- automated testing system

Also the HTML code and CSS code is mostly copied from: https://github.com/CoreyMSchafer/code_snippets/tree/master/Python/Flask_Blog, all copyrights reserved to Corey Schafer. 
