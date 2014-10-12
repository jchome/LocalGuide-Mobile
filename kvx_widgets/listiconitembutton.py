'''
Created on Oct 12, 2014

@author: julien
'''
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty, VariableListProperty, NumericProperty
from kivy.metrics import sp
from kivy.uix.behaviors import ButtonBehavior


Builder.load_string("""
<ListIconItemButton>:
	_label_text: _label_text_id
	_padding_right: _padding_right_id
	_padding_left: _padding_left_id
	_left_icon: _left_icon_id
	_right_icon: _right_icon_id
	rows: 1
	size_hint_y: None
	height: sp(50)
	
	Label:
		id: _padding_left_id
		text: ""
		size_hint_x: None
		width: sp(4)
	Label:
		canvas.before:
			Color:
				rgba: 1,1,1, 1
			Rectangle:
				pos: self.pos
				size: self.size
				source: "images/ic_action_star.png"
		id: _left_icon_id
		text: ""
		size_hint_x: None
		width: sp(50)
		
		
	Label:
		id: _label_text_id
		text: "dummy"
		size_hint_x: 1
		halign: 'left'
		valign: 'middle'
		text_size: self.size
		
	Label:
		canvas.before:
			Color:
				rgba: 1,1,1, 1
			Rectangle:
				pos: self.pos
				size: self.size
				source: "images/ic_action_next.png"
		id: _right_icon_id
		text: ""
		size_hint_x: None
		width: sp(25)
	
	Label:
		id: _padding_right_id
		text: ""
		size_hint_x: None
		width: sp(4)
""")



class ListIconItemButton(ButtonBehavior, GridLayout):
	text = StringProperty("")
	text_color = VariableListProperty([0,0,0,1])
	font_size = NumericProperty(sp(18))
	index = NumericProperty(0)
	padding = VariableListProperty([sp(2),sp(2)])
	left_icon_width = NumericProperty(sp(50))
	right_icon_width = NumericProperty(sp(50))
	left_icon = StringProperty("")
	right_icon = StringProperty("")

	def __init__(self, **kwargs):
		super(ListIconItemButton, self).__init__(**kwargs)
		self.bind(text = ListIconItemButton.set_text,
				text_color = ListIconItemButton.set_text_color,
				font_size = ListIconItemButton.set_font_size,
				index = ListIconItemButton.set_index,
				padding = ListIconItemButton.set_padding,
				left_icon_width = ListIconItemButton.set_left_icon_width,
				right_icon_width = ListIconItemButton.set_right_icon_width,
				left_icon = ListIconItemButton.set_left_icon,
				right_icon = ListIconItemButton.set_right_icon
				)
		
		
	def set_text(self, aText):
		self._label_text.text = aText
	
	def set_index(self, aNumber):
		self.item_index = aNumber
	
	def get_index(self):
		return self.item_index
	
	def set_padding(self, aPadding):
		if isinstance(aPadding, (float,int,long,float)):
			self._padding_left.width = aPadding
			self._padding_right.width = aPadding
		else:
			self._padding_left.width = aPadding[0]
			self._padding_right.width = aPadding[1]
		
	def set_font_size(self, aSize):
		self._label_text.font_size = aSize

	def set_text_color(self, aColor):
		self._label_text.color = aColor
		
	def set_left_icon_width(self, aWidth):
		self._left_icon.width = aWidth

	def set_right_icon_width(self, aWidth):
		self._right_icon.width = aWidth
		
	def set_left_icon(self, aSourceImage):
		if aSourceImage == "" or aSourceImage is None:
			self.remove_widget(self._left_icon)
		else:
			self._left_icon.canvas.before.children[1].source = aSourceImage
		
	def set_right_icon(self, aSourceImage):
		if aSourceImage == "" or aSourceImage is None:
			self.remove_widget(self._right_icon)
		else:
			self._right_icon.canvas.before.children[1].source = aSourceImage
		