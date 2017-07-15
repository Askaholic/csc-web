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

    flag = db.relationship("Flag")


class CTF(db.Model):
    __tablename__ = "ctfs"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    description = db.Column(db.Text)

    flags = db.relationship("Flag")
    flags_active = db.relationship("Flag", primaryjoin="and_(CTF.id==Flag.ctf_id, Flag.is_active==true)")


class Flag(db.Model):
    __tablename__ = "flags"

    id = db.Column(db.Integer, primary_key=True)
    ctf_id = db.Column(db.Integer, db.ForeignKey("ctfs.id"))
    name = db.Column(db.Text, nullable=False, unique=True)
    key = db.Column(db.Text, nullable=False)
    points = db.Column(db.Integer, nullable=False, server_default="1", default=1)
    description = db.Column(db.Text)
    hint = db.Column(db.String)
    is_active = db.Column(db.Boolean, nullable=False, server_default="T", default=True)

    ctf = db.relationship("CTF", back_populates="flags")


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, server_default="true", default=True)
    is_admin = db.Column(db.Boolean, nullable=False, server_default="false", default=False)

    complete_flags = db.relationship("CompleteFlag")
