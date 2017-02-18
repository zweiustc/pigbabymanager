import pecan
from wsme import types as wtypes

from pig_manage.api.controllers import base


class Collection(base.APIBase):

    @property
    def collection(self):
        return getattr(self, self._type)
