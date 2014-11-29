import webapp2
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'data_model'))

from data_model import blog_data_model

import jinja2
from jinja_helper import *
from google.appengine.ext import db
from google.appengine.api import memcache
import time
import calendar

jinja_environment = jinja2.Environment(autoescape=True,
	loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))
	
class NewBlogHandler(Handler):
	def get(self):
		self.render("NewBlog.html")
	
	def post(self):
		subject = self.request.get('subject')
		content = self.request.get('content')
			
		if subject and content:
			blog = blog_data_model.Blog(subject=subject, content=content)
			blog.put()
			id = blog.key().id()
			self.redirect("/blog/" + str(id))
		else:
			self.render("NewBlog.html", error="Please enter both subject and content", subject=subject, content=content)
		
class ViewBlogHandler(Handler):
	def get_blog(self, id, fetch = None):
		if fetch == True or not memcache.get(id):
			blog = db.Key.from_path("Blog", int(id))
			blog = db.get(blog)
			while not memcache.add(id, (blog, time.gmtime())):
				pass
		return memcache.get(id)
			
	def get(self, id):
		data = self.get_blog(id)
		if data:
			self.render("ViewBlog.html", blog=data[0], timediff=(calendar.timegm(time.gmtime()) - calendar.timegm(data[1])))

import json
class BlogEntryJSONHandler(Handler):
	def get(self, id):
		id = id.split(".")[0]
		blog = db.Key.from_path("Blog", int(id))
		blog = db.get(blog)
		lst = []
		blogdata = {}
		blogdata["subject"] = blog.subject
		blogdata["content"] = blog.content
		blogdata["created"] = blog.created.strftime("%a %b  %d %H:%M:%S %Y")
		blogdata["last_modified"] = blog.created.strftime("%a %b  %d %H:%M:%S %Y")
		#lst.append(blogdata)
		jsondata = json.dumps(blogdata)
		#self.render_json(jsondata)
		self.response.headers["Content-Type"] = "application/json; charset=UTF-8"
		self.write(jsondata)
		
class AllBlogsJSONHandler(Handler):
	def get(self):
		q = db.GqlQuery("Select * from Blog")
		blogs = q.run()
		lst = []
		for blog in blogs:
			blogdata = {}
			blogdata["subject"] = blog.subject
			blogdata["content"] = blog.content
			blogdata["created"] = blog.created.strftime("%a %b  %d %H:%M:%S %Y")
			blogdata["last_modified"] = blog.created.strftime("%a %b  %d %H:%M:%S %Y")
			lst.append(blogdata)
			
		jsondata = json.dumps(lst)
		#self.render_json(jsondata)
		self.response.headers["Content-Type"] = "application/json; charset=UTF-8"
		self.write(jsondata)
		
class BlogHomePageHandler(Handler):
	def get_blogs(self, fetch = None):
		if fetch == True or not memcache.get("blogs"):
			blogs = []
			q = db.GqlQuery("Select * from Blog order by created Desc")
			for blog in q.run(limit=10):
				blogs.append(blog)
			while not memcache.add("blogs",(blogs, time.gmtime())):
				pass
		return memcache.get("blogs")		
	
	def get(self):
		res = self.get_blogs() 
		if res:
			blogs, timestamp = res
		self.render("BlogHomePage.html", blogs=blogs, timediff=(calendar.timegm(time.gmtime()) - calendar.timegm(timestamp)))

import re
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$") 

class SignUpHandler(Handler):
	def write_html(self, username='', username_error='', password_error='', verify_password_error='', email='', email_error=''):
		self.render("SignUp.html", username=username, username_error=username_error, password_error=password_error, verify_password_error=verify_password_error, email=email,
				email_error=email_error)
	
	def valid_username(self,username):
		return USER_RE.match(username)	
	
	def username_exists(self, username):
		q = db.GqlQuery("Select * from User where username = '%s'" % (username,))
		try:
			return q.get()
		except Exception:
			return False
			
	def valid_password(self,password):
		return PASS_RE.match(password)
	
	def valid_email(self,email):
		return EMAIL_RE.match(email)
	
	def get(self):
		self.write_html()
	
	def post(self):
		username = self.request.get("username")
		password = self.request.get("password")
		verify = self.request.get("verify")
		email = self.request.get("email")
		username_error, password_error, verify_password_error, email_error = "","","",""
		
		if not self.valid_username(username):
			username_error = "That's not a valid username"
		elif self.username_exists(username):
			username_error = "Username already exists"
		if not self.valid_password(password):
			password_error = "That wasn't a valid password."
		elif password != verify:
			verify_password_error =  "Your passwords didn't match."
		if email != "" and not self.valid_email(email):
			email_error = "That's not a valid email."
		
		if username_error == '' and password_error == "" and verify_password_error == "" and email_error == "":
			userid = blog_data_model.UserHelper.adduser(username, password, email)
			self.response.headers.add_header('set-cookie','user_id=%s; Path=/' % userid)
			self.redirect("/blog/welcome")
		else:
			self.write_html(username, username_error, password_error, verify_password_error, email, email_error)

class WelcomeUserHandler(Handler):
	def get(self):
		if self.request.cookies.get("user_id"):
			username = blog_data_model.UserHelper.getusername(self.request.cookies.get("user_id"))
			if username:
				self.response.write("<h1>Welcome %s</h1>" % (username,))
			else:
				self.redirect("/blog/signup")
		else:
			self.redirect("/blog/signup")
			
class SignInHandler(Handler):
	def get(self):
		self.render("SignIn.html")
	
	def post(self):
		username = self.request.get("username")
		password = self.request.get("password")
		
		if username and password:
			user_id = blog_data_model.UserHelper.isavaliduser(username, password)
			if user_id:
				self.response.headers.add_header("set-cookie",'user_id=%s; Path=/' % user_id)
				self.redirect("/blog/welcome")
			else:
				self.render("SignIn.html", error = "Invalid username or password")
		else:
			self.render("SignIn.html", error = "Please enter both username and password")

class SignOutHandler(Handler):
	def get(self):
		self.request.cookies.get("user_id")
		self.response.headers.add_header('set-cookie','user_id=;Path=/')
		self.redirect('/blog/signup')

class FlushDataHandler(Handler):
	def get(self):
		memcache.flush_all()
		self.redirect("/blog")