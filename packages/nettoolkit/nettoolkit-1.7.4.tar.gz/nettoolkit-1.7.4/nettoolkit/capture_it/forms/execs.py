
from nettoolkit.nettoolkit.forms.formitems import *
from nettoolkit.nettoolkit_common import read_yaml_mode_us, create_folders, open_text_file
from pathlib import *
import sys

from nettoolkit.capture_it import capture, LogSummary
from nettoolkit.capture_it import quick_display

# ====================================================================================
def get_item_list(file, index=None):
	with open(file, 'r') as f:
		lns = f.readlines()
	if index is not None:
		try:
			return [line.strip().split()[index] for line in lns]
		except:
			pass
	return [ line.strip() for line in lns]
			


#### -- cache updates -- ####

def update_cache_cit(i):
	update_cache(CACHE_FILE, cit_cred_un=i['cit_cred_un'])
	update_cache(CACHE_FILE, cit_path_captures=i['cit_path_captures'])
	update_cache(CACHE_FILE, cit_path_logs=i['cit_path_logs'])
	update_cache(CACHE_FILE, cit_path_summary=i['cit_path_summary'])
	update_cache(CACHE_FILE, cit_file_hosts=i['cit_file_hosts'])
	update_cache(CACHE_FILE, cit_file_cisco=i['cit_file_cisco'])
	update_cache(CACHE_FILE, cit_file_juniper=i['cit_file_juniper'])
	update_cache(CACHE_FILE, cit_file_custom_yml=i['cit_file_custom_yml'])


def exec_cit_file_hosts_open(i):
	open_text_file(i['cit_file_hosts'])
def exec_cit_file_cisco_open(i):
	open_text_file(i['cit_file_cisco'])
def exec_cit_file_juniper_open(i):
	open_text_file(i['cit_file_juniper'])


def add_path(file):
	p = Path(file)
	_path = p.resolve().parents[0]
	sys.path.insert(len(sys.path), str(_path))

def capture_it_start(i):
	if i['cit_file_custom_yml']:
		add_path(i['cit_file_custom_yml'])
		custom =  read_yaml_mode_us(i['cit_file_custom_yml']) 
	auth = { 'un':i['cit_cred_un'], 'pw':i['cit_cred_pw'], 'en':i['cit_cred_en'] if i['cit_cred_en'] else i['cit_cred_pw'] }
	devices = get_item_list(i['cit_file_hosts'], index=0)
	cmds = {
	    'cisco_ios': get_item_list(i['cit_file_cisco']),
    	'juniper_junos': get_item_list(i['cit_file_juniper']),
	}
	cumulative = True
	if i['cit_opt_cumulative'] == 'cumulative': cumulative = True 
	elif i['cit_opt_cumulative'] == 'non-cumulative': cumulative = False
	elif i['cit_opt_cumulative'] == 'both': cumulative = 'both'
	#
	c = capture(
		ip_list=devices, 
		auth=auth, 
		cmds=cmds, 
		capture_path=i['cit_path_captures'], 
		exec_log_path=i['cit_path_logs'],
	)
	c.cumulative = cumulative
	c.forced_login = i['cit_opt_forced_login']
	c.parsed_output = False
	c.max_connections = int(i['cit_opt_max_connections'])
	c.append_capture = i['cit_opt_append']
	c.missing_captures_only = i['cit_opt_missing']
	#
	if i['cit_opt_dependent'] and i['cit_file_custom_yml']:
		try:
			c.dependent_cmds(custom_dynamic_cmd_class=custom['capture_it']['custom_dynamic_cmd_class'])
		except:
			print(f"Cutom Commands fetch fails")
	#
	if i['cit_opt_parsed_output'] and i['cit_file_custom_yml']:
		try:
			c.generate_facts(CustomDeviceFactsClass=custom['facts_finder']['CustomDeviceFactsClass'], foreign_keys=custom['facts_finder']['foreign_keys'])
		except:
			print(f"Custom Parser functions fetcg fails")
	#
	c()
	#
	c.log_summary(
		onscreen=True, 
		to_file=i['cit_path_summary'] + "/capture_it_summary_log.txt", 
		excel_report_file=i['cit_path_summary'] + "/capture_it_summary_log.xlsx",
		transpose_excel_report=i['cit_opt_summary_xpose'],
	)
	print("Capture Task(s) Complete..")



# ======================================================================================

CATPUREIT_EVENT_FUNCS = {
	'cit_cred_un': 	update_cache_cit,
	'cit_path_captures': update_cache_cit,
	'cit_path_logs': update_cache_cit,
	'cit_path_summary': update_cache_cit,
	'cit_file_hosts': update_cache_cit,
	'cit_file_cisco': update_cache_cit,
	'cit_file_juniper': update_cache_cit,
	'cit_file_custom_yml': update_cache_cit,
	'cit_btn_start': capture_it_start,
	'cit_file_hosts_open': exec_cit_file_hosts_open,
	'cit_file_cisco_open': exec_cit_file_cisco_open,
	'cit_file_juniper_open': exec_cit_file_juniper_open,
}
CAPTUREIT_EVENT_UPDATERS = set()
CAPTUREIT_ITEM_UPDATERS = set()

CAPTUREIT_RETRACTABLES = {
	'cit_cred_un', 'cit_cred_en', 'cit_cred_pw',
	'cit_path_captures', 'cit_path_summary', 'cit_path_logs',
	'cit_file_cisco', 'cit_file_juniper', 'cit_file_hosts',
}
