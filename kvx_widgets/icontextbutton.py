'''
Created on Oct 11, 2014

@author: julien
'''
from kivy.uix.behaviors import ButtonBehavior
from kvx_widgets.icontext import IconText


class IconTextButton(ButtonBehavior, IconText):
	
	def __init__(self, **kwargs):
		super(IconTextButton, self).__init__(**kwargs)
	
			