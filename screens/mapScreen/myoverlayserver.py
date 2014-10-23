'''
Created on Sep 23, 2014

@author: Julien CORON
'''
from kvmap.overlays.overlayserver import OverlayServer


from kivy.graphics import Ellipse, Color, Rectangle
from database.categorydatareader import CategoryDataReader
import math

class MyOverlayServer(OverlayServer):

	def __init__(self):
		'''
		Constructor
		'''
		self.type = 'simple'
		# points on interest for this OverlayServer
		self.pois = []
		self.categories = CategoryDataReader().getAllRecords()
		self.current_position = (0,0)
	
	def draw_in(self, aMapViewer):
		'''implement the method to draw in the MapViewer
		'''
		radius = 150.0/aMapViewer.scale
		x = aMapViewer.cmin[0]
		y = aMapViewer.cmin[1]
		(display_width, display_height) = aMapViewer.parent.size
		
		for aPoi in self.pois:
			(poi_x,poi_y) = aMapViewer.get_local_xy_from_latlon(float(aPoi.poinulat), float(aPoi.poinulon), display_width, display_height)
			img_poi = Rectangle( pos=(x + poi_x/aMapViewer.scale - radius/2, y + poi_y/aMapViewer.scale ) )
			img_poi.source='images/location_%s.png' % self.categories[aPoi.poiidcat].catcdcode
			img_poi.size = (radius,radius)
			aMapViewer.canvas.add(img_poi)
		
		# draw the current position
		(curr_x, curr_y) = aMapViewer.get_local_xy_from_latlon(self.current_position[0], self.current_position[1], display_width, display_height)
		img_position = Rectangle( pos=(x + curr_x/aMapViewer.scale - radius/2, y + curr_y/aMapViewer.scale - radius/2) )
		img_position.source='images/my-position.png'
		img_position.size = (radius,radius)
		aMapViewer.canvas.add(img_position)
		
		return
	
	def get_info(self, aMapViewer, lat, lon, scale):
		(display_width, display_height) = aMapViewer.parent.size
		(clickPos_x, clickPos_y) = aMapViewer.get_local_xy_from_latlon(lat, lon, display_width, display_height)

		for aPoi in self.pois:
			(poi_x,poi_y) = aMapViewer.get_local_xy_from_latlon(float(aPoi.poinulat), float(aPoi.poinulon), display_width, display_height)
			dist = math.sqrt( (clickPos_x - poi_x)**2 + (clickPos_y - poi_y - 100)**2 )
			# distance in pixels
			if dist < 40:
				self.display_popup(aMapViewer, aPoi)
				return
		
	def display_popup(self, aMapViewer, aPoi):
		map_screen = aMapViewer.parent.parent.parent.parent
		map_screen.display_poi(aPoi)
		
	def set_current_position(self, lat, lon):
		self.current_position = (lat, lon)
		
		