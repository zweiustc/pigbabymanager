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

class StatesController(rest.RestController):
    """REST state for Default section"""

    _state_keys = ['id', 'name']

    def __init__(self):
        super(StatesController, self).__init__()

    def _format_state(self, db_state):
        state = dict()
        state['id'] = db_state.id
        state['name'] = db_state.name
        #state['created_at'] = db_state.created_at
        #state['updated_at'] = db_state.updated_at
        
        return state

    # disable the useful but fake interface
    @expose.expose(wtypes.text, int, int, wtypes.text, wtypes.text,
            wtypes.text, wtypes.text)
    def get_all(self, PageLimit=100, CurrentPage=1,
            SortKey='id', SortDir='asc', key=None, value=None):

        filters = None
        if key is not None:
            filters= {key: value}

        states, total = objects.State().list(
                pecan.request.context, limit=PageLimit,
                marker=CurrentPage, sort_dir=SortDir,
                sort_key=SortKey, filters=filters)

        reload(sys)
        sys.setdefaultencoding('utf-8')
        result = [self._format_state(state) for state in states]
        return {'states': result, 'Total': total,
            'PageLimit': PageLimit, 'CurrentPage': CurrentPage,
            'SortKey': SortKey, 'SortDir': SortDir}

    @expose.expose(wtypes.text, wtypes.text)
    def get_one(self,id):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        state = objects.State().get_by_id(pecan.request.context,id)
        result = self._format_state(state)
        return {'state': result}

    # expose the first value is response type, the second and others
    # are the parameters of the function
    @expose.expose(wtypes.text, body=wtypes.text, status_code=201)
    def post(self, values):
        body = dict(values)

        _actions = {
            'CreateState': self._action_create_state,
        }
        for action, data in body.iteritems():
            if action not in _actions.keys():
                msg = _('State do not support %s action') % action
                raise webob.exc.HTTPBadRequest(explanation=msg)

            return _actions[action](pecan.request.context, data)

    def _action_create_state(self, context, state_dict):
        for key in state_dict.keys():
            if key not in self._state_keys:
                #raise exception.Invalid('Invalid key in body')
                msg = "Invalid key  %s in body" % key
                raise webob.exc.HTTPBadRequest(explanation=msg)

        state_obj = objects.State(context)
        state_obj.update(state_dict)
        result = state_obj.create(context) 
        return {"state": self._format_state(result)}

    @expose.expose(None, wtypes.text)
    def delete(self, fqdn):
        state_list = {'state': 'test'}
        return state_list

    def patch(self, fqdn, patch):
        state_list = {'state': 'test'}
        return state_list

    @expose.expose(wtypes.text, wtypes.text, body=wtypes.text)
    def put(self, id, patch):
        state_dict = patch.get('UpdateState', None)
        state_obj = objects.State.get_by_id(pecan.request.context,
                id)
        state_obj.update(state_dict)
        state_obj.save()
        return {"state": self._format_state(state_obj)}

    @expose.expose(None, wtypes.text, status_code=201)
    def delete(self, id):
        state_obj = objects.State.get_by_id(pecan.request.context,
                        id)
        state_obj.delete()
