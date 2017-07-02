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
            "nav_entry": mod.get_navbar_entry()
        })
        print("Adding: {}".format(mod.get_navbar_entry()))
    return render_template("index.html", modules=mods)
