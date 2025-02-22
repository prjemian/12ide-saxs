"""
local, custom Device definitions
"""

# from ophyd.log import config_ophyd_logging
# config_ophyd_logging(level="DEBUG")
#     # 'ophyd' — the logger to which all ophyd log records propagate
#     # 'ophyd.objects' — logs records from all devices and signals (that is, OphydObject subclasses)
#     # 'ophyd.control_layer' — logs requests issued to the underlying control layer (e.g. pyepics, caproto)
#     # 'ophyd.event_dispatcher' — issues regular summaries of the backlog of updates from the control layer that are being processed on background threads

from .aps_source import *
from .aps_undulator import *
from .monochromator import *
from .shutters import *
from .stages import *
from .scaler import *
from .struck3820 import *

# from .area_detector import *
# from .calculation_records import *
# from .fourc_diffractometer import *
# from .ioc_stats import *
# from .motors import *
# from .noisy_detector import *
# from .scaler import *
# from .shutter_simulator import *
# from .simulated_fourc import *
# from .simulated_kappa import *
# from .slits import *
# from .sixc_diffractometer import *
# from .temperature_signal import *