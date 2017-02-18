import six

from oslo_log import log

LOG = log.getLogger(__name__)


class KingcloudosException(Exception):
    """Base Kingcloudos Exception

    To correctly use this class, inherit from it and define
    a 'message' property. That message will get printf'd
    with the keyword arguments provided to the constructor.

    """
    message = "An unknown exception occurred."
    code = 500

    def __init__(self, message=None, **kwargs):
        self.kwargs = kwargs

        if 'code' not in self.kwargs and hasattr(self, 'code'):
            self.kwargs['code'] = self.code

        if message:
            self.message = message

        try:
            self.message = self.message % kwargs
        except Exception:
            # kwargs doesn't match a variable in the message
            # log the issue and the kwargs
            LOG.exception('Exception in string format operation, '
                              'kwargs: %s' % kwargs)
        super(KingcloudosException, self).__init__(self.message)

    def __str__(self):
        if six.PY3:
            return self.message
        return self.message.encode('utf-8')

    def __unicode__(self):
        return self.message

    def format_message(self):
        if self.__class__.__name__.endswith('_Remote'):
            return self.args[0]
        else:
            return six.text_type(self)


class ObjectNotFound(KingcloudosException):
    message = "The %(name)s %(id)s could not be found."


class ResourceNotFound(ObjectNotFound):
    message = "The %(name)s resource %(id)s could not be found."
    code = 404

class BadRequest(KingcloudosException):
    message = "The %(field)s could not be found."
    code = 400

class ActionNotSupport(KingcloudosException):
    message = "The %(action)s could not be supported."
    code = 400
