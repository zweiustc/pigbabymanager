import wsme
from wsme import types as wtypes

from kingcloudos.api.controllers import base
from kingcloudos import objects
from kingcloudos.api.controllers.v1 import types

options = { 'kdfs_disks': [],
            'state': '',
            'extnet_nic': '',
            'datanet_nic': '',
            'mgmtnet_nic': '',}

class Node(base.APIBase):

    my_fqdn_long  = wtypes.text
    """Node long fqdn"""

    my_ip = wtypes.text
    """Node ip address"""

    my_fqdn = wtypes.text
    """Node fqdn"""

    mac = wtypes.text
    """Node mac address"""

    kdfs_gateway_counts = wsme.wsattr(wtypes.IntegerType(minimum=1), default=1)
    """kdfs gateway counts"""

    kdfs_enable_ioaddr = wsme.wsattr(types.boolean)
    """kdfs enable ioaddr"""

    mgmtnet_nic = wtypes.text
    """management nic name"""

    datanet_nic = wtypes.text
    """data nic name"""

    extnet_nic = wtypes.text
    """external nic name"""

    state = wtypes.text
    """state of this node"""

    def __init__(self, **kwargs):
        self.fields = []
        for field in objects.Node.fields:
            if not hasattr(self, field):
                continue
            self.fields.append(field)
            setattr(self, field, kwargs.get(field, wtypes.Unset))

    @classmethod
    def convert(self, node):
        return Node(**node.as_dict())
