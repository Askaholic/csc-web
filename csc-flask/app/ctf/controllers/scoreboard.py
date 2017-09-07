# scoreboard.py
# Rohan Weeden
# Created: June 15, 2017

# Controllers having to do with the scoreboard

from .. import mod
from .authentication import logged_in
from .controllers import get_ctfs
from flask import render_template
from ..models import CompleteFlag, CTF, Flag, User


@mod.route('/scoreboard')
@mod.route('/scoreboard/<challenge_name>')
@logged_in()
def scoreboard(user, challenge_name=None):
    context_info = {}
    if challenge_name is not None:
        context_info = get_score_info(challenge_name)
    return render_template('ctf/scoreboard.html', **context_info, challenges=get_ctfs())


def get_score_info(ctf_name):
    ctf = CTF.query.filter_by(name=ctf_name).first()
    if ctf is None:
        return {}
    info = {}
    for flag in ctf.flags_active:
        for cf in flag.complete_flags:
            user_name = cf.user.username
            points = cf.flag.points
            if user_name in info:
                points += info[user_name]
            info.update({user_name: points})
    users = []
    for name in info:
        users.append({
            "name": name,
            "points": info[name]
        })
    sorted_users = sorted(users, reverse=True, key=lambda x: x['points'])
    return {"ctf_name": ctf_name, "ctf_description": ctf.description, "sorted_users": sorted_users}
