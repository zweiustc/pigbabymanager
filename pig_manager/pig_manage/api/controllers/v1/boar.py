import pecan
from pecan import rest
import wsme
from wsme import types as wtypes

from pig_manage.api import expose
from pig_manage.api.controllers import base
from pig_manage.api.controllers import collection
from pig_manage.common import exception

from pig_manage import objects


class Boar(base.APIBase):
    id = wtypes.text
    ear_tag = wtypes.text
    ear_lack = wtypes.text
    #birthday = wtypes.datetime
    #entryday = wtypes.datetime
    birthday = wtypes.text
    entryday = wtypes.text

    dormitory_id = wtypes.text
    category_id = wtypes.text
    breed_num = wtypes.IntegerType
    breed_acceptability = wtypes.text
    source_id = wtypes.text

    def __init__(self, **kwargs):
        self.fields = []
        for field in objects.Boar.fields:
            if not hasattr(self, field):
                continue
            self.fields.append(field)
            setattr(self, field, kwargs.get(field, wtypes.Unset))

    @classmethod
    def convert(self, boar):
        return Boar(**boar.as_dict())


class BoarCollection(collection.Collection):

    boars = [Boar]

    def __init__(self, **kwargs):
        self._type = 'boars'

    @staticmethod
    def convert(boars):
        collection = BoarCollection()
        collection.boars = [Boar.convert(p)
                for p in boars]
        return collection


class BoarsController(rest.RestController):
    """REST boar for Default section"""
    def __init__(self):
        super(BoarsController, self).__init__()

    # disable the useful but fake interface
    #@expose.expose(wtypes.text)
    #def get_all(self):
    #    boar_list = {'boar': 'test'}
    #    return [boar_list]

    @expose.expose(wtypes.text)
    def get_all(self):
        boars = objects.Boar().list(
                pecan.request.context)
        import pdb; pdb.set_trace()
        return BoarCollection.convert(boars)

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
