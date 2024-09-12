
from nettoolkit.capture_it.forms.execs import CAPTUREIT_ITEM_UPDATERS
from nettoolkit.facts_finder.forms.execs import FACTSFINDER_ITEM_UPDATERS
from nettoolkit.j2config.forms.execs import J2CONFIG_ITEM_UPDATERS
from nettoolkit.pyVig.forms.execs import PYVIG_ITEM_UPDATERS
from nettoolkit.configure.forms.execs import CONFIGURE_ITEM_UPDATERS
from nettoolkit.addressing.forms.execs import ADDRESSING_ITEM_UPDATERS
from nettoolkit.pyJuniper.forms.execs import JUNIPER_ITEM_UPDATERS
from nettoolkit.pyNetCrypt.forms.execs import CRYPT_ITEM_UPDATERS

# ---------------------------------------------------------------------------------------
EVENT_ITEM_UPDATORS = set()
EVENT_ITEM_UPDATORS = EVENT_ITEM_UPDATORS.union(CRYPT_ITEM_UPDATERS)
EVENT_ITEM_UPDATORS = EVENT_ITEM_UPDATORS.union(ADDRESSING_ITEM_UPDATERS)
EVENT_ITEM_UPDATORS = EVENT_ITEM_UPDATORS.union(JUNIPER_ITEM_UPDATERS)
EVENT_ITEM_UPDATORS = EVENT_ITEM_UPDATORS.union(CAPTUREIT_ITEM_UPDATERS)
EVENT_ITEM_UPDATORS = EVENT_ITEM_UPDATORS.union(FACTSFINDER_ITEM_UPDATERS)
EVENT_ITEM_UPDATORS = EVENT_ITEM_UPDATORS.union(J2CONFIG_ITEM_UPDATERS)
EVENT_ITEM_UPDATORS = EVENT_ITEM_UPDATORS.union(PYVIG_ITEM_UPDATERS)
EVENT_ITEM_UPDATORS = EVENT_ITEM_UPDATORS.union(CONFIGURE_ITEM_UPDATERS)		
# ---------------------------------------------------------------------------------------


__all__ = [EVENT_ITEM_UPDATORS]