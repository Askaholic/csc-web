# controllers.py
# Rohan Weeden
# Created: July 2, 2017

# Controllers for test module

from flask import Blueprint, render_template, url_for

class TestMod(Blueprint):
    def get_navbar_extension(self):
        return '''<form class="navbar-form navbar-right">
                    <div class="input-group">
                        <input type="text" class="form-control" placeholder="Search">
                        <div class="input-group-btn">
                            <button class="btn btn-default" type="submit">
                                <i class="glyphicon glyphicon-search"></i>
                            </button>
                        </div>
                    </div>
                </form>'''

mod = TestMod('test', __name__, url_prefix='/test')

@mod.route('/')
def index():
    pass
