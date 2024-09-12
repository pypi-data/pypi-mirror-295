
from nettoolkit.capture_it.forms.execs import CAPTUREIT_RETRACTABLES
from nettoolkit.facts_finder.forms.execs import FACTSFINDER_RETRACTABLES
from nettoolkit.j2config.forms.execs import J2CONFIG_RETRACTABLES
from nettoolkit.pyVig.forms.execs import PYVIG_RETRACTABLES
from nettoolkit.configure.forms.execs import CONFIGURE_RETRACTABLES
from nettoolkit.addressing.forms.execs import ADDRESSING_RETRACTABLES
from nettoolkit.pyJuniper.forms.execs import JUNIPER_RETRACTABLES
from nettoolkit.pyNetCrypt.forms.execs import CRYPT_RETRACTABLES

# -------------------------------------------------------------------------
RETRACTABLES = set()
RETRACTABLES = RETRACTABLES.union(CRYPT_RETRACTABLES)
RETRACTABLES = RETRACTABLES.union(ADDRESSING_RETRACTABLES)
RETRACTABLES = RETRACTABLES.union(JUNIPER_RETRACTABLES)
RETRACTABLES = RETRACTABLES.union(CAPTUREIT_RETRACTABLES)
RETRACTABLES = RETRACTABLES.union(FACTSFINDER_RETRACTABLES)
RETRACTABLES = RETRACTABLES.union(J2CONFIG_RETRACTABLES)
RETRACTABLES = RETRACTABLES.union(PYVIG_RETRACTABLES)
RETRACTABLES = RETRACTABLES.union(CONFIGURE_RETRACTABLES)
# -------------------------------------------------------------------------

__all__ = [RETRACTABLES]