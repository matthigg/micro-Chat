# Web Programming with Python and JavaScript - Project 2

# Description
- This is project 2 for CS50 Web Development with Python and Javascript. It is a chat application that uses Flask SocketIO that allows users to create a username (but not a password), create and join chatroom channels, and send messages that can be seen by other users within the channel.

# Configuration
- Before launching the Flask application you have to set the FLASK_APP environment variable. In Powershell you can set FLASK_APP as well as other environment variables manually from the command line:

  $ FLASK_APP='application.py'
  $ FLASK_ENV='development'
  $ FLASK_DEBUG='0'   
  $ SECRET_KEY='qwerty'

  ... setting FLASK_DEBUG='1' returns ValueError: signal only works in main thread. Basically, there is some issue with auto-reloading the server when changes are made while using Flask-SocketIO (2/13/2019).

  ... in Powershell you can see which environment variables have currently been set by typing:

  $ Get-ChildItem Env:

- Once the environment variables have been set you can start a Flask server with:

  $ flask run

# What's contained in the files
login.html, login.js
Users are prompted to enter a username when intitially visiting the site, nbsp/space key is the only key that is prevented. There are no passwords associated with usernames.

index.html, index.js
A greeting to the user includes a randomly generated avatar, a list of active channels (if any), an input field that allows for the creation of a new channel, and a logout link.

channel.html, channel.js
Within each channel the user is greeted with a message letting them know which channel they are in, followed by chat history (if any) that includes up to the most recent 100 messages. There is an input field to submit messages with no character restrictions, followed by a link to log out of the channel, or to log out of both the channel and the user session.

application.py
The username and channel_name are stored server-side via application.py using Flask-Session and the g variable -- both are used in redirecting the user to appropriate pages. The username is also associated with every message a user posts in a chatroom.

When a new channel is created, a generic route is used to create the new chatroom (channel and chatroom are used interchangeably), and the channel name is stored in session['channel_name'] before the user is redirected to the new chatroom. 

Once in the chatroom, the user can log out of the chatroom -- this clears session['channel_name'], but not session['username']. Afterwards, the user is redirected to index.html. From there, if a user clicks on an active channel link then the channel name is assigned to session['channel_name'] by passing ?name=channel_name in the URL.

Within a chatroom, a user can send messages with no character restrictions. The display name of the user and timestamp are associated with the message, along with their randomly generated avatar. These messages can be viewed by other users who are currently in the chatroom without having to refresh the browser.

If a user has an active session, ie. session['username'] is True, then if they close their browser and open it again, they should still be logged in. Likewise, if session['channel_name'] is True, then if they close their browser and open the application again, they should be directed to their current channel.

# Personal touch
The personal touch was associating randomly-generated avatars with each unique username using the Adorable Avatars API at http://avatars.adorable.io/.