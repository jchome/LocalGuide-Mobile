#!/usr/bin/python
# -*- coding: utf-8 -*-
import kivy
kivy.require('1.0.5')

from kivy.config import Config

# Samsung S4 : 1080x1920
Config.set('graphics', 'width', '450')
Config.set('graphics', 'height', '800')

__version__ = '1.0'
## install & run with 
# buildozer android debug deploy run

## see logs with
# adb logcat -s "python"

from kivy.app import App
from kivy.uix.screenmanager import SlideTransition

from screens.customscreen import CustomScreenManager, CustomScreen
from screens.localitysScreen.listlocalitys import ListLocalitysApp
from screens.localitysScreen.locality import LocalityApp
from screens.pointofinterestsScreen.listpointofinterests import ListPointOfInterestsApp
from screens.pointofinterestsScreen.pointofinterest import PointOfInterestApp
from screens.mapScreen.map import MapApp

from database.localitydatareader import LocalityDataReader

### import des entités
#from clients import ClientsApp


class Welcome(CustomScreen):

	def do_enter(self):
		self.manager.go_next()
		### passer a l'écran clients
		localityHelper = LocalityDataReader()
		self.manager.get_screen("ListLocalitys").setItems( localityHelper.getAllRecords() )


class WelcomeApp(App):
	
	def build(self):
		manager = CustomScreenManager()
		
		### ajout de l'instance de page d'accueil
		welcomeScreen = Welcome(name='Welcome')
		
		manager.add_screen(welcomeScreen)
		
		for app in [ListLocalitysApp(), LocalityApp(), ListPointOfInterestsApp(), MapApp(), PointOfInterestApp()]:
			app.load_kv()
			aView = app.build()
			manager.add_screen(aView)
		

		manager.transition = SlideTransition(direction="left")
		return manager

if __name__ == '__main__':
	WelcomeApp().run()

