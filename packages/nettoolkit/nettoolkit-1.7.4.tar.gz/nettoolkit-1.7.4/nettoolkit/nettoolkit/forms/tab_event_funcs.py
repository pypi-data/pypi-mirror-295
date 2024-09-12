
# ---------------------------------------------------------------------------------------
from collections import OrderedDict
from nettoolkit.capture_it.forms.frames import CAPTUREIT_FRAMES
from nettoolkit.facts_finder.forms.frames import FACTSFINDER_FRAMES
from nettoolkit.j2config.forms.frames import J2CONFIG_FRAMES
from nettoolkit.pyVig.forms.frames import PYVIG_FRAMES
from nettoolkit.configure.forms.frames import CONFIGURE_FRAMES
from nettoolkit.addressing.forms.frames import ADDRESSING_FRAMES
from nettoolkit.pyJuniper.forms.frames import JUNIPER_FRAMES
from nettoolkit.pyNetCrypt.forms.frames import CRYPT_FRAMES

# ---------------------------------------------------------------------------------------
#   ADD ANY NEW SERVICE BUTTON HERE 
# ---------------------------------------------------------------------------------------
BUTTUN_PALLETE_NAMES = OrderedDict()
BUTTUN_PALLETE_NAMES["Addressing"] = 'btn_addressing'
BUTTUN_PALLETE_NAMES["Capture-IT"] = 'btn_captureit'
BUTTUN_PALLETE_NAMES["Configure"] = 'btn_configure'	
BUTTUN_PALLETE_NAMES["Config Gen"] = 'btn_j2config'
BUTTUN_PALLETE_NAMES["Crypt"] = 'btn_cryptology'
BUTTUN_PALLETE_NAMES["Facts"] = 'btn_factsfinder'
BUTTUN_PALLETE_NAMES["Juniper"] = 'btn_juniper'
BUTTUN_PALLETE_NAMES["Visio Gen"] = 'btn_pyvig'
TAB_EVENT_UPDATERS = set(BUTTUN_PALLETE_NAMES.values())
#
# ---------------------------------------------------------------------------------------
ALL_TABS = set()
ALL_TABS = ALL_TABS.union(ADDRESSING_FRAMES.keys())
ALL_TABS = ALL_TABS.union(JUNIPER_FRAMES.keys())
ALL_TABS = ALL_TABS.union(CRYPT_FRAMES.keys())
ALL_TABS = ALL_TABS.union(CAPTUREIT_FRAMES.keys())
ALL_TABS = ALL_TABS.union(FACTSFINDER_FRAMES.keys())
ALL_TABS = ALL_TABS.union(J2CONFIG_FRAMES.keys())
ALL_TABS = ALL_TABS.union(PYVIG_FRAMES.keys())
ALL_TABS = ALL_TABS.union(CONFIGURE_FRAMES.keys())

# ---------------------------------------------------------------------------------------

def enable_disable(obj, * , group, group_frames, all_tabs, event_updaters):
	"""enable/disable provided object frames

	Args:
		obj (NGui): NGui class instance object
		group (str): button group key, which is to enabled.
		group_frames (list): list of frames to be enabled
		all_tabs (set): set of all frames keys
		event_updaters (set): set of Button pallet names button keys
	"""	
	tabs_to_disable = all_tabs.difference(group_frames)
	buttons_to_rev = event_updaters.difference(group)
	for tab in tabs_to_disable:
		d = {tab: {'visible':False}}
		obj.event_update_element(**d)	
	for i, tab in enumerate(group_frames):
		e = {tab: {'visible':True}}
		obj.event_update_element(**e)
		if i ==0: obj.w[tab].select()
	if group:
		for tab in buttons_to_rev:
			e = {tab: {'button_color': 'gray'}}
			obj.event_update_element(**e)
		e = {group: {'button_color': 'blue'}}
		obj.event_update_element(**e)



# ---------------------------------------------------------------------------------------
#  ADD / EDIT FRAMES UPDATE HERE
#

def btn_addressing_exec(obj):
	enable_disable(obj, group_frames=ADDRESSING_FRAMES.keys(), group='btn_addressing', all_tabs=ALL_TABS, event_updaters=TAB_EVENT_UPDATERS)

def btn_juniper_exec(obj):
	enable_disable(obj, group_frames=JUNIPER_FRAMES.keys(), group='btn_juniper', all_tabs=ALL_TABS, event_updaters=TAB_EVENT_UPDATERS)

def btn_cryptology_exec(obj):
	enable_disable(obj, group_frames=CRYPT_FRAMES.keys(), group='btn_cryptology', all_tabs=ALL_TABS, event_updaters=TAB_EVENT_UPDATERS)

def btn_captureit_exec(obj):
	enable_disable(obj, group_frames=CAPTUREIT_FRAMES.keys(), group='btn_captureit', all_tabs=ALL_TABS, event_updaters=TAB_EVENT_UPDATERS)

def btn_factsfinder_exec(obj):
	enable_disable(obj, group_frames=FACTSFINDER_FRAMES.keys(), group='btn_factsfinder', all_tabs=ALL_TABS, event_updaters=TAB_EVENT_UPDATERS)

def btn_j2config_exec(obj):
	enable_disable(obj, group_frames=J2CONFIG_FRAMES.keys(), group='btn_j2config', all_tabs=ALL_TABS, event_updaters=TAB_EVENT_UPDATERS)

def btn_pyvig_exec(obj):
	enable_disable(obj, group_frames=PYVIG_FRAMES.keys(), group='btn_pyvig', all_tabs=ALL_TABS, event_updaters=TAB_EVENT_UPDATERS)

def btn_configure_exec(obj):
	enable_disable(obj, group_frames=CONFIGURE_FRAMES.keys(), group='btn_configure', all_tabs=ALL_TABS, event_updaters=TAB_EVENT_UPDATERS)


BUTTON_PALLET_BTN_FUNCS = {
	'btn_captureit': btn_captureit_exec,
	'btn_factsfinder': btn_factsfinder_exec,
	'btn_j2config': btn_j2config_exec,
	'btn_pyvig': btn_pyvig_exec,
	'btn_configure': btn_configure_exec,
	'btn_addressing': btn_addressing_exec,
	'btn_juniper': btn_juniper_exec,
	'btn_cryptology': btn_cryptology_exec,
}

# ---------------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Main Function
# ------------------------------------------------------------------------------
if __name__ == '__main__':
	pass
# ------------------------------------------------------------------------------
