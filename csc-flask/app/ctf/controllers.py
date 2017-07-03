# controllers.py
# Rohan Weeden
# Created: July 3, 2017

# Controllers for pages in ctf module

from . import mod
from flask import render_template

@mod.route('/')
def index():
    return ""

@mod.route('/login')
def login():
    return render_template('ctf/login.html')

@mod.route('/challenges')
def challenges():
    return ""

@mod.route('/scoreboard')
def scoreboard():
    return ""
