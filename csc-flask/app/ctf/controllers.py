# controllers.py
# Rohan Weeden
# Created: July 3, 2017

# Controllers for pages in ctf module

from . import mod
from app import socketio
from flask import render_template

@mod.route('/')
def index():
    return ""

@mod.route('/login')
def login():
    return render_template('ctf/login.html')

@mod.route('/challenges')
def challenges():
    challenges = [
        {"name": "Dope-CTF"},
        {"name": "Cyber"}
    ]
    return render_template('ctf/challenges.html', challenges=challenges)

@mod.route('/scoreboard')
def scoreboard():
    challenges = [
        {"name": "Dope-CTF"},
        {"name": "Cyber"}
    ]
    return render_template('ctf/scoreboard.html', challenges=challenges)

@socketio.on('my event')
def handle_message(data):
    print('Received message: ' + str(data))
