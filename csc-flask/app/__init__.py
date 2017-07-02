# __init__.py
# Rohan Weeden
# Created: July 2, 2017

# Flask app module

from flask import Flask

app = Flask(__name__.split('.')[0])

from . import controllers
