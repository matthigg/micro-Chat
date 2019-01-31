import json, os, requests
from dotenv import load_dotenv, find_dotenv
from flask import Flask, g, redirect, render_template, request, session, url_for
from flask_session import Session
from flask_socketio import SocketIO, emit

# Startup
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# Load environment variables 
load_dotenv(find_dotenv())
FLASK_APP = os.getenv("FLASK_APP")
FLASK_ENV = os.getenv("FLASK_ENV")
FLASK_DEBUG = os.getenv("FLASK_DEBUG")

# This array holds a list of all active channels
channels = []

# Run this before every GET or POST request to check that user is logged in
@app.before_request
def before_request():
  g.username = None
  if 'username' in session:
    g.username = session['username']

# Index page will check to see if a new channel name is already taken before 
# allowing a user to create another one.
@app.route("/", methods=["GET", "POST"])
def index():
  if g.username:
    if request.method == "POST":
      channel_exists = False
      new_channel = request.form.get('new_channel')
      for channel in channels:
        if channel == new_channel:
          channel_exists = True
      if channel_exists == False:    
        channels.append(new_channel)
        return redirect(url_for("channel", channel_name=new_channel))
      else:
        error = "Channel already exists."
        return render_template("index.html", channels=channels, error=error)
    else:
      return render_template("index.html", channels=channels)
  else:
    return redirect(url_for("login"))

# This allows a route to create any number of new channels, which is named after
# the new channel name that a user types in when creating a new channel on the
# index page
@app.route("/channel/<string:channel_name>")
def channel(channel_name):
  return render_template("channel.html", channel_name=channel_name)

# Login using the session variable
@app.route("/login", methods=["GET", "POST"])
def login():
  if request.method == "POST":
    session.pop('username', None)
    session['username'] = request.form.get('username')
    return redirect(url_for("index"))
  else:
    return render_template("login.html")

# Logout
@app.route("/logout")
def logout():
  session.pop('username', None)
  return redirect(url_for("login"))

# Listen for chatroom messages
@socketio.on("submit message")
def message(data):
  message = data["message"]
  username = data["username"]
  emit("announce message", {"message": message, "username": username}, broadcast=True)