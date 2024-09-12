

# ---------------------------------------------------------------------------------------
#
#
from nettoolkit.capture_it.forms.frames import CAPTUREIT_FRAMES
from nettoolkit.facts_finder.forms.frames import FACTSFINDER_FRAMES
from nettoolkit.j2config.forms.frames import J2CONFIG_FRAMES
from nettoolkit.pyVig.forms.frames import PYVIG_FRAMES
from nettoolkit.configure.forms.frames import CONFIGURE_FRAMES
from nettoolkit.addressing.forms.frames import ADDRESSING_FRAMES
from nettoolkit.pyJuniper.forms.frames import JUNIPER_FRAMES
from nettoolkit.pyNetCrypt.forms.frames import CRYPT_FRAMES
#
#
from nettoolkit.compare_it.forms.compare_configs import *
#
#
# ---------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------
FRAMES = {}
FRAMES.update(CRYPT_FRAMES)
FRAMES.update(ADDRESSING_FRAMES)
FRAMES.update(JUNIPER_FRAMES)
FRAMES.update(CAPTUREIT_FRAMES)
FRAMES.update(FACTSFINDER_FRAMES)
FRAMES.update(J2CONFIG_FRAMES)
FRAMES.update(PYVIG_FRAMES)
FRAMES.update(CONFIGURE_FRAMES)
# ---------------------------------------------------------------------------------------

__all__ = [FRAMES]