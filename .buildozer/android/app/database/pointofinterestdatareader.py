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
	
	def refreshData(self, message_writer = None):
		allObjects = PointOfInterestJsonRetriever().retrieveAll(message_writer)
		if allObjects is None:
			return
		self.purgeTable(message_writer)
		
		for anObject in allObjects.itervalues():
			json_data = { "poiidpoi" : anObject.poiidpoi, "poilbnom" : anObject.poilbnom, "poiidcat" : anObject.poiidcat, "poiidloc" : anObject.poiidloc, "poinulat" : anObject.poinulat, "poinulon" : anObject.poinulon, "poitxdes" : anObject.poitxdes, "poifiaud" : anObject.poifiaud, "poifipho" : anObject.poifipho }
			self.insertData(json_data, message_writer)

			if anObject.poifiaud is not None and anObject.poifiaud != "":
				message_writer.write("Recuperation de fichier (Audio)")
				PointOfInterestJsonRetriever().retrieve_file_poifiaud(anObject.poiidpoi, self.stored_files_path)
			if anObject.poifipho is not None and anObject.poifipho != "":
				message_writer.write("Recuperation de fichier (Photo)")
				PointOfInterestJsonRetriever().retrieve_file_poifipho(anObject.poiidpoi, self.stored_files_path)

	def saveOrUpdate(self, anObject, message_writer = None):
		json_data = { "poiidpoi" : anObject.poiidpoi, "poilbnom" : anObject.poilbnom, "poiidcat" : anObject.poiidcat, "poiidloc" : anObject.poiidloc, "poinulat" : anObject.poinulat, "poinulon" : anObject.poinulon, "poitxdes" : anObject.poitxdes, "poifiaud" : anObject.poifiaud, "poifipho" : anObject.poifipho }
		if anObject.poiidpoi is None:
			anObject.poiidpoi = self.insertData(json_data, message_writer)
		else:
			self.updateData(json_data, message_writer)

	

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
		
	def retrieveAll(self, message_writer):
		URL_ALL = "pointofinterest/listpointofinterestsjson"
		fullDict = self.retrieveFromUrl(URL_ALL, message_writer)
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
		


	def retrieve_file_poifiaud(self, key, path_to_save):
		URL_GET_FILE = "pointofinterest/getpointofinterestjson/get_file_poifiaud/" + key
		self.retrieveFile(URL_GET_FILE, "poifiaud", path_to_save)

	def retrieve_file_poifipho(self, key, path_to_save):
		URL_GET_FILE = "pointofinterest/getpointofinterestjson/get_file_poifipho/" + key
		self.retrieveFile(URL_GET_FILE, "poifipho", path_to_save)


	