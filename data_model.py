# shebang line:  #! /usr/bin/env python

# Author: Jayant Arora
# Contributors: 
# Description: This file defines the data model for the palsoncampus application.
# Date: Mon April 3 2017

### TODO
	# 1. Convert password to hash64 -- md5?
	# 2. Generate a random salt to append to the password.
	# 3. Make StructuredProperty for past campuses.
	# 4. Limit about to 255 characters. -- ComputedProperty maybe?
	# 5. Define StructuredProperty for uploadedPictures.

from google.appengine.ext import ndb

class Profile(ndb.Model):
	profileID = ndb.KeyProperty(required = True)
	email = ndb.StringProperty(required = True)
	nickName = ndb.StringProperty()

	password = ndb.StringProperty(required = True) # Needs to have salt added to it and the converted to hash64
	salt = ndb.StringProperty() # this will generate a random value that will be appended to the password to make it strong. 

	firstName = ndb.StringProperty(required = True)
	lastName = ndb.StringProperty(required = True)
	birthDate = ndb.DateProperty(required = True)

	status = ndb.BooleanProperty(required = True) # Shows inactive or active -- false or true respectively
	public = ndb.BooleanProperty()

	campus = ndb.StringProperty(required = True) # This will store key from the collegeScorecard db and will referenced as such. 
	pastCampus = ndb.StructuredProperty()
	howetown = ndb.StringProperty() # TEMPORARY until we have an API
	about = ndb.StringProperty() # Something about yourself - Limit for 255 chr still needed.
	profilePicture = ndb.StringProperty() # this will store the url for the profile picture.

	uploadedPictures = ndb.StructuredProperty() # TODO
	interests = ndb.StructuredProperty() # TODO
	likedPages = ndb.StructuredProperty() # TODO
	campusInvolvement = ndb.StructuredProperty() # TODO
	gender = ndb.StructuredProperty() # TODO
	phone = ndb.IntegerProperty()

