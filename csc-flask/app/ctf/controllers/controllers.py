# controllers.py
# Rohan Weeden
# Created: July 3, 2017

# Controllers for pages in ctf module

from .. import mod
from app import socketio
from flask import render_template
from ..models import CTF


def get_ctfs():
    ctfs = []
    for ctf in CTF.query.all():
        ctfs.append({
            "name": ctf.name
        })
    return ctfs


@mod.route('/')
def index():
    return ""


@socketio.on('my event')
def handle_message(data):
    print('Received message: ' + str(data))
