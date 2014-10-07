#!/usr/bin/python
# -*- coding: utf-8 -*-

__all__ = ('Locality')
'''Localité englobant les données de position
'''
class Locality():
	
	def __init__(self):
		''' Identifiant interne ; type int'''
		self.locidloc = None;

		''' Nom de la localité ; type varchar(255)'''
		self.loclbnom = None;

		''' Latitude du centre de la localité ; type float(24)'''
		self.locnulat = None;

		''' Longitude du centre de la localité ; type float(24)'''
		self.locnulon = None;

	
	def readFromDict(self, aDict):
		self.locidloc = aDict["locidloc"]
		self.loclbnom = aDict["loclbnom"]
		self.locnulat = aDict["locnulat"]
		self.locnulon = aDict["locnulon"]
		return self
	
	def toDict(self):
		return { "locidloc": self.locidloc, "loclbnom": self.loclbnom, "locnulat": self.locnulat, "locnulon": self.locnulon}
	
	@staticmethod
	def readAllFromDict(aDictOfDict):
		allObjects = {}
		for key, aDict in aDictOfDict.iteritems():
			allObjects[key] = Locality().readFromDict(aDict)
		return allObjects
	
	def __repr__(self):
		return "<Locality instance : %s>" % ( self.toDict() )
	
	