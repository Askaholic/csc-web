# __init__.py
# Rohan Weeden
# Created: July 2, 2017

# Flask app module

from flask import Flask
# from flask_simpleldap import LDAP
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from jinja2 import Environment, FileSystemLoader
from ldap3 import Server
import os
import uuid


app = Flask(__name__.split('.')[0])
app.config.from_json("../config.json")
if app.secret_key is None:
    app.secret_key = uuid.uuid4().hex


db = SQLAlchemy(app)
socketio = SocketIO(app)
ldap_server = Server(app.config["LDAP_SERVER"], use_ssl=True)

from .ctf import mod as mod_ctf
app.register_blueprint(mod_ctf)

from app import controllers
from .ctf.models import *
db.create_all()


# generate the layout.html template based on which modules are installed
@app.before_first_request
def create_layout_template():
    template_folder = os.path.join(os.path.dirname(__file__), app.template_folder)
    env = Environment(loader=FileSystemLoader(template_folder))
    template = env.get_template("base.html")

    # Create the dictionary of installed mods menu items
    mods = []
    for mod in app.iter_blueprints():
        mod_dict = {
            "name": mod.name
        }
        if hasattr(mod, "navbar_entry"):
            mod_dict.update({
                "nav_entry": mod.navbar_entry
            })
        if hasattr(mod, "navbar_extension"):
            mod_dict.update({
                "nav_extension": mod.navbar_extension
            })
        if hasattr(mod, "scripts"):
            mod_dict.update({
                "scripts": mod.scripts
            })
        if hasattr(mod, "stylesheets"):
            mod_dict.update({
                "stylesheets": mod.stylesheets
            })
        mods.append(mod_dict)
    with open(os.path.join(template_folder, "layout.html"), "w") as layout_template_file:
        layout_template_file.write(template.render(modules=mods))
