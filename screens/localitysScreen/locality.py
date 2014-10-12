#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on Oct 3, 2014

@author: julien
'''
from screens.customscreen import CustomScreen
from kivy.app import App
from database.localitydatareader import LocalityDataReader
from database.categorydatareader import CategoryDataReader
from database.pointofinterestdatareader import PointOfInterestDataReader
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import SlideTransition

from kivy.properties import StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kvx_widgets.icontext import IconText

class Locality(CustomScreen):


	def __init__(self, aName):
		super(Locality, self).__init__()
		self.name = aName
		self.locality = None
		self.categories = CategoryDataReader().getAllRecords()

	def set_locality(self, aLocality):
		self.locality = aLocality
		self.locality_label.text = self.locality.loclbnom
		
		poiHelper = PointOfInterestDataReader()
		self.pois = poiHelper.getAllRecordsBy_poiidloc( self.locality.locidloc )
		repartition_catidcat = {}
		for aPoi in self.pois.values():
			if not repartition_catidcat.has_key(aPoi.poiidcat):
				repartition_catidcat[aPoi.poiidcat] = []
			repartition_catidcat[aPoi.poiidcat].append(aPoi)
		
		self.grid_widget.clear_widgets()
		
		for aCategory in self.categories.values():
			if repartition_catidcat.has_key(aCategory.catidcat):
				nb_pois = len(repartition_catidcat[aCategory.catidcat] )
				picto = IconText()
				picto.set_text( "%s : x %s" % (aCategory.catlblib, nb_pois) )
				picto.set_icon( 'images/category_%s.png' % aCategory.catcdcode )
				self.grid_widget.add_widget( picto )
			
		
		
	def refresh(self):
		localityHelper = LocalityDataReader()
		localityHelper.refreshData()
		matching_localitys = localityHelper.getAllRecordsBy_locidloc(self.locality.locidloc)
		self.set_locality( matching_localitys[0] )
		
		# refresh also categories from Web to Database
		CategoryDataReader().refreshData()
		self.categories = CategoryDataReader().getAllRecords()

	def display_map(self):
		self.manager.get_screen("Map").setItems( self.locality, self.pois.values() )
		self.manager.transition = SlideTransition(direction="left")
		self.manager.current = "Map"
		
	def display_list(self):
		self.manager.get_screen("ListPointOfInterests").setItems( self.locality, self.pois )
		self.manager.transition = SlideTransition(direction="left")
		self.manager.current = "ListPointOfInterests"


		

class Picto_Button(ButtonBehavior, BoxLayout):
	text = StringProperty("")
	image_source = StringProperty("")
	
	
	def __init__(self, **kwargs):
		super(Picto_Button, self).__init__(**kwargs)
		self.orientation = 'vertical'
		self.bind(text=self.set_text, 
				image_source=self.set_image_source)
		
	def set_text(self, aWidget, aValue):
		self.textButton.text = aValue

	def set_image_source(self, aWidget, aValue):
		self.imageButton.source = aValue
		
	


class LocalityApp(App):
	screenName = 'Locality'
	
	def build(self):
		return Locality(self.screenName)
	