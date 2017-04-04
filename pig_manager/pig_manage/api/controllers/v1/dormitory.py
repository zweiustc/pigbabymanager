import pecan
import sys
import webob
from pecan import rest
import wsme
from wsme import types as wtypes

from pig_manage.api import expose
from pig_manage.api.controllers import base
from pig_manage.api.controllers import collection
from pig_manage.common import exception

from pig_manage import objects

class DormitorysController(rest.RestController):
    """REST dormitory for Default section"""

    _dormitory_keys = ['id', 'name']

    def __init__(self):
        super(DormitorysController, self).__init__()

    def _format_dormitory(self, db_dormitory):
        dormitory = dict()
        dormitory['id'] = db_dormitory.id
        dormitory['name'] = db_dormitory.name
        #dormitory['created_at'] = db_dormitory.created_at
        #dormitory['updated_at'] = db_dormitory.updated_at
        
        return dormitory

    # disable the useful but fake interface
    @expose.expose(wtypes.text, int, int, wtypes.text, wtypes.text,
            wtypes.text, wtypes.text)
    def get_all(self, PageLimit=20, CurrentPage=1,
            SortKey='id', SortDir='asc', key=None, value=None):

        filters = None
        if key is not None:
            filters= {key: value}

        dormitorys, total = objects.Dormitory().list(
                pecan.request.context, limit=PageLimit,
                marker=CurrentPage, sort_dir=SortDir,
                sort_key=SortKey, filters=filters)

        reload(sys)
        sys.setdefaultencoding('utf-8')
        result = [self._format_dormitory(dormitory) for dormitory in dormitorys]
        return {'dormitorys': result, 'Total': total,
            'PageLimit': PageLimit, 'CurrentPage': CurrentPage,
            'SortKey': SortKey, 'SortDir': SortDir}

    @expose.expose(wtypes.text, wtypes.text)
    def get_one(self,id):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        dormitory = objects.Dormitory().get_by_id(pecan.request.context,id)
        result = self._format_dormitory(dormitory)
        return {'dormitory': result}

    # expose the first value is response type, the second and others
    # are the parameters of the function
    @expose.expose(wtypes.text, body=wtypes.text, status_code=201)
    def post(self, values):
        body = dict(values)

        _actions = {
            'CreateDormitory': self._action_create_dormitory,
        }
        for action, data in body.iteritems():
            if action not in _actions.keys():
                msg = _('Dormitory do not support %s action') % action
                raise webob.exc.HTTPBadRequest(explanation=msg)

            return _actions[action](pecan.request.context, data)

    def _action_create_dormitory(self, context, dormitory_dict):
        for key in dormitory_dict.keys():
            if key not in self._dormitory_keys:
                #raise exception.Invalid('Invalid key in body')
                msg = "Invalid key  %s in body" % key
                raise webob.exc.HTTPBadRequest(explanation=msg)

        dormitory_obj = objects.Dormitory(context)
        dormitory_obj.update(dormitory_dict)
        result = dormitory_obj.create(context) 
        return {"dormitory": self._format_dormitory(result)}

    @expose.expose(None, wtypes.text)
    def delete(self, fqdn):
        dormitory_list = {'dormitory': 'test'}
        return dormitory_list

    def patch(self, fqdn, patch):
        dormitory_list = {'dormitory': 'test'}
        return dormitory_list

    @expose.expose(wtypes.text, wtypes.text, body=wtypes.text)
    def put(self, id, patch):
        dormitory_dict = patch.get('UpdateDormitory', None)
        dormitory_obj = objects.Dormitory.get_by_id(pecan.request.context,
                id)
        dormitory_obj.update(dormitory_dict)
        dormitory_obj.save()
        return {"dormitory": self._format_dormitory(dormitory_obj)}

    @expose.expose(None, wtypes.text, status_code=201)
    def delete(self, id):
        dormitory_obj = objects.Dormitory.get_by_id(pecan.request.context,
                        id)
        dormitory_obj.delete()
