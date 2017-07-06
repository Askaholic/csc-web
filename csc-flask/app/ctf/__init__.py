# __init__.py
# Rohan Weeden
# Created: July 3, 2017

# CTF scoreboard module

from flask import Blueprint, url_for


class CTFBlueprint(Blueprint):
    def get_navbar_entry(self):
        navbar_entry = '''
        <li class="dropdown">
            <a class="dropdown-toggle" data-toggle="dropdown" href="#">CTF
                <span class="caret"></span>
            </a>
            <ul class="dropdown-menu">
                <li><a href="{}">Login</a></li>
                <li><a href="{}">Challenges</a></li>
                <li><a href="{}">Scoreboard</a></li>

            </ul>
        </li>
        '''.format(url_for("ctf.login"), url_for("ctf.challenges"), url_for("ctf.scoreboard"))
        return navbar_entry

    def get_script(self):
        return "ctf.js"


mod = CTFBlueprint("ctf", __name__, url_prefix="/ctf", template_folder="templates", static_folder="static")

from . import controllers
