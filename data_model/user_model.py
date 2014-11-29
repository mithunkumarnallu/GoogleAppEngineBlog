import hashlib
from google.appengine.ext import db

class UserHelper():
	@staticmethod
	def gethash(content):
		return hashlib.sha256(content).hexdigest()
		
	@staticmethod
	def adduser(username, password, email):
		hashedpassword = UserHelper.gethash(password)
		user = UserHelper.User(username=username, password_hash=hashedpassword, email=email)
		user.put()
		return "%s|%s" % (user.key().id(), UserHelper.gethash(str(user.key().id())))
	
	@staticmethod
	def getusername(id):
		if id:
			id_hash = id.split("|")
			if UserHelper.gethash(id_hash[0]) == id_hash[1]:
				user = db.Key.from_path("User", int(id_hash[0]))
				user = db.get(user)
				return user.username
			else:
				return None
		else:
			return None
	
	@staticmethod
	def isavaliduser(username, password):
		q = db.GqlQuery("Select * from User where username = '%s' and password_hash = '%s'" % (username, UserHelper.gethash(password)))
		user = q.get()
		if user:
			#user = db.get(user)
			return "%s|%s" % (str(user.key().id()),UserHelper.gethash(str(user.key().id())))
		else:
			return None
		
	class User(db.Model):
		username = db.StringProperty(required = True)
		password_hash = db.StringProperty(required = True)
		email = db.StringProperty()