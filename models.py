
import datetime

from google.appengine.api import memcache
from google.appengine.api import users
from google.appengine.ext import db

class User(db.Model):
    username = db.TextProperty()
    email = db.TextProperty()
    password = db.TextProperty()
    joined_at = db.DateTimeProperty(datetime.datetime.now)
    is_admin = db.BooleanProperty(default=False)


def initialize():
    null
