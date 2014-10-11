'''
Created on Oct 5, 2014

@author: julien
'''


from screens.customscreen import CustomScreen
from database.categorydatareader import CategoryDataReader
from kivy.app import App
import os
from kivy.uix.screenmanager import SlideTransition

class PointOfInterest(CustomScreen):

	def __init__(self, aName):
		super(PointOfInterest, self).__init__()
		self.name = aName
		self.locality = None
		self.poi = None
		self.categories = CategoryDataReader().getAllRecords()
	
	def setItems(self, aLocality, aPoi):
		self.locality = aLocality
		self.poi = aPoi
		self.poi_label.text = aPoi.poilbnom
		self.cat_label.text = self.categories[aPoi.poiidcat].catlblib
		self.poi_image.canvas.before.children[1].source = "images/category_%s.png" % self.categories[aPoi.poiidcat].catcdcode
		self.poi_description.text = aPoi.poitxdes
		
	def go_back(self):
		self.manager.transition = SlideTransition(direction="right")
		self.manager.current = "ListPointOfInterests"
		return True


class PointOfInterestApp(App):
	screenName = 'PointOfInterest'
	
	def build(self):
		return PointOfInterest(self.screenName)

if __name__ == '__main__':
	os.chdir("../..")
	PointOfInterestApp().run()
