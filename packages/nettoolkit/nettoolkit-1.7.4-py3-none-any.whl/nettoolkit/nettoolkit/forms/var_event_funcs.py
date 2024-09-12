

# ---------------------------------------------------------------------------------------
#
from .tab_event_funcs import BUTTON_PALLET_BTN_FUNCS
#
from nettoolkit.capture_it.forms.execs import CATPUREIT_EVENT_FUNCS
from nettoolkit.facts_finder.forms.execs import FACTSFINDER_EVENT_FUNCS
from nettoolkit.j2config.forms.execs import J2CONFIG_EVENT_FUNCS
from nettoolkit.pyVig.forms.execs import PYVIG_EVENT_FUNCS
from nettoolkit.configure.forms.execs import CONFIGURE_EVENT_FUNCS
from nettoolkit.addressing.forms.execs import ADDRESSING_EVENT_FUNCS
from nettoolkit.pyJuniper.forms.execs import JUNIPER_EVENT_FUNCS
from nettoolkit.pyNetCrypt.forms.execs import CRYPT_EVENT_FUNCS
#
#
#
from nettoolkit.compare_it.forms.compare_configs import *
#
#
# ---------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------
EVENT_FUNCTIONS = {}
EVENT_FUNCTIONS.update(BUTTON_PALLET_BTN_FUNCS)
EVENT_FUNCTIONS.update(CRYPT_EVENT_FUNCS)
EVENT_FUNCTIONS.update(ADDRESSING_EVENT_FUNCS)
EVENT_FUNCTIONS.update(JUNIPER_EVENT_FUNCS)
EVENT_FUNCTIONS.update(CATPUREIT_EVENT_FUNCS)
EVENT_FUNCTIONS.update(FACTSFINDER_EVENT_FUNCS)
EVENT_FUNCTIONS.update(J2CONFIG_EVENT_FUNCS)
EVENT_FUNCTIONS.update(PYVIG_EVENT_FUNCS)
EVENT_FUNCTIONS.update(CONFIGURE_EVENT_FUNCS)
# ---------------------------------------------------------------------------------------
__all__ = [EVENT_FUNCTIONS]

