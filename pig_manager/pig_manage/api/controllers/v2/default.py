import pecan
from pecan import rest
import wsme
from wsme import types as wtypes

from kingcloudos.api import expose
from kingcloudos.api.controllers import base
from kingcloudos import objects

class Default(base.APIBase):

    controller_nodes = wsme.wsattr([wtypes.text], readonly=True)
    """A list of controller nodes"""

    compute_nodes = wsme.wsattr([wtypes.text], readonly=True)
    """A list of controller nodes"""

    network_nodes = wsme.wsattr([wtypes.text], readonly=True)
    """A list of controller nodes"""

    virtual_ip = wtypes.text
    """Virtual ip address"""

    zabbix_virtual_ip = wtypes.text
    """Zabbix virtual ip address"""

    dhcp_subnet = wtypes.text
    """DHCP subnet"""

    dhcp_netmask = wtypes.text
    """DHCP netmask"""

    network_vlan_ranges = wtypes.text
    """Network vlan ranges"""

    def __init__(self, **kwargs):
        self.fields = []
        for field in objects.Default.fields:
            if not hasattr(self, field):
                continue
            self.fields.append(field)
            setattr(self, field, kwargs.get(field, wtypes.Unset))

    @classmethod
    def convert(self, default):
        return Default(**default.as_dict())


class DefaultController(rest.RestController):
    """REST controller for Default section"""


    @expose.expose(Default)
    def get_all(self):
        context = pecan.request.context
        default = objects.Default.get()
        return Default.convert(default)

    @expose.expose(Default, body=wtypes.DictType(str, str))
    def patch(self, patch):
        default = objects.Default.update(patch)
        return Default.convert(default)
