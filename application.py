import copy, datetime, os
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
from flask import Flask, g, redirect, render_template, request, session, url_for
from flask_session import Session
from flask_socketio import SocketIO, emit

# Startup.
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# Load environment variables.
load_dotenv(find_dotenv())
FLASK_APP = os.getenv("FLASK_APP")
FLASK_ENV = os.getenv("FLASK_ENV")
FLASK_DEBUG = os.getenv("FLASK_DEBUG")

# Global variables.
all_message_data = {}
channels = []
message_id = 0
usernames = []

# Run this before every GET or POST request to get channel_name and username.
@app.before_request
def before_request():
  g.channel_name = None
  g.username = None
  if 'channel_name' in session:
    g.channel_name = session['channel_name']
  if 'username' in session:
    g.username = session['username']

# ==================== INDEX ====================================================

@app.route("/", methods=["GET", "POST"])
def index():
  if g.username and g.channel_name == None:

    # POST
    if request.method == "POST":
      channel_exists = False
      new_channel = request.form.get('new_channel')

      # Check for existing channels with the same name.
      for channel in channels:
        if channel == new_channel:
          channel_exists = True
      if channel_exists == False:  
        channels.append(new_channel)
        session['channel_name'] = new_channel
        return redirect(url_for("channel", channel_name=new_channel))
      else:
        return render_template("index.html", channels=channels, error="Channel already exists.")
    
    # GET
    else:
      return render_template("index.html", channels=channels)

  # If user closes app and re-opens, they'll be taken back into their channel.
  elif g.username and g.channel_name:
    return redirect(url_for("channel", channel_name=g.channel_name))
  else:
    return redirect(url_for("login"))

# ==================== CHANNEL ==================================================

@app.route("/channel/<string:channel_name>")
def channel(channel_name):

  # If the URL contains a 'name' key via a GET request, ie. url?name=channel_name, 
  # then request.args.get('name') == True and therefore 'channel_name' gets 
  # assigned to session['channel_name'] and g.channel_name.
  #  
  # This means that a user could create a channel by manually typing it into
  # the URL bar and then submitting a GET request, but if they do this then the 
  # channel will not get saved in the channels[] list and therefore will not be 
  # displayed on index.html, and other users would only be able to access that
  # channel by manually typing the channel name & submitting a GET request as
  # well.
  if request.args.get('name'):
    print('======= pass ')
    session['channel_name'] = request.args.get('name')
    g.channel_name = request.args.get('name')

  # Make sure the user is logged in and is currently assigned to a channel.
  if g.username and g.channel_name:

    # Search all_message_data{} to pull relevant chat history and store in 
    # chat_history{}, which is -supposed- to contain up to the last 100 messages.
    # Use deepcopy because all_message_data{} stores the date as an integer in
    # miliseconds UNIX time, and here it is being reformatted as a more user-
    # friendly string to be displayed by each message in the chatroom (deepcopy
    # passes objects within objects by value, whereas regular copy does not).
    chat_history = {}
    for key in all_message_data:
      if all_message_data[int(key)]["channel_name"] == channel_name:
        chat_history[key] = copy.deepcopy(all_message_data[key])
    for key in chat_history:
      chat_history[key]['date'] = datetime.fromtimestamp(chat_history[key]['date'] / 1000.0).strftime('%m/%d/%Y, %H:%M:%S')
    
    print('===== channel_name =====: ', channel_name)
    print('===== chat_history =====: ', chat_history)
    
    return render_template("channel.html", channel_name=channel_name, chat_history=chat_history)
  else:
    return redirect(url_for("login"))

# ==================== LOGIN ========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

  # POST
  if request.method == "POST":

    # Check to see if username exists in global usernames[] list.
    for username in usernames:
      if username == request.form.get('username'):
        return render_template("login.html", error='Username already exists.')
    else:
      usernames.append(request.form.get('username'))
      session.pop('channel_name', None)
      session.pop('username', None)
      session['username'] = request.form.get('username')
      return redirect(url_for("index"))

  # GET
  else:
    return render_template("login.html")

# ==================== LOGOUT OF USERNAME & CHANNEL ==============================

@app.route("/logout")
def logout():

  # Since the usernames[] list is unordered, the 'count' variable is used to get 
  # the correct usernames[] index to delete.
  count = 0
  for username in usernames:
    if username == session['username']:
      del(usernames[count])
    count += 1
  session.pop('channel_name', None)
  session.pop('username', None)
  return redirect(url_for("login"))

# ==================== LOGOUT OF CHANNEL ========================================

@app.route("/logout_channel")
def logout_channel():
  session.pop('channel_name', None)
  return redirect(url_for("index"))

# ==================== LISTEN FOR CHATROOM MESSAGES =============================

@socketio.on("submit message")
def message(data):

  print('===== data =====: ', data)

  channel_name = data["channel_name"]
  date = data["date"]
  message = data["message"]
  username = data["username"]

  # The 'global message_id' statement allows the global message_id variable to be
  # modified/passed by reference instead of by value.
  global message_id
  message_id += 1

  # Add every message sent from every chatroom by every user into one large global
  # dictionary called all_message_data{}. The message_id variable is an arbitrary
  # number that serves as the key for each message.
  individual_message = { "channel_name": channel_name, "date": date, "message_id": message_id, "message": message, "username": username }
  all_message_data[message_id] = individual_message

  # The container_100 list contains the message_id and date (in milliseconds) for
  # each message in the current channel, and stores both values together as 
  # tuples. This list is ultimately used in the process of deleting old messages.
  container_100 = []
  for key in all_message_data:
    if all_message_data[key]["channel_name"] == channel_name:

      # container_100 is a list of tuples
      container_100.append((all_message_data[key]['message_id'], all_message_data[key]['date']))

  # The tuple with the minimum date value corresponds to the oldest message, and
  # its key is used to find and delete the corresponding message stored in the
  # all_message_data{} dictionary. The idea is the only retain the most recent
  # 100 messages per chatroom.
  if len(container_100) > 100:
    min_date = min(container_100, key=lambda x: x[1])[1]
    for tuple in container_100:
      if tuple[1] == min_date:
        min_date_key = tuple[0]
        del all_message_data[min_date_key]

  # Change the timestamp format for individual_message, aka messages that users
  # submit in chatrooms.
  individual_message_copy = individual_message.copy()
  individual_message_copy["date"] = datetime.fromtimestamp(individual_message["date"] / 1000.0).strftime('%m/%d/%Y, %H:%M:%S')

  # The first argument is customized so that the chat_history{} dictionary that is 
  # emitted is detected client-side only if the client-side user has the correct
  # channel_name. For example, the JavaScript code on the client's computer looks
  # like this:
  #
  #  socket.on('announce message' + ':' + channel_name, new_message => {...}
  #
  # ... so if their channel_name matches the channel_name here on the backend,
  # then they will receive, or "hear" the message.

  emit("announce message" + ":" + channel_name, individual_message_copy, broadcast=True)

if __name__ == "__main__":
  socketio.run(app)