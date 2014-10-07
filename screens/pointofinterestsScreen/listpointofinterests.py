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
kivy.require('1.0.5')

from kivy.app import App
from kivy.adapters.listadapter import ListAdapter
from kivy.lang import Builder
from screens.customscreen import CustomScreen
from database.pointofinterestdatareader import PointOfInterestDataReader

__all__ = ("ListPointOfInterests", "ListPointOfInterestsApp")

Builder.load_string("""
[CustomListItemPointOfInterest@SelectableView+BoxLayout]:
	orientation: 'horizontal'
	spacing: '10sp'
	padding: (sp(20), 0)
	size_hint_y: None
	height: '64sp'
	index: ctx.index
	canvas.after:
		Color:
			rgb: 0.5,0.5,0.5
		Line:
			rectangle: self.x,self.y+self.height,self.width,0
	
	
	# Icon of item
	ListItemButton:
		id: mainListItemButton
		canvas.before:
			Color:
				rgba: 1,1,1, 1
			Rectangle:
				source: "images/category_%s.png" % ctx.category.catcdcode
				pos: self.pos
				size: self.size
		size_hint_x: None
		width: '64sp'
		selected_color: 0,0,0, 0
		deselected_color: 1,1,1, 0
		background_color: 1,1,1, 0
		background_normal: ""
		background_down: ""
		
	ListItemButton:
		selected_color: 0,0,1, 0
		deselected_color: 1,1,1, 0
		background_color: 1,1,1, 0
		background_normal: ""
		background_down: ""
		
		halign: 'left'
		text_size: (self.width , None)
		color: [1,1,1, 1]
		text: ctx.text
		markup: True
		font_size: '22sp'
		

""")

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
		
	def updateDisplay(self):
		list_item_args_converter = \
			lambda row_index, obj: {'text': obj.poilbnom,
									'category': self.category_collection[obj.poiidcat],
									'index': row_index,
									'id': "itemindex_%d" % row_index, 
									'is_selected': False,
									'size_hint_y': None,
									'height': 25}
		
		my_adapter = ListAdapter(data = self.allItems.itervalues(),
									args_converter=list_item_args_converter,
									selection_mode='single',
									allow_empty_selection=True,
									template='CustomListItemPointOfInterest')
		
		my_adapter.bind(on_selection_change=self.item_changed)
		self.containerListView.adapter = my_adapter
		
	def item_changed(self, adapter, *args):
		if len(adapter.selection) == 0:
			return
		self.pointofinterest = adapter.data[adapter.selection[0].parent.index]
		adapter.selection[0].deselect()
		
		self.manager.get_screen("PointOfInterest").setItems( self.locality, self.pointofinterest )
		self.manager.transition = SlideTransition(direction="left")
		self.manager.current = "PointOfInterest"
		
	
	def display_map(self):
		self.manager.get_screen("Map").setItems( self.locality, self.allItems.values() )
		self.manager.transition = SlideTransition(direction="left")
		self.manager.current = "Map"
		
	def go_back(self):
		self.manager.transition = SlideTransition(direction="right")
		self.manager.current = "Locality"

		
	def setItems(self, aLocality, data):
		self.allItems = data
		self.locality = aLocality
		self.updateDisplay()
		self.pointofinterest = None
		

	def refresh(self):
		pointofinterestHelper = PointOfInterestDataReader()
		pointofinterestHelper.refreshData()
		self.setItems(pointofinterestHelper.getAllRecordsBy_poiidloc( self.locality.locidloc ) )
	
class ListPointOfInterestsApp(App):
	screenName = 'ListPointOfInterests'
	
	def build(self):
		return ListPointOfInterests(self.screenName)
	
