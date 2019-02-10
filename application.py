import datetime, json, os, requests
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

# Global variables
channels = []
all_message_data = {}
message_id = 0

# Run this before every GET or POST request to check that user is logged in
@app.before_request
def before_request():
  g.channel_name = None
  g.username = None
  if 'channel_name' in session:
    g.channel_name = session['channel_name']
  if 'username' in session:
    g.username = session['username']

# Index page will check to see if a new channel name is already taken before 
# allowing a user to create another one.
@app.route("/", methods=["GET", "POST"])
def index():
  if g.username and g.channel_name == None:
    # POST request
    if request.method == "POST":
      channel_exists = False
      new_channel = request.form.get('new_channel')
      for channel in channels:
        if channel == new_channel:
          channel_exists = True
      if channel_exists == False:  
        # In Python, using *.append() to add to a list will pass by reference and
        # change the global channels[] list 
        channels.append(new_channel)
        session['channel_name'] = new_channel
        return redirect(url_for("channel", channel_name=new_channel))
      else:
        return render_template("index.html", channels=channels, error="Channel already exists.")
    # GET request
    else:
      return render_template("index.html", channels=channels)
  elif g.username and g.channel_name:
    return redirect(url_for("channel", channel_name=g.channel_name))
  else:
    return redirect(url_for("login"))

# This is a generic route that allows for the creation any number of new channels
@app.route("/channel/<string:channel_name>")
def channel(channel_name):
  if g.username:
    chat_history = {}
    session.pop('channel_name', None)
    session['channel_name'] = channel_name

    # Search all_message_data{} to pull relevant chat history and store in the
    # chat_history{} dictionary
    for key in all_message_data:
      if all_message_data[int(key)]["channel_name"] == channel_name:
        chat_history[key] = all_message_data[key]

    return render_template("channel.html", channel_name=channel_name, chat_history=chat_history)
  else:
    return redirect(url_for("login"))

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
  session.pop('channel_name', None)
  session.pop('username', None)
  return redirect(url_for("login"))

# Logout of channel
@app.route("/logout_channel")
def logout_channel():
  session.pop('channel_name', None)
  return redirect(url_for("index"))

# Listen for chatroom messages
@socketio.on("submit message")
def message(data):
  channel_name = data["channel_name"]
  date = data["date"]
  message = data["message"]
  username = data["username"]
  # date_modified = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')

  # The 'global message_id' statement allows the global message_id variable to be
  # modified/pass by reference instead of by value
  global message_id
  message_id += 1

  # Add every message sent from every chatroom by every user into one large global
  # dictionary called all_message_data{}. The message_id variable is an arbitrary
  # number that serves as the key for each message.
  individual_message = { "channel_name": channel_name, "date": date, "message_id": message_id, "message": message, "username": username }
  all_message_data[message_id] = individual_message

  # Delete oldest messages from the all_message_data{} dictionary if there are 
  # more than 100 entries per channel
  container_100 = []
  for key in all_message_data:
    if all_message_data[key]["channel_name"] == channel_name:
      # container_100 is a list of tuples
      container_100.append((all_message_data[key]['message_id'], all_message_data[key]['date']))

  # Date is measured in milliseconds since Jan 1, 1970, the message with the 
  # smallest number of milliseconds is the oldest
  if len(container_100) > 100:
    min_date = min(container_100, key=lambda x: x[1])[1]
    for tuple in container_100:
      if tuple[1] == min_date:
        min_date_key = tuple[0]
        del all_message_data[min_date_key]

  # The first argument is customized so that the chat_history{} dictionary that is 
  # emitted is detected client-side only if the client-side user has the correct
  # channel_name. 
  emit("announce message" + ":" + channel_name, individual_message, broadcast=True)
