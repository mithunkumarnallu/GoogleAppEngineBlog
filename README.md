GoogleAppEngineBlog
===================

Blog I created as a part of Udacity's Web Development course in Python using Goggle App Engine framework

Live demo
===================
You can see the live working version of it at "mithunnallu-webdev.appspot.com/blog".

Usage
===================
You can deploy this as a Google App Engine application and this blog resides at <YOUR_APP>/blog.
The homepage of this blog shows the top 10 latest blogs posted
You can add a new blog by visiting <YOUR_APP>/blog/newpost
You can click on any blog entry to visit its details page where I recently integrated with disqus to facilitate commenting

This blog also supports returning data in json format for someone to query and use.
The json query urls are "<YOUR_APP>/blog/.json" to view all blogs data in json format and "<YOUR_APP>/blog/<BLOG_ID>.json" to get the json data of this particular blogid in json


Extendability
===================
There is also a user sign up and login features I developed but not integrated with the blogging system. One can extend this user creation to the blogs feature thereby keeping track of what users posted what.
A working Sign up page is available at <YOUR_APP>/blog/signup and login is available at <YOUR_APP>/blog/login

Good luck!
