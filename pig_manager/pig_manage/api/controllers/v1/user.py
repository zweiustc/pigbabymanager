import pecan
import sys
import webob
from pecan import rest
import wsme
import uuid
import json
from wsme import types as wtypes

from pig_manage.api import expose
from pig_manage.api.controllers import base
from pig_manage.api.controllers import collection
from pig_manage.common import exception

from pig_manage import objects

class UsersController(rest.RestController):
    """REST user for Default section"""

    _user_keys = ['uuid', 'project_id', 'name', 'phone',
        'email', 'role', 'address', 'extra', 'password']

    def __init__(self):
        super(UsersController, self).__init__()

    def _format_user(self, db_user):
        user = dict()
        user['uuid'] = db_user.uuid
        user['project_id'] = db_user.project_id
        user['name'] = db_user.name
        user['phone'] = db_user.phone
        user['email'] = db_user.email
        if db_user.role:
            user.update(json.loads(db_user.role))
        #user['role'] = json.loads(db_user.role)['role']
        user['address'] = db_user.address
        user['extra'] = db_user.extra

        if 'project' in db_user.keys():
            user['project'] = db_user.project.encode('utf-8')

        return user

    # disable the useful but fake interface
    @expose.expose(wtypes.text, int, int, wtypes.text, wtypes.text,
            wtypes.text, wtypes.text,
            wtypes.text, wtypes.text)
    def get_all(self, PageLimit=20, CurrentPage=1,
            SortKey='id', SortDir='asc', key=None, value=None,
            key1=None, value1=None):

        filters = {}
        if key is not None:
            filters[key] = value
        if key1 is not None:
            filters[key1] = value1

        users, total = objects.User().list(
                pecan.request.context, limit=PageLimit,
                marker=CurrentPage, sort_dir=SortDir,
                sort_key=SortKey, filters=filters)

        reload(sys)
        sys.setdefaultencoding('utf-8')
        result = [self._format_user(user) for user in users]
        return {'users': result, 'Total': total,
            'PageLimit': PageLimit, 'CurrentPage': CurrentPage,
            'SortKey': SortKey, 'SortDir': SortDir}

    @expose.expose(wtypes.text, wtypes.text)
    def get_one(self,id):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        user = objects.User().get_by_id(pecan.request.context,id)
        result = self._format_user(user)
        return {'user': result}

    # expose the first value is response type, the second and others
    # are the parameters of the function
    @expose.expose(wtypes.text, body=wtypes.text, status_code=201)
    def post(self, values):
        body = dict(values)

        # Login body should be like this:
        # {"auth": {"passwordCredentials": {"username": "ksc-user",
        # "password": "password"}}}'
        _actions = {
            'CreateUser': self._action_create_user,
            'Auth': self._action_login,
        }
        for action, data in body.iteritems():
            if action not in _actions.keys():
                msg = ('User do not support %s action') % action
                raise webob.exc.HTTPBadRequest(explanation=msg)

            return _actions[action](pecan.request.context, data)

    def _action_create_user(self, context, user_dict):

        self.validate_register_user(context, user_dict)

        for key in user_dict.keys():
            if key not in self._user_keys:
                #raise exception.Invalid('Invalid key in body')
                msg = "Invalid key  %s in body" % key
                raise webob.exc.HTTPBadRequest(explanation=msg)

        user_obj = objects.User(context)
        user_dict['uuid'] = uuid.uuid4()

        user_dict['project_id'] = self.search_project_id_for_user(context,
                                    user_dict)

        role = user_dict.get('role', ['member'])
        user_dict['role'] = json.dumps({"role": role})

        user_obj.update(user_dict)
        result = user_obj.create(context) 
        return {"user": self._format_user(result)}

    def search_project_id_for_user(self, context, user_dict):
        project_id = user_dict.get('project_id', None)
        if project_id is None:
            project_id = 'c92b01a4-1354-4623-b68d-689dbeb0cc94'

        return project_id

    def validate_register_user(self, context, user_dict):
        if 'name' not in user_dict or 'password' not in user_dict:
            msg = "name and password are both needed to register new user"
            raise webob.exc.HTTPBadRequest(explanation=msg)

        # Check whether the user name has been registered
        filters = {"name": user_dict['name']}
        users, total = objects.User().list(
            context, filters=filters)
        if total > 0:
            msg = "name %s has been registered" % user_dict['name']
            raise webob.exc.HTTPBadRequest(explanation=msg)

    def _action_login(self, context, user_dict):
    # '{"Auth": {"passwordCredentials": {"username": "user", "password": "password"}}}'
        passwordCredentials = user_dict.get("passwordCredentials", None)
        if passwordCredentials is None:
            msg = "passwordCredentials infomation is needed"
            raise webob.exc.HTTPBadRequest(explanation=msg)

        username = passwordCredentials.get("username", None)
        password = passwordCredentials.get("password", None)
        if username is None:
            msg = "username is needed!"
            raise webob.exc.HTTPBadRequest(explanation=msg)

        filters = {"name": username}
        users, total = objects.User().list(
                context, filters=filters)
        if total == 0:
            msg = "username has not been registered!"
            raise webob.exc.HTTPBadRequest(explanation=msg)

        if users[0].password == password:
            result = self._format_user(users[0])
        else:
            #msg = "wrong password for user: %s" % username
            #raise webob.exc.HTTPUnauthorized(explation=msg)
            raise webob.exc.HTTPUnauthorized()

        return {'user': result}

    @expose.expose(wtypes.text, wtypes.text, body=wtypes.text)
    def put(self, id, patch):
        user_dict = patch.get('UpdateUser', None)
        user_obj = objects.User.get_by_id(pecan.request.context,
                id)
        user_obj.update(user_dict)
        user_obj.save()
        return {"user": self._format_user(user_obj)}

    @expose.expose(None, wtypes.text, status_code=201)
    def delete(self, id):
        user_obj = objects.User.get_by_id(pecan.request.context,
                        id)
        user_obj.delete()
