"""
example scaler
"""

__all__ = """
    scaler1
    timebase I01 I02 ITS
""".split()

import logging

logger = logging.getLogger(__name__)

logger.info(__file__)

from .. import iconfig
from ophyd.scaler import ScalerCH
import time


IOC = iconfig.get("GP_IOC_PREFIX", "gp:")

# make an instance of the entire scaler, for general control
#scaler1 = ScalerCH(f"{IOC}scaler1", name="scaler1", labels=["scalers", "detectors"])
scaler1 = ScalerCH('12idc:scaler1', name='scaler1', labels=[])
scaler1.wait_for_connection()

if not len(scaler1.channels.chan01.chname.get()):
    # CAUTION: define channel names JUST for this simulation.
    # For a real instrument, the names are assigned when the
    # detector pulse cables are connected to the scaler channels.
    logger.info(
        f"{scaler1.name} has no channel names.  Assigning channel names."
    )
    scaler1.channels.chan01.chname.put("timebase")
    scaler1.channels.chan02.chname.put("I01")
    scaler1.channels.chan03.chname.put("I02")
    scaler1.channels.chan04.chname.put("ITS")
    time.sleep(1)  # wait for IOC

# choose just the channels with EPICS names
scaler1.select_channels()

# examples: make shortcuts to specific channels assigned in EPICS

timebase = scaler1.channels.chan01.s
I01 = scaler1.channels.chan02.s
I02 = scaler1.channels.chan03.s
ITS = scaler1.channels.chan04.s


for item in (timebase, I01, I02, ITS):
    item._ophyd_labels_ = set(["channel", "counter"])
