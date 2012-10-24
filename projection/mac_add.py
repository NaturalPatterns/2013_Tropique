# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 11:10:59 2012

@author: tropic
"""

from SystemConfiguration import *    # from pyObjC
import socket

def GetIPv4Addresses():
    """
    Get all IPv4 addresses assigned to local interfaces.
    Returns a generator object that produces information
    about each IPv4 address present at the time that the
    function was called.

    For each IPv4 address, the returned generator yields
    a tuple consisting of the interface name, address
    family (always socket.AF_INET), the IP address, and
    the netmask.  The tuple elements may also be accessed
    by the names: "ifname", "family", "address", and
    "netmask".
    """
    ds = SCDynamicStoreCreate(None, 'GetIPv4Addresses', None, None)
    # Get all keys matching pattern State:/Network/Service/[^/]+/IPv4
    pattern = SCDynamicStoreKeyCreateNetworkServiceEntity(None,
                                                          kSCDynamicStoreDomainState,
                                                          kSCCompAnyRegex,
                                                          kSCEntNetIPv4)
    patterns = CFArrayCreate(None, (pattern, ), 1, kCFTypeArrayCallBacks)
    valueDict = SCDynamicStoreCopyMultiple(ds, None, patterns)

    ipv4info = namedtuple('ipv4info', 'ifname family address netmask')

    for serviceDict in valueDict.values():
        ifname = serviceDict[u'InterfaceName']
        for address, netmask in zip(serviceDict[u'Addresses'], serviceDict[u'SubnetMasks']):
            yield ipv4info(ifname, socket.AF_INET, address, netmask)