# __init__.py
# Rohan Weeden
# Created: July 3, 2017

# CTF scoreboard module

from flask import Blueprint


class CTFBlueprint(Blueprint):
    navbar_entry = "ctf/nav/navbar.html"
    navbar_extension = "ctf/nav/nav_extension.html"
    scripts = ["ctf.js"]
    stylesheets = ["ctf.css"]


mod = CTFBlueprint("ctf", __name__, url_prefix="/ctf", template_folder="templates", static_folder="static")

from . import controllers
