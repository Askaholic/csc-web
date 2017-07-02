# app.py
# Rohan Weeden
# Created: July 2, 2017

# Main flask launch script

from app import app as application

if __name__ == "__main__":
    application.debug = True
    application.run()
