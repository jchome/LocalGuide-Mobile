#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
This code is generated.
'''

###
# AFTER CODE GENRATION : use this code into the "main.py" file to insert a screen 
# from screens.localitysScreen.listlocalitys import ListLocalitysApp
#
# app = ListLocalitysApp()
# app.load_kv()
# localitysView = app.build()
# manager.add_widget(localitysView)
###

import kivy
from kivy.metrics import sp
from kvx_widgets.refreshpopup import RefreshPopup
from kivy.clock import Clock
import time
from kivy.animation import Animation
import threading
kivy.require('1.0.5')

from kivy.app import App
from screens.customscreen import CustomScreen
from database.localitydatareader import LocalityDataReader
from database.categorydatareader import CategoryDataReader
from kvx_widgets.listiconitembutton import ListIconItemButton


__all__ = ("ListLocalitys", "ListLocalitysApp")



class ListLocalitys(CustomScreen):
	
	def __init__(self, aName):
		super(ListLocalitys, self).__init__()
		self.name = aName
		self.allItems = {}
		# prepare display
		self.setItems( {} )
		self.updateDisplay()
		self.locality = None
		
	def updateDisplay(self):
		self.list_items.clear_widgets()
		total_height = 0
		for (index, locality) in self.allItems.items():
			itemButton = ListIconItemButton()
			itemButton.set_left_icon(None)
			itemButton.set_text(locality.loclbnom)
			itemButton.set_font_size(sp(22))
			itemButton.set_index(index)
			itemButton.height = sp(80)
			itemButton.left_icon_width = sp(80)
			itemButton.right_icon_width = sp(40)
			itemButton.bind(on_press=self.select_item)
			self.list_items.add_widget(itemButton)
			total_height += itemButton.height
		self.list_items.height = total_height
		
	def select_item(self, anItem):
		self.locality = self.allItems[anItem.get_index()]
		nextScreen = self.manager.go_next()
		nextScreen.set_locality(self.locality)
		
	def setItems(self, data):
		self.allItems = data
		#self.logLabel.text = "count : %s" % len(self.allItems)
		self.updateDisplay()
		self.locality = None
		
		
	def refresh(self):
		popup = RefreshPopup(on_open=self._popup_opened)
		popup.open()
	
	def _popup_opened(self, popup):
		threading.Thread(target=self._start_refresh, args=(popup,)).start()
		
	def _start_refresh(self, popup):
		popup.write("1/2 : Mise à jour des Localités :")
		localityHelper = LocalityDataReader()
		localityHelper.refreshData(popup)
		self.setItems(localityHelper.getAllRecords())
	
		# refresh also categories from Web to Database
		popup.write("2/2 : Mise à jour des Catégories :")
		CategoryDataReader().refreshData(popup)
		
		popup.write("Terminé !")
		popup.dismiss()
		
		
	
class ListLocalitysApp(App):
	screenName = 'ListLocalitys'
	
	def build(self):
		return ListLocalitys(self.screenName)
	