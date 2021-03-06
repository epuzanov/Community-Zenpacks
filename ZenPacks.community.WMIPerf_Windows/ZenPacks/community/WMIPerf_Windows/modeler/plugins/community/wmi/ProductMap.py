################################################################################
#
# This program is part of the WMIPerf_Windows Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""ProductMap

ProductMap finds various software packages installed on a device.

$Id: ProductMap.py,v 1.6 2010/07/23 00:06:29 egor Exp $"""

__version__ = '$Revision: 1.6 $'[11:-2]

from ZenPacks.community.WMIDataSource.WMIPlugin import WMIPlugin
from Products.DataCollector.plugins.DataMaps import MultiArgs
from Products.DataCollector.EnterpriseOIDs import EnterpriseOIDs

class ProductMap(WMIPlugin):

    maptype = "SoftwareMap"
    modname = "Products.ZenModel.Software"
    relname = "software"
    compname = "os"

    tables = {
            "Win32_Product":
                (
                "Win32_Product",
                None,
                "root/cimv2",
                    {
                    'Name':'setProductKey',
                    'Description':'_description',
                    'InstallDate':'_setInstallDate',
                    'InstallDate2':'setInstallDate',
                    'Vendor':'_vendor',
#                    'Version':'version',
                    }
                ),
            }


    def process(self, device, results, log):
        """collect WMI information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        instances = results.get("Win32_Product", None)
        if not instances: return
        rm = self.relMap()
        for instance in instances:
            try:
                if instance['setInstallDate']:
                    instance['setInstallDate'] = str(instance['setInstallDate'])
                elif instance['_setInstallDate']:
                    instance['setInstallDate'] = '%s/%s/%s 00:00:00' % (
                                                instance['_setInstallDate'][:4],
                                                instance['_setInstallDate'][4:6],
                                                instance['_setInstallDate'][6:8])
                else: instance['setInstallDate'] = '1968/01/08 00:00:00'
                om = self.objectMap(instance)
                om.id = self.prepId(om.setProductKey)
                if om._vendor: om._vendor = om._vendor.split()[0]
                if om._vendor not in EnterpriseOIDs.values():
                    om._vendor = 'Unknown'
                om.setProductKey = MultiArgs(om.setProductKey, om._vendor)
                rm.append(om)
            except AttributeError:
                continue
        return rm
