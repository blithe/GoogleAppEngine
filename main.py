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
import cgi
import re


def escape_html(s):
	return cgi.escape(s, quote = True) 
	
form="""
  	<form method="post">
  		<input type="text" value="%(q)s" name="q"><br>
  		<input type="submit">
  		<div style="color:red">%(error)s</div>
  	</form>
"""
 
form1="""
  	<form method="post">
  		<textarea name="text">%(text)s</textarea><br>
  		<input type="submit">
  		<div style="color:red">%(error)s</div>
  	</form>
"""



def valid_q(user_q):
	if user_q: 
		if user_q == "a":
			return user_q

						
def rot13(user_text):
	return user_text.encode('rot13')			

#This is the main page, right now it is just blank
class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.out.write('')

#This is the form page, the only valid input is the string "a"
class OtherPage(webapp2.RequestHandler):
    def write_form(self, error="", q=""):
    	self.response.out.write(form % {"error":error, "q":escape_html(q)})
    
    
    def get(self):
        self.write_form()
    
    def post(self):
    	user_q = self.request.get('q')
    	q = valid_q(user_q)
    	
    	if not (q):
    		self.write_form("Invalid input.", user_q)
    	else:
    		self.redirect("/thanks")	


    				


#This is the Rot13 page
#Preserves capitalization, punctuation, and white space
class Rot13Page(webapp2.RequestHandler):

    
    def write_form1(self, error="", text=""):
    	self.response.out.write(form1 % {"error":error, "text":escape_html(text)})
    
    
    def get(self):
        self.write_form1()
    
    def post(self):
    	user_text = self.request.get('text')
    	text = rot13(user_text)
    	
    	if not (text):
    		self.write_form1("Invalid input.", user_text)
    	else:
    		self.write_form1("Valid input.", text)	
	
				
   		
#This is the thanks page for a correct input into the form    		
class ThanksHandler(webapp2.RequestHandler):
    def get(self):
    	self.response.out.write("Thanks!")
    	

    	
#This is the hello page
class HelloPage(webapp2.RequestHandler):
    def get(self):
    	self.response.out.write("Hello, Udacity!")     	    		    

app = webapp2.WSGIApplication([('/', MainPage), ('/thanks', ThanksHandler), ('/hello', HelloPage), ('/other', OtherPage), ('/rot13', Rot13Page)],
                              debug=True)
