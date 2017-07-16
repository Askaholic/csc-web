# scoreboard.py
# Rohan Weeden
# Created: June 15, 2017

# Controllers having to do with the scoreboard

from .. import mod
from .authentication import logged_in
from .controllers import get_ctfs
from flask import render_template


@mod.route('/scoreboard')
@mod.route('/scoreboard/<challenge_name>')
@logged_in()
def scoreboard(user, challenge_name=None):
    context_info = {}
    if challenge_name is not None:
        context_info = {
            "ctf_name": challenge_name
        }
    return render_template('ctf/scoreboard.html', **context_info, challenges=get_ctfs())
