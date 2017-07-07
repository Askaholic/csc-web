# ctf.py
# Rohan Weeden
# Created: July 6, 2017

# Controllers for ctf functions

from .. import mod
from app import db
from .authentication import csrf_protected, csrf_token
from .controllers import get_ctfs
from flask import abort, render_template, request, session
from ..models import CTF, User


@mod.route('/challenges')
def challenges():
    is_admin = False
    if "user" in session:
        user = User.query.filter_by(username=session['user']).first()
        is_admin = user.is_admin
        print("User is_admin {}".format(is_admin))
    return render_template('ctf/challenges.html', challenges=get_ctfs(), is_admin=is_admin)


@mod.route('/createform')
@csrf_token
def get_ctf_form(token):
    return render_template('ctf/new_ctf.html', csrf_token=token)


@mod.route('create', methods=['GET', 'POST'])
@csrf_protected
def create_ctf():
    if "user" in session:
        user = User.query.filter_by(username=session['user']).first()
        if user is None or user.is_admin is False:
            abort(403)
        else:
            name = request.form.get('name')
            desc = request.form.get('desc', "")
            if name is None:
                return "A name is required"
            else:
                newCTF = CTF(
                    name=name,
                    description=desc
                )
                db.session.add(newCTF)
                try:
                    db.session.commit()
                except:
                    db.session.rollback()
                    return "Database failure! Please contact an administrator."
    else:
        abort(401)

    return challenges()
