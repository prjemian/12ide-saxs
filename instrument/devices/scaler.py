"""
example scaler
"""

__all__ = """
    scaler1
    timebase IC IC2 BS
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
    scaler1.channels.chan02.chname.put("IC")
    scaler1.channels.chan03.chname.put("IC2")
    scaler1.channels.chan04.chname.put("BS")
    scaler1.channels.chan05.chname.put("If")
    time.sleep(1)  # wait for IOC

# choose just the channels with EPICS names
scaler1.select_channels()

# examples: make shortcuts to specific channels assigned in EPICS

timebase = scaler1.channels.chan01.s
IC = scaler1.channels.chan02.s
IC2 = scaler1.channels.chan03.s
BS = scaler1.channels.chan04.s


for item in (timebase, IC, IC2, BS):
    item._ophyd_labels_ = set(["channel", "counter"])
