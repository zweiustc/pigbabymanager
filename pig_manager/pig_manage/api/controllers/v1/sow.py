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

class SowsController(rest.RestController):
    """REST sow for Default section"""

    _sow_keys = ['ear_tag', 'ear_lack', 'birthday', 'entryday',
        'dormitory_id', 'category_id', 'gestational_age', 'accum_return',
        'state_id','state_day','source_id']

    def __init__(self):
        super(SowsController, self).__init__()

    def _format_sow(self, db_sow):
        sow = dict()
        sow['id'] = db_sow.id
        sow['ear_tag'] = db_sow.ear_tag
        sow['ear_lack'] = db_sow.ear_lack
        sow['birthday'] = db_sow.birthday
        sow['entryday'] = db_sow.entryday
        sow['dormitory_id'] = db_sow.dormitory_id
        sow['category_id'] = db_sow.category_id
        sow['gestational_age'] = db_sow.gestational_age
        sow['accum_return'] = db_sow.accum_return
        sow['state_id'] = db_sow.state_id
        sow['state_day'] = db_sow.state_day
        sow['source_id'] = db_sow.source_id
        #sow['created_at'] = db_sow.created_at
        #sow['updated_at'] = db_sow.updated_at
        
        if 'category' in db_sow.keys():
            sow['category'] = db_sow.category.encode('utf-8')
        if 'dormitory' in db_sow.keys():
            sow['dormitory'] = db_sow.dormitory.encode('utf-8')
        if 'source' in db_sow.keys():
            sow['source'] = db_sow.source.encode('utf-8')
        if 'state' in db_sow.keys():
            sow['state'] = db_sow.state.encode('utf-8')

        return sow

    # disable the useful but fake interface
    @expose.expose(wtypes.text, int, int, wtypes.text, wtypes.text,
            wtypes.text, wtypes.text)
    def get_all(self, PageLimit=20, CurrentPage=1,
            SortKey='id', SortDir='asc', key=None, value=None):

        filters = None
        if key is not None:
            filters= {key: value}

        sows, total = objects.Sow().list(
                pecan.request.context, limit=PageLimit,
                marker=CurrentPage, sort_dir=SortDir,
                sort_key=SortKey, filters=filters)

        reload(sys)
        sys.setdefaultencoding('utf-8')
        result = [self._format_sow(sow) for sow in sows]
        return {'sows': result, 'Total': total,
            'PageLimit': PageLimit, 'CurrentPage': CurrentPage,
            'SortKey': SortKey, 'SortDir': SortDir}

    @expose.expose(wtypes.text, wtypes.text)
    def get_one(self,id):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        sow = objects.Sow().get_by_id(pecan.request.context,id)
        result = self._format_sow(sow)
        return {'sow': result}

    # expose the first value is response type, the second and others
    # are the parameters of the function
    @expose.expose(wtypes.text, body=wtypes.text, status_code=201)
    def post(self, values):
        body = dict(values)

        _actions = {
            'CreateSow': self._action_create_sow,
        }
        for action, data in body.iteritems():
            if action not in _actions.keys():
                msg = _('Sow do not support %s action') % action
                raise webob.exc.HTTPBadRequest(explanation=msg)

            return _actions[action](pecan.request.context, data)

    def _action_create_sow(self, context, sow_dict):
        for key in sow_dict.keys():
            if key not in self._sow_keys:
                #raise exception.Invalid('Invalid key in body')
                msg = "Invalid key  %s in body" % key
                raise webob.exc.HTTPBadRequest(explanation=msg)

        sow_obj = objects.Sow(context)
        sow_obj.update(sow_dict)
        result = sow_obj.create(context) 
        return {"sow": self._format_sow(result)}

    @expose.expose(None, wtypes.text)
    def delete(self, fqdn):
        sow_list = {'sow': 'test'}
        return sow_list

    def patch(self, fqdn, patch):
        sow_list = {'sow': 'test'}
        return sow_list

    @expose.expose(wtypes.text, wtypes.text, body=wtypes.text)
    def put(self, id, patch):
        sow_dict = patch.get('UpdateSow', None)
        sow_obj = objects.Sow.get_by_id(pecan.request.context,
                id)
        sow_obj.update(sow_dict)
        sow_obj.save()
        return {"sow": self._format_sow(sow_obj)}

    @expose.expose(None, wtypes.text, status_code=201)
    def delete(self, id):
        sow_obj = objects.Sow.get_by_id(pecan.request.context,
                        id)
        sow_obj.delete()
