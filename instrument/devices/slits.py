"""
2D slits, 4 individual motorized blades.

.. note:: The motor assignments are set in the IOC
    when loading the ``2slit.db`` database.

There are two representations of the same ``2slit.db`` database.
Choose between a hierarchical (``Optics2Slit2D_HV()``)
or flat structure (``Optics2Slit2D_InbOutBotTop()`):

* ``Optics2Slit2D_HV()`` has a hierarchical structure::

   slit1
       h
           xp, xn, size, center
       v
           xp, xn, size, center

* ``Optics2Slit2D_InbOutBotTop()`` has a flat structure::

   slit1
       top
       bot
       out
       inb
       hsize
       hcenter
       vsize
       vcenter

Coordinates of each representation (viewing from detector towards source)::

    Optics2Slit2D_HV        Optics2Slit2D_InbOutBotTop
        v.xp                        top
    h.xn    h.xp                inb     out
        v.xn                        bot

**Motor Assignments**

This information is for reference only.  The Python configuration
here does not need to know the motor assignments.  That is part
of the IOC configuration.

======   ==========  ==================
motor    position    assignment
======   ==========  ==================
m41      v.xp        Slit1V:mXp
m42      v.xn        Slit1V:mXn
m5 (!)   h.xp        Slit1H:mXp
m6 (!)   h.xn        Slit1H:mXn
======   ==========  ==================

.. warning: (!) Some motor assignments in the training IOC are misconfigured.
   The misconfiguration happens in the IOC configuration in the
   ``prjemian/custom-synapps-6.2`` docker image.
   (https://hub.docker.com/r/prjemian/custom-synapps-6.2)

   ==========   ==========  ============
   in docker    should be   assignment
   ==========   ==========  ============
   m5           m43         Slit1H:mXp
   m6           m44         Slit1H:mXn
   ==========   ==========  ============

   These assignments will be corrected in a future version of the
   docker image: ``prjemian/synapps``.

**References**

* https://github.com/epics-modules/optics/blob/master/opticsApp/Db/2slit.db
* https://bcda-aps.github.io/apstools/latest/api/synApps/_db_2slit.html#apstools.synApps.db_2slit.Optics2Slit2D_InbOutBotTop
* https://github.com/prjemian/epics-docker/tree/main/v1.1/n5_custom_synApps#motor-assignments
"""

__all__ = """
    guard_slit
""".split()

import logging
from ophyd import Component, EpicsSignal, MotorBundle, EpicsMotor
from .. import iconfig

logger = logging.getLogger(__name__)
logger.info(__file__)

# Choose between alternate interfaces to the same controls:
#from apstools.synApps import Optics2Slit2D_HV
#from apstools.synApps import Optics2Slit2D_InbOutBotTop
#IOC = iconfig.get("GP_IOC_PREFIX", "gp:")
#slit1 = Optics2Slit2D_HV(f"{IOC}Slit1", name="slit1")


class GuardSlitMotor(EpicsMotor):
    process_record = Component(EpicsSignal, ".PROC", kind="omitted")
    status_update = Component(EpicsSignal, ".STUP", kind="omitted")


class GSlitDevice(MotorBundle):
    """
    guard slits

    * aperture: (h_size, v_size)
    """
    bot  = Component(GuardSlitMotor, '12idc:m19', labels=("gslit",))
    inb  = Component(GuardSlitMotor, '12idc:m17', labels=("gslit",))
    outb = Component(GuardSlitMotor, '12idc:m18', labels=("gslit",))
    top  = Component(GuardSlitMotor, '12idc:m20', labels=("gslit",))
   
    #h_size = Component(EpicsSignal, 'usxLAX:GSlit1H:size')
    #v_size = Component(EpicsSignal, 'usxLAX:GSlit1V:size')
    #h_sync_proc = Component(EpicsSignal, 'usxLAX:GSlit1H:sync.PROC')
    #v_sync_proc = Component(EpicsSignal, 'usxLAX:GSlit1V:sync.PROC')


    def set_size(self, *args, h=None, v=None):
        """move the slits to the specified size"""
        if h is None:
            raise ValueError("must define horizontal size")
        if v is None:
            raise ValueError("must define vertical size")
        yield from bps.mv(
            self.h_size, h,
            self.v_size, v,
        )

    def process_motor_records(self):
        yield from bps.mv(self.top.process_record, 1)
        yield from bps.mv(self.outb.process_record, 1)
        yield from bps.sleep(0.05)
        yield from bps.mv(self.bot.process_record, 1)
        yield from bps.mv(self.inb.process_record, 1)
        yield from bps.sleep(0.05)


guard_slit = GSlitDevice('', name='guard_slit')
sd.baseline.append(guard_slit)
