# 8th-Wonder

## Organization and name scheme for the workspace
	8th-Wonder was hired to create a web application for a Putt Putt Golf tournament.
	The 8th-Wonder Putt Putt Golf web app will be stored in this repository.
	The documentation and resources for this project will be kept in the "docs" folder. 
	This includes use case diagrams, the project plan, database diagrams, and more as the project progresses.
	The project will kept in the folder "src".

## Version-control procedures
	Collaborators should have a forked repository of the app in Evelyn's account of the project "8th-Wonder", 
	in their Github. Each collaborator should clone the forked repository. Before each meeting, 
	collaborators should submit a pull request so we can monitor progress and discuss issues.

## Tool stack description and setup procedure
	We will be using python and Django as a framework since we are all familiar and have experience with it.
	We will be using a SQL database and AWS to host our web application.
	
### Communication Information
    Our team will be meeting through discord daily, beginning each meeting with a stand-up 
    in order to assess progress and hold each other accountable. New tasks will be assigned to 
    developers as needed. Discord is our main channel for communication. It is used for group calls, 
    file sharing, and other collaborative activities. Google Drive is used for storage for files 
    needing collaborative efforts. GitHub is used as our normal repository used for submissions, 
    version control, data tracking, and communication with Professor Dan Watson. Trello is used for 
    organization of tasks in the project, keeping track of what is finished and who is working on what.

  
## Build instructions

	Instructions for local Server:

	Clone the repository in git bash
	$ git clone https://github.com/PokeGon/8th-Wonder.git
    
    Inside cloned repository "src/" use the command
    $ python manage.py runsever

    The git window will give you a location to explore the site like the example below
    $ http://127.0.0.1:8000/

    Put that address into your search bar and run and you should be on the site!

	To access the live site, enter IP address into browser: 52.41.103.175

## Unit testing instructions
	Unit tests will cover all use cases laid out in the use case diagrams. They will be found in a designated 
	unit tests file. The unit test class will prompt the user to select which use cases should be executed.
 
## System testing instructions
    Each member has an AWS account and access to the server which may be tested through the AWS command line.
	The web app may be tested by going to the website and creating an account. 
	A admin account will be created in order to test all the actions from any user.

## Login Credentials
    Player: playerusername playerpassword
    Sponsor: sponsorusername sponsorpassword
    Manager: managerusername managerpassword
    Drink Meister: drinkmeisterusername drinkmeisterpassword

## Other development notes, as needed


