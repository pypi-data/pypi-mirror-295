
from nettoolkit.capture_it.forms.execs import CAPTUREIT_EVENT_UPDATERS
from nettoolkit.facts_finder.forms.execs import FACTSFINDER_EVENT_UPDATERS
from nettoolkit.j2config.forms.execs import J2CONFIG_EVENT_UPDATERS
from nettoolkit.pyVig.forms.execs import PYVIG_EVENT_UPDATERS
from nettoolkit.configure.forms.execs import CONFIGURE_EVENT_UPDATERS
from nettoolkit.addressing.forms.execs import ADDRESSING_EVENT_UPDATERS
from nettoolkit.pyJuniper.forms.execs import JUNIPER_EVENT_UPDATERS
from nettoolkit.pyNetCrypt.forms.execs import CRYPT_EVENT_UPDATERS


# ---------------------------------------------------------------------------------------
EVENT_UPDATORS = set()
EVENT_UPDATORS = EVENT_UPDATORS.union(CRYPT_EVENT_UPDATERS)
EVENT_UPDATORS = EVENT_UPDATORS.union(ADDRESSING_EVENT_UPDATERS)
EVENT_UPDATORS = EVENT_UPDATORS.union(JUNIPER_EVENT_UPDATERS)
EVENT_UPDATORS = EVENT_UPDATORS.union(CAPTUREIT_EVENT_UPDATERS)
EVENT_UPDATORS = EVENT_UPDATORS.union(FACTSFINDER_EVENT_UPDATERS)
EVENT_UPDATORS = EVENT_UPDATORS.union(J2CONFIG_EVENT_UPDATERS)
EVENT_UPDATORS = EVENT_UPDATORS.union(PYVIG_EVENT_UPDATERS)
EVENT_UPDATORS = EVENT_UPDATORS.union(CONFIGURE_EVENT_UPDATERS)		
# ---------------------------------------------------------------------------------------


__all__ = [EVENT_UPDATORS]