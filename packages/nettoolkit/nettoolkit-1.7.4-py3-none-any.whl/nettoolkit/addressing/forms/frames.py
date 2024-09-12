
from nettoolkit.nettoolkit.forms.formitems import *

# ============================ [ IP Scanner ] ======================================= #

def ipscanner_frame():
	"""tab display

	Returns:
		sg.Frame: Frame with filter selection components
	"""    		
	return sg.Frame(title=None, 
					relief=sg.RELIEF_SUNKEN, 
					layout=[


		[sg.Text('IP Subnet Scanner', font=('TimesNewRoman', 12), text_color="black") ],

		[sg.Text('Output folder:',  text_color="yellow"),
		 sg.InputText(get_cache(CACHE_FILE, 'addressing_ipscan_folder_output'), key='addressing_ipscan_folder_output'), sg.FolderBrowse(), ],

		[sg.Text("Prefixes", text_color="yellow")],
		[sg.Multiline("", key='addressing_ipscan_pfxs', autoscroll=True, size=(30,7), disabled=False),
		 sg.Button("Count_ips", change_submits=True, key='addressing_ipscan_btn_count_ip', button_color='grey'), 
		 sg.Text('', key="addressing_ipscan_ip_count") ],

		[sg.Text('Scan till ip: [n]', text_color="black"), 
		 sg.InputCombo(list(range(1,256)), key='addressing_ipscan_till', size=(20,1)),  
		 sg.Text('Sockets', text_color="black"), sg.InputText(500, key='addressing_ipscan_socket', size=(20,1))],  

		[sg.Checkbox('Separate tab for each subnet', key='addressing_ipscan_cb_tab', default=True, text_color='black'),
		# ------------------------------------------------------------------------------------
		 sg.Text('\t\t\t\t\t'),
		 sg.Button("IP-Scan", change_submits=True, key='addressing_ipscan_btn_start', button_color="blue"),],
		under_line(80),
		# ------------------------------------------------------------------------------------


		[sg.Text('Compare - IP Scanner Output files', font=('TimesNewRoman', 12), text_color="black") ],

		[sg.Text('Select first scanner file:\t', text_color="black"), 
		 sg.InputText(key='addressing_ipscan_compare_file_1'), sg.FileBrowse()],

		[sg.Text('Select second scanner file:\t', text_color="black"), 
		 sg.InputText(key='addressing_ipscan_compare_file_2'), sg.FileBrowse()],
		# ------------------------------------------------------------------------------------
		[sg.Text('\t\t\t\t\t\t\t\t'),
		 sg.Button("Compare scans", change_submits=True, key='addressing_ipscan_compare_btn_start', button_color="blue"),],


		])


# ============================ [ Prefix operations ] ======================================= #

def prefix_oper_frame():
	"""tab display

	Returns:
		sg.Frame: Frame with filter selection components
	"""    		
	return sg.Frame(title=None, 
					relief=sg.RELIEF_SUNKEN, 
					layout=[


		[sg.Text('Summarize Prefixes', font=('TimesNewRoman', 12), text_color="black") ],

		[sg.Text('Prefixes:\t\t\t\t\tSummaries', text_color="black"), ],
		[sg.Multiline("", key='pfxs_oper_summary_input', autoscroll=True, size=(30,5), disabled=False),
		 sg.Multiline("", key='pfxs_oper_summary_output', autoscroll=True, size=(30,5), disabled=True), ],
		[sg.Text('\t\t\t\t\t\t\t\t'),
		 sg.Button("Summarize", change_submits=True, key='pfxs_oper_summary_btn_start', button_color="blue"),],
		under_line(80),
		# ------------------------------------------------------------------------------------
		[sg.Text('Break Prefix', font=('TimesNewRoman', 12), text_color="black") ],

		[sg.Text('Subnet:', text_color="black"), 
		 sg.InputText(key='pfxs_oper_break_subnet', size=(15,1)),
		 sg.Text('devide by [/n]:', text_color="black"),
		 sg.InputCombo(list(range(1,256)), key='pfxs_oper_break_pieces', size=(4,1)),],
		[sg.Text('Result:', text_color="black"),
		 sg.Multiline("", key='pfxs_oper_break_result', autoscroll=True, size=(20,5), disabled=True),], 
		[sg.Text('\t\t\t\t\t\t\t\t'),
		 sg.Button("  Break  ", change_submits=True, key='pfxs_oper_break_btn_start', button_color="blue"),],
		under_line(80),
		# ------------------------------------------------------------------------------------
		[sg.Text('Check - Is Subset', font=('TimesNewRoman', 12), text_color="black") ],

		[sg.Text('Subnet:', text_color="yellow"), 
		 sg.InputText(key='pfxs_oper_issubset_input_subnet', size=(15,1)),], 
		[sg.Text('Supernet:', text_color="yellow"), 
		 sg.InputText(key='pfxs_oper_issubset_input_supernet', size=(15,1)),], 
		[sg.Text('Result:', text_color="black"),
		 sg.InputText('', key='pfxs_oper_issubset_result' , size=(5,1),  text_color="black")], 
		[sg.Text('\t\t\t\t\t\t\t\t'),
		 sg.Button("Is Subset?", change_submits=True, key='pfxs_oper_issubset_btn_start', button_color="blue"),],
		under_line(80),

		])


# ============================ [ make batch ] ======================================= #

def make_batch_frame():
	"""tab display

	Returns:
		sg.Frame: Frame with filter selection components
	"""    		
	return sg.Frame(title=None, 
					relief=sg.RELIEF_SUNKEN, 
					layout=[


		[sg.Text('Make Batch', font=('TimesNewRoman', 12), text_color="black") ],

		[sg.Text('output folder:', text_color="black"), 
		 sg.InputText('', key='batch_folder_output'), sg.FolderBrowse(),],
		
		[sg.Column([
		  [sg.Text("Prefixes", text_color="black"),],
		  [sg.Multiline("", key='batch_pfxs', autoscroll=True, size=(25,5), disabled=False),],
		  # [sg.Text("Example: \n10.10.10.0/24\n10.10.30.0/24,10.10.50.0/25")],
		 ]),
 
		 sg.Column([
		  [sg.Text("Names", text_color="black")],
		  [sg.Multiline("", key='batch_pfx_names', autoscroll=True, size=(25,5), disabled=False) ],
		  # [sg.Text("Example: \nVlan-1\nVlan-2,Loopback0")],
		 ]),

		 sg.Column([
		  [sg.Text("IP(s)", text_color="black")],
		  [sg.Multiline("", key='batch_ips', autoscroll=True, size=(10,5), disabled=False) ],
		  # [sg.Text("Example: \n1\n3,4,5")],
		 ]),
		],

		[sg.Text("Length of Prefixes and Prefix Names entries must match exactly", text_color="black")],
		[sg.Text("Entries can be line(Enter) or comma(,) separated", text_color="black")],

		[sg.Text('\t\t\t\t\t\t\t\t'),
		 sg.Button("Make Batch", change_submits=True, key='batch_make_btn_start', button_color="blue"),],
		under_line(80),

		])





# ========================================================================
ADDRESSING_FRAMES = {
	'IP Scanner': ipscanner_frame(),
	'Prefix Operations': prefix_oper_frame(),
	'Ping Batch': make_batch_frame(),
}