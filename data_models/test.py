# Testing module to test datamodels.

# Author: Jayant Arora
# Contributors: []
# Description: This file defines unit test for data model for the palsoncampus application.
# Date: Mon April 18 2017

import unittest
import sys
import datetime
sys.path.insert(1, '/home/jaror001/google-cloud-sdk/platform/google_appengine/')
sys.path.insert(1, '/home/jaror001/google-cloud-sdk/platform/google_appengine/lib/yaml/lib')
sys.path.insert(1, '/home/jaror001/files/spring2017/csc485Cloud/sdk/fork-palsoncampus/lib')

from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import testbed

import profile, post

class ProfileTest(unittest.TestCase):

    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        # Clear ndb's in-context cache between tests.
        # This prevents data from leaking between tests.
        # Alternatively, you could disable caching by
        # using ndb.get_context().set_cache_policy(False)
        ndb.get_context().clear_cache()

    def test_create_profile(self):
    	email = 'first@last.com'  
    	password = 'pass1'
    	firstName = 'first'
    	lastName = 'last' 
    	birthDate = datetime.date.today()
    	campus = 'SUNY Plattsburgh' 
    	newUser = profile.Profile.create_user(email=email, password=password, firstName=firstName, lastName=lastName, birthDate=birthDate, campus=campus)
    	self.assertTrue(newUser)

    def test_login_user(self):
    	### User test_create_profile to use data from previous method. ###
    	self.test_create_profile()
    	### end create user ###

        ### test with correct credentials ###
    	email = 'first@last.com'
    	password = 'pass1'
    	user = profile.Profile.login_user(email=email, password=password)
    	self.assertIsInstance(user, profile.Profile)
        ### end test with correct credentials ###

        ### test with incorrect email but correct password ###
        email = 'first@notlast.com'
        password = 'pass1'
        with self.assertRaises(profile.UserNotFoundError):
            profile.Profile.login_user(email=email, password=password)
        ### end test with incorrect email but correct password ###

        ### test with correct email but incorrect password ###
        email = 'first@last.com'
        password = 'pass34'
        with self.assertRaises(profile.PasswordIncorrectError):
            profile.Profile.login_user(email=email, password=password)
        ### end test with correct eamil but incorrect password ###

        ### test with incorrect email and incorrect password ###
        email = 'first@lastnot.com'
        password = 'pass123'
        with self.assertRaises(profile.UserNotFoundError):
            profile.Profile.login_user(email=email, password=password)
        ### end test with incorrect email and incorrect password ###

    	return user

    def test_update_pastCampus(self):
    	### login user first ###
    	user = self.test_login_user()
    	### end user login ###
    	newCampus = 'SUNY Albany'
    	self.assertEqual([], user.pastCampus)
    	profile.Profile.update_pastCampus(user, newCampus)
    	self.assertEqual('SUNY Albany', user.pastCampus[0].pastCampus)

    def test_update_hometown(self):
    	### login user ###
    	user = self.test_login_user()
    	### end user login ###
    	newHometown = 'Plattsburgh'
    	self.assertEqual(None, user.hometown)
    	profile.Profile.update_hometown(user, newHometown)
    	self.assertEqual(newHometown, user.hometown)

    def test_update_about(self):
        ### login User ###
        user = self.test_login_user()
        ### end login user ###
        about = "This is all about a person"
        self.assertEqual(None, user.about)
        profile.Profile.update_about(user, about)
        self.assertEqual(about, user.about)

    def test_update_gender(self):
        ### login user ###
        user = self.test_login_user()
        ### end login user ###

        ### test with gender as M == male ###
        gender = 'M'
        self.assertEqual(None, user.gender)
        profile.Profile.update_gender(user, gender)
        self.assertEqual(gender, user.gender)
        ### end male gender test ###

        ### test with gender as F == female ###
        gender = 'F'
        self.assertEqual('M', user.gender)
        profile.Profile.update_gender(user, gender)
        self.assertEqual(gender, user.gender)
        ### end female gender test ###

        ### test with gender as O == other ###
        gender = 'O'
        self.assertEqual('F', user.gender)
        profile.Profile.update_gender(user, gender)
        self.assertEqual(gender, user.gender)
        ### end other gender test ### 

        ### test with invalid gender ###
        gender = 'asdfj'
        with self.assertRaises(profile.GenderDoesNotExistError):
            profile.Profile.update_gender(user, gender)
        ### end test with invalid gender ###

    def test_update_phone(self):
        ### login user ###
        user = self.test_login_user()
        ### end login user ###

        ### test with correct phone number ###
        phone = 1234567890
        self.assertEqual(None, user.phone)
        profile.Profile.update_phone(user, phone)
        self.assertEqual(phone, user.phone)
        ### end test with correct phone number ###

        ### test with invalid length of phone number ###
        phone = 123456789123424
        with self.assertRaises(ValueError):
            profile.Profile.update_phone(user, phone)
        ### end test with invalid length of phoen number ###

        ### test with invlid type of phone number ###
        phone = 'hello'
        with self.assertRaises(TypeError):
            profile.Profile.update_phone(user, phone)
        ### end test with invlid type of phone number ###

    def tearDown(self):
    	self.testbed.deactivate()

class PostTest(unittest.TestCase):

    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        # Clear ndb's in-context cache between tests.
        # This prevents data from leaking between tests.
        # Alternatively, you could disable caching by
        # using ndb.get_context().set_cache_policy(False)
        ndb.get_context().clear_cache()

    def test_create_post(self):
        email = 'first@last.com'
        description = "This is a test post"
        postkey = post.Post.create_post(profileID=email, description=description, test=True)
        self.assertEqual(email, postkey.key.parent().id())
        self.assertEqual(description, postkey.description)
        return postkey

    def test_add_comment(self):
        # activate post
        newPost = self.test_create_post()
        # end activate post
        post.Post.add_comment(profileID='new@comment.com', post=newPost, comment='This is a test comment')
        self.assertEqual('new@comment.com', newPost.comments[0].profileID)
        self.assertEqual('This is a test comment', newPost.comments[0].comment)

    def tearDown(self):
        self.testbed.deactivate()

if __name__ == '__main__':
    unittest.main()
