
"""
beam attenuating filters
"""

__all__ = [
    'pf4_AlTi',
    'pf4_glass',
    ]

import logging

logger = logging.getLogger(__name__)
logger.info(__file__)

from apstools.devices import DualPf4FilterBox

pf4_AlTi = DualPf4FilterBox("9idcRIO:pf4:", name="pf4_AlTi")
pf4_glass = DualPf4FilterBox("9idcRIO:pf42:", name="pf4_glass")
