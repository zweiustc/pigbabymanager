import pecan
import webob
from pecan import rest
import wsme
from wsme import types as wtypes

from pig_manage.api import expose
from pig_manage.api.controllers import base
from pig_manage.api.controllers import collection
from pig_manage.common import exception

from pig_manage import objects


#class Boar(base.APIBase):
#    id = wtypes.text
#    ear_tag = wtypes.text
#    ear_lack = wtypes.text
#    #birthday = wtypes.datetime
#    #entryday = wtypes.datetime
#    birthday = wtypes.text
#    entryday = wtypes.text
#
#    dormitory_id = wtypes.text
#    category_id = wtypes.text
#    breed_num = wtypes.IntegerType
#    breed_acceptability = wtypes.text
#    source_id = wtypes.text
#
#    def __init__(self, **kwargs):
#        self.fields = []
#        for field in objects.Boar.fields:
#            if not hasattr(self, field):
#                continue
#            self.fields.append(field)
#            setattr(self, field, kwargs.get(field, wtypes.Unset))
#
#    @classmethod
#    def convert(self, boar):
#        return Boar(**boar.as_dict())
#
#
#class BoarCollection(collection.Collection):
#
#    boars = [Boar]
#
#    def __init__(self, **kwargs):
#        self._type = 'boars'
#
#    @staticmethod
#    def convert(boars):
#        collection = BoarCollection()
#        collection.boars = [Boar.convert(p)
#                for p in boars]
#        return collection


class BoarsController(rest.RestController):
    """REST boar for Default section"""

    _boar_keys = ['ear_tag', 'ear_lack', 'birthday', 'entryday',
        'dormitory_id', 'category_id', 'breed_num', 'breed_acceptability',
        'source_id']

    def __init__(self):
        super(BoarsController, self).__init__()

    def _format_boar(self, db_boar):
        boar = dict()
        boar['id'] = db_boar.id
        boar['ear_tag'] = db_boar.ear_tag
        boar['ear_lack'] = db_boar.ear_lack
        boar['birthday'] = db_boar.birthday
        boar['entryday'] = db_boar.entryday
        boar['dormitory_id'] = db_boar.dormitory_id
        boar['category_id'] = db_boar.category_id
        boar['breed_num'] = db_boar.breed_num
        boar['breed_acceptability'] = db_boar.breed_acceptability
        boar['source_id'] = db_boar.source_id
        if 'category' in db_boar.keys():
            boar['category'] = db_boar.category
        if 'dormitory' in db_boar.keys():
            boar['dormitory'] = db_boar.dormitory
        if 'source' in db_boar.keys():
            boar['source'] = db_boar.source
        #boar['created_at'] = db_boar.created_at
        #boar['updated_at'] = db_boar.updated_at
        
        return boar

    @expose.expose(wtypes.text)
    def get_all(self):
        boars = objects.Boar().list(
                pecan.request.context)
        result = [self._format_boar(boar) for boar in boars]
        return {'boars': result}
    
    @expose.expose(wtypes.text, wtypes.text)
    def get_one(self,id):
        boar = objects.Boar().get_by_id(pecan.request.context,id)
        result = self._format_boar(boar)
        return {'boar': result}

    # expose the first value is response type, the second and others
    # are the parameters of the function
    @expose.expose(wtypes.text, body=wtypes.text, status_code=201)
    def post(self, values):
        body = dict(values)

        _actions = {
            'CreateBoar': self._action_create_boar,
        }
        for action, data in body.iteritems():
            if action not in _actions.keys():
                msg = _('Boar do not support %s action') % action
                raise webob.exc.HTTPBadRequest(explanation=msg)

            return _actions[action](pecan.request.context, data)

    def _action_create_boar(self, context, boar_dict):
        for key in boar_dict.keys():
            if key not in self._boar_keys:
                #raise exception.Invalid('Invalid key in body')
                msg = "Invalid key  %s in body" % key
                raise webob.exc.HTTPBadRequest(explanation=msg)

        boar_obj = objects.Boar(context)
        boar_obj.update(boar_dict)
        result = boar_obj.create(context) 
        return {"boar": self._format_boar(result)}

    @expose.expose(wtypes.text, wtypes.text, body=wtypes.text)
    def put(self, id, patch):
        boar_dict = patch.get('UpdateBoar', None)
        boar_obj = objects.Boar.get_by_id(pecan.request.context,
                id)
        boar_obj.update(boar_dict)
        boar_obj.save()
        return {"boar": self._format_boar(boar_obj)}

    @expose.expose(None, wtypes.text, status_code=201)
    def delete(self, id):
        boar_obj = objects.Boar.get_by_id(pecan.request.context,
                        id)
        boar_obj.delete()

