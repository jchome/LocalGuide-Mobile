#!/usr/bin/python
# -*- coding: utf-8 -*-

### generated from template <objectdatareader.py>
###
# AFTER CODE GENRATION : add this to the "__init__.py" file:
#  __all__ = ["datareader", ... , 
#		"localitydatareader.LocalityDataReader", "localitydatareader.LocalityJsonRetriever"
#	]
###

from .datareader import DataReader, JsonRetriever
from models.localityModel import Locality

"""Localité englobant les données de position
"""
class LocalityDataReader(DataReader):
	
	def __init__(self):
		DataReader.__init__(self, "locgui_localite", "locidloc", ["locidloc", "loclbnom", "locnulat", "locnulon"])
		
	def getAllRecords(self):
		fullDict = DataReader.getAllRecords(self)
		return Locality.readAllFromDict(fullDict)
	
	def refreshData(self, message_writer = None):
		allObjects = LocalityJsonRetriever().retrieveAll()
		if allObjects is None:
			return None
		self.purgeTable(message_writer)
		for anObject in allObjects.itervalues():
			json_data = { "locidloc" : anObject.locidloc, "loclbnom" : anObject.loclbnom, "locnulat" : anObject.locnulat, "locnulon" : anObject.locnulon }
			self.insertData(json_data, message_writer)


	def saveOrUpdate(self, anObject, message_writer = None):
		json_data = { "locidloc" : anObject.locidloc, "loclbnom" : anObject.loclbnom, "locnulat" : anObject.locnulat, "locnulon" : anObject.locnulon }
		if anObject.locidloc is None:
			anObject.locidloc = self.insertData(json_data, message_writer)
		else:
			self.updateData(json_data, message_writer)

	

	# get all <Localité> by <Identifiant>, using <locidloc>
	def getAllRecordsBy_locidloc(self, value):
		fullDict = DataReader.getAllRecordsEquals(self, "locidloc", value)
		return Locality.readAllFromDict(fullDict)
		


class LocalityJsonRetriever(JsonRetriever):
	
	def __init__(self):
		JsonRetriever.__init__(self)
		
	def retrieveAll(self):
		URL_ALL = "locality/listlocalitysjson"
		fullDict = self.retrieveFromUrl(URL_ALL)
		if fullDict is not None:
			return Locality.readAllFromDict(fullDict)


	# get all <Localité> by <Identifiant>, using <locidloc>
	def retrieveAllBy_locidloc(self, value):
		URL_ALL = "locality/listlocalitysjson/findBy_locidloc/"+str(value)
		fullDict = self.retrieveFromUrl(URL_ALL)
		if fullDict is not None:
			return Locality.readAllFromDict(fullDict)
		



	