
from nettoolkit.nettoolkit.forms.formitems import *

# ===================================================================

def facts_finder_frame():
	"""tab display - Credential inputs

	Returns:
		sg.Frame: Frame with filter selection components
	"""    		
	return sg.Frame(title=None, 
					relief=sg.RELIEF_SUNKEN, 
					layout=[

		[sg.Text('Facts Generator', font=('TimesNewRoman', 12), text_color="black") ],

		[sg.Text('log files', text_color="black"), 
			sg.InputText('', key='ff_log_files'), sg.FilesBrowse(key='ff_log_files_btn') ],
		under_line(80),
		[sg.Text('Options',  font=('TimesNewRoman', 12), text_color="black") ],

		[sg.Checkbox('convert to capture_it ', key='ff_convert_to_cit', default=True, text_color='black')],
		[sg.Checkbox('remove backup/tmp file', key='ff_remove_cit_bkp', default=True, text_color='black')],
		[sg.Checkbox('skip parsed excel outputs', key='ff_skip_txtfsm', default=True, text_color='black')],
		[sg.Text('clean file suffix', text_color="black"),  sg.InputText('-clean', key='ff_new_suffix',),],
		[sg.Text('',) ],
		[sg.Text('Custom Package Yaml file:\t', text_color="black"), 
	     sg.InputText(get_cache(CACHE_FILE, 'cit_file_custom_yml'), key='ff_file_custom_yml', change_submits=True,), 
	     sg.FileBrowse(button_color="grey"), ],
		under_line(80),


		[sg.Text('\t\t\t\t\t\t\t\t\t'),
		 sg.Button("Facts-Finder", change_submits=True, key='ff_btn_start', button_color="blue"),],

		])


FACTSFINDER_FRAMES = {
	'Facts-Finder': facts_finder_frame(),
}