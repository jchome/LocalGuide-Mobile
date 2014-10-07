#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
This code is generated.
'''

###
# AFTER CODE GENRATION : use this code into the "main.py" file to insert a screen 
# from screens.categorysScreen.listcategorys import ListCategorysApp
#
# app = ListCategorysApp()
# app.load_kv()
# categorysView = app.build()
# manager.add_widget(categorysView)
###

import kivy
kivy.require('1.0.5')

from kivy.app import App
from kivy.adapters.listadapter import ListAdapter
from kivy.lang import Builder
from screens.customscreen import CustomScreen
from database.categorydatareader import CategoryDataReader

__all__ = ("ListCategorys", "ListCategorysApp")

Builder.load_string("""
[CustomListItemCategory@SelectableView+BoxLayout]:
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
				source: "images/ic_action_star.png"
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
		text: '%s\\n[size=14sp][color=bfbfbf]%s[/color][/size]' % (ctx.text, ctx.subtext)
		markup: True
		font_size: '22sp'
		

""")

class ListCategorys(CustomScreen):
	
	def __init__(self, aName):
		super(ListCategorys, self).__init__()
		self.name = aName
		self.allItems = {}
		# prepare display
		self.setItems( {} )
		self.updateDisplay()
		self.category = None
		
	def updateDisplay(self):
		list_item_args_converter = \
			lambda row_index, obj: {'text': obj.catidcat,
									'subtext': "Lorem ipsum",
									'index': row_index,
									'id': "itemindex_%d" % row_index, 
									'is_selected': False,
									'size_hint_y': None,
									'height': 25}
		
		my_adapter = ListAdapter(data = self.allItems.itervalues(),
									args_converter=list_item_args_converter,
									selection_mode='single',
									allow_empty_selection=True,
									template='CustomListItemCategory')
		
		my_adapter.bind(on_selection_change=self.item_changed)
		self.containerListView.adapter = my_adapter
		
	def item_changed(self, adapter, *args):
		if len(adapter.selection) == 0:
			return
		self.category = adapter.data[adapter.selection[0].parent.index]
		adapter.selection[0].deselect()
		
		nextScreen = self.manager.go_next()
		nextScreen.setItems( ... ) #TODO: ajouter les paramètres pour l'ecran suivant
		
		
	def setItems(self, data):
		self.allItems = data
		#self.logLabel.text = "count : %s" % len(self.allItems)
		self.updateDisplay()
		self.category = None
		
		
	def newItem(self):
		pass

	def refresh(self):
		categoryHelper = CategoryDataReader()
		categoryHelper.refreshData()
		self.setItems(categoryHelper.getAllRecords())
	
class ListCategorysApp(App):
	screenName = 'ListCategorys'
	
	def build(self):
		return ListCategorys(self.screenName)
	
