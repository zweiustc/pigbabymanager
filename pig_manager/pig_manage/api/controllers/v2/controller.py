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


class ControllerCollection(collection.Collection):

    controllers = [node.Node]

    def __init__(self, **kwargs):
        self._type = 'controllers'

    @staticmethod
    def convert(controllers):
        collection = ControllerCollection()
        collection.controllers = [node.Node.convert(p)
                                  for p in controllers]
        return collection


class ControllersController(rest.RestController):
    """REST controller for Default section"""
    def __init__(self):
        super(ControllersController, self).__init__()


    @expose.expose(ControllerCollection)
    def get_all(self):
        controllers = objects.controller_obj.get_all()
        return ControllerCollection.convert(controllers)

    @expose.expose(node.Node, wtypes.text)
    def get_one(self, fqdn):
        controller = objects.controller_obj.get_by_fqdn(fqdn)
        if controller is None:
            raise exception.ResourceNotFound(name='controller',
                                             id=fqdn)
        return node.Node.convert(controller)


    @expose.expose(node.Node, body=node.Node, status_code=201)
    def post(self, controller):
        controller_dict = controller.as_dict()
        for (key, value) in node.options.items():
            if not controller_dict.has_key(key):
                controller_dict[key] = value

        new_controller = objects.Controller(**controller_dict)
        return node.Node.convert(objects.controller_obj.create(new_controller))


    @expose.expose(None, wtypes.text)
    def delete(self, fqdn):
        objects.controller_obj.delete(fqdn)


    @expose.expose(node.Node, wtypes.text, body=wtypes.DictType(str,str))
    def patch(self, fqdn, patch):
        controller = objects.controller_obj.update(fqdn, patch)
        if controller is None:
            raise exception.ResourceNotFound(name='controller',
                                             id=fqdn)
        return controller
