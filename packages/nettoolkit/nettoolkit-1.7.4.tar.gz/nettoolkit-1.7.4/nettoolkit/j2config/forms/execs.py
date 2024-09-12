
from nettoolkit.nettoolkit.forms.formitems import *
from nettoolkit.nettoolkit_common import read_yaml_mode_us, create_folders, open_text_file
from pathlib import *
import sys

from nettoolkit.j2config import PrepareConfig


# ====================================================================================

#### -- cache updates -- ####
def update_cache_j2(i):
	update_cache(CACHE_FILE, cit_file_custom_yml=i['j2_file_custom_yml'])

def add_path(file):
	sys.path.insert(len(sys.path), str(Path(file).resolve().parents[0]))


def get_custom_classes(custom):
	return {k: v for k, v in custom['j2_class_filters'].items() }

def get_custom_funcs(custom):
	return { v for k, v in custom['j2_functions_filters'].items() }


def j2config_start(i):
	if i['j2_file_custom_yml']:
		add_path(i['j2_file_custom_yml'])
		custom =  read_yaml_mode_us(i['j2_file_custom_yml']) 
	#
	regional_file = i['j2_file_regional'] if i['j2_file_regional'] else None
	regional_class = custom['j2_regional']['regional_class'] if i['j2_file_custom_yml'] else None
	#
	PrCfg = PrepareConfig(
		data_file=i['j2_file_data'],
		jtemplate_file=i['j2_file_template'],
		output_folder=i['j2_output_folder'],
		regional_file=regional_file,
		regional_class=regional_class,
	)
	custom_classes = get_custom_classes(custom)
	custom_funcs = get_custom_funcs(custom)
	#
	PrCfg.custom_class_add_to_filter(**custom_classes)
	PrCfg.custom_module_methods_add_to_filter(*custom_funcs)
	#
	PrCfg.start()

	print("Configuration Generation All Task(s) Complete..")



# ======================================================================================

J2CONFIG_EVENT_FUNCS = {
	'j2_btn_start': j2config_start,
	'j2_file_custom_yml': update_cache_j2,
}
J2CONFIG_EVENT_UPDATERS = set()
J2CONFIG_ITEM_UPDATERS = set()

J2CONFIG_RETRACTABLES = {
	'j2_file_template', 'j2_file_data', 
}

