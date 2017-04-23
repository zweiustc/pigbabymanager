import abc

from oslo_db import api as db_api
from oslo_log import log as logging
import six

from pig_manage import config as conf

CONF = conf.CONF

_BACKEND_MAPPING = {'sqlalchemy': 'pig_manage.db.sqlalchemy.api'}
IMPL = db_api.DBAPI.from_config(CONF, backend_mapping=_BACKEND_MAPPING,
                                lazy=True)

LOG = logging.getLogger(__name__)


def get_instance():
    """Return a DB API instance."""
    return IMPL

@six.add_metaclass(abc.ABCMeta)
class Connection(object):
    """Base class for storage system connections."""

    @abc.abstractmethod
    def __init__(self):
        """Constructor."""

    @abc.abstractmethod
    def get_sow_list(cls, context, filters=None, limit=None,
            marker=None, sort_key=None, sort_dir=None):
        """return all sow record in database."""

    @abc.abstractmethod
    def create_sow(cls, context, values):
        """Create a new sow record."""

    @abc.abstractmethod
    def get_sow_by_id(cls, context, id):
        """Get sow by id."""

    @abc.abstractmethod
    def update_sow(cls, context, id, updates):
        """Update sow info."""

    @abc.abstractmethod
    def delete_sow(cls, context, id):
        """delete sow info."""

    @abc.abstractmethod
    def get_boar_list(cls, context, filters=None, limit=None,
            marker=None, sort_key=None, sort_dir=None):
        """return all boar record in database."""

    @abc.abstractmethod
    def create_boar(cls, context, values):
        """Create a new boar record."""

    @abc.abstractmethod
    def get_boar_by_id(cls, context, id):
        """Get boar by id."""

    @abc.abstractmethod
    def update_boar(cls, context, id, updates):
        """Update boar info."""

    @abc.abstractmethod
    def delete_boar(cls, context, id):
        """delete boar info."""

    @abc.abstractmethod
    def get_parturition_record_list(cls, context, filters=None, limit=None,
            marker=None, sort_key=None, sort_dir=None):
        """return all parturition records in database."""

    @abc.abstractmethod
    def count_sow_by_filter(cls, context, filters=None):
        """return number of records satified the filter in database."""

    @abc.abstractmethod
    def get_dormitory_list(cls, context, filters=None, limit=None,
            marker=None, sort_key=None, sort_dir=None):
        """return all dormitory record in database."""

    @abc.abstractmethod
    def create_dormitory(cls, context, values):
        """Create a new dormitory record."""

    @abc.abstractmethod
    def get_dormitory_by_id(cls, context, id):
        """Get dormitory by id."""

    @abc.abstractmethod
    def update_dormitory(cls, context, id, updates):
        """Update dormitory info."""

    @abc.abstractmethod
    def delete_dormitory(cls, context, id):
        """delete dormitory info."""

    @abc.abstractmethod
    def get_state_list(cls, context, filters=None, limit=None,
            marker=None, sort_key=None, sort_dir=None):
        """return all state record in database."""

    @abc.abstractmethod
    def create_state(cls, context, values):
        """Create a new state record."""

    @abc.abstractmethod
    def get_state_by_id(cls, context, id):
        """Get state by id."""

    @abc.abstractmethod
    def update_state(cls, context, id, updates):
        """Update state info."""

    @abc.abstractmethod
    def delete_state(cls, context, id):
        """delete state info."""

    @abc.abstractmethod
    def get_user_list(cls, context, filters=None, limit=None,
            marker=None, sort_key=None, sort_dir=None):
        """return all user record in database."""

    @abc.abstractmethod
    def create_user(cls, context, values):
        """Create a new user record."""

    @abc.abstractmethod
    def get_user_by_id(cls, context, id):
        """Get user by id."""

    @abc.abstractmethod
    def update_user(cls, context, id, updates):
        """Update user info."""

    @abc.abstractmethod
    def delete_user(cls, context, id):
        """delete user info."""
