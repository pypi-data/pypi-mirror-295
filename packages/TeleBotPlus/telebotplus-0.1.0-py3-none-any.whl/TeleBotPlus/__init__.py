"""
\u0420\u0430\u0437\u0440\u0430\u0431\u043E\u0442\u0447\u0438\u043A: MainPlay TG
https://t.me/MainPlayCh"""

__scripts__ = []
__all__ = ["Assets", "HTML", "Lang", "TeleBotPlus", "utils"]
from . import HTML
from . import utils
from ._module_info import version as __version__
from .assets import Assets
from .lang import Lang
from .main import TeleBotPlus
__all__.sort()
