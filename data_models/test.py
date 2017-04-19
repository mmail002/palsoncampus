# Testing module to test datamodels.

import unittest
import sys
import datetime
sys.path.insert(1, '/home/jaror001/google-cloud-sdk/platform/google_appengine/')
sys.path.insert(1, '/home/jaror001/google-cloud-sdk/platform/google_appengine/lib/yaml/lib')
sys.path.insert(1, '/home/jaror001/files/spring2017/csc485Cloud/sdk/fork-palsoncampus/lib')

from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import testbed
import profile

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
    	email = 'first@last.com'
    	password = 'pass1'
    	user = profile.Profile.login_user(email=email, password=password)
    	self.assertIsInstance(user, profile.Profile)
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

    def tearDown(self):
    	self.testbed.deactivate()

if __name__ == '__main__':
    unittest.main()
