# --------------------------------------------
# IMPORTS
# --------------------------------------------
import pandas as pd
from collections import OrderedDict
from dataclasses import dataclass
from nettoolkit.nettoolkit_db import write_to_xl

# -----------------------------------------------------------------------------
# STATIC VAR
# -----------------------------------------------------------------------------
BANNER = '> ~~~ RAW COMMANDS CAPTURE SUMMARY (aholo2000@gmail.com) ~~~ <'

# -----------------------------------------------------------------------------
# LogSummary Class
# -----------------------------------------------------------------------------

class LogSummary():
	"""class generating summary report for the commands log/raw capture

	Args:
		c (conn): connection object
		on_screen_display (bool, optional): display result summary on screen. Defaults to False.
		write_to (str, optional): filename, writes result summary to file. Defaults to None(i.e. off).
	"""	

	def __init__(self, c, 
		split_cisco_juniper=True,
		on_screen_display=False, 
		write_to=None, 
		):
		"""class instance initializer

		Args:
			c (conn): connection object
			print (bool, optional): display result summary on screen. Defaults to False.
			write_to (str, optional): filename, writes result summary to file. Defaults to None(i.e. off).
		"""		
		self.s = ""
		self.cmd_exec_logs_all = c.cmd_exec_logs_all
		self.set_cmd_listd_dict(c)
		self.device_type_all = c.device_type_all
		self.host_vs_ips = c.host_vs_ips
		#
		self.trim_juniper_no_more()
		self.hosts = self.cmd_exec_logs_all.keys()
		self.add_trailing_space_to_row_items()
		self.add_trailing_space_to_result()
		if split_cisco_juniper: self.split_device_type_wise()
		self.s = self.concate_row_col_data()
		if on_screen_display is True: self.print()
		if write_to: self.write(write_to, wa='w')

	def set_cmd_listd_dict(self, c):
		"""set command list dictionary for all commands executed for a given connection

		Args:
			c (conn): connection object
		"""		
		self.cmd_list_dict = c.all_cmds
		try:
			self.cmd_list_dict = { dt: sorted(list(set(cmds))) for dt, cmds in c.all_cmds.items() }
		except:
			pass

	@property
	def summary(self):
		"""report summary

		Returns:
			str: Multiline report summary
		"""		
		banner = f'! {"="*len(BANNER)} !\n  {BANNER}  \n! {"="*len(BANNER)} !\n'
		return banner+self.s

	def print(self):
		"""prints report summary on screen
		"""		
		print(self.summary)

	def write(self, file, wa='w'):
		"""writes result summary to file

		Args:
			file (str): filename to write to output result summary
		"""		
		try:
			with open(file, wa) as f:
				f.write(self.s)
				print(f'Info:\tcommands capture log write to {file}.. done')
		except:
			print(f'Info:\tcommands capture log write to {file}.. failed')

	def trim_juniper_no_more(self):
		"""trip juniper commands by removing no-more word
		"""		
		for host, cmd_exec_logs in self.cmd_exec_logs_all.items():
			for i, item in enumerate(cmd_exec_logs):
				item['command'] = item['command'].replace("| no-more ", "")

	def get_raw_log(self, host_cmd_exec_log, cmd):
		"""get raw log of given command from provided host command execution log list.

		Args:
			host_cmd_exec_log (list): command execution log list of a host
			cmd (str): command for which raw log requires to be returned

		Returns:
			str: returns `success` if raw log was successful else `failed`.  returns `undefined` if undetected or else.
		"""		
		for item in host_cmd_exec_log:
			if item['command'] == cmd:
				if item['raw'] is True:
					return "success"
				elif  item['raw'] is False:
					return "failed"
				else:
					return "undefined"
		return ""

	def get_raw_logs(self, hostname):
		"""get all commands raw logs for given device(hostname)

		Args:
			hostname (str): hostname for which raw logs to be retuned

		Returns:
			list: list of raw log entries
		"""		
		host_cmd_exec_log = self.cmd_exec_logs_all[hostname]
		logs = []
		cmd_list = self.cmd_list_dict[self.device_type_all[hostname]]
		for cmd in cmd_list:
			logs.append(self.get_raw_log(host_cmd_exec_log, cmd))
		return logs


	def get_all_raw_logs(self):
		"""get raw logs for all devices

		Returns:
			dict: dictionary of {device_hostname: raw_log_entries}
		"""		
		logs = OrderedDict()
		for host in self.hosts:
			logs[host] = self.get_raw_logs(host)
		return logs

	def get_max_cmd_length(self, cmd_list):
		"""returns maximum command length from provided cmd_list

		Args:
			cmd_list (list): list of commands

		Returns:
			int: length of maximum length command
		"""		
		max_len = 0
		for cmd in cmd_list:
			cmd_len = len(cmd)
			if cmd_len > max_len:
				max_len = cmd_len
		if max_len<=11: max_len=11
		return max_len

	def add_trailing_space_to_row_items(self):
		"""adds trailing spaces to commands to make all same length. stores them in new trailing_cmd_dict dictionary
		"""		
		self.trailing_cmd_dict = {}
		for dev_type, cmd_list in self.cmd_list_dict.items():
			max_len = self.get_max_cmd_length(cmd_list)
			doubleline = f'+ {"="*max_len} +'
			trailing_cmd_list = [ doubleline, f'| hosts     >{" "*(max_len-11)} |', ]
			trailing_cmd_list.extend([f'| commands V{" "*(max_len-10)} |', doubleline])
			for cmd in cmd_list:
				cmd_len = len(cmd)
				spaces = max_len - cmd_len
				trailing_cmd_list.append(f'| {cmd}{" "*spaces} |')
			trailing_cmd_list.append(doubleline)
			self.trailing_cmd_dict[dev_type] = trailing_cmd_list

	def get_ip(self, hostname, d):
		"""returns ip address of asked hostname from provided dictionary d 

		Args:
			hostname (str): hostname of device
			d (dict): dictionary of all raw logs

		Returns:
			str: ip address for given hostname
		"""		
		return self.host_vs_ips[hostname]

	def add_trailing_space_to_result(self):
		"""adds trailing spaces to results to make all same length. stores them in new trailing_results_dict dictionary 
		"""		
		d = self.get_all_raw_logs()
		max_len_static = 9
		self.trailing_results_dict = {}
		for hn, cmd_results in d.items():
			ip = self.get_ip(hn, d)
			max_len = len(hn) if len(hn) > max_len_static else max_len_static
			if len(ip) > max_len: max_len = len(ip) 
			doubleline = f' {"="*max_len} +'
			self.trailing_results_dict[hn] = [doubleline, f' {hn}{" "*(max_len-len(hn))} |']
			self.trailing_results_dict[hn].extend([f' {ip}{" "*(max_len-len(ip))} |', doubleline])
			for cmd_reulst in cmd_results:
				spaces = max_len - len(cmd_reulst)
				self.trailing_results_dict[hn].append(f' {cmd_reulst}{" "*spaces} |')
			self.trailing_results_dict[hn].append(doubleline)


	def concate_row_col_data(self):
		"""concatenates comands and hosts data to generate string summary 

		Returns:
			str: summary report in text format
		"""		
		fs = ''
		for dev_type, devices in self.dev_type_hn_dict.items():
			s = '\n'
			s += dev_type + "\n"
			tclist = self.trailing_cmd_dict[dev_type]
			for i, cmd in enumerate(tclist):
				s += cmd
				for hn in devices:
					thlist = self.trailing_results_dict[hn]
					s += thlist[i]
				s += "\n"
			s += "\n"
			fs += s
		return fs

	def split_device_type_wise(self):
		"""distribute hosts as per device type i.e. cisco_ios, juniper_junos etc.. and stores them in a new dictionary dev_type_hn_dict dictionary.

		Returns:
			dict: device type wise dictionary {device_type: [hosts,]}
		"""		
		dev_type_hn_dict = {}		
		for hn, dev_type in self.device_type_all.items():
			if not dev_type_hn_dict.get(dev_type):
				dev_type_hn_dict[dev_type] = []
			dev_type_hn_dict[dev_type].append(hn)
		self.dev_type_hn_dict = dev_type_hn_dict
		return dev_type_hn_dict

# -----------------------------------------------------------------------------



class SummaryDisplay():

	def __init__(self, d):
		self.df = pd.DataFrame(d).fillna("")

	def show(self, rows=0, cols=0, transpose=False, sortrows=0, sortcols=0):
		if transpose: self.df = self.df.T
		if not rows: rows = len(self.df)
		self.set_col_display_options(cols)
		print(self.df.head(rows))

	def set_col_display_options(self, n):
		if n ==0: n = None
		pd.set_option('display.max_columns', n)
		pd.set_option("max_colwidth", 5)


	# def other_set_options(self):
	# 	pd.set_option('display.max_columns', None)
	# 	pd.set_option('max_columns', None)
	# 	pd.set_option("max_rows", None)
	# 	pd.set_option("max_colwidth", None)


# # ==========================================================================================
# from pprint import pprint
# import pandas as pd

# d = {
# 	'hosta': {'cmd-a': 'abfadf jklhad fdf'},
# 	'hostb': {'cmd-b': 'abfadf jklhad fdf'},
# 	'hostc': {'cmd-a': 'abfadf jklhad fdf'},
# 	'hostd': {'cmd-a': 'abfadf jklhad fdf'},
# 	'hoste': {'cmd-b': 'abfadf jklhad fdf'},
# 	'hostg': {'cmd-a': 'abfadf jklhad fdf'},
# 	'hostj': {'cmd-d': 'abfadf jklhad fdf', 'cmd-a': 'abfadf jklhad fdf',},
# 	'hostf': {'cmd-a': 'abfadf jklhad fdf'},
# 	'hosth': {'cmd-c': 'abfadf jklhad fdf', 'cmd-a': 'abfadf jklhad fdf'},
# 	'hostk': {'cmd-a': 'abfadf jklhad fdf'},
# 	'hosti': {'cmd-a': 'abfadf jklhad fdf', 'cmd-c': 'abfadf jklhad fdf'},
# 	'hostl': {'cmd-a': 'abfadf jklhad fdf'},
# 	'hostm': {'cmd-a': 'abfadf jklhad fdf'},
# }

# df = pd.DataFrame(d)


# SD = SummaryDisplay(d)
# SD.show(
# 	# rows=5,
# 	# cols=0, 
# 	# transpose=True, 
# 	sortrows=0, 
# 	sortcols=0,
# )

# # ==========================================================================================

@dataclass
class ExcelReport():
	"""class defining methods and properties to write the execution log summary report to excel

	Args:
		all_cmds (dict): 
		cmd_exec_logs_all (dict): 
		host_vs_ips (dict): 
		device_type_all (dict): 
	"""    	
	all_cmds: dict
	cmd_exec_logs_all: dict
	host_vs_ips: dict
	device_type_all: dict

	def __call__(self, transpose_report=False):
		self.split_by_device_types()
		self.get_updated_cmd_exec_log(transpose=transpose_report)

	def split_by_device_types(self):
		"""split the device based on its device types
		"""    		
		self.new_cmd_exec_log = {}
		for hn, dt in self.device_type_all.items():
			if not self.new_cmd_exec_log.get(dt): self.new_cmd_exec_log[dt]={}
			self.new_cmd_exec_log[dt][hn]={}

	def get_updated_cmd_exec_log(self, *, transpose):
		"""get the updated command execution log in DFD format to write to excel

		Args:
			transpose (bool): transpose the output in excel
		"""    		
		for dt, new_d in self.new_cmd_exec_log.items():
			for device, ip in self.host_vs_ips.items():
				if self.device_type_all[device] != dt: continue
				device_cmds = set(self.all_cmds[dt])
				dev_cmd_exist = set()
				for cmd in device_cmds:
					if not new_d.get(device): 
						new_d[device] = {}
						dev_dict = new_d[device]
					for _ in self.cmd_exec_logs_all[device]:
						if _['command'] != cmd: continue
						dev_dict[cmd] = 'success' if _['raw'] else 'failure'
						dev_cmd_exist.add(cmd) 
				for cmd in device_cmds.difference(dev_cmd_exist):
					dev_dict[cmd] = ''
			self.new_cmd_exec_log[dt] = pd.DataFrame(new_d)
			if transpose:
				self.new_cmd_exec_log[dt] = self.new_cmd_exec_log[dt].T

	def write_to(self, file):
		"""writes execution log DFD to provided excel file.

		Args:
			file (str): excel file name with full path
		"""    		
		write_to_xl(file, self.new_cmd_exec_log, overwrite=True, index=True)
		print(f"Info:	commands capture log summary write to {file}.. done")

