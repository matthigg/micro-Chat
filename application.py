import copy, datetime, json, os, requests
from datetime import datetime
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

# Run this before every GET or POST request to get channel_name and username
@app.before_request
def before_request():
  g.channel_name = None
  g.username = None
  if 'channel_name' in session:
    g.channel_name = session['channel_name']
  if 'username' in session:
    g.username = session['username']

# Index page
@app.route("/", methods=["GET", "POST"])
def index():
  if g.username and g.channel_name == None:
    # POST request
    if request.method == "POST":
      channel_exists = False
      new_channel = request.form.get('new_channel')
      # Check for existing channels with the same name
      for channel in channels:
        if channel == new_channel:
          channel_exists = True
      if channel_exists == False:  
        channels.append(new_channel)
        session['channel_name'] = new_channel
        return redirect(url_for("channel", channel_name=new_channel))
      else:
        return render_template("index.html", channels=channels, error="Channel already exists.")
    # GET request
    else:
      return render_template("index.html", channels=channels)
  # If user closes app and re-opens, they'll be taken back into their channel
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

    # Search all_message_data{} to pull relevant chat history and store in
    # chat_history{}
    for key in all_message_data:
      if all_message_data[int(key)]["channel_name"] == channel_name:
        chat_history[key] = all_message_data[key]

    # Use deepcopy and reformat the timestamps on all messages in chat_history{}
    chat_history_copy = copy.deepcopy(chat_history)
    for key in chat_history_copy:
      chat_history_copy[key]['date'] = datetime.fromtimestamp(chat_history_copy[key]['date'] / 1000.0).strftime('%m/%d/%Y, %H:%M:%S')
    
    # print("===========================================")
    # print("COPY: ", chat_history_copy)
    # print("AMD: ", all_message_data)
    # print("same: ", all_message_data == chat_history_copy)
    # print("===========================================")

    return render_template("channel.html", channel_name=channel_name, chat_history=chat_history_copy)
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

  # The container_100 list contains the message_id and date (in milliseconds) for
  # each message in the current channel, and stores both values together as tuples
  container_100 = []
  for key in all_message_data:
    if all_message_data[key]["channel_name"] == channel_name:
      # container_100 is a list of tuples
      container_100.append((all_message_data[key]['message_id'], all_message_data[key]['date']))

  # print("===========================================")
  # print("CONTAINER_100: ", container_100[0])
  # print("AMD: ", all_message_data)
  # print("===========================================")

  # The tuple with the minimum date value corresponds to the oldest message, and
  # its key is used to find and delete the corresponding message stored in the
  # all_message_data{} dictionary
  # container_100_copy = container_100.copy()
  if len(container_100) > 3:
    min_date = min(container_100, key=lambda x: x[1])[1]
    for tuple in container_100:
      if tuple[1] == min_date:
        min_date_key = tuple[0]
        del all_message_data[min_date_key]

  # Change the timestamp format for individual_message
  individual_message_copy = individual_message.copy()
  individual_message_copy["date"] = datetime.fromtimestamp(individual_message["date"] / 1000.0).strftime('%m/%d/%Y, %H:%M:%S')

  # print("=================================")
  # print("IMC: ", individual_message_copy)
  # print("AMD: ", all_message_data)
  # print("=================================")

  # The first argument is customized so that the chat_history{} dictionary that is 
  # emitted is detected client-side only if the client-side user has the correct
  # channel_name. 
  emit("announce message" + ":" + channel_name, individual_message_copy, broadcast=True)
