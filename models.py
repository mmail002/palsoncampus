# Author: Naz-Al Islam
# Contributors: []
# Description: User datamodel for palsoncampus application
# Date: Apr 10, 2017


import datetime

from google.appengine.api import memcache
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import ndb

class User(ndb.Model):
    username = ndb.StringProperty()
    email = ndb.StringProperty()
    password = ndb.StringProperty()
    joined_at = ndb.DateTimeProperty() 
    updated_at = ndb.DateTimeProperty() 
    is_admin = ndb.BooleanProperty(default=False)

    #flask-login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    @classmethod
    def create_user(cls, username, email, password, is_admin=False):

        user = User(id=username, username=username, email=email, password=password, is_admin=is_admin, joined_at=datetime.datetime.now())

	user.put()
        return user

    @classmethod
    def exists(cls, username):

        k = ndb.Key('User', username)
  
        user = k.get()

        return user

    @classmethod
    def update_user(cls, username, email, password, admin):

        k = ndb.Key('User', username)
  
        user = k.get()
        user.username=username
	user.email=email
	user.password=password
	user.is_admin=admin
        user.updated_at=datetime.datetime.now()

	user.put()

        return user

    @classmethod
    def delete_user(cls, username):

        k = ndb.Key('User', username)
  
        k.delete()


def initialize():
    null


