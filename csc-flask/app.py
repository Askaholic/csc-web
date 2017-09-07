# app.py
# Rohan Weeden
# Created: July 2, 2017

# Main flask launch script

from app import socketio, app
app.debug = True

if __name__ == "__main__":
    app.debug = True
    socketio.run(app)
