
from nettoolkit.nettoolkit.forms.formitems import *
from nettoolkit.nettoolkit_common import read_yaml_mode_us, create_folders, open_text_file
from pathlib import *
import sys

from nettoolkit.pyJuniper.juniper import Juniper


# ================================ [ Juniper ] ========================================

def mini_juniper_to_set_start(i):
	if i['mini_juniper_file_input'] == '' or i['mini_juniper_folder_output'] == '': return
	p = Path(i['mini_juniper_file_input'])
	input_file = p.name
	output_file = i['mini_juniper_folder_output'] + '/' + ".".join(input_file.split(".")[:-1]) + '.set.txt'
	J = Juniper(i['mini_juniper_file_input'], output_file)    # define a Juniper Object
	s = J.convert_to_set(to_file=True)      # convert the Juniper config to set mode.

def mini_juniper_remove_remarks_start(i):
	if i['mini_juniper_file_input'] == '' or i['mini_juniper_folder_output'] == '': return
	p = Path(i['mini_juniper_file_input'])
	input_file = p.name
	output_file = i['mini_juniper_folder_output'] + '/' + ".".join(input_file.split(".")[:-1]) + '.-remarks.txt'
	J = Juniper(i['mini_juniper_file_input'], output_file)    # define a Juniper Object
	s = J.remove_remarks(to_file=True)      # convert the Juniper config to set mode.


# ======================================================================================

JUNIPER_EVENT_FUNCS = {
	'mini_juniper_to_set_btn_start': mini_juniper_to_set_start,
	'mini_juniper_remove_remarks_btn_start': mini_juniper_remove_remarks_start,
}
JUNIPER_EVENT_UPDATERS = set()
JUNIPER_ITEM_UPDATERS = set()
JUNIPER_RETRACTABLES = {'mini_juniper_file_input', 'mini_juniper_folder_output'}

