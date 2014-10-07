'''
Created on Sep 23, 2014

@author: julien
'''

class OverlayServer(object):
	'''
	Abstract class to implement your custom OverlayServer
	'''


	def __init__(self):
		'''
		Constructor
		'''
		self.type = 'abstract'
		
	def get_info(self, aMapViewer, lat, lon, epsilon):
		return None
	
	def draw_in(self, aMapViewer):
		'''implement the method to draw in the MapViewer
		'''
		return
	