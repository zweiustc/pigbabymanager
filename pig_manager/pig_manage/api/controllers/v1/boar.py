import pecan
from pecan import rest
import wsme
from wsme import types as wtypes

from pig_manage.api import expose
from pig_manage.api.controllers import base
from pig_manage.api.controllers import collection
from pig_manage.common import exception

from pig_manage import objects


class BoarsController(rest.RestController):
    """REST boar for Default section"""
    def __init__(self):
        super(BoarsController, self).__init__()

    # disable the useful but fake interface
    @expose.expose(wtypes.text)
    def get_all(self):
        boar_list = {'boar': 'test'}
        return [boar_list]

    #@expose.expose(wtypes.text)
    #def get_all(self):
    #    boars = objects.Sow().list(
    #            pecan.request.context)
    #    return boars

    def post(self, network):
        boar_list = {'boar': 'test'}
        return boar_list

    @expose.expose(None, wtypes.text)
    def delete(self, fqdn):
        boar_list = {'boar': 'test'}
        return boar_list

    def patch(self, fqdn, patch):
        boar_list = {'boar': 'test'}
        return boar_list
