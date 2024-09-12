
# ---------------------------------------------------------------------------------------
try:
	import PySimpleGUI as sg
except:
	pass
from abc import abstractclassmethod, abstractproperty
from dataclasses import dataclass, field

from .formitems import *

# ---------------------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# Class to Define a standard UserForm Template
# -----------------------------------------------------------------------------

@dataclass(eq=False, repr=False)
class GuiTemplate():
	'''Minitools UserForm asking user inputs.	'''
	version: str = field(init=False, default='0.4.1')
	header: str
	banner: str
	form_width: int
	form_height: int
	tabs_dic: dict = field(default_factory=dict)
	event_catchers: set = field(default_factory=set)
	event_updaters: set = field(default_factory=set)
	event_item_updaters: set = field(default_factory=set)
	retractables: set = field(default_factory=set)
	button_pallete_dic: dict = field(default_factory=dict)

	# Object Initializer
	def __post_init__(self):
		self.var_dict = {}

	def __call__(self, initial_frames_load=None):
		self.standard_button_pallete_buttons()
		self.set_button_pallete()
		self.create_form(initial_frames_load)

	def create_form(self, initial_frames_load):
		"""initialize the form, and keep it open until some event happens.
		"""    	
		layout = [
			banner(self.banner), 
			self.button_pallete(),
			tabs_display(**self.tabs_dic),
			footer(self.version, self.form_width),
		]

		self.w = sg.Window(self.header, layout, size=(self.form_width, self.form_height), finalize=True)#, icon='data/sak.ico')
		if initial_frames_load:
			initial_frames_load(self)			
		while True:
			event, (i) = self.w.Read()

			# - Events Triggers - - - - - - - - - - - - - - - - - - - - - - - 
			if event in ('Close', sg.WIN_CLOSED) : 
				break
			if event in ('Clear',) : 
				self.clear_fields()
				pass
			if event in self.event_catchers:
				try:
					# ---------------------------------------------
					if event in self.event_item_updaters:
						self.event_catchers[event](self, i, event)
					elif event in self.event_updaters:
						self.event_catchers[event](self, i)	
					elif event in self.tab_updaters:
						self.event_catchers[event](self)	
					else:
						self.event_catchers[event](i)
				except Exception as e:
					# ---------------------------------------------
					print(f"Error: {e}\nEvent Error {event},")
					# ---------------------------------------------

			self.user_events(i, event)

		self.w.Close()

	@abstractclassmethod
	def user_events(self, i, event):
		pass

	@abstractproperty
	def cleanup_fields(self):
		return []

	def standard_button_pallete_buttons(self):
		"""get list of standard button pallete
		"""		
		self._button_pallete_buttons = [ 
			button_cancel("Close"),
			sg.Button("Clear", change_submits=True,size=(10, 1), key='Clear')
		]

	def set_button_pallete(self):
		nbpb = [sg.Button(name, change_submits=True, key=key) for name, key in self.button_pallete_dic.items()]
		self.add_to_button_pallete_buttons(nbpb)

	@property
	def button_pallete_buttons(self):
		return self._button_pallete_buttons

	def add_to_button_pallete_buttons(self, nbpb):
		"""add new buttons to button pallete

		Args:
			nbpb (list): list of additional buttons in pysimplegui format
		"""		
		self._button_pallete_buttons.extend(nbpb)


	def button_pallete(self):
		"""button pallete frame 

		Returns:
			list: list with sg.Frame containing buttons
		"""    		
		return [sg.Frame(title='Button Pallete', 
				title_color='blue', 
				relief=sg.RELIEF_RIDGE, 
				layout=[self.button_pallete_buttons] ),]

	def event_update_element(self, **kwargs):
		"""update an element based on provided kwargs
		"""    		
		for element, update_values in kwargs.items():
			self.w.Element(element).Update(**update_values)

	def event_update_list_element(self, **kwargs):
		"""update a list element based on provided kwargs
		"""    		
		for element, update_values in kwargs.items():
			self.w.Element(element).update(update_values)

	def clear_fields(self):
		"""clear field values to null
		"""		
		for field in self.cleanup_fields:
			try:
				if field:
					d = {field:{'value':''}}
					self.event_update_element(**d)
			except:
				pass
			try:
				if field:
					d = {field: []}
					self.event_update_list_element(**d)
			except:
				pass
		self.var_dict = {}


# # ---------------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Main Function
# ------------------------------------------------------------------------------
if __name__ == '__main__':
	pass
# ------------------------------------------------------------------------------
