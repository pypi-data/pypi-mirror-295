
from nettoolkit.nettoolkit.forms.formitems import *

# ============================ [ Juniper ] ======================================= #

def juniper_frame():
	"""tab display

	Returns:
		sg.Frame: Frame with filter selection components
	"""    		
	return sg.Frame(title=None, 
					relief=sg.RELIEF_SUNKEN, 
					layout=[


		[sg.Text('Juniper Set converter', font=('TimesNewRoman', 12), text_color="black") ],

		[sg.Text('Juniper Config file:\t',  text_color="black"), 
		 sg.InputText(key='mini_juniper_file_input'), sg.FileBrowse()],

		[sg.Text('Output folder:\t',  text_color="black"), 
		 sg.InputText('', key='mini_juniper_folder_output'), sg.FolderBrowse(), ],
		[sg.Text('\t\t\t\t\t\t\t'),
		 sg.Button("  Convert to set   ", change_submits=True, key='mini_juniper_to_set_btn_start', button_color="blue"),],
		[sg.Text('\t\t\t\t\t\t\t'),
		 sg.Button("Remove Remarks", change_submits=True, key='mini_juniper_remove_remarks_btn_start', button_color="blue"), ],
		under_line(80),

		])

# ========================================================================
JUNIPER_FRAMES = {
	'Juniper Converter': juniper_frame(),
}