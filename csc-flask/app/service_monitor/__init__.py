# __init__.py
# Rohan Weeden
# Created: July 18, 2017

# Service Monitor module. Provides a scoreboard showing which of CSC's services
# are up.

from flask import Blueprint


class CTFBlueprint(Blueprint):
    navbar_entry = "monitor/nav/navbar.html"
    navbar_extension = "monitor/nav/nav_extension.html"


mod = CTFBlueprint("monitor", __name__, url_prefix="/monitor", template_folder="templates", static_folder="static")

from . import controllers
