import pecan
from pecan import rest
import wsme
from wsme import types as wtypes

from kingcloudos.api import expose
from kingcloudos.api.controllers import base
from kingcloudos.api.controllers import collection
from kingcloudos import objects
from kingcloudos.api.controllers.v1 import node
from kingcloudos.common import exception


class NetworkCollection(collection.Collection):

    networks = [node.Node]

    def __init__(self, **kwargs):
        self._type = 'networks'

    @staticmethod
    def convert(networks):
        collection = NetworkCollection()
        collection.networks = [node.Node.convert(p)
                                  for p in networks]
        return collection


class NetworksController(rest.RestController):
    """REST network for Default section"""
    def __init__(self):
        super(NetworksController, self).__init__()


    @expose.expose(NetworkCollection)
    def get_all(self):
        networks = objects.network_obj.get_all()
        return NetworkCollection.convert(networks)

    @expose.expose(node.Node, wtypes.text)
    def get_one(self, fqdn):
        network = objects.network_obj.get_by_fqdn(fqdn)
        if network is None:
            raise exception.ResourceNotFound(name='network',
                                             id=fqdn)
        return node.Node.convert(network)


    @expose.expose(node.Node, body=node.Node, status_code=201)
    def post(self, network):
        network_dict = network.as_dict()
        for (key, value) in node.options.items():
            if not network_dict.has_key(key):
                network_dict[key] = value

        new_network = objects.Network(**network_dict)
        return node.Node.convert(objects.network_obj.create(new_network))


    @expose.expose(None, wtypes.text)
    def delete(self, fqdn):
        objects.network_obj.delete(fqdn)


    @expose.expose(node.Node, wtypes.text, body=wtypes.DictType(str,str))
    def patch(self, fqdn, patch):
        network = objects.network_obj.update(fqdn, patch)
        if network is None:
            raise exception.ResourceNotFound(name='network',
                                             id=fqdn)
        return network
