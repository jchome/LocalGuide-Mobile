#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on Oct 3, 2014

@author: julien
'''
from screens.customscreen import CustomScreen
from kivy.app import App
from database.localitydatareader import LocalityDataReader
from database.categorydatareader import CategoryDataReader
from database.pointofinterestdatareader import PointOfInterestDataReader
from kivy.uix.screenmanager import SlideTransition

from kvx_widgets.icontextcounterbutton import IconTextCounterButton
from kvx_widgets.refreshpopup import RefreshPopup
from kivy.clock import Clock
import threading

class Locality(CustomScreen):


	def __init__(self, aName):
		super(Locality, self).__init__()
		self.name = aName
		self.locality = None
		self.categories = CategoryDataReader().getAllRecords()
		self.active_categories = self.categories.keys()

	def set_locality(self, aLocality):
		self.locality = aLocality
		self.locality_label.text = self.locality.loclbnom
		
		poiHelper = PointOfInterestDataReader()
		self.pois = poiHelper.getAllRecordsBy_poiidloc( self.locality.locidloc )
		repartition_catidcat = {}
		for aPoi in self.pois.values():
			if not repartition_catidcat.has_key(aPoi.poiidcat):
				repartition_catidcat[aPoi.poiidcat] = []
			repartition_catidcat[aPoi.poiidcat].append(aPoi)
		
		self.grid_widget.clear_widgets()
		
		for aCategory in self.categories.values():
			if repartition_catidcat.has_key(aCategory.catidcat):
				nb_pois = len(repartition_catidcat[aCategory.catidcat] )
				picto = IconTextCounterButton()
				picto.id = "category_%d" % aCategory.catidcat
				picto.text = aCategory.catlblib
				picto.icon = 'images/category_%s.png' % aCategory.catcdcode
				picto.counter = "%s" % nb_pois
				picto.counter_position = 'top-right'
				picto.bind(on_press=self.switch_category)
				self.grid_widget.add_widget( picto )
				
			
	def switch_category(self, aIconTextCounterButton):
		category_id = aIconTextCounterButton.id.split('_')[1]
		aCategory = self.categories[int(category_id)]
		if aIconTextCounterButton.is_active():
			aIconTextCounterButton.set_inactive()
			aIconTextCounterButton.icon = 'images/category_%s-disabled.png' % aCategory.catcdcode
			if aCategory.catidcat in self.active_categories:
				self.active_categories.remove(aCategory.catidcat)
		else:
			aIconTextCounterButton.set_active()
			aIconTextCounterButton.icon = 'images/category_%s.png' % aCategory.catcdcode
			if not aCategory.catidcat in self.active_categories:
				self.active_categories.append(aCategory.catidcat)
		
		
	def refresh(self):
		popup = RefreshPopup(on_open=self._popup_opened)
		popup.open()
	
	def _popup_opened(self, popup):
		threading.Thread(target=self._start_refresh, args=(popup,)).start()
		
	def _start_refresh(self, popup):
		popup.write("1/2 : Mise à jour de la Localité :")
		localityHelper = LocalityDataReader()
		localityHelper.refreshData(popup)
		matching_localitys = localityHelper.getAllRecordsBy_locidloc(self.locality.locidloc)
		if 0 in matching_localitys.keys():
			self.set_locality( matching_localitys[0] )
		
		# refresh also categories from Web to Database
		self.write("2/2 : Mise à jour des Catégories :")
		CategoryDataReader().refreshData(popup)
		self.categories = CategoryDataReader().getAllRecords()
		
		self.write("Terminé !")
		
	
	def _do_refresh_data(self, popup):
		popup.write("1/2 : Mise à jour de la Localité :")
		localityHelper = LocalityDataReader()
		localityHelper.refreshData(popup)
		matching_localitys = localityHelper.getAllRecordsBy_locidloc(self.locality.locidloc)
		if 0 in matching_localitys.keys():
			self.set_locality( matching_localitys[0] )
		
		# refresh also categories from Web to Database
		popup.write("2/2 : Mise à jour des Catégories :")
		CategoryDataReader().refreshData(popup)
		self.categories = CategoryDataReader().getAllRecords()
		popup.write("Terminé !")
		popup.dismiss()

	def display_map(self):
		self.manager.get_screen("Map").set_active_categories(self.active_categories)
		self.manager.get_screen("Map").setItems( self.locality, self.pois.values() )
		self.manager.transition = SlideTransition(direction="left")
		self.manager.current = "Map"
		
	def display_list(self):
		self.manager.get_screen("ListPointOfInterests").set_active_categories(self.active_categories)
		self.manager.get_screen("ListPointOfInterests").setItems( self.locality, self.pois )
		self.manager.transition = SlideTransition(direction="left")
		self.manager.current = "ListPointOfInterests"


class LocalityApp(App):
	screenName = 'Locality'
	
	def build(self):
		return Locality(self.screenName)
	