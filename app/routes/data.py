from sys import getprofile
from tokenize import String
from typing import KeysView
from xmlrpc.client import Boolean

from setuptools import SetuptoolsDeprecationWarning
from app import app
from flask import flash
from flask_login import UserMixin
from mongoengine import Document, StringField, FileField, EmailField,  CASCADE
from flask_mongoengine import Document
import datetime as dt
import jwt
from time import time
from bson.objectid import ObjectId



class User(UserMixin, Document):
    gid = StringField(sparse=True, unique=True)
    gname = StringField()
    gprofile_pic = StringField()
    username = StringField()
    fname = StringField()
    lname = StringField()
    email = EmailField()
    image = FileField()
    prononuns = StringField()
    adult_fname = StringField()
    adult_lname = StringField()
    adult_email = StringField()

    meta = {
        'ordering': ['lname','fname']
    }


class MathTopic(Document):
    math_level = StringField('Math Level', choices=[('algebra1', 'Algebra 1', ('algebra2', 'Algebra 2'),('geometry', 'Geometry'), ('precalculus', 'Pre Calculus'), ('stats', 'Statistics'))])
    practice_problem_one = StringField()
    practice_problem_two= StringField()
    practice_problem_three = StringField()
    solution_one = StringField()
    solution_two = StringField()
    solution_three = StringField()
    topic_name = StringField()
    tutorial_video = FileField()
