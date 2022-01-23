#CS50 Final Project – Web Programming with Python and JavaScript

This application called Mammam – a social network that allow users to share their recipes. The recipe is mainly for baby or toddler. Each recipe included type of food, image, ingredients, steps. User can create their all recipe or also search other’s recipe using keywords.
Although this project is a social network but is indistinct from Project 4 as it is not focus on interaction among user through comment, like. This project is mainly focus on advanced the function of backend (searching function) and front-end (add /remove ingredients and steps). This also extend the complexity by using jquery to manage database.
The web application utilizes Django as a backend and JavaScript on the front-end. The jquery is also used to for database management purpose.  
All webpages of the project are mobile-responsive.

##Files and directories
•	final_project – project name
•	mammam- main application directory.
o	static/mammam contains all static content.
	style.css - contains compiled CSS file and its map.
	recipe.js – script that run in create.html and update.html template to display input form for user’s recipe
	view.js – script that manage the front-end of view recipe 
o	templates/djangoapp contains all application templates.
	create.html – this template shows the form of recipe that user could fill in to submit their recipe
	index.html – this template shows the index of the website
	layout.html – layout template. Other templates are extended by this layout
	login.html- template for allow user login and logout
	register.html – template that allow user to register the account
	update.html – template that shows the front end of the website once user want to update recipe
	view.html – template of each card displays recipe’s view
o	admin.py - here I added some admin classes and re-registered User model.
o	models.py contains the Recipe models of the project. 
o	urls.py - all application URLs.
o	views.py this file contains all functions that help to run the project
•	media/images - contains photos of the recipes. All user’s photo also be saved in this folder 

##Installation
•	Install project dependencies by running pip install -r requirements.txt. Dependencies include Django and Pillow module that allows Django to work with images.
•	In the terminal, cd into the final_project directory.
•	Run python manage.py makemigrations mail to make migrations for the mammam app.
•	Run python manage.py migrate to apply migrations to database.
•	Go to website address and register an account.

##Demo:
https://www.youtube.com/watch?v=Tyj0ZVEZJNU
