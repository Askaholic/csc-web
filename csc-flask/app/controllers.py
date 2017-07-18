# controllers.py
# Rohan Weeden
# Created July 2, 2017

from . import app
from flask import render_template


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/contact")
@app.route("/contact/")
def contact():
    return render_template("contact.html")
#
# @app.route('/ldap')
# @ldap.login_required
# def ldap_protected():
#     return 'Success!'
