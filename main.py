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
import json
from google.appengine.ext import db

class Experience(db.Model):
	SId = db.StringProperty()
	LoId = db.StringProperty()
	title = db.StringProperty()
	level = db.IntegerProperty()
	ttc = db.FloatProperty()
	score = db.IntegerProperty()
	rating = db.FloatProperty()
	ldu = db.DateTimeProperty(auto_now = True)

class LearningObject(db.Model):
	LoId = db.StringProperty()
	Ctitle = db.StringProperty()
	level = db.IntegerProperty()
	title = db.StringProperty()
	author = db.StringProperty()
	otype = db.StringProperty()
	rating = db.FloatProperty()

class Course(db.Model):
	CId = db.StringProperty()
	CTitle = db.StringProperty()
	CDescription = db.StringProperty()

class AddCourse(webapp2.RequestHandler):
	def post(self):
		CId = self.request.get("id")
		CTitle = self.request.get("title")
		CDescription = self.request.get("description")
		course = Course(CId = CId, CTitle = CTitle, CDescription = CDescription)
		course.put()
		self.response.write(json.dumps({"result": "success"}))

class AddExperience(webapp2.RequestHandler):
	def post(self):
		SId = self.request.get("sid")
		LoId = self.request.get("loid")
		title = self.request.get("title")
		level = self.request.get("level")
		ttc = self.request.get("ttc")
		score = self.request.get("score")
		rating = self.request.get("rating")
		experience = Experience(SId = SId, LoId = LoId, title = title, level = int(level), ttc = float(ttc), score = int(score), rating = float(rating))
		experience.put()
		self.response.write(json.dumps({"result": "success"}))

class AddLearningObject(webapp2.RequestHandler):
	def post(self):
		LoId = self.request.get("id")
		Ctitle = self.request.get("ctitle")
		level = self.request.get("level")
		title = self.request.get("title")
		author = self.request.get("author")
		otype = self.request.get("otype")
		rating = self.request.get("rating")
		learningobjects = LearningObject.all()
		learningobjects.filter("LoId =", str(LoId))
		learningobject = LearningObject(LoId = LoId, Ctitle = Ctitle, level = int(level), title = title, author = author, otype = otype, rating = float(rating))
		learningobject.put()
		self.response.write(json.dumps({'result': 'success'}))

class CourseSummary(webapp2.RequestHandler):
	def post(self):
		title = self.request.get("title")
		learningobjects = LearningObject.all()
		learningobjects.filter("Ctitle =", str(title))
		lojsons = []
		for learningobject in learningobjects:
			lojson = {'loid': learningobject.LoId, 'ctitle': learningobject.Ctitle, 'level': learningobject.level, 'title': learningobject.title, 'author': learningobject.author, 'type': learningobject.otype, 'rating': learningobject.rating}
			lojsons.append(lojson)
		lojson = {'summary': lojsons}
		self.response.write(json.dumps(lojson))

class LevelObjects(webapp2.RequestHandler):
	def post(self):
		title = self.request.get("title")
		level = self.request.get("level")
		learningobjects = LearningObject.all()
		learningobjects.filter("Ctitle =", str(title))
		learningobjects.filter("level =", int(level))
		lojsons = []
		for learningobject in learningobjects:
			lojson = {'loid': learningobject.LoId, 'ctitle': learningobject.Ctitle, 'level': learningobject.level, 'title': learningobject.title, 'author': learningobject.author, 'type': learningobject.otype, 'rating': learningobject.rating}
			lojsons.append(lojson)
		lojson = {'summary': lojsons}
		self.response.write(json.dumps(lojson))

class CourseProgressSummary(webapp2.RequestHandler):
	def post(self):
		title = self.request.get("title")
		sid = self.request.get("sid")
		experiences = Experience.all()
		experiences.filter("SId =", str(sid))
		experiences.filter("title =", str(title))
		experiencejsons = []
		for experience in experiences:
			experiencejson = {'loid': experience.LoId, 'title': experience.title, 'level': experience.level, 'ttc': experience.ttc, 'score': experience.score, 'rating': experience.rating, 'ldu': str(experience.ldu)}
			experiencejsons.append(experiencejson)
		experiencejson = {'summary': experiencejsons}
		self.response.write(json.dumps(experiencejson))		

app = webapp2.WSGIApplication([
    ('/coursesummary', CourseSummary),
    ('/levelobjects', LevelObjects),
    ('/courseprogress', CourseProgressSummary),
    ('/addcourse', AddCourse),
    ('/addlearningobject', AddLearningObject),
    ('/addexperience', AddExperience)
], debug=True)
