import datetime
import pecan
from pecan import rest
import wsme
from wsme import types as wtypes
from webob import exc

from kingcloudos.api import expose
from kingcloudos.api.controllers import base
from kingcloudos.api.controllers import collection
from kingcloudos import objects
from kingcloudos.common import exception


class Token(base.APIBase):

    token = wtypes.text
    """token content"""

    expired_at = wsme.wsattr(datetime.datetime, readonly=True)
    """the expired time"""

    def __init__(self, **kwargs):
        self.fields = []
        for field in objects.Token.fields:
            if not hasattr(self, field):
                continue
            self.fields.append(field)
            setattr(self, field, kwargs.get(field, wtypes.Unset))

    @classmethod
    def convert(self, token):
        return Token(**token.as_dict())


class TokenCollection(collection.Collection):

    tokens = [Token]

    def __init__(self, **kwargs):
        self._type = 'tokens'

    @staticmethod
    def convert(tokens):
        collection = TokenCollection()
        collection.tokens = [Token.convert(p)
                                  for p in tokens]
        return collection


class TokensController(rest.RestController):
    """REST token for Default section"""
    def __init__(self):
        super(TokensController, self).__init__()


    @expose.expose(TokenCollection)
    def get_all(self):
        tokens = objects.token_obj.get_all()
        return TokenCollection.convert(tokens)


    @expose.expose(Token,
                   body=wtypes.DictType(str, str),
                   status_code=201)
    def post(self, creds):
        user = creds.get('username')
        password = creds.get('password')
        if not objects.token.is_valid_user(password):
            raise exc.HTTPUnauthorized('401 Unauthorized')

        return Token.convert(objects.token_obj.create())



    @expose.expose(None, wtypes.text)
    def delete(self, token):
        objects.token_obj.delete(token)
