'''
Created on Oct 12, 2014

@author: julien
'''
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder
from kivy.properties import StringProperty, VariableListProperty, NumericProperty
from kivy.metrics import sp

Builder.load_string("""
<ScrollableText>:
	_text_widget: _text_widget_id
	_padding_top: _padding_top_id
	_padding_left: _padding_left_id
	_padding_right: _padding_right_id
	_padding_bottom: _padding_bottom_id
	canvas.before:
		Color:
			rgba: self.background_color
		Rectangle:
			pos: self.pos
			size: self.size
	GridLayout:
		cols: 1
		height: _text_widget_id.height + _padding_top_id.height + _padding_bottom_id.height
		size_hint_y: None
		
		Label:
			id: _padding_top_id
			text: " "
			size_hint_y: None
			height: sp(4)
			
		GridLayout:
			rows: 1
			Label:
				id: _padding_left_id
				text: " "
				size_hint_x: None
				width: sp(8)
			Label:
				id: _text_widget_id
				text: "no text yet"
				font_size: '18sp'
				color: (0.1,0.1,0.1, 1)
				valign: 'top'
				# make it scrollable
				text_size: (self.width, None)
				size_hint_y: None
				size: (self.parent.width, self.texture_size[1] )
			Label:
				id: _padding_right_id
				text: " "
				size_hint_x: None
				width: sp(8)
		Label:
			id: _padding_bottom_id
			text: " "
			size_hint_y: None
			height: sp(4)
""")

class ScrollableText(ScrollView):
	text = StringProperty("")
	background_color = VariableListProperty([1,1,1,0])
	text_color = VariableListProperty([0,0,0,1])
	padding = VariableListProperty([sp(8), sp(8), sp(8), sp(8)])
	font_size = NumericProperty(sp(18))

	def __init__(self, **kwargs):
		super(ScrollableText, self).__init__(**kwargs)
		self.bind(text = ScrollableText.set_text,
				text_color = ScrollableText.set_text_color,
				padding = ScrollableText.set_padding,
				font_size = ScrollableText.set_font_size
				)
	
	def set_text(self, aText):
		self._text_widget.text = aText
		
	def set_text_color(self, aColor):
		self._text_widget.color = aColor
		
	def set_padding(self, aPadding):
		"""Top, Right, Bottom, Left
		"""
		if isinstance(aPadding, (float,int,long,float)):
			self._padding_top.height = aPadding
			self._padding_right.width = aPadding
			self._padding_bottom.height = aPadding
			self._padding_left.width = aPadding
		if len(aPadding) == 4:
			self._padding_top.height = aPadding[0]
			self._padding_right.width = aPadding[1]
			self._padding_bottom.height = aPadding[2]
			self._padding_left.width = aPadding[3]
		elif len(aPadding) == 2:
			self._padding_top.height = aPadding[0]
			self._padding_right.width = aPadding[1]
			self._padding_bottom.height = aPadding[0]
			self._padding_left.width = aPadding[1]
		
	def set_font_size(self, aSize):
		self._text_widget.font_size = aSize
		