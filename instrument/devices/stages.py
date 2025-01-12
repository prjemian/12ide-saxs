
"""
SAXS device stages
"""

__all__ = [
    'sample_table',     # sample table x, and y
    'gantry',           # gantry x, and y
    'saxs_bb',          # SAXS beam block X
    'waxs_bb',          # WAXS beam block X     
]


import logging

logger = logging.getLogger(__name__)
logger.info(__file__)

from ophyd import Component, MotorBundle, EpicsMotor
#from bluesky import plan_stubs as bps
# from ophyd import Kind
# from ophyd import EpicsScaler
# from ophyd.scaler import ScalerCH

from ..framework import sd


# --------------  Sample Table  -----------------------------

class SAXSSampleTable(MotorBundle):
    """SAXS sample table"""
    x = Component(EpicsMotor, '12idc:m8', labels=("Sample Table",))
    y = Component(EpicsMotor, '12idc:m7', labels=("Sample Table",))
 
# ----- end of Sample Table ------

# --------------  Gantry  -----------------------------

class Gantry(MotorBundle):
    """Gantry motions"""
    x = Component(EpicsMotor, '12idc:m5', labels=("Gantry",))
    y = Component(EpicsMotor, '12idc:m6', labels=("Gantry",))
 
# ----- end of Gantry ------

# --------------  SAXS beam block  -----------------------------
saxs_bb = EpicsMotor(
    '12idcACS1:m7',
    name='saxs_bb',
    labels=("saxs_bb", "motor"))  # SAXS beam block X
# ----- end of SAXS beam block ------
# --------------  WAXS beam block  -----------------------------
waxs_bb = EpicsMotor(
    '12idcACS1:m8',
    name='waxs_bb',
    labels=("waxs_bb", "motor"))  # WAXS beam block X
 # ----- end of WAXS beam block ------

sample_table    = SAXSSampleTable('', name='sample_table')
gantry    = Gantry('', name='Gantry')


# waxs2x = EpicsMotor(
#     'usxAERO:m7',
#     name='waxs2x',
#     labels=("waxs2", "motor"))  # WAXS2 X

for _s in (sample_table, gantry):
    sd.baseline.append(_s)

sd.baseline.append(saxs_bb)
sd.baseline.append(waxs_bb)
