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


class ComputeCollection(collection.Collection):

    computes = [node.Node]

    def __init__(self, **kwargs):
        self._type = 'computes'

    @staticmethod
    def convert(computes):
        collection = ComputeCollection()
        collection.computes = [node.Node.convert(p)
                                  for p in computes]
        return collection


class ComputesController(rest.RestController):
    """REST compute for Default section"""
    def __init__(self):
        super(ComputesController, self).__init__()


    @expose.expose(ComputeCollection)
    def get_all(self):
        computes = objects.compute_obj.get_all()
        return ComputeCollection.convert(computes)

    @expose.expose(node.Node, wtypes.text)
    def get_one(self, fqdn):
        compute = objects.compute_obj.get_by_fqdn(fqdn)
        if compute is None:
            raise exception.ResourceNotFound(name='compute',
                                             id=fqdn)
        return node.Node.convert(compute)


    @expose.expose(node.Node, body=node.Node, status_code=201)
    def post(self, compute):
        compute_dict = compute.as_dict()
        for (key, value) in node.options.items():
            if not compute_dict.has_key(key):
                compute_dict[key] = value

        new_compute = objects.Compute(**compute_dict)
        return node.Node.convert(objects.compute_obj.create(new_compute))


    @expose.expose(None, wtypes.text)
    def delete(self, fqdn):
        objects.compute_obj.delete(fqdn)


    @expose.expose(node.Node, wtypes.text, body=wtypes.DictType(str,str))
    def patch(self, fqdn, patch):
        compute = objects.compute_obj.update(fqdn, patch)
        if compute is None:
            raise exception.ResourceNotFound(name='compute',
                                             id=fqdn)
        return compute
