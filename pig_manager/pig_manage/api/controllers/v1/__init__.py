import pecan
from pecan import rest
from webob import exc
from wsme import types as wtypes

from pig_manage.api import expose
from pig_manage.api.controllers import base
from pig_manage.api.controllers import link
from pig_manage.api.controllers.v1 import pig
from pig_manage.api.controllers.v1 import sow
from pig_manage.api.controllers.v1 import boar
from pig_manage.api.controllers.v1 import gestational_age_report

BASE_VERSION = 1

MIN_VER_STR = '1.1'

MAX_VER_STR = '1.1'


MIN_VER = base.Version({base.Version.string: MIN_VER_STR},
                       MIN_VER_STR, MAX_VER_STR)
MAX_VER = base.Version({base.Version.string: MAX_VER_STR},
                       MIN_VER_STR, MAX_VER_STR)


class V1(wtypes.Base):
    """The representation of the version 1 of the API."""

    id = wtypes.text
    """The ID of the version, also acts as the release number"""

    @staticmethod
    def convert():
        v1 = V1()
        v1.id = "v1"
        v1.links = [link.Link.make_link('self', pecan.request.host_url,
                                        'v1', '', bookmark=True),
                    link.Link.make_link('describedby',
                                        'http://docs.openstack.org',
                                        'developer/ironic/dev',
                                        'api-spec-v1.html',
                                        bookmark=True, type='text/html')
                    ]
        #v1.defaults = [link.Link.make_link('self', pecan.request.host_url,
        #                                  'default', ''),
        #              link.Link.make_link('bookmark',
        #                                  pecan.request.host_url,
        #                                  'default', '',
        #                                  bookmark=True)]
        #v1.controllers = [link.Link.make_link('self', pecan.request.host_url,
        #                                  'controllers', ''),
        #              link.Link.make_link('bookmark',
        #                                  pecan.request.host_url,
        #                                  'controllers', '',
        #                                  bookmark=True)]
        #v1.computes = [link.Link.make_link('self', pecan.request.host_url,
        #                                   'computes', ''),
        #              link.Link.make_link('bookmark',
        #                                  pecan.request.host_url,
        #                                  'computes', '',
        #                                  bookmark=True)]
        #v1.networks = [link.Link.make_link('self', pecan.request.host_url,
        #                                   'networks', ''),
        #              link.Link.make_link('bookmark',
        #                                  pecan.request.host_url,
        #                                  'networks', '',
        #                                  bookmark=True)]
        v1.pigs = [link.Link.make_link('self', pecan.request.host_url,
                                           'pigs', ''),
                      link.Link.make_link('bookmark',
                                          pecan.request.host_url,
                                          'pigs', '',
                                          bookmark=True)]
        v1.sows = [link.Link.make_link('self', pecan.request.host_url,
                                           'sows', ''),
                      link.Link.make_link('bookmark',
                                          pecan.request.host_url,
                                          'sows', '',
                                          bookmark=True)]
        v1.boars = [link.Link.make_link('self', pecan.request.host_url,
                                           'boars', ''),
                      link.Link.make_link('bookmark',
                                          pecan.request.host_url,
                                          'boars', '',
                                          bookmark=True)]
        v1.gestational_age_reports = [link.Link.make_link('self', pecan.request.host_url,
                                           'gestational_age_reports', ''),
                      link.Link.make_link('bookmark',
                                          pecan.request.host_url,
                                          'gestational_age_reports', '',
                                          bookmark=True)]
        #v1.tokens = [link.Link.make_link('self', pecan.request.host_url,
        #                                'tokens', ''),
        #              link.Link.make_link('bookmark',
        #                                  pecan.request.host_url,
        #                                  'tokens', '',
        #                                  bookmark=True)]

        return v1


class Controller(rest.RestController):
    """Version 1 API controller root."""

    pigs = pig.PigsController()
    sows = sow.SowsController()
    boars = boar.BoarsController()
    gestational_age_reports = gestational_age_report.GestationalAgeReportsController()
    #defaults = default.DefaultController()
    #controllers = controller.ControllersController()
    #computes = compute.ComputesController()
    #networks = network.NetworksController()
    #tokens = token.TokensController()
    #deploy = deploy.DeployController()

    @expose.expose(V1)
    def get(self):
        # NOTE: The reason why convert() it's being called for every
        #       request is because we need to get the host url from
        #       the request object to make the links.
        return V1.convert()

    def _check_version(self, version, headers=None):
        if headers is None:
            headers = {}
        # ensure that major version in the URL matches the header
        if version.major != BASE_VERSION:
            raise exc.HTTPNotAcceptable(_(
                "Mutually exclusive versions requested. Version %(ver)s "
                "requested but not supported by this service. The supported "
                "version range is: [%(min)s, %(max)s].") % {'ver': version,
                'min': MIN_VER_STR, 'max': MAX_VER_STR}, headers=headers)
        # ensure the minor version is within the supported range
        if version < MIN_VER or version > MAX_VER:
            raise exc.HTTPNotAcceptable(_(
                "Version %(ver)s was requested but the minor version is not "
                "supported by this service. The supported version range is: "
                "[%(min)s, %(max)s].") % {'ver': version, 'min': MIN_VER_STR,
                                          'max': MAX_VER_STR}, headers=headers)

    @pecan.expose()
    def _route(self, args):
        v = base.Version(pecan.request.headers, MIN_VER_STR, MAX_VER_STR)

        # Always set the min and max headers
        pecan.response.headers[base.Version.min_string] = MIN_VER_STR
        pecan.response.headers[base.Version.max_string] = MAX_VER_STR

        # assert that requested version is supported
        self._check_version(v, pecan.response.headers)
        pecan.response.headers[base.Version.string] = str(v)
        pecan.request.version = v

        return super(Controller, self)._route(args)


__all__ = (Controller)
