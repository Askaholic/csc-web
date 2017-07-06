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
    error = None
    if user is not None:
        return render_template("ctf/loggedin.html", username=user)
    elif request.method == "POST":
        create = request.form.get("create")
        user = request.form.get("user")
        pasw = request.form.get("pass")
        conf = request.form.get("conf")

        if pasw is None or pasw == "":
            error = "Password must not be empty!"
        elif create == "on":
            if User.query.filter_by(username=user).first() is not None:
                error = "That username is taken!"
            elif pasw != conf:
                error = "Your passwords do not match!"
            else:
                # Hash password (sha256 to make sure password length does not exceed 72)
                hash = bcrypt.hashpw(
                    base64.b64encode(hashlib.sha256(pasw.encode()).digest()),
                    bcrypt.gensalt()
                )
                newUser = User(
                    username=user,
                    password=hash.decode()
                )
                db.session.add(newUser)
                try:
                    db.session.commit()
                    session['user'] = user
                    return render_template("ctf/loggedin.html")
                except:
                    db.session.rollback()
                    error = "Database failure! Please contact an administrator."
                    raise
        elif create is False or create is None:
            # Check hash
            db_user = User.query.filter_by(username=user).first()
            if db_user is None:
                error = "Login failed, please try again."
            elif bcrypt.checkpw((hashlib.sha256(pasw.encode(), db_user.hash))):
                if db_user.is_active is True:
                    session['user'] = user
                    return render_template("ctf/loggedin.html")
                else:
                    error = "Login falied, your account is not active. Please contact an administrator."
            else:
                error = "Login failed, please try again."
    if error is not None:
        return render_template('ctf/login.html', error=error)
    else:
        return render_template('ctf/login.html')


@mod.route('/logout')
def logout():
    session.clear()
    return "You've been logged out"


@mod.route('/challenges')
def challenges():
    is_admin = False
    if "username" in session:
        user = User.query.filter_by(username=session['username']).first()
        is_admin = user.is_admin
    return render_template('ctf/challenges.html', challenges=get_ctfs(), is_admin=is_admin)


@mod.route('/scoreboard')
def scoreboard():
    return render_template('ctf/scoreboard.html', challenges=get_ctfs())


@socketio.on('my event')
def handle_message(data):
    print('Received message: ' + str(data))
