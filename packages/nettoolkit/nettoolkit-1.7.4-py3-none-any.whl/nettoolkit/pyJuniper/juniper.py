
# ------------------------------------------------------------------------------
from nettoolkit.nettoolkit_common.gpl import STR, IO
import os
from .hierarchy import Hierarchy 
from .jset import JSet
# ------------------------------------------------------------------------------

class Juniper():
	"""Juniper configuration file related class

	Args:
		input_file (str): _description_
		output_file (str, optional): output file name. Defaults to None.
	"""    	

	def __init__(self, input_file, output_file=None):
		"""Initialize object by giving input file name
		"""    		
		self.input_file = input_file
		self.output_file = output_file

	def _get_clean_output_file_lst(self):
		output_file_lst = []
		for line in self.input_file_lst:
			if len(line.lstrip()) > 0:
				if line.lstrip()[0] == "#": continue
				output_file_lst.append(line.rstrip("\n"))
		return output_file_lst

	def remove_remarks(self, to_file=True):
		"""remove all remark lines from config

		Args:
			to_file (bool, optional): save output to file if True. Defaults to True.

		Returns:
			lst: list of output
		"""    		
		self.input_file_lst = IO.file_to_list(self.input_file)
		output_file_lst = self._get_clean_output_file_lst()
		if to_file and self.output_file:
			IO.to_file(self.output_file, output_file_lst)
		return output_file_lst

	def convert_to_set(self, to_file=True):
		"""convert configuration to set mode

		Args:
			to_file (bool, optional): save output to file if True. Defaults to True.

		Returns:
			lst: list of output
		"""    		
		J = JSet(self.input_file)
		J.to_set
		if to_file and self.output_file:
			IO.to_file(self.output_file, J.output)
		return J.output

	def convert_to_hierarchy(self, to_file=True):
		"""convert set configuration to hiearchical configuration

		Args:
			to_file (bool, optional): save output to file if True. Defaults to True.

		Returns:
			lst: list of output
		"""    		
		H = Hierarchy(self.input_file, self.output_file)
		H.convert()
		if to_file and self.output_file:
			IO.to_file(self.output_file, H.output)
		return H.output

def convert_to_set_from_captures(conf_file, output_file=None):
	"""enhanced version of jset conversion, which identify the show configuration from multiple show output captures, captured by capture-it and convert it to set.

	Args:
		conf_file (str): configuration capture file, using capture-it
		output_file (str, optional): output file name. Defaults to None.

	Returns:
		_type_: _description_
	"""	
	with open(conf_file, 'r') as f:
		ops = f.readlines()
	toggle = False
	conflist = ""
	for line in ops:
		if line.startswith("# output for command: show configuration| no-more"):
			toggle=True
			continue
		if not toggle: continue
		if line.startswith("# output for command: "): 
			break
		conflist+=line
	_tmp_config = conf_file[:-4]+".tmp"
	with open(_tmp_config, 'w') as f:
		f.write(conflist)
	J = Juniper(_tmp_config, output_file)
	set_list = J.convert_to_set(output_file)
	os.remove(_tmp_config)
	return set_list

# ------------------------------------------------------------------------------
if __name__ == '__main__':
	pass
# ------------------------------------------------------------------------------
