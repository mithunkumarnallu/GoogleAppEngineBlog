#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import os

import jinja2
from jinja_helper import *
import blog

jinja_environment = jinja2.Environment(autoescape=True,
	loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))
	
'''
import cgi
class MainHandler(webapp2.RequestHandler):
    def get(self):
		template = jinja_environment.get_template('ShoppingList.html')
		items = self.request.get_all("food")
		self.response.write(template.render({"items" : items })) #form)

class TestHandler(webapp2.RequestHandler):
    def post(self):
        self.response.write(self.request.get('q'))
		#self.response.headers["content-type"] = "text/plain"
		#self.response.write(self.request)

class Rot13Handler(webapp2.RequestHandler):
	def write_html(self, ip=''):
		#if ip != None:
		return rot13_html % {"ip":ip}
		#else: return rot13_html % {"ip":''}
		
	def get(self):
		self.response.write(self.write_html())	
	
	def post(self):
		text = self.request.get("text")
		ip = list(text)		
		for index in range(len(ip)):
			if str.isalpha(str(ip[index])):
				if ip[index].islower():
					ip[index] = chr((ord(ip[index]) - ord('a') + 13) % 26 + ord('a'))
				else:
					ip[index] = chr((ord(ip[index]) - ord('A') + 13) % 26 + ord('A'))
				
		text = ''.join(ip)
		#text = cgi.escape(text, quote=True)
		self.response.write(self.write_html(text))

		
class WelcomeHandler(webapp2.RequestHandler):
	def get(self):
		self.response.write("Welcome, %s!"%self.request.get("username"))
		
class FizzBuzzHandler(webapp2.RequestHandler):
	def get(self):
		template = jinja_environment.get_template('FizzBuzz.html')
		self.response.write(template.render({"n":int(self.request.get("n"))}))

#PAGE_VIEW_RE = r'/wiki/(?:[a-zA-Z0-9_-]+/?)*'
#PAGE_EDIT_RE = r'/wiki/_edit/(?:[a-zA-Z0-9_-]+/?)*'
'''
PAGE_VIEW_RE = r'/wiki/([a-zA-Z0-9_-]*$)'
PAGE_EDIT_RE = r'/wiki/_edit/([a-zA-Z0-9_-]*$)'

app = webapp2.WSGIApplication([
    ("/blog/signup", blog.SignUpHandler),("/blog/login", blog.SignInHandler),("/blog/logout", blog.SignOutHandler),
	("/blog/welcome", blog.WelcomeUserHandler),("/blog/flush", blog.FlushDataHandler),
	("/blog/newpost", blog.NewBlogHandler),("/blog",blog.BlogHomePageHandler),("/blog/.json",blog.AllBlogsJSONHandler),(r"/blog/(.*[0-9])",blog.ViewBlogHandler),(r"/blog/(.*[0-9].json$)",blog.BlogEntryJSONHandler)
], debug=True)
