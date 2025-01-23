
"""
Bluesky plans to scan various axes and stages

NOTE:  Don't use blocking calls here
"""

__all__ = """
    empty_plan
    scan_sa_x
    """.split()

import logging

logger = logging.getLogger(__name__)
logger.info(__file__)

from bluesky import plan_stubs as bps
from ophyd import Kind
import time

#from apstools.plans import plotxy

from ..devices import scaler1 
from ..devices.stages import sample_table       
from ..devices.shutters import mono_shutter, uniblitz_shutter
from ..devices.monochromator import monochromator
from ..framework import RE, bec
from apstools.plans import lineup2
from apstools.utils import trim_plot_lines
from apstools.utils import trim_plot_by_name
from apstools.callbacks.scan_signal_statistics import SignalStatsCallback




def scan_sa_x(scan_range,numPoints,countTime, md={}):
    yield from bps.mv(
        mono_shutter, "open",
        uniblitz_shutter, "open",
        scaler1.preset_time, countTime,
        scaler1.count_mode, "OneShot",
    )
    md['plan_name'] = "scan_sa_x"
    logger.info(f"scanning axis: {sample_table.x.name}")
    #axis_start = sample_table.x.position
    scaler1.select_channels(["BS"])
    trim_plot_by_name(5)
    stats=SignalStatsCallback()
    yield from lineup2([scaler1],sample_table.x, -scan_range,scan_range,numPoints,nscans=1,signal_stats=stats, md=md)
    #print(stats.report())
    yield from bps.mv(
        uniblitz_shutter, "close",
        scaler1.count_mode, "AutoCount",
    )
    scaler1.select_channels(None)
    #if stats.analysis.success:
    #yield from bps.mv(terms.USAXS.mr_val_center, m_stage.r.position)
    #logger.info(f"final position: {m_stage.r.position}")
    #else:
    #    print(f"tune_mr failed for {stats.analysis.reasons}")  
    
def empty_plan(*args, **kwargs):
    logger.info(f"Doing nothing: args={args}, kwargs={kwargs}")
    yield from bps.null()



# def tune_dx(md={}):
#     yield from bps.mv(
#         mono_shutter, "open",
#         uniblitz_shutter, "open",
#         scaler0.preset_time, countTime,
#         scaler0.count_mode, "OneShot",
#     )
#     yield from bps.sleep(0.1)   # piezo is fast, give the system time to react
#     yield from bps.mv(scaler0.preset_time, 0.1)
#     yield from bps.mv(upd_controls.auto.mode, "manual")
#     md['plan_name'] = "tune_dx"
#     yield from IfRequestedStopBeforeNextScan()
#     logger.info(f"tuning axis: {d_stage.x.name}")
#     #axis_start = d_stage.x.position
#     yield from bps.mv(
#         mono_shutter, "open",
#         uniblitz_shutter, "open",
#     )
#     yield from autoscale_amplifiers([upd_controls, I0_controls, I00_controls])
#     trim_plot_by_name(5)
#     scaler0.select_channels(["PD_USAXS"])
#     stats=SignalStatsCallback()
#     yield from lineup2([scaler0],d_stage.x, -d_stage.x.tune_range.get(),d_stage.x.tune_range.get(),31,nscans=1,signal_stats=stats, md=md)
#     print(stats.report())
#     yield from bps.mv(
#         uniblitz_shutter, "close",
#         scaler0.count_mode, "AutoCount",
#         upd_controls.auto.mode, "auto+background",
#     )
#     scaler0.select_channels(None)
#     #if stats.analysis.success:
#     yield from bps.mv(
#         terms.USAXS.DX0, d_stage.x.position,
#     )
#     logger.info(f"final position: {d_stage.x.position}")
#     #else: 
#     #    print(f"tune_dx failed for {stats.analysis.reasons}")  



# def tune_dy(md={}):
#     yield from bps.mv(ti_filter_shutter, "open")
#     yield from bps.sleep(0.1)   # piezo is fast, give the system time to react
#     yield from bps.mv(scaler0.preset_time, 0.1)
#     yield from bps.mv(upd_controls.auto.mode, "manual")
#     md['plan_name'] = "tune_dy"
#     yield from IfRequestedStopBeforeNextScan()
#     logger.info(f"tuning axis: {d_stage.y.name}")
#     #axis_start = d_stage.y.position
#     yield from bps.mv(
#         mono_shutter, "open",
#         ti_filter_shutter, "open",
#     )
#     yield from autoscale_amplifiers([upd_controls, I0_controls, I00_controls])
#     scaler0.select_channels(["PD_USAXS"])
#     trim_plot_by_name(5)
#     stats=SignalStatsCallback()
#     yield from lineup2([scaler0],d_stage.y, -d_stage.y.tune_range.get(),d_stage.y.tune_range.get(),31,nscans=1,signal_stats=stats, md=md)
#     print(stats.report())
#     yield from bps.mv(
#         ti_filter_shutter, "close",
#         scaler0.count_mode, "AutoCount",
#         upd_controls.auto.mode, "auto+background",
#     )
#     scaler0.select_channels(None)
#     #if stats.analysis.success:
#     yield from bps.mv(terms.SAXS.dy_in, d_stage.y.position)
#     logger.info(f"final position: {d_stage.y.position}")
#     #else:
#     #    print(f"tune_dy failed for {stats.analysis.reasons}")  



# def tune_diode(md={}):
#     yield from tune_dx(md=md)
#     yield from tune_dy(md=md)



# def user_defined_settings():
#     """
#     plan: users may redefine this function to override any instrument defaults

#     This is called from beforePlan() (in 50-plans.py) at the start of
#     every batch set of measurements.  Among the many things a user might
#     override could be the default ranges for tuning various optical axes.
#     Such as::

#         a_stage.r.tuner.width = 0.01

#     NOTE:  Don't use blocking calls here

#         It is important that the user not use any blocking calls
#         such as setting or getting PVs in EPICS.  Blocking calls
#         will *block* the python interpreter for long periods
#         (such as ``time.sleep()``) or make direct calls
#         for EPICS or file I/O that interrupt how the Bluesky
#         RunEngine operates.

#         It is OK to set local python variables since these do not block.

#         Write this routine like any other bluesky plan code,
#         using ``yield from bps.mv(...)``,  ``yield from bps.sleep(...)``, ...
#     """
#     yield from bps.null()
