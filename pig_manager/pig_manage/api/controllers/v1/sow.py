import pecan
from pecan import rest
import wsme
from wsme import types as wtypes

from pig_manage.api import expose
from pig_manage.api.controllers import base
from pig_manage.api.controllers import collection
from pig_manage.common import exception

from pig_manage import objects

class SowsController(rest.RestController):
    """REST sow for Default section"""
    def __init__(self):
        super(SowsController, self).__init__()

    # disable the useful but fake interface
    @expose.expose(wtypes.text)
    def get_all(self):
        sow_list = {'sow': 'test'}
        return [sow_list]

    #@expose.expose(wtypes.text)
    #def get_all(self):
    #    sows = objects.Sow().list(
    #            pecan.request.context)
    #    return sows

    def post(self, network):
        sow_list = {'sow': 'test'}
        return sow_list

    @expose.expose(None, wtypes.text)
    def delete(self, fqdn):
        sow_list = {'sow': 'test'}
        return sow_list

    def patch(self, fqdn, patch):
        sow_list = {'sow': 'test'}
        return sow_list
