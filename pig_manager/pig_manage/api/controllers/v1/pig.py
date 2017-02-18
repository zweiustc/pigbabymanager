import pecan
from pecan import rest
import wsme
from wsme import types as wtypes

from pig_manage.api import expose
from pig_manage.api.controllers import base
from pig_manage.api.controllers import collection
from pig_manage.common import exception


#class PigCollection(collection.Collection):
#
#    pigs = []
#
#    def __init__(self, **kwargs):
#        self._type = 'pigs'
#
#    @staticmethod
#    def convert(pigs):
#        collection = PigCollection()
#        collection.pigs = pigs 
#        return Collection


class PigsController(rest.RestController):
    """REST pig for Default section"""
    def __init__(self):
        super(PigsController, self).__init__()


    #@expose.expose(PigCollection)
    @expose.expose(wtypes.text)
    def get_all(self):
        pig_list = {'pig': 'test'}
        return [pig_list]

    def post(self, network):
        pig_list = {'pig': 'test'}
        return pig_list

    @expose.expose(None, wtypes.text)
    def delete(self, fqdn):
        pig_list = {'pig': 'test'}
        return pig_list

    def patch(self, fqdn, patch):
        pig_list = {'pig': 'test'}
        return pig_list
