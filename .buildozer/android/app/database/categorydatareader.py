#!/usr/bin/python
# -*- coding: utf-8 -*-

### generated from template <objectdatareader.py>
###
# AFTER CODE GENRATION : add this to the "__init__.py" file:
#  __all__ = ["datareader", ... , 
#		"categorydatareader.CategoryDataReader", "categorydatareader.CategoryJsonRetriever"
#	]
###

from .datareader import DataReader, JsonRetriever
from models.categoryModel import Category

"""Catégorie de point d’intérêt
"""
class CategoryDataReader(DataReader):
	
	def __init__(self):
		DataReader.__init__(self, "locgui_category", "catidcat", ["catidcat", "catlblib", "catcdcode"])
		
	def getAllRecords(self):
		fullDict = DataReader.getAllRecords(self)
		return Category.readAllFromDict(fullDict)
	
	def refreshData(self):
		self.purgeTable()
		allObjects = CategoryJsonRetriever().retrieveAll()
		for anObject in allObjects.itervalues():
			json_data = { "catidcat" : anObject.catidcat, "catlblib" : anObject.catlblib, "catcdcode" : anObject.catcdcode }
			self.insertData(json_data)
		
	def saveOrUpdate(self, anObject):
		json_data = { "catidcat" : anObject.catidcat, "catlblib" : anObject.catlblib, "catcdcode" : anObject.catcdcode }
		if anObject.catidcat is None:
			anObject.catidcat = self.insertData(json_data)
		else:
			self.updateData(json_data)

	

	# get all <Categorie> by <Identifiant>, using <catidcat>
	def getAllRecordsBy_catidcat(self, value):
		fullDict = DataReader.getAllRecordsEquals(self, "catidcat", value)
		return Category.readAllFromDict(fullDict)
		


class CategoryJsonRetriever(JsonRetriever):
	
	def __init__(self):
		JsonRetriever.__init__(self)
		
	def retrieveAll(self):
		URL_ALL = "category/listcategorysjson"
		fullDict = self.retrieveFromUrl(URL_ALL)
		return Category.readAllFromDict(fullDict)


	# get all <Categorie> by <Identifiant>, using <catidcat>
	def retrieveAllBy_catidcat(self, value):
		URL_ALL = "category/listcategorysjson/findBy_catidcat/"+str(value)
		fullDict = self.retrieveFromUrl(URL_ALL)
		return Category.readAllFromDict(fullDict)
		
