#!/usr/bin/python
# -*- coding: utf-8 -*-
'''Lieux où il y a quelque chose d'intéressant
'''
class PointOfInterest():
	
	def __init__(self):
		''' Identifiant interne ; type int'''
		self.poiidpoi = None;

		''' Nom du point d'interet ; type varchar(255)'''
		self.poilbnom = None;

		''' Lien vers la catégorie ; type int'''
		self.poiidcat = None;

		''' Lien vers la zone ; type int'''
		self.poiidloc = None;

		''' Latitude du centre du point d'intérêt ; type float(24)'''
		self.poinulat = None;

		''' Longitude du centre du point d'intérêt ; type float(24)'''
		self.poinulon = None;

		''' Description du point d'interet ; type text(4000)'''
		self.poitxdes = None;

		''' Fichier audio du point d'intéret ; type file'''
		self.poifiaud = None;

		''' Fichier photo aperçu ; type file'''
		self.poifipho = None;

	
	def readFromDict(self, aDict):
		self.poiidpoi = aDict["poiidpoi"]
		self.poilbnom = aDict["poilbnom"]
		self.poiidcat = aDict["poiidcat"]
		self.poiidloc = aDict["poiidloc"]
		self.poinulat = aDict["poinulat"]
		self.poinulon = aDict["poinulon"]
		self.poitxdes = aDict["poitxdes"]
		self.poifiaud = aDict["poifiaud"]
		self.poifipho = aDict["poifipho"]
		return self
	
	def toDict(self):
		return { "poiidpoi": self.poiidpoi, "poilbnom": self.poilbnom, "poiidcat": self.poiidcat, "poiidloc": self.poiidloc, "poinulat": self.poinulat, "poinulon": self.poinulon, "poitxdes": self.poitxdes, "poifiaud": self.poifiaud, "poifipho": self.poifipho}
	
	@staticmethod
	def readAllFromDict(aDictOfDict):
		allObjects = {}
		for key, aDict in aDictOfDict.iteritems():
			allObjects[key] = PointOfInterest().readFromDict(aDict)
		return allObjects
	
	def __repr__(self):
		return "<PointOfInterest instance : %s>" % ( self.toDict() )
	
	