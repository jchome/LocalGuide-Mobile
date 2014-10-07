#!/usr/bin/python
# -*- coding: utf-8 -*-

### generated from template <objectdatareader.py>
###
# AFTER CODE GENRATION : add this to the "__init__.py" file:
#  __all__ = ["datareader", ... , 
#		"pointofinterestdatareader.PointOfInterestDataReader", "pointofinterestdatareader.PointOfInterestJsonRetriever"
#	]
###

from .datareader import DataReader, JsonRetriever
from models.pointofinterestModel import PointOfInterest

"""Lieux où il y a quelque chose d'intéressant
"""
class PointOfInterestDataReader(DataReader):
	
	def __init__(self):
		DataReader.__init__(self, "locgui_poi", "poiidpoi", ["poiidpoi", "poilbnom", "poiidcat", "poiidloc", "poinulat", "poinulon", "poitxdes", "poifiaud", "poifipho"])
		
	def getAllRecords(self):
		fullDict = DataReader.getAllRecords(self)
		return PointOfInterest.readAllFromDict(fullDict)
	
	def refreshData(self):
		self.purgeTable()
		allObjects = PointOfInterestJsonRetriever().retrieveAll()
		for anObject in allObjects.itervalues():
			json_data = { "poiidpoi" : anObject.poiidpoi, "poilbnom" : anObject.poilbnom, "poiidcat" : anObject.poiidcat, "poiidloc" : anObject.poiidloc, "poinulat" : anObject.poinulat, "poinulon" : anObject.poinulon, "poitxdes" : anObject.poitxdes, "poifiaud" : anObject.poifiaud, "poifipho" : anObject.poifipho }
			self.insertData(json_data)
		
	def saveOrUpdate(self, anObject):
		json_data = { "poiidpoi" : anObject.poiidpoi, "poilbnom" : anObject.poilbnom, "poiidcat" : anObject.poiidcat, "poiidloc" : anObject.poiidloc, "poinulat" : anObject.poinulat, "poinulon" : anObject.poinulon, "poitxdes" : anObject.poitxdes, "poifiaud" : anObject.poifiaud, "poifipho" : anObject.poifipho }
		if anObject.poiidpoi is None:
			anObject.poiidpoi = self.insertData(json_data)
		else:
			self.updateData(json_data)

	

	# get all <Point d'interet> by <Identifiant>, using <poiidpoi>
	def getAllRecordsBy_poiidpoi(self, value):
		fullDict = DataReader.getAllRecordsEquals(self, "poiidpoi", value)
		return PointOfInterest.readAllFromDict(fullDict)
		
	# get all <Point d'interet> by <Categorie>, using <poiidcat>
	def getAllRecordsBy_poiidcat(self, value):
		fullDict = DataReader.getAllRecordsEquals(self, "poiidcat", value)
		return PointOfInterest.readAllFromDict(fullDict)
		
	# get all <Point d'interet> by <Localité>, using <poiidloc>
	def getAllRecordsBy_poiidloc(self, value):
		fullDict = DataReader.getAllRecordsEquals(self, "poiidloc", value)
		return PointOfInterest.readAllFromDict(fullDict)
		


class PointOfInterestJsonRetriever(JsonRetriever):
	
	def __init__(self):
		JsonRetriever.__init__(self)
		
	def retrieveAll(self):
		URL_ALL = "pointofinterest/listpointofinterestsjson"
		fullDict = self.retrieveFromUrl(URL_ALL)
		return PointOfInterest.readAllFromDict(fullDict)


	# get all <Point d'interet> by <Identifiant>, using <poiidpoi>
	def retrieveAllBy_poiidpoi(self, value):
		URL_ALL = "pointofinterest/listpointofinterestsjson/findBy_poiidpoi/"+str(value)
		fullDict = self.retrieveFromUrl(URL_ALL)
		return PointOfInterest.readAllFromDict(fullDict)
		
	# get all <Point d'interet> by <Categorie>, using <poiidcat>
	def retrieveAllBy_poiidcat(self, value):
		URL_ALL = "pointofinterest/listpointofinterestsjson/findBy_poiidcat/"+str(value)
		fullDict = self.retrieveFromUrl(URL_ALL)
		return PointOfInterest.readAllFromDict(fullDict)
		
	# get all <Point d'interet> by <Localité>, using <poiidloc>
	def retrieveAllBy_poiidloc(self, value):
		URL_ALL = "pointofinterest/listpointofinterestsjson/findBy_poiidloc/"+str(value)
		fullDict = self.retrieveFromUrl(URL_ALL)
		return PointOfInterest.readAllFromDict(fullDict)
		
