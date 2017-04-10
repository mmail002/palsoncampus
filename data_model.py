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

### DONE
	# 3. Make StructuredProperty for past campuses.
	# 5. Define StructuredProperty for uploadedPictures.
	# 7. Define StructuredProperty for interests.
	# 8. Define StructuredProperty for likedPages.
	# 9. Define StructuredProperty for campusInvolvement.

from google.appengine.ext import ndb

class PastCampus(ndb.Model):
	pastCampus = ndb.StringProperty() # ID in string format.

class UploadedPictures(ndb.Model):
	picture = ndb.StringProperty() # store url to the image. 
	public = ndb.BooleanProperty() # Is the picture available to public or not?

class Interests(ndb.Model):
	interest = ndb.StringProperty()

class LikedPages(ndb.Model):
	page = ndb.StringProperty() # store ID for the page. Might be changed to KeyProperty

class CampusInvolvement(ndb.Model):
	name = ndb.StringProperty()
	start_date = ndb.DateTimeProperty()
	end_date = ndb.DateTimeProperty()

class Profile(ndb.Model):
	# No need to set up a key, google datastore already does that in key.id() field.
	email = ndb.StringProperty(required = True)	# In the mean time use this as key.
	nickName = ndb.StringProperty()

	password = ndb.StringProperty(required = True) # TODO Needs to have salt added to it and the converted to hash64
	salt = ndb.StringProperty() # TODO this will generate a random value that will be appended to the password to make it strong. 

	firstName = ndb.StringProperty(required = True)
	lastName = ndb.StringProperty(required = True)
	birthDate = ndb.DateProperty(required = True)
	status = ndb.BooleanProperty(required = True) # Shows inactive or active -- false or true respectively
	public = ndb.BooleanProperty(required = True) # True if profile is public and false is not.
	campus = ndb.StringProperty(required = True) # This will store key from the collegeScorecard db and will referenced as such. 
	pastCampus = ndb.StructuredProperty(PastCampus, repeated = True)

	hometown = ndb.StringProperty() # TODO TEMPORARY until we have an API
	about = ndb.StringProperty() # Something about yourself - Limit for 255 chr still needed.

	profilePicture = ndb.StringProperty() # this will store the url for the profile picture.
	uploadedPictures = ndb.StructuredProperty(UploadedPictures, repeated = True)
	interests = ndb.StructuredProperty(Interests, repeated = True)
	likedPages = ndb.StructuredProperty(LikedPages, repeated = True)
	campusInvolvement = ndb.StructuredProperty(CampusInvolvement, repeated = True)

	gender = ndb.StringProperty() # Changed to string. Should be handled via form validation. 
	phone = ndb.IntegerProperty()

	############ Class methods go here ###########

	@classmethod
	def create_user(cls, email, nickName=None, password, firstName, lastName, birthDate, status=True, public=True, campus, pastCampus=None, hometown=None, about=None, profilePicture=None, uploadedPictures=None, interests=None, likedPages=None, campusInvolvement=None, gender=None, phone=None):
		'''
			Saves user information to db.

			Args:
				email: email from the user. Must be of type abc@xyz.com
				nickName: user's nickname. Type string. Default None.
				password: set as string. Required.
				firstName: string. Required
				lastName: strign. Requried
				birthDate: type data: Check dataProperty for info. Required
				status: Active or Inactive -- True/False. Default True. should not be modified.
				public: True/False: User can set its profile to be public/private. Default: True
				campus: ID of the campus where user belongs to. Refer to collegescorecard ID. Required.
				pastCampus: if user has been associated with past campuses. Should not be set here. User other function to set pastCampus. Do not modify.
				hometown: Location as a string. [Temporary]. 
				about: About user. Restrict this to 300 words. Restriction recommended, not necessary
				profilePicture: store url of profile pic. Upload not handled here.
				uploadedPictures: store url's of images. Upload not handled here.
				likedPages: ID of pages liked by user. Do not modify. Like is not handled here. 
				campusInvolvement: DO not modify. Not handled here.
				gender: Set this as a string of atmost one char. 'M', 'F' or 'O'
				phone: User's phone number. Type check required.

		'''
		user = Profile(email=email, nickName=nickName, password=password, firstName=firstName, lastName=lastName, birthDate=birthDate, status=status, public=public, campus=campus, pastCampus=pastCampus, hometown=hometown, about=about, profilePicture=profilePicture, uploadedPictures=uploadedPictures, interests=interests, likedPages=likedPages, campusInvolvement=campusInvolvement, gender=gender, phone=phone)
		user.put()
		return True

