# __init__.py
# Rohan Weeden
# Created: July 2, 2017

# Flask app module

from flask import Flask

app = Flask(__name__.split('.')[0])

from .test.controllers import mod as mod_test
app.register_blueprint(mod_test)

from . import controllers
