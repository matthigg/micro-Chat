import json
import os
import requests
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

# Complete Channel Creation
# Complete Channel List
# Complete Messages View 
# Complete Sending Messages
# Complete Remembering the Channel
# Complete Personal Touch

channels = []

@app.before_request
def before_request():
  g.username = None
  if 'username' in session:
    g.username = session['username']

@app.route("/", methods=["GET", "POST"])
def index():
  # if g.username:
  #   if request.method == "POST":
  #     new_channel = request.form.get('new_channel')
  #     channels.append(new_channel)
  #     return redirect(url_for("channel"))
  #   else:
  #     return render_template("index.html", channels=channels)
  # else:
  #   return redirect(url_for("login"))

  if g.username:
    return render_template("index.html")
  else:
    return redirect(url_for("login"))

@app.route("/channel")
def channel():
  return render_template("channel.html")

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

@socketio.on("submit vote")
def vote(data):
  selection = data["selection"]
  emit("announce vote", {"selection": selection}, broadcast=True)