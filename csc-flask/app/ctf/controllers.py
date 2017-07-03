# controllers.py
# Rohan Weeden
# Created: July 3, 2017

# Controllers for pages in ctf module

from . import mod
from app import db, socketio
import base64
import bcrypt
from flask import render_template, request, session
import hashlib
from .models import CTF, User


def get_ctfs():
    ctfs = []
    for ctf in CTF.query.all():
        ctfs.append({
            "name": ctf.name
        })
    return ctfs


@mod.route('/')
def index():
    return ""


@mod.route('/login', methods=['GET', 'POST'])
def login():
    user = session.get("user")
    if user is not None:
        return render_template("ctf/loggedin.html", username=user)
    else:
        user = request.args.get("user")
        pasw = request.args.get("pass")

        if pasw is not None:
            # Hash password (sha256 to make sure password length does not exceed 72)
            hashed = bcrypt.hashpw(
                base64.b64encode(hashlib.sha256(pasw.encode()).digest()),
                bcrypt.gensalt()
            )
    return render_template('ctf/login.html')


@mod.route('/challenges')
def challenges():
    return render_template('ctf/challenges.html', challenges=get_ctfs())


@mod.route('/scoreboard')
def scoreboard():
    return render_template('ctf/scoreboard.html', challenges=get_ctfs())


@socketio.on('my event')
def handle_message(data):
    print('Received message: ' + str(data))
