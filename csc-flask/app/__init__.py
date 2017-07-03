# __init__.py
# Rohan Weeden
# Created: July 2, 2017

# Flask app module

from flask import Flask, render_template
# from flask_simpleldap import LDAP
from flask_socketio import SocketIO
from jinja2 import Environment, FileSystemLoader
import os


app = Flask(__name__.split('.')[0])
socketio = SocketIO(app)

app.config['LDAP_BASE_DN'] = 'OU=users,dc=csc,dc=uaf,dc=edu'
app.config['LDAP_USERNAME'] = 'CN=user,OU=Users,DC=csc,DC=uaf,DC=edu'
app.config['LDAP_PASSWORD'] = 'password'

# ldap = LDAP(app)

from .ctf import mod as mod_ctf
app.register_blueprint(mod_ctf)

from . import controllers


# generate the layout.html template based on which modules are installed
@app.before_first_request
def create_layout_template():
    template_folder = os.path.join(os.path.dirname(__file__), app.template_folder)
    env = Environment(loader=FileSystemLoader(template_folder))
    template = env.get_template("base.html")

    # Create the dictionary of installed mods menu items
    mods = []
    for mod in app.iter_blueprints():
        mods.append({
            "name": mod.name,
            "nav_entry": mod.get_navbar_entry() if hasattr(mod, "get_navbar_entry") else "",
            "nav_extension" : mod.get_navbar_extension() if hasattr(mod, "get_navbar_extension") else ""
        })
    with open(os.path.join(template_folder, "layout.html"), "w") as layout_template_file:
        layout_template_file.write(template.render(modules=mods))
