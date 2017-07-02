# controllers.py
# Rohan Weeden
# Created July 2, 2017

from . import app
from flask import render_template

@app.route("/")
def index():
    mods = []
    for mod in app.iter_blueprints():
        mods.append({
            "href": mod.get_navbar_href(),
            "name": mod.get_navbar_name()
        })
    return render_template("base.html", modules=mods)
