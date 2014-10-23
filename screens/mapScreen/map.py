#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on Oct 2, 2014

@author: julien
'''
from kivy.app import App
from kvmap.core.mapviewer import MapViewer
from screens.customscreen import CustomScreen
from screens.mapScreen.myoverlayserver import MyOverlayServer
from kivy.uix.screenmanager import SlideTransition
from plyer import gps

class Map(CustomScreen):
	
	def __init__(self, aName):
		super(CustomScreen, self).__init__()
		self.name = aName
		self.mapview = MapViewer(maptype="Roadmap", provider="openstreetmap")
		self.active_categories = []
		self.layout.add_widget(self.mapview)
		self.mapview.map.scale = 10000
		self.overlay_server = MyOverlayServer()
		self.mapview.map.overlays.append( self.overlay_server )
		self.overlay_server.set_current_position(45.671344,4.748361)
		self.gps = None
		try:
			self.gps = gps
			self.gps.configure(on_location=self.update_position)
			self.gps.start()
		except:
			pass

	def setItems(self, aLocality, aSetOfPOIs):
		self.locality = aLocality
		allPois = []
		for aPoi in aSetOfPOIs:
			if aPoi.poiidcat in self.active_categories:
				allPois.append(aPoi)
		self.overlay_server.pois = allPois
		
	def set_active_categories(self, anArray):
		self.active_categories = anArray
		
	def on_pre_enter(self):
		# attention, "self.parent.width" n'est disponible qu'après affichage
		center_coord = (float(self.locality.locnulat), float(self.locality.locnulon))
		self.mapview.center_to_latlon( center_coord, self.parent.width, self.parent.height )
		try:
			self.gps.configure(on_location=self.update_position)
			self.gps.start()
		except NotImplementedError:
			#import traceback; traceback.print_exc()
			#self.gps_status = 'GPS is not implemented for your platform'
			pass
		
		return True

	def go_back(self):
		self.manager.transition = SlideTransition(direction="right")
		self.manager.current = "Locality"
		try:
			self.gps.stop()
		except:
			pass

	def display_poi(self, aPoi):
		self.manager.get_screen("PointOfInterest").setItems( self.locality, aPoi )
		self.manager.transition = SlideTransition(direction="left")
		self.manager.current = "PointOfInterest"
		try:
			self.gps.stop()
		except:
			pass


	def update_position(self, **kwargs):
		try:
			lat = kwargs['lat']
			lon = kwargs['lon']
			self.overlay_server.set_current_position(lat, lon)
		except:
			pass

class MapApp(App):
	screenName = 'Map'
	
	def build(self):
		return Map(self.screenName)
	
