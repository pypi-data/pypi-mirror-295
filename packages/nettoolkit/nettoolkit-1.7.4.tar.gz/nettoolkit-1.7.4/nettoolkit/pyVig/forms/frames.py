
from nettoolkit.nettoolkit.forms.formitems import *

# ===================================================================

def pyvig_frame():
	"""tab display

	Returns:
		sg.Frame: Frame with filter selection components
	"""    		
	return sg.Frame(title=None, 
					relief=sg.RELIEF_SUNKEN, 
					layout=[

		[sg.Text('Cable Matrix & Visio Drawing Generation', font=('TimesNewRoman', 12), text_color="black") ],
		under_line(80),

		[sg.Text('clean data files:\t', text_color="black"),
		 sg.InputText('', key='pv_files_clean_data'), sg.FilesBrowse(),
		],
		[sg.Text('Stencil Folder:\t', text_color="black"),
		 sg.InputText(get_cache(CACHE_FILE, 'pv_folder_stencil'), key='pv_folder_stencil'), sg.FolderBrowse(),
		],
		[sg.Text('Default Stencil:\t', text_color="black"),
		 sg.InputText(get_cache(CACHE_FILE, 'pv_file_default_stencil'), key='pv_file_default_stencil'), sg.FileBrowse(),
		],
		[sg.Text('output folder:\t',text_color='black'), 
		 sg.InputText(get_cache(CACHE_FILE, 'pv_folder_output'), key='pv_folder_output', change_submits=True),  
		 sg.FolderBrowse(),
		],
		[sg.Text('output filename:\t', text_color="black"), 
		 sg.InputText("", key='pv_file_output_db', change_submits=True),  
		],


		[sg.Text('Custom Package Yaml file:\t  ', text_color="black"), 
	     sg.InputText(get_cache(CACHE_FILE, 'cit_file_custom_yml'), key='pv_file_custom_yml', change_submits=True,), 
	     sg.FileBrowse(button_color="grey"), ],
		under_line(80),

		[sg.Text('Add Sheet Filters (if any) - in python dictionary format', text_color='black'),], 
		[sg.Multiline("""{\n}""", 
			key='pv_custom_sheet_filters', text_color='black', size=(40,5)),], 
		[sg.Text('Options', font=('TimesNewRoman', 12), text_color="black") ],
		[sg.Checkbox('Keep All Columns\t\t', key='pv_opt_keep_all_cols', default=True, text_color='black'),],

		# ------------------------------------------------------------------------------------
		[sg.Text('\t\t\t\t\t\t\t\t'),
		 sg.Button("Cable Matrix Prepare", change_submits=True, key='pv_btn_start_cm', button_color="blue"),
		 sg.Button("Visio Generate", change_submits=True, key='pv_btn_start_visio', button_color="blue"),],

		])


PYVIG_FRAMES = {
	'Visio Drawing Generation': pyvig_frame(),
}