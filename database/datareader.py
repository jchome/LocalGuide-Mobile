#!/usr/bin/python
# -*- coding: utf-8 -*-


import json
import urllib, urllib2
import sqlite3
from base64 import b64decode
import os

class InterationService():
	def _write_message(self, writer, message):
		if writer is None:
			print(message)
		else:
			writer.write(message)

class DataReader(InterationService):
	
	def __init__(self, aTablename, keyField, fieldsArray):
		self.database = 'database/database.sdb'
		self.tablename = aTablename
		self.fields = fieldsArray
		self.key = keyField
		self.stored_files_path = "database/files/"
	
				
	def purgeTable(self, message_writer = None):
		deleteStatment = "delete from "+self.tablename
		con = None
		try:
			con = sqlite3.connect(self.database)
			cur = con.cursor()
			self._write_message(message_writer, "Purge de la table %s" % self.tablename)
			cur.execute(deleteStatment);
			con.commit()
		except sqlite3.Error, e:
			self._write_message(message_writer, "Erreur : %s" % e)
			return False
		finally:
			if con:
				con.close()

	def insertData(self, json_data, message_writer = None):
		idOfKey = None
		try:
			con = sqlite3.connect(self.database)
			cur = con.cursor()
			
			fieldsComaSep = ', '.join(self.fields)
			questionMarks = ', '.join(["?"]*len(self.fields))
			insertStatment = "INSERT INTO "+self.tablename+"("+fieldsComaSep+") VALUES("+questionMarks+")"
			
			self._write_message(message_writer, "Insertion dans %s" % self.tablename)
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
			self._write_message(message_writer, "Erreur : %s" % e)
			return False
		finally:
			if con:
				con.close()
		return idOfKey

	"""Update in SQLite3 database and return TRUE if success
	"""
	def updateData(self, json_data, message_writer = None):
		try:
			con = sqlite3.connect(self.database)
			cur = con.cursor()
			allSetValue = []
			for field in self.fields:
				allSetValue.append(field + " = ?")
				
			questionMarks = ', '.join(allSetValue)
			updateStatment = "UPDATE "+self.tablename+" set "+questionMarks+" where "+self.key+" = ?"
			
			self._write_message(message_writer, "Mise à jour dans %s" % self.tablename)
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
			self._write_message(message_writer, "Erreur : %s" % e)
			return False
		finally:
			if con:
				con.close()
		return True

	def __getRecords(self, statment, data = None, message_writer = None):
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
			self._write_message(message_writer,"Error with database: %s" % e)
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
		
class JsonRetriever(InterationService):
	serverURL = ""
	def __init__(self, aServerURL = "http://jc.specs.free.fr/LocalGuide/index.php/"):
		self.serverURL = aServerURL
	
	def retrieveFromUrl(self, urlForAllEntities, message_writer = None):
		data = "{}"
		try:
			data = urllib2.urlopen(self.serverURL + urlForAllEntities).read()
		except :
			message_writer.write("Erreur d'accès à l'URL : " + self.serverURL + urlForAllEntities)
			return None
		json_data = ""
		try:
			json_data = json.loads(data)
		except :
			message_writer.write("Erreur de lecture des données JSON : \n%s" % data)
			return None
		return json_data

	def sendPostData(self, url, dictForData, message_writer = None):
		params = urllib.urlencode(dictForData)
		data= None
		try:
			response = urllib2.urlopen(self.serverURL + url, params)
			data = response.read()
		except :
			self._write_message(message_writer,"Unable to read URL : " + self.serverURL + params)
			return None
		return data
	
	def retrieveFile(self, url_json, field, path_to_save, message_writer = None):
		fullDict = self.retrieveFromUrl(url_json, message_writer)
		if fullDict is None:
			return
		file_raw_data = fullDict[field]["data"]
		file_name = fullDict[field]["id"]
		if file_name == '':
			return
		file_b4_data = file_raw_data.split(',')[1]
		file_data = b64decode(file_b4_data)
		if not os.path.exists(os.path.join(os.getcwd(), path_to_save)):
			os.mkdir(os.path.join(os.getcwd(), path_to_save))
		new_file = open (os.path.join(os.getcwd(), path_to_save,file_name), "wb")
		new_file.write(file_data)
