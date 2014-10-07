#!/usr/bin/python
# -*- coding: utf-8 -*-

from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.core.window import Window


class CustomScreenManager(ScreenManager):
	def __init__(self, **kwargs):
		super(ScreenManager, self).__init__(**kwargs)
		self.allScreens = []
		self.screenIndex = 0
		Window.bind(on_keyboard=self.hook_keyboard)
		
	def hook_keyboard(self, window, key, *largs):
		if key == 27: # BACK
			return self.current_screen.go_back()
		elif key in (282, 319): # SETTINGS
			print("SETTINGS")
			
	
	def add_screen(self, aScreen):
		self.allScreens.append(aScreen.name)
		self.add_widget(aScreen)
		
	def go_next(self):
		resultOK = self.current_screen.pre_next()
		if not resultOK:
			return False
		self.screenIndex = self.screenIndex + 1
		self.transition = SlideTransition(direction="left")
		self.current = self.allScreens[self.screenIndex]
		self.current_screen.post_next()
		return self.current_screen
	
	def go_back(self):
		resultOK = self.current_screen.pre_back()
		if not resultOK:
			return False
		if self.screenIndex == 0:
			return False
		self.screenIndex = self.screenIndex - 1
		self.transition = SlideTransition(direction="right")
		self.current = self.allScreens[self.screenIndex]
		self.current_screen.post_back()
		return True
	
	def get_previous_screen(self):
		name_of_previous_screen = self.allScreens[self.screenIndex -1]
		return self.get_screen(name_of_previous_screen)

class CustomScreen(Screen):
	def __init__(self, **kwargs):
		super(Screen, self).__init__(**kwargs)
		
	def go_back(self):
		return self.manager.go_back()
		
	def pre_next(self):
		return True

	def post_next(self):
		pass

	def pre_back(self):
		return True

	def post_back(self):
		pass


