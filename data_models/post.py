# Author: Jayant Arora
# Contributors: []
# Description: This file defines the POST data model for the palsoncampus application.
# Date: Mon April 19 2017

from google.appengine.ext import ndb
import profile

class Likes(ndb.Model):
	# TODO
	pass

class Revision(ndb.Model):
	#TODO
	pass

class Comment(ndb.Model):
	#TODO
	pass

class Post(ndb.Model):
	
	#postID will be auto-generated.
	public = ndb.BooleanProperty(required = True)
	likes = ndb.StructuredProperty(Likes, repeated = True)
	description = ndb.StringProperty(required = True)
	profileID = ndb.StringProperty(required = True)
	revisionHistory = ndb.StructuredProperty(Revision, repeated = True)
	image = ndb.StringProperty()
	comments = ndb.StructuredProperty(Comment, repeated = True)

	### Class methods go here ###

	@classmethod
	def create_post(cls, profileID, description, public=True, image=None, test=False):
		'''
			This method will create a post and save to the database

			Args:
				profileID: email of user posting a post
				description: content of the post
				public: True == is public and False == private
				image: url for the image 

				test: ONLY FOR DEBUGGING PURPOSES

			Return:
				None

				if Debugging: Post object
		'''
		## setup author key
		postAuthor = ndb.Key(profile.Profile, profileID)

		## allocate id for new post
		post_id = ndb.Model.allocate_ids(size=1, parent=postAuthor)[0]

		post = Post(profileID=profileID, description=description, image=image, public=public)
		post.key = ndb.Key('Post', post_id, parent=postAuthor)
		post.put()
		if(test == True):
			return post


