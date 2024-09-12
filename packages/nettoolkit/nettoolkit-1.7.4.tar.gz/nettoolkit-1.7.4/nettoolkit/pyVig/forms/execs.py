
from nettoolkit.nettoolkit.forms.formitems import *
from nettoolkit.nettoolkit_common import read_yaml_mode_us, create_folders, open_text_file
from nettoolkit.nettoolkit_db import write_to_xl
from pathlib import *
import sys

from nettoolkit.pyVig import pyVig, CableMatrix


# ====================================================================================

#### -- cache updates -- ####
def update_cache_pyvig(i):
	update_cache(CACHE_FILE, cit_file_custom_yml=i['pv_file_custom_yml'])
	update_cache(CACHE_FILE, pv_folder_stencil=i['pv_folder_stencil'])
	update_cache(CACHE_FILE, pv_file_default_stencil=i['pv_file_default_stencil'])
	update_cache(CACHE_FILE, pv_folder_output=i['pv_folder_output'])

def add_path(file):
	sys.path.insert(len(sys.path), str(Path(file).resolve().parents[0]))

def get_filename(file):
	return Path(file).stem


def pyvig_start_cm(i):
	if i['pv_file_custom_yml']:
		add_path(i['pv_file_custom_yml'])
		custom =  read_yaml_mode_us(i['pv_file_custom_yml'])['pyvig'] 
	#
	files = i['pv_files_clean_data'].split(";")
	default_stencil = get_filename(i['pv_file_default_stencil'])
	opd = {'sheet_filters': {}}
	CM = CableMatrix(files)
	CM.custom_attributes( default_stencil=default_stencil )
	CM.custom_functions(
	  hierarchical_order=custom['custom_functions']['hierarchical_order'],
	  item=custom['custom_functions']['item'],
	)
	CM.custom_var_functions(
	  ip_address=custom['custom_var_functions']['ip_address'],
	)
	CM.run()
	CM.update(custom['update']['sheet_filter_columns_add'])
	opd['sheet_filters'] = custom['sheet_filter']['get_sheet_filter_columns'](CM.df_dict)
	opd['is_sheet_filter'] = True if opd['sheet_filters'] else False 
	#
	CM.calculate_cordinates(sheet_filter_dict=opd['sheet_filters'])
	CM.arrange_cablings(keep_all_cols=i['pv_opt_keep_all_cols'])
	opd['data_file'] = i['pv_folder_output'] + "/" + i['pv_file_output_db'] + ".xlsx"
	write_to_xl(opd['data_file'], CM.df_dict, index=False, overwrite=True)
	#
	print("Cable Matrix Preparation All Task(s) Complete..")
	return opd


def pyvig_start_visio(i):
	if i['pv_file_custom_yml']:
		add_path(i['pv_file_custom_yml'])
		custom =  read_yaml_mode_us(i['pv_file_custom_yml']) 
	#
	dic = {'stencil_folder': i['pv_folder_stencil']}
	dic['op_file'] = i['pv_folder_output'] + "/" + i['pv_file_output_db'] + ".vsdx"
	# dic['cols_to_merge'] = [ 'ip_address', 'device_model', 'serial_number', 'vlan_info' ]
	dic.update( pyvig_start_cm(i) )
	pyVig(**dic)

	print("Visio Drawing Generation All Task(s) Complete..")


# ======================================================================================

PYVIG_EVENT_FUNCS = {
	'pv_btn_start_cm': pyvig_start_cm,
	'pv_btn_start_visio': pyvig_start_visio,
	'pv_file_custom_yml': update_cache_pyvig,
	'pv_folder_stencil': update_cache_pyvig,
	'pv_file_default_stencil': update_cache_pyvig,
	'pv_folder_output': update_cache_pyvig,
}
PYVIG_EVENT_UPDATERS = set()
PYVIG_ITEM_UPDATERS = set()

PYVIG_RETRACTABLES = {
	'pv_files_clean_data', 'pv_folder_stencil', 'pv_file_default_stencil', 


}

