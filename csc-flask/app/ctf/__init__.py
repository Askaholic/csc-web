# __init__.py
# Rohan Weeden
# Created: July 3, 2017

# CTF scoreboard module

from flask import Blueprint, url_for

class CTFBlueprint(Blueprint):
    def get_navbar_entry(self):
        return '<li><a href="{}">CTF</a></li>'.format(url_for('.index'))

mod = CTFBlueprint("ctf", __name__, url_prefix="/ctf", template_folder="templates")

from . import controllers
