'''
Created on Oct 5, 2014

@author: julien
'''


from screens.customscreen import CustomScreen
from database.categorydatareader import CategoryDataReader
from kivy.app import App
import os
from kivy.uix.screenmanager import SlideTransition
from kivy.core.audio import SoundLoader
from database.pointofinterestdatareader import PointOfInterestDataReader
from kivy.clock import Clock
from kivy.metrics import sp
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class PointOfInterest(CustomScreen):

	def __init__(self, aName):
		super(PointOfInterest, self).__init__()
		self.name = aName
		self.locality = None
		self.poi = None
		self.categories = CategoryDataReader().getAllRecords()
		self.audio = None
		
	
	def setItems(self, aLocality, aPoi):
		self.locality = aLocality
		self.poi = aPoi
		self.poi_label.text = aPoi.poilbnom
		self.poi_icon.text = self.categories[aPoi.poiidcat].catlblib
		self.poi_icon.icon = "images/category_%s.png" % self.categories[aPoi.poiidcat].catcdcode
		self.poi_description.text = aPoi.poitxdes
		
		if self.poi.poifiaud is None or self.poi.poifiaud == "":
			# cacher le widget
			if self.btn_audio in self.grid_btn.children:
				self.grid_btn.remove_widget(self.btn_audio)
		else:
			# ajouter le widget
			if self.btn_audio not in self.grid_btn.children:
				self.grid_btn.add_widget(self.btn_audio)
			
		if self.poi.poifipho is None or self.poi.poifipho == "":
			# cacher le widget
			if self.btn_photo in self.grid_btn.children:
				self.grid_btn.remove_widget(self.btn_photo)
		else:
			# ajouter le widget
			if self.btn_photo not in self.grid_btn.children:
				self.grid_btn.add_widget(self.btn_photo)
		
		if len(self.grid_btn.children) == 0 and self.grid_btn in self.multimedia_widgets_container.children:
			self.multimedia_widgets_container.remove_widget(self.multimedia_title_label)
			self.multimedia_widgets_container.remove_widget(self.grid_btn)
			self.multimedia_widgets_container.height = 0
		elif len(self.grid_btn.children) > 0 and self.grid_btn not in self.multimedia_widgets_container.children:
			self.multimedia_widgets_container.add_widget(self.multimedia_title_label)
			self.multimedia_widgets_container.add_widget(self.grid_btn)
			self.multimedia_widgets_container.height = sp(130)
			
		
	def go_back(self):
		self.stop_audio()
		self.manager.transition = SlideTransition(direction="right")
		self.manager.current = "ListPointOfInterests"
		return True

	def play_audio(self):
		if self.audio is not None:
			self.audio.stop()
		self.audio = SoundLoader.load(os.path.join(PointOfInterestDataReader().stored_files_path,self.poi.poifiaud))
		Clock.schedule_once(self._play_audio, 0)
	
	def _play_audio(self, dt):
		self.audio.play()
		self.audio.bind(on_stop = self.stop_audio)
	
	def stop_audio(self,  arg = None):
		try:
			if self.audio is not None:
				self.audio.unbind(on_stop = self.stop_audio)
				self.audio.stop()
		except:
			pass
		self.audio = None
	
	
	def show_photo(self):
		layout = BoxLayout(orientation="vertical")
		layout.add_widget(Image(source=os.path.join(PointOfInterestDataReader().stored_files_path,self.poi.poifipho)))
		button = Button(text="Fermer", size_hint=(1, 0.15), font_size=sp(20))
		layout.add_widget(button)
		popup = Popup(title=self.poi.poilbnom,
			content=layout,
			size_hint=(1,1))
		button.bind(on_press=popup.dismiss) 
		popup.open()
		

class PointOfInterestApp(App):
	screenName = 'PointOfInterest'
	
	def build(self):
		return PointOfInterest(self.screenName)

if __name__ == '__main__':
	os.chdir("../..")
	PointOfInterestApp().run()
