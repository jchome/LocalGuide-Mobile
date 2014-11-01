#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on Oct 29, 2014

@author: julien
'''
from kivy.uix.popup import Popup
from kivy.lang import Builder


Builder.load_string("""
<RefreshPopup>:
	label_widget: label_widget_id
	title: "Mise à jour des données..."
	separator_color: [1,1,1,0.8]
	size_hint: (0.8,0.5)
	ScrollableText:
		id: label_widget_id
		text: ""
		background_color: (0,0,0,0)
		text_color: (0.9,0.9,0.9, 1)
		font_size: sp(12)
""")

class RefreshPopup(Popup):
	def __init__(self, **kwargs):
		super(RefreshPopup, self).__init__(**kwargs)
	
	def write(self, message):
		self.label_widget.text += "\n%s" % message
		