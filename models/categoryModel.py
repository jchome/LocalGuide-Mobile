#!/usr/bin/python
# -*- coding: utf-8 -*-
'''Catégorie de point d’intérêt
'''
class Category():
	
	def __init__(self):
		''' Identifiant interne ; type int'''
		self.catidcat = None;

		''' Nom de la catégorie ; type varchar(255)'''
		self.catlblib = None;

		''' Code de la catégorie ; type char(30)'''
		self.catcdcode = None;

	
	def readFromDict(self, aDict):
		self.catidcat = aDict["catidcat"]
		self.catlblib = aDict["catlblib"]
		self.catcdcode = aDict["catcdcode"]
		return self
	
	def toDict(self):
		return { "catidcat": self.catidcat, "catlblib": self.catlblib, "catcdcode": self.catcdcode}
	
	@staticmethod
	def readAllFromDict(aDictOfDict):
		allObjects = {}
		for key, aDict in aDictOfDict.iteritems():
			allObjects[key] = Category().readFromDict(aDict)
		return allObjects
	
	def __repr__(self):
		return "<Category instance : %s>" % ( self.toDict() )
	
	