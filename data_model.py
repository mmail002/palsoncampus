# shebang line:  #! /usr/bin/env python

# Author: Jayant Arora
# Contributors: []
# Description: This file defines the data model for the palsoncampus application.
# Date: Mon April 3 2017

### TODO
	# 1. Convert password to hash64 -- md5?
	# 2. Generate a random salt to append to the password.
	# 4. Limit about to 255 characters. -- ComputedProperty maybe?
	# 6. Hometown API integration
	# 7. Define StructuredProperty for interests.
	# 8. Define StructuredProperty for likedPages.

### DONE
	# 3. Make StructuredProperty for past campuses.
	# 5. Define StructuredProperty for uploadedPictures.



from google.appengine.ext import ndb

class PastCampus(ndb.Model):
	pastCampus = ndb.StringProperty() # ID in string format.

class UploadedPictures(ndb.Model):
	picture = ndb.StringProperty() # store url to the image. 
	public = ndb.BooleanProperty() # Is the picture available to public or not?

class Profile(ndb.Model):
	profileID = ndb.KeyProperty(required = True)
	email = ndb.StringProperty(required = True)
	nickName = ndb.StringProperty()

	password = ndb.StringProperty(required = True) # TODO Needs to have salt added to it and the converted to hash64
	salt = ndb.StringProperty() # TODO this will generate a random value that will be appended to the password to make it strong. 

	firstName = ndb.StringProperty(required = True)
	lastName = ndb.StringProperty(required = True)
	birthDate = ndb.DateProperty(required = True)
	status = ndb.BooleanProperty(required = True) # Shows inactive or active -- false or true respectively
	public = ndb.BooleanProperty() # True if profile is public and false is not.
	campus = ndb.StringProperty(required = True) # This will store key from the collegeScorecard db and will referenced as such. 
	pastCampus = ndb.StructuredProperty(PastCampus, repeated = True)

	howetown = ndb.StringProperty() # TODO TEMPORARY until we have an API
	about = ndb.StringProperty() # Something about yourself - Limit for 255 chr still needed.

	profilePicture = ndb.StringProperty() # this will store the url for the profile picture.
	uploadedPictures = ndb.StructuredProperty(UploadedPictures, repeated = True)
	
	interests = ndb.StructuredProperty() # TODO
	likedPages = ndb.StructuredProperty() # TODO
	campusInvolvement = ndb.StructuredProperty() # TODO
	gender = ndb.StructuredProperty() # TODO
	phone = ndb.IntegerProperty()

