# controllers.py
# Rohan Weeden
# Created: July 2, 2017

# Controllers for test module

from flask import Blueprint, url_for

class TestMod(Blueprint):
    def get_navbar_entry(self):
        return '<li><a href="{}">Test</a></li>'.format(url_for("test.index"))

mod = TestMod('test', __name__, url_prefix='/test')

@mod.route('/')
def index():
    pass
