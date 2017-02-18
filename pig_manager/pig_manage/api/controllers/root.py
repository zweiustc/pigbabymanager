import pecan
from pecan import rest
from pecan import secure
from wsme import types as wtypes

from pig_manage.api import expose
from pig_manage.api.controllers import link
from pig_manage.api.controllers import base
from pig_manage.api.controllers import v1


class Version(base.APIBase):
    """An API version representation"""

    id = wtypes.text
    """The ID of the version, also acts as the release number"""

    links = [link.Link]

    @staticmethod
    def convert(id):
        version = Version()
        version.id = id
        version.links = [link.Link.make_link('self', pecan.request.host_url,
                                             id, '', bookmark=True)]
        return version


class Root(base.APIBase):

    name = wtypes.text
    """The name of the API"""

    description = wtypes.text
    """Some information about this API"""

    versions = [Version]
    """Links to all the versions available in this API"""

    default_version = Version
    """A link to the default version of the API"""


    @staticmethod
    def convert():
        root = Root()
        root.name = "Pig API"
        root.description = ("Pig Manager is an application for "
                "pig farm management")
        root.versions = [Version.convert('v1')]
        root.default_version = Version.convert('v1')
        return root


#class RootController(hooks.HookController):
class RootController(rest.RestController):

    _versions = ['v1']

    _default_version = 'v1'

    v1 = v1.Controller()


    @classmethod
    def check_permissions(self):
        return True
        if (pecan.request.method == 'POST' and
            'tokens' in pecan.request.path):
            return True
        if (pecan.request.method == 'GET' and
            'deploy' in pecan.request.path):
            return True
        headers = pecan.request.headers
        user = headers.get('X-Auth-User')
        password = headers.get('X-Auth-Password')
        token = headers.get('X-Auth-Token')
        if (token is not None and objects.token.is_valid_token(token)):
            return True
        if (password is not None and objects.token.is_valid_user(password)):
            return True
        return False

    @expose.expose(Root)
    def get(self):
        return Root.convert()

    @secure.secure('check_permissions')
    @pecan.expose()
    def _route(self, args):
        if args[0] and args[0] not in self._versions:
            args = [self._default_version] + args
        return super(RootController, self)._route(args)
