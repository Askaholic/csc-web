# controllers.py
# Rohan Weeden
# Created July 2, 2017

from . import app, ldap_server
from flask import render_template
from ldap3 import Connection, ALL


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/contact")
@app.route("/contact/")
def contact():
    return render_template("contact.html")


@app.route('/ldap')
def ldap():
    conn = Connection(ldap_server, 'uid=admin,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org', 'Secret123')
    conn.bind()
    conn.search('dc=demo1,dc=freeipa,dc=org', '(objectclass=person)', attributes=["memberOf", "password"])
    return str(conn.entries)
