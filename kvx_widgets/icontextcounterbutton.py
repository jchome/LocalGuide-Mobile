'''
Created on Oct 23, 2014

@author: julien
'''
from kvx_widgets.icontextcounter import IconTextCounter
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import StringProperty

class IconTextCounterButton(ButtonBehavior, IconTextCounter):

	_state = StringProperty("")
	
	def __init__(self, **kwargs):
		super(IconTextCounterButton, self).__init__(**kwargs)
		self.set_active()
		
	def is_active(self):
		if self._state == 'ACTIVE':
			return True
		elif self._state == 'INACTIVE':
			return False
		else: 
			return None
		
	def _set_state(self, aState):
		self._state = aState
		
	def set_active(self):
		self._set_state('ACTIVE')
		
	def set_inactive(self):
		self._set_state('INACTIVE')
		