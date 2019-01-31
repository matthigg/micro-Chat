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

channels = []

@app.before_request
def before_request():
  g.username = None
  if 'username' in session:
    g.username = session['username']

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

@app.route("/channel/<string:channel_name>")
def channel(channel_name):
  return render_template("channel.html", channel_name=channel_name)

@app.route("/login", methods=["GET", "POST"])
def login():
  if request.method == "POST":
    session.pop('username', None)
    session['username'] = request.form.get('username')
    return redirect(url_for("index"))
  else:
    return render_template("login.html")

@app.route("/logout")
def logout():
  session.pop('username', None)
  return redirect(url_for("login"))

@socketio.on("submit message")
def message(data):
  selection = data["message"]
  emit("announce message", {"message": selection}, broadcast=True)