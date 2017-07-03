# models.py
# Rohan Weeden
# Created: July 3, 2017

# Declare the database models needed for the ctf module

from app import db


class CompleteFlag(db.Model):
    __tablename__ = "complete_flags"

    id = db.Column(db.Integer, primary_key=True)
    flag_id = db.Column(db.Integer, db.ForeignKey("flags.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    flag = db.relationship("Flag", backref=db.backref("flags", lazy="dynamic"))
    user = db.relationship("User", backref=db.backref("users", lazy="dynamic"))


class CTF(db.Model):
    __tablename__ = "ctfs"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)


class Flag(db.Model):
    __tablename__ = "flags"

    id = db.Column(db.Integer, primary_key=True)
    ctf_id = db.Column(db.Integer, db.ForeignKey("ctfs.id"))
    name = db.Column(db.Text, nullable=False)
    key = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    hint = db.Column(db.String)
    active = db.Column(db.Boolean, nullable=False, server_default="T", default="T")

    ctf = db.relationship("CTF", backref=db.backref("ctfs", lazy="dynamic"))


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    active = db.Column(db.Boolean, nullable=False, server_default="T", default="T")
    admin = db.Column(db.Boolean, nullable=False, server_default="F", default="F")
