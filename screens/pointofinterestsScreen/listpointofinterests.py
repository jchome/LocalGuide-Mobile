#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
This code is generated.
'''

###
# AFTER CODE GENRATION : use this code into the "main.py" file to insert a screen 
# from screens.pointofinterestsScreen.listpointofinterests import ListPointOfInterestsApp
#
# app = ListPointOfInterestsApp()
# app.load_kv()
# pointofinterestsView = app.build()
# manager.add_widget(pointofinterestsView)
###

import kivy
from database.categorydatareader import CategoryDataReader
from kivy.uix.screenmanager import SlideTransition
from kvx_widgets.listiconitembutton import ListIconItemButton
from kivy.metrics import sp
from kvx_widgets.refreshpopup import RefreshPopup
import threading
kivy.require('1.0.5')

from kivy.app import App
from screens.customscreen import CustomScreen
from database.pointofinterestdatareader import PointOfInterestDataReader


__all__ = ("ListPointOfInterests", "ListPointOfInterestsApp")

class ListPointOfInterests(CustomScreen):
	
	def __init__(self, aName):
		super(ListPointOfInterests, self).__init__()
		self.name = aName
		self.allItems = {}
		# prepare display
		self.setItems( None, {} )
		self.updateDisplay()
		self.pointofinterest = None
		self.locality = None
		self.category_collection = CategoryDataReader().getAllRecords()
		self.active_categories = []
		
	def updateDisplay(self):
		self.list_items.clear_widgets()
		total_height = 0
		for (index, poi) in self.allItems.items():
			category = self.category_collection[poi.poiidcat]
			# ne pas présenter les poi qui ont la categorie desactivée
			if not category.catidcat in self.active_categories:
				continue
			itemButton = ListIconItemButton()
			itemButton.set_left_icon( "images/category_%s.png" % category.catcdcode )
			itemButton.set_text(poi.poilbnom)
			itemButton.set_font_size(sp(22))
			itemButton.set_index(index)
			itemButton.height = sp(80)
			itemButton.left_icon_width = sp(76)
			itemButton.right_icon_width = sp(40)
			itemButton.bind(on_press=self.select_item)
			self.list_items.add_widget(itemButton)
			total_height += itemButton.height
		self.list_items.height = total_height
			
		
	def select_item(self, anItem):
		self.pointofinterest = self.allItems[anItem.get_index()]
		self.manager.get_screen("PointOfInterest").setItems( self.locality, self.pointofinterest )
		self.manager.transition = SlideTransition(direction="left")
		self.manager.current = "PointOfInterest"
		
	
	def display_map(self):
		self.manager.get_screen("Map").set_active_categories(self.active_categories)
		self.manager.get_screen("Map").setItems( self.locality, self.allItems.values() )
		self.manager.transition = SlideTransition(direction="left")
		self.manager.current = "Map"
		
	def go_back(self):
		self.manager.transition = SlideTransition(direction="right")
		self.manager.current = "Locality"
		return True
	
		
	def setItems(self, aLocality, data):
		self.allItems = data
		self.locality = aLocality
		self.updateDisplay()
		self.pointofinterest = None
		
	def set_active_categories(self, anArray):
		self.active_categories = anArray
		
	def refresh(self):
		popup = RefreshPopup(on_open=self._popup_opened)
		popup.open()
	
	def _popup_opened(self, popup):
		threading.Thread(target=self._start_refresh, args=(popup,)).start()
		
	def _start_refresh(self, popup):
		popup.write("1/2 : Mise à jour des Points d'intérêt :")
		pointofinterestHelper = PointOfInterestDataReader()
		pointofinterestHelper.refreshData(popup)
		self.setItems(self.locality, pointofinterestHelper.getAllRecordsBy_poiidloc( self.locality.locidloc ) )
		
		# refresh also categories from Web to Database
		popup.write("2/2 : Mise à jour des Catégories :")
		CategoryDataReader().refreshData(popup)
		self.category_collection = CategoryDataReader().getAllRecords()
		popup.write("Terminé !")
		popup.dismiss()
		
	
class ListPointOfInterestsApp(App):
	screenName = 'ListPointOfInterests'
	
	def build(self):
		return ListPointOfInterests(self.screenName)
	
