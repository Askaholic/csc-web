# ctf.py
# Rohan Weeden
# Created: July 6, 2017

# Controllers for ctf functions

from .. import mod
from app import db
from .authentication import csrf_protected, logged_in
from .controllers import get_ctfs
from flask import abort, redirect, render_template, request, session, url_for
from .. import formatting
from ..models import CompleteFlag, CTF, Flag, User

HTTP_400_BAD_REQUEST = 400
HTTP_401_UNAUTHORIZED = 401
HTTP_403_FORBIDDEN = 403


@mod.route('/challenges')
@logged_in()
def challenges(user):
    is_admin = user.is_admin
    return render_template('ctf/challenges.html', challenges=get_ctfs(), is_admin=is_admin, csrf_token=session.get('csrf_token'))


@mod.route('/get_flags', methods=['GET', 'POST'])
@csrf_protected
@logged_in()
def get_flags(user):
    ctf_name = request.args.get('ctf')
    if ctf_name is None:
        abort(HTTP_400_BAD_REQUEST)
    ctf = CTF.query.filter_by(name=ctf_name).first()
    if ctf is None:
        abort(HTTP_400_BAD_REQUEST)
    complete_list = [flag.flag_id for flag in user.complete_flags]
    flags = []
    for flag in ctf.flags_active:
        d = formatting.flag_to_dict(flag)
        complete = False
        if flag.id in complete_list:
            complete = True
        d.update({"complete": complete})
        flags.append(d)
    return render_template("ctf/flags.html", ctf_name=ctf_name, ctf_description=ctf.description, flags=flags, is_admin=user.is_admin)


@mod.route('/submit_flag', methods=['GET', 'POST'])
@csrf_protected
@logged_in()
def submit_flag(user):
    flag_id = request.args.get("id")
    flag_key = request.args.get("flag")
    if flag_id is None or flag_key is None or not flag_id.isdigit():
        abort(HTTP_400_BAD_REQUEST)
    flag = Flag.query.filter_by(id=int(flag_id)).first()
    if flag is None:
        abort(HTTP_400_BAD_REQUEST)
    if flag.key == flag_key:
        cf = CompleteFlag(
            flag_id=flag.id
        )
        user.complete_flags.append(cf)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return "Database failure! Please contact an administrator."
        return ""
    else:
        abort(HTTP_400_BAD_REQUEST)


@mod.route('/createform')
@logged_in(is_admin=True)
def get_ctf_form(user):
    return render_template('ctf/admin/new_ctf.html', csrf_token=session.get('csrf_token'))


@mod.route('/createflag', methods=['GET'])
@logged_in(is_admin=True)
def get_flag_form(user):
    ctf_name = request.args.get('ctf')
    if ctf_name is None:
        abort(HTTP_400_BAD_REQUEST)
    return render_template('ctf/admin/new_flag.html', ctf_name=ctf_name, csrf_token=session.get('csrf_token'))


@mod.route('/editflag', methods=['GET', 'POST'])
@csrf_protected
@logged_in(is_admin=True)
def get_flag_edit_form(user):
    flag_id = request.args.get("id")
    if flag_id is None or not flag_id.isdigit():
        abort(HTTP_400_BAD_REQUEST)
    flag = Flag.query.filter_by(id=flag_id)
    if flag is None:
        abort(HTTP_400_BAD_REQUEST)
    return render_template('ctf/admin/edit_flag.html', csrf_token=session.get('csrf_token'), flag=formatting.flag_to_dict(flag))


@mod.route('/create', methods=['GET', 'POST'])
@csrf_protected
@logged_in(is_admin=True)
def create_ctf(user):
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

    return redirect(url_for("ctf.challenges"))


@mod.route('/add', methods=['GET', 'POST'])
@csrf_protected
@logged_in(is_admin=True)
def add_flag(user):
    ctf_name = request.form.get('ctf')
    if ctf_name is None:
        abort(HTTP_400_BAD_REQUEST)
    ctf = CTF.query.filter_by(name=ctf_name).first()
    if ctf is None:
        abort(HTTP_400_BAD_REQUEST)
    flag_name = request.form.get('name')
    if flag_name is None:
        return "Flag name is required!"
    flag_key = request.form.get('flag')
    if flag_key is None:
        return "Flag is required!"
    flag_desc = request.form.get('desc')
    flag_hint = request.form.get('hint')
    newFlag = Flag(
        name=flag_name,
        key=flag_key,
        description=flag_desc,
        hint=flag_hint
    )
    ctf.flags.append(newFlag)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return "Database failure! Please contact an administrator."
    return redirect(url_for("ctf.challenges"))


@mod.route('/edit', methods=['GET', 'POST'])
@csrf_protected
@logged_in(is_admin=True)
def edit_flag(user):
    flag_id = request.form.get("id")
    if flag_id is None:
        abort(HTTP_400_BAD_REQUEST)
    flag_name = request.form.get("name")
    flag_key = request.form.get("flag")
    flag_desc = request.form.get("desc")
    flag_hint = request.form.get("hint")
    flag = Flag.query.filter_by(id=flag_id).first()
    if flag is None:
        abort(HTTP_400_BAD_REQUEST)
    flag.name = flag_name
    flag.key = flag_key
    flag.desc = flag_desc
    flag.hint = flag_hint
    return ""
