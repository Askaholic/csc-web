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
            "nav_entry": mod.get_navbar_entry() if hasattr(mod, "get_navbar_entry") else "",
            "nav_extension" : mod.get_navbar_extension() if hasattr(mod, "get_navbar_extension") else ""
        })
    return render_template("index.html", modules=mods)
