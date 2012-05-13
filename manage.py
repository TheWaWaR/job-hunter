#!/usr/bin/env python
#coding=utf-8

from flask import Flask, current_app
from flaskext.script import Command, Manager, Server, Shell, prompt_bool

from hunt import create_app
from hunt.extensions import db

manager = Manager(create_app('configure.cfg'))
manager.add_command('runserver', Server('127.0.0.1', port=9999))

def _make_context():
    return dict(db=db)
manager.add_command('shell', Shell(make_context=_make_context))

@manager.command
def createall():
    db.create_all()

@manager.command
def dropall():
    if prompt_bool("Are you sure ? You will lose all your data !"):
        db.drop_all()

if __name__ == '__main__':
    manager.run()
