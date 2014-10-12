'''
Created on Oct 11, 2014

@author: julien
'''
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, NumericProperty, VariableListProperty
from kivy.metrics import sp
from kivy.lang import Builder

Builder.load_string("""
<IconText>:
	size_hint_y: None
	height: sp(100)
	_text_widget: _text_widget_id
	_icon_widget: _icon_widget_id
	Label:
		canvas.before:
			Color:
				rgba: 1,1,1, 1
			Rectangle:
				pos: self.pos
				size: self.size
				source: "images/ic_action_star.png"
		id: _icon_widget_id
		text: " "
		size_hint: (None, None)
		size: (sp(80), sp(80))
		pos_hint: {'center_x':0.5, 'top':0}
		
	Label:
		id: _text_widget_id
		text: "abc"
		font_size: '18sp'
		color: (0.2,0.2,0.2, 1)
""")


class IconText(BoxLayout):
	text = StringProperty("")
	icon = StringProperty("")
	icon_size = NumericProperty(sp(80))
	font_size = NumericProperty(sp(18))
	text_color = VariableListProperty([0,0,0,1])
	forced_width = NumericProperty(sp(80))
	
	def __init__(self, **kwargs):
		super(IconText, self).__init__(**kwargs)
		self.orientation = 'vertical'
		self.bind(text = IconText.set_text, 
				icon = IconText.set_icon,
				icon_size = IconText.set_icon_size,
				font_size = IconText.set_font_size,
				text_color = IconText.set_text_color,
				forced_width = IconText.set_forced_width
				)
	
	def set_text(self, aText):
		self._text_widget.text = aText
		
	def set_icon(self, aSourceImage):
		self._icon_widget.canvas.before.children[1].source = aSourceImage
		
	def set_icon_size(self, aWidthHeight):
		self._icon_widget.size = (aWidthHeight, aWidthHeight)
	
	def set_font_size(self, aFontSize):
		self._text_widget.font_size = aFontSize
	
	def set_text_color(self, aColor):
		self._text_widget.color = aColor
		
	def set_forced_width(self, aWidth):
		if aWidth is not None:
			self.size_hint_x = None
			self.width = aWidth
			