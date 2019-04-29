# Web Programming with Python and JavaScript - Project 2

# Description
- This website is a chat application that uses Flask SocketIO which allows users to create a username, create and join chatroom channels, and send messages that can be seen by other users within the channel.

- This is project 2 for CS50 - Web Programming with Python and Javascript:

  https://docs.cs50.net/web/2018/x/projects/2/project2.html

# Development Setup & Configuration
- Environment variables are used to start the server, access the database, access the Goodreads API, and toggle development settings. Using Powershell you can set environment variables manually from the command line:

  $ $env:DATABASE_URL = "database URL"
  $ $env:FLASK_APP = "application.py"
  $ $env:GOODREADS_API_KEY = "goodsreads api key"
  $ $env:FLASK_ENV = "development"  // debugger + automatic reloader
  $ $env:FLASK_DEBUG = "1"          // debugger
  $ $env:FLASK_ENV = "production"   // turn off development (off by default)
  $ $env:SECRET_KEY = "secret key"  // encrypt session cookies
  $ Get-ChildItem Env:              // view environment variables

  ... or you can store the variables in a .env file within the root directory and retrieve them via dotenv: https://pypi.org/project/python-dotenv/#installation. Make sure to set FLASK_ENV = "production" (or just omit the FLASK_ENV variable entirely) in production.

  ... setting FLASK_DEBUG='1' returns: 
  
    > ValueError: signal only works in main thread. 
    
  ... basically, there is some issue with auto-reloading the server when changes are made while using Flask-SocketIO (2/13/2019). 
  
    https://stackoverflow.com/questions/51179369/flask-socketio-auto-reload-is-not-working-on-code-change-development

- Once the environment variables have been set you can start a Flask server with:

  $ flask run

# Display Name
- Files: login.html, login.js

- Creating a Login Page: https://www.youtube.com/watch?v=eBwhBrNbrNI

- Visitors are prompted to enter a display name when intitially visiting the site; the nbsp/space key is the only key that is prevented. There are no passwords associated with usernames. Once a user enters a display name, they are considered to be "logged on".

- Login & Sessions:

  1. The time between when a client logs on and logs off is called a "session", and Flask uses a "session object" to store information about a client during this time. So in Flask, a "session" is basically both a length of time and an object.

  3. When a visitor enters a display name it is stored in a "session object". A "session object" is basically a dictionary of key:value pairs used to represent an active session. Flask places the session object in a cookie and uses a "secret key" to encrypt it. When creating an instance of a Flask application within app.py or application.py (whatever the controller file is) its secret key can be set like this:

    > app = Flask(__name__)
    > app.secret_key = <secret key goes here>

    ... to generate a random key from the command line:

    $ python -c 'import os; print(os.urandom(16))'

# Channel Creation & Channel List
- Files: index.html, index.js

- Once a visitor has chosen a display name they are taken to index.html which displays a greeting to the user, a randomly generated avatar, a list of active channels (if any), an input field that allows for the creation of a new channel, and a logout link. From here, visitors can create new channels or join existing channels.

# Messages View & Sending Messages
- Files: channel.html, channel.js

- Within each channel the user is greeted with a message letting them know which channel they are in, followed by chat history (if any) that includes up to the most recent 100 messages. There is an input field to submit messages (with no character restrictions, which is probably not safe for production), followed by a link to log out of the channel, and another link to log out of both the channel and the user session.

# Remembering the Channel
- File: application.py

- The display name (username) and channel (channel_name) are stored server-side via application.py using Flask-Session/"session object" and the g variable -- both are used in redirecting the user to appropriate pages. The username is also associated with every message a user posts in a chatroom.

- When a new channel is created, a generic route is used to create the new chatroom (channel and chatroom are used interchangeably), and the channel name is stored in session['channel_name'] before the user is redirected to the newly created chatroom. 

- Once in the chatroom, the user can log out of the chatroom -- this clears session['channel_name'], but not session['username']. Afterwards, the user is redirected to index.html. From there, if a user clicks on an active channel link then the channel name is assigned to session['channel_name'] by passing it via a GET request, ie. url?name=channel_name.

- Visitors can send messages in chat rooms with no character restrictions. The display name of the user and timestamp are associated with the message, along with their randomly generated avatar. These messages can be viewed by other users who are currently in the chatroom without having to refresh the browser thanks to Flask-SocketIO.

- If a user has an active session, ie. session['username'] == True, and they close their browser and open it again, they should still be logged in. Likewise, if session['channel_name'] == True, then if they close their browser and open the application again they should be directed to their current channel.

# Personal touch
- The personal touch was associating randomly-generated avatars with each unique username using the Adorable Avatars API at http://avatars.adorable.io/.

# Production
- This app is a project for CS50 - Web Development with JavaScript and Python, and hasn't been pushed to production. However, in the event that it does get deployed, it would probably be a good idea to put some kind of filter on chatroom messages to prevent hax and also check out these resources:

  1. http://flask.pocoo.org/docs/1.0/tutorial/deploy/
  2. http://flask.pocoo.org/docs/1.0/config/

# Notes
- It's a good idea to add *.pyc to the .gitignore file, and additionally you can ask git to remove any *.pyc files that happen to already be tracked by git by running the following from the command line:

  $ git rm --cached *.pyc

  ... https://coderwall.com/p/wrxwog/why-not-to-commit-pyc-files-into-git-and-how-to-fix-if-you-already-did

- The flask_session folder should also be added to the .gitignore file.