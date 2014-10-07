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
from database.categorydatareader import CategoryDataReader
from kivy.uix.screenmanager import SlideTransition
kivy.require('1.0.5')

from kivy.app import App
from kivy.adapters.listadapter import ListAdapter
from kivy.lang import Builder
from screens.customscreen import CustomScreen
from database.localitydatareader import LocalityDataReader

__all__ = ("ListLocalitys", "ListLocalitysApp")

Builder.load_string("""
[CustomListItemLocality@SelectableView+BoxLayout]:
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
		list_item_args_converter = \
			lambda row_index, obj: {'text': obj.loclbnom,
									'index': row_index,
									'id': "itemindex_%d" % row_index, 
									'is_selected': False,
									'size_hint_y': None,
									'height': 25}
		
		my_adapter = ListAdapter(data = self.allItems.itervalues(),
									args_converter=list_item_args_converter,
									selection_mode='single',
									allow_empty_selection=True,
									template='CustomListItemLocality')
		
		my_adapter.bind(on_selection_change=self.item_changed)
		self.containerListView.adapter = my_adapter
		
	def item_changed(self, adapter, *args):
		if len(adapter.selection) == 0:
			return
		self.locality = adapter.data[adapter.selection[0].parent.index]
		adapter.selection[0].deselect()
		
		nextScreen = self.manager.go_next()
		nextScreen.set_locality(self.locality)
		
		
	def setItems(self, data):
		self.allItems = data
		#self.logLabel.text = "count : %s" % len(self.allItems)
		self.updateDisplay()
		self.locality = None
		
		
	def refresh(self):
		localityHelper = LocalityDataReader()
		localityHelper.refreshData()
		self.setItems(localityHelper.getAllRecords())
		
		# refresh also categories from Web to Database
		CategoryDataReader().refreshData()
	
class ListLocalitysApp(App):
	screenName = 'ListLocalitys'
	
	def build(self):
		return ListLocalitys(self.screenName)
	