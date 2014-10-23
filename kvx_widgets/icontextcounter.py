'''
Created on Oct 11, 2014

@author: julien
'''
from kivy.properties import StringProperty, NumericProperty, VariableListProperty
from kivy.metrics import sp
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout

Builder.load_string("""
<IconTextCounter>:
	_icontext: _icontext_id
	_counter: _counter_id
	IconText:
		id: _icontext_id
		text: "dummy"
		icon: "images/ic_action_star.png"
		pos_hint: {'x':0, 'top':1}
		
	Label:
		canvas.before:
			Color:
				rgba: 1,1,1, 1
			Rectangle:
				pos: self.pos
				size: self.size
				source: "kvx_widgets/images/counter_bg.png"
		id: _counter_id
		text: "x"
		pos_hint: {'center_x':0.95, 'top':0.65}
		size_hint: (None, None)
		size: (self.texture_size[0]+sp(16), self.texture_size[1]+sp(8))
		font_size: sp(12)
	
""")


class IconTextCounter(FloatLayout):
	counter = StringProperty("")
	counter_position = StringProperty("")
	counter_background = StringProperty("")
	
	text = StringProperty("")
	icon = StringProperty("")
	icon_size = NumericProperty(sp(80))
	font_size = NumericProperty(sp(18))
	text_color = VariableListProperty([0,0,0,1])
	forced_width = NumericProperty(sp(80))
	
	def __init__(self, **kwargs):
		super(IconTextCounter, self).__init__(**kwargs)
		self.bind(counter = IconTextCounter.set_counter,
				counter_position = IconTextCounter.set_counter_position,
				counter_background = IconTextCounter.set_counter_background,
				text = IconTextCounter.set_text,
				icon = IconTextCounter.set_icon,
				icon_size = IconTextCounter.set_icon_size,
				font_size = IconTextCounter.set_font_size,
				text_color = IconTextCounter.set_text_color,
				forced_width = IconTextCounter.set_forced_width
				)
	
	def set_counter(self, aValue):
		self._counter.text = aValue
		
		
	def set_counter_position(self, aPosition):
		delta = 0.15
		center_x = 0.5
		top = 0.80
		if aPosition == 'top-left':
			center_x -= delta
			top += delta
		elif aPosition == 'top-right':
			center_x += delta
			top += delta
		elif aPosition == 'bottom-left':
			center_x -= delta
			top -= delta
		elif aPosition == 'bottom-right':
			center_x += delta
			top -= delta
		
		self._counter.pos_hint = {'center_x':center_x, 'top':top}
		
	
	def set_counter_background(self, aSourceImage):
		self._counter.canvas.before.children[1].source = aSourceImage
		
	## define all IconText methods
	def set_text(self, aText):
		self._icontext.text = aText
		
	def set_icon(self, aSourceImage):
		self._icontext.icon = aSourceImage
		
	def set_icon_size(self, aWidthHeight):
		self._icontext.icon_size = aWidthHeight
	
	def set_font_size(self, aFontSize):
		self._icontext.font_size = aFontSize
	
	def set_text_color(self, aColor):
		self._icontext.text_color = aColor
		
	def set_forced_width(self, aWidth):
		self._icontext.forced_width = aWidth
	