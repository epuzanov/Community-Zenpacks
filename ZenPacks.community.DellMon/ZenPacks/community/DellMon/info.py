################################################################################
#
# This program is part of the DellMon Zenpack for Zenoss.
# Copyright (C) 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""info.py

Representation of hardware components.

$Id: info.py,v 1.1 2010/07/07 13:42:07 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

from zope.interface import implements
from Products.Zuul.infos import ProxyProperty
from Products.Zuul.infos.component import ComponentInfo
from Products.Zuul.decorators import info
from ZenPacks.community.DellMon import interfaces


class DellStorageCntlrInfo(ComponentInfo):
    implements(interfaces.IDellStorageCntlrInfo)

    serialNumber = ProxyProperty("serialNumber")
    FWRev = ProxyProperty("FWRev")
    controllerType = ProxyProperty("controllerType")
    slot = ProxyProperty("slot")
    cacheSize = ProxyProperty("cacheSize")

    @property
    @info
    def manufacturer(self):
        pc = self._object.productClass()
        if (pc):
            return pc.manufacturer()

    @property
    @info
    def product(self):
        return self._object.productClass()

    @property
    def SWVer(self):
        return self._object.SWVer.strip('"')

    @property
    def role(self):
        return self._object.roleString()

    @property
    def status(self):
        if not hasattr(self._object, 'statusString'): return 'Unknown'
        else: return self._object.statusString()
