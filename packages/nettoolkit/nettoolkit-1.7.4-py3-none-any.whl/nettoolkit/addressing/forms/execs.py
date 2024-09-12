
from nettoolkit.nettoolkit.forms.formitems import *
from nettoolkit.nettoolkit_common import read_yaml_mode_us, create_folders, open_text_file
from pathlib import *
import sys

from nettoolkit.nettoolkit_common import STR, LOG
from nettoolkit.addressing.subnetscan import Ping, compare_ping_sweeps
from nettoolkit.addressing import addressing
from nettoolkit.addressing.addressing import get_summaries, addressing, isSubset
from nettoolkit.addressing.batch import create_batch_file

# ====================================================================================

def update_cache_addressing(i): 
	update_cache(CACHE_FILE, addressing_ipscan_folder_output=i['addressing_ipscan_folder_output'])

# ================================ [ ip scanner ] ========================================

def ipscanner_start(i):
	if i['addressing_ipscan_folder_output'] == '' or i['addressing_ipscan_pfxs'] == "": return
	#
	file = 'ping_scan_result_'
	op_file = f"{STR.get_logfile_name(i['addressing_ipscan_folder_output'], file, ts=LOG.time_stamp())[:-4]}.xlsx"
	pfxs = get_list(i['addressing_ipscan_pfxs'])
	try:
		concurrent_connections = int(i['addressing_ipscan_socket'])
	except:
		concurrent_connections = 500
	#
	P = Ping(pfxs, i['addressing_ipscan_till'], concurrent_connections, i['addressing_ipscan_cb_tab'])
	P.op_to_xl(op_file)
	sg.Popup("Scan completed, \nFile write completed, \nVerify output")

def ipscanner_count_ips(obj, i):
	pfxs = i['addressing_ipscan_pfxs']
	till = i['addressing_ipscan_till']
	try:
		count = 0
		if not pfxs: return count
		hostlist = []
		pfxs = get_list(pfxs)
		for pfx in pfxs:
			subnet = addressing(pfx)
			try:
				if till:
					hosts = subnet[1:int(till)+1]
				else:
					hosts =subnet[0:len(subnet)]
			except:
				hosts =subnet[0:len(subnet)]
			hostlist.extend([host for host in hosts])
		count = len(set(hostlist))
		obj.event_update_element(addressing_ipscan_ip_count={'value': count})
	except:
		pass

def compare_scanner_outputs_exec(i):
	if i['addressing_ipscan_compare_file_1'] == '' or i['addressing_ipscan_compare_file_2'] == '': return
	compare_ping_sweeps(i['addressing_ipscan_compare_file_1'], i['addressing_ipscan_compare_file_2'])


# ================================ [ Prefixes ] ========================================

def pfxs_oper_summary_start(obj, i):
	if i['pfxs_oper_summary_input'] == '': return
	_summaries = get_summaries(*get_list(i['pfxs_oper_summary_input']))
	obj.event_update_element(pfxs_oper_summary_output={'value': "\n".join([ str(p) for p in _summaries])})	

def pfxs_oper_issubset_start(obj, i):
	if i['pfxs_oper_issubset_input_subnet'] == '' or i['pfxs_oper_issubset_input_supernet'] == '': return
	result = isSubset(i['pfxs_oper_issubset_input_subnet'], i['pfxs_oper_issubset_input_supernet'])
	if result:
		obj.event_update_element(pfxs_oper_issubset_result={'value': 'Yes', 'text_color': "green" })	
	else:
		obj.event_update_element(pfxs_oper_issubset_result={'value': 'No', 'text_color': "red" })	

def pfxs_oper_break_start(obj, i):
	if i['pfxs_oper_break_subnet'] == '' or i['pfxs_oper_break_pieces'] == '': reutrn
	ipobj = addressing(i['pfxs_oper_break_subnet'])
	result = ipobj / int(i['pfxs_oper_break_pieces'])
	obj.event_update_element(pfxs_oper_break_result={'value': "\n".join([ str(p) for p in result])})	



# ================================ [ Make batch ] ========================================

def batch_make_start(i):
	if (i['batch_folder_output'] == "" 
		or i['batch_pfxs'] == "" 
		or i['batch_pfx_names'] == "" 
		or i['batch_ips'] == ""
		): return

	pfxs_create_batch = get_list(i['batch_pfxs'])
	names_create_batch = get_list(i['batch_pfx_names'])
	ips_create_batch = get_list(i['batch_ips'])
	for ip in ips_create_batch:
		success = create_batch_file(pfxs_create_batch, names_create_batch, ip, i['batch_folder_output'])
	if success:
		s = 'batch file creation process complete. please verify'
		print(s)
		sg.Popup(s)
	else:
		s = 'batch file creation process encounter errors. please verify inputs'
		print(s)
		sg.Popup(s)

# ======================================================================================

ADDRESSING_EVENT_FUNCS = {
	'addressing_ipscan_btn_start': ipscanner_start,
	'addressing_ipscan_btn_count_ip': ipscanner_count_ips,
	'addressing_ipscan_folder_output': update_cache_addressing,
	'confit_cred_un': update_cache_addressing,
	'confit_cred_un': update_cache_addressing,
	'pfxs_oper_summary_btn_start': pfxs_oper_summary_start, 
	'pfxs_oper_issubset_btn_start': pfxs_oper_issubset_start,
	'pfxs_oper_break_btn_start': pfxs_oper_break_start,
	'batch_make_btn_start': batch_make_start,
	'addressing_ipscan_compare_btn_start': compare_scanner_outputs_exec,
}
ADDRESSING_EVENT_UPDATERS = { 
	'addressing_ipscan_btn_count_ip', 
	'pfxs_oper_summary_btn_start', 'pfxs_oper_issubset_btn_start', 'pfxs_oper_break_btn_start',
}
ADDRESSING_ITEM_UPDATERS = set()

ADDRESSING_RETRACTABLES = {
	'addressing_ipscan_folder_output', 'addressing_ipscan_pfxs', 'addressing_ipscan_ip_count' ,
	'batch_pfxs', 'batch_pfx_names', 'batch_ips', 
	'addressing_ipscan_compare_file_1', 'addressing_ipscan_compare_file_2',

}

