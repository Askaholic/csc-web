# controllers.py
# Rohan Weeden
# Created: July 3, 2017

# Controllers for pages in ctf module

from . import mod
from flask import render_template

@mod.route('/')
def index():
    return render_template('ctf/index.html')
