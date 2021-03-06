# shebang line:  #! /usr/bin/env python

# Author: Jayant Arora
# Contributors: []
# Description: This file defines the PROFILE data model for the palsoncampus application.
# Date: Mon April 3 2017

### TODO
	# 2. Generate a random salt to append to the password.
	# 4. Limit about to 255 characters. -- ComputedProperty maybe?
	# 6. Hometown API integration

### DONE
	# 3. Make StructuredProperty for past campuses.
	# 5. Define StructuredProperty for uploadedPictures.
	# 7. Define StructuredProperty for interests.
	# 8. Define StructuredProperty for likedPages.
	# 9. Define StructuredProperty for campusInvolvement.
	# 1. Convert password to hash64 -- md5?

from google.appengine.ext import ndb
import hashlib

class UserAlreadyExistsError(Exception):
	pass

class UserNotFoundError(Exception):
	pass

class PasswordIncorrectError(Exception):
	pass

class GenderDoesNotExistError(Exception):
	pass

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
	profileStatus = ndb.BooleanProperty(required = True) # Shows inactive or active -- false or true respectively
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
	def exists(cls, email):
		'''
			Checks for existence of user in the database.

			Args:
				email: Use email as it is the key for the db

			Returns:
				True: if user is found
				False: if user is not found.
		'''

		userKey = ndb.Key('Profile', email)

		user = userKey.get()

		if(user == None):
			return False
		else:
			return True

	@classmethod
	def create_user(cls, email,  password, firstName, lastName, birthDate, campus, profileStatus=True, public=True,  pastCampus=None, hometown=None, about=None, profilePicture=None, uploadedPictures=None, interests=None, likedPages=None, campusInvolvement=None, gender=None, phone=None, nickName=None):
		'''
			Saves user information to db.
			Key: email and password

			Args:
				email: email from the user. Must be of type abc@xyz.com
				nickName: user's nickname. Type string. Default None.
				password: set as string. Required.
				firstName: string. Required
				lastName: string. Requried
				birthDate: type data: Check dataProperty for info. Required
				profileStatus: Active or Inactive -- True/False. Default True. should not be modified.
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

			Return:
				True: if user setup was successful.
				UserAlreadyExistsError if user is already registered.

		'''
		check = Profile.exists(email)
		if(check == False):
			password = hashlib.sha224(password).hexdigest() # password encrypted using sha224
			user = Profile(id=email, email=email, nickName=nickName, password=password, firstName=firstName, lastName=lastName, birthDate=birthDate, profileStatus=profileStatus, public=public, campus=campus, pastCampus=[], hometown=hometown, about=about, profilePicture=profilePicture, uploadedPictures=[], interests=[], likedPages=[], campusInvolvement=[], gender=gender, phone=phone)
			user.key = ndb.Key('Profile', email)
			user.put()
			return True
		else:
			raise UserAlreadyExistsError

	@classmethod
	def login_user(cls, email, password):
		'''
			Login model function. Raises PasswordIncorrectError is password is incorrect. Raises UserNotFoundError if user is not registered.

			Args: 
				email: user's email
				password: user's password

			Return:
				Person object if authentication is successful.

		'''
		userCheck = Profile.exists(email)
		if(userCheck == False):
			raise UserNotFoundError
		else:
			key = ndb.Key('Profile', email)
			user = key.get()
			passwordConvert = hashlib.sha224(password).hexdigest()
			if(passwordConvert == user.password):
				return user
			else:
				raise PasswordIncorrectError

	@classmethod
	def update_pastCampus(cls, user, campusName):
		'''
			Adds pastcampus to user's profile. 
			THIS WILL NOT REMOVE A CAMPUS.

			Args:
				user: a Profile object that was returned during login.
				campusName: the name of the campus retrieved from the user.

			Return:
				None.
		'''
		user.pastCampus.append(PastCampus(pastCampus= campusName))
		user.put()

	@classmethod
	def update_hometown(cls, user, newHometown):
		'''
			Update hometown of the user.

			Args:
				user: a Profile object needs to be passed that was returned during login
				newHometown: the name of the new hometown that the user wants to set.

			Return:
				None
		'''
		user.hometown = newHometown
		user.put()

	def get_id(user):
		'''
			This method is used to facilitate login_user function for flask. 

			Return:
				email of the user. which is actually the id of the user in the db
		'''
		return user.email

	@classmethod
	def get_user(cls, email):
		'''
			This method is only here to support get_user for maintaining flask sessions. 
			SHOULD NOT BE USED ANYWHERE ELSE
			
			Args:
				email: this is the email of the user. 

			Return: 
				Profile object
		'''
		key = ndb.Key('Profile', email)
		user = key.get()
		## required for flask integration.
		if(user == None):
			raise UserNotFoundError
		else:
			user.is_authenticated = True
			return user

	@classmethod
	def update_about(cls, user, about):
		'''
			This method will update 'about' section for the user's profile. 

			Args:
				user: Profile object
				about: the new about provided by the user

			Return:
				None
		'''
		user.about = about
		user.put()

	@classmethod
	def update_gender(cls, user, gender):
		'''
			This method will update the gender attribute of the user's profile

			Args:
				user: Profile object
				gender: M == male, F == female and O == other. No other value will accepted. 
					will raise GenderDoesNotExistError if any other value is passed.

			Return:
				None
		'''
		if(gender == 'M' or gender == 'F' or gender == 'O'):
			user.gender = gender
			user.put()
		else:
			raise GenderDoesNotExistError

	@classmethod
	def update_phone(cls, user, phone):
		'''
			This metod will update phone number of user

			Args:
				user: a Profile object
				phone: phone number. Max length accepted is 10 digits.
					ValueError if number is greater than 10 digits
					TypeError if type of phone number is not integer

			Return:
				None
		'''
		if(type(phone) == int):
			if(len(str(phone)) > 10):
				raise ValueError
			else:
				user.phone = phone
				user.put()
		else:
			raise TypeError
