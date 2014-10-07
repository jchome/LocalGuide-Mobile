#!/usr/bin/python
# -*- coding: utf-8 -*-


import json
import urllib, urllib2
import sqlite3


class DataReader():
	
	def __init__(self, aTablename, keyField, fieldsArray):
		self.database = 'database/database.sdb'
		self.tablename = aTablename
		self.fields = fieldsArray
		self.key = keyField
		
	def purgeTable(self):
		deleteStatment = "delete from "+self.tablename
		con = None
		try:
			con = sqlite3.connect(self.database)
			cur = con.cursor()
			print("Database intialisation...")
			cur.execute(deleteStatment);
			con.commit()
		except sqlite3.Error, e:
			print("Error with database: %s" % e)
			return False
		finally:
			if con:
				con.close()

	def insertData(self, json_data):
		idOfKey = None
		try:
			con = sqlite3.connect(self.database)
			cur = con.cursor()
			
			fieldsComaSep = ', '.join(self.fields)
			questionMarks = ', '.join(["?"]*len(self.fields))
			insertStatment = "INSERT INTO "+self.tablename+"("+fieldsComaSep+") VALUES("+questionMarks+")"
			
			print("Data insertion...")
			objectAsTuple = []
			i=0
			for fieldName in self.fields:
				objectAsTuple.insert(i,json_data[ fieldName ])
				i = i+1
			#print(objectAsTuple)
			cur.execute(insertStatment, tuple(objectAsTuple) )
			idOfKey = cur.lastrowid
			con.commit()

		except sqlite3.Error, e:
			print("Error with database: %s" % e)
			return False
		finally:
			if con:
				con.close()
		return idOfKey

	"""Update in SQLite3 database and return TRUE if success
	"""
	def updateData(self, json_data):
		try:
			con = sqlite3.connect(self.database)
			cur = con.cursor()
			allSetValue = []
			for field in self.fields:
				allSetValue.append(field + " = ?")
				
			questionMarks = ', '.join(allSetValue)
			updateStatment = "UPDATE "+self.tablename+" set "+questionMarks+" where "+self.key+" = ?"
			
			print("Data updating...")
			objectAsTuple = []
			i=0
			for fieldName in self.fields:
				objectAsTuple.insert(i,json_data[ fieldName ])
				i = i+1
			objectAsTuple.insert(i,json_data[ self.key ])
			#print(objectAsTuple)
			cur.execute(updateStatment, tuple(objectAsTuple) )
			con.commit()

		except sqlite3.Error, e:
			print("Error with database: %s" % e)
			return False
		finally:
			if con:
				con.close()
		return True

	def __getRecords(self, statment, data = None):
		allRecords = {}
	
		try:
			con = sqlite3.connect(self.database)
			cur = con.cursor()
			if data is None:
				cur.execute(statment)
			else:
				cur.execute(statment, data)
			rows = cur.fetchall()
			for row in rows:
				aRecord = {}
				i=0
				for fieldName in self.fields:
					aRecord[ fieldName ] = row[i]
					i = i+1
				allRecords[row[0]] = aRecord
		except sqlite3.Error, e:
			print("Error with database: %s" % e)
		finally:
			if con:
				con.close()
		return allRecords

	def getAllRecords(self):
		fieldsComaSep =  ', '.join(self.fields)
		return self.__getRecords("SELECT "+fieldsComaSep+" FROM "+self.tablename)

	def getAllRecordsEquals(self, aFieldname, aValue):
		fieldsComaSep =  ', '.join(self.fields)
		return self.__getRecords("SELECT "+fieldsComaSep+" FROM "+self.tablename + " where "+aFieldname+ " = ?", (aValue,))
		
class JsonRetriever():
	serverURL = ""
	def __init__(self, aServerURL = "http://jc.specs.free.fr/LocalGuide/index.php/"):
		self.serverURL = aServerURL
	
	def retrieveFromUrl(self, urlForAllEntities):
		data = "{}"
		try:
			data = urllib2.urlopen(self.serverURL + urlForAllEntities).read()
		except :
			print("Unable to read URL : " + self.serverURL + urlForAllEntities)
		json_data = json.loads(data)
		return json_data

	def sendPostData(self, url, dictForData):
		params = urllib.urlencode(dictForData)
		data= None
		try:
			response = urllib2.urlopen(self.serverURL + url, params)
			data = response.read()
		except :
			print("Unable to read URL : " + self.serverURL + params)
		return data
		
