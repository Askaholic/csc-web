# login.py
# Rohan Weeden
# Created: July 6, 2017

# Controllers for authentication functions

from .. import mod
from app import db
import base64
import bcrypt
from flask import abort, redirect, render_template, request, session, url_for
import hashlib
from ..models import User
import random
import string


# Decorator for making a function protected from CSRF
def csrf_protected(func):
    def wrapper():
        if "csrf_token" not in session or "key" not in request.form or session['csrf_token'] != request.form['key']:
            abort(400)
        else:
            return func()

    wrapper.__name__ = func.__name__
    return wrapper


def set_csrf_token():
    token = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(32))
    session['csrf_token'] = token


def is_valid_username(username):
    if len(username) > 30:
        return False
    return True


def get_username_chars_message():
    return "Usernames must be less than 30 characters and only contain letters, numbers, and underscores."


@mod.route('/makeadmin')
def makeadmin():
    User.query.filter_by(username=session['user']).first().is_admin = True
    db.session.commit()
    print("Is admin " + str(User.query.filter_by(username=session['user']).first().is_admin))
    return "It's been done"


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
            elif not is_valid_username(user):
                error = "That username is invalid! {}".format(get_username_chars_message())
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

                    set_csrf_token()
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
                    set_csrf_token()
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
    return redirect(url_for("ctf.login"))
