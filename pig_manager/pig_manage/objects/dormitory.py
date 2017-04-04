import datetime

from oslo_versionedobjects import  fields
from oslo_log import log
from pig_manage.db import api as dbapi
from pig_manage.objects import base
from pig_manage import utils
from pig_manage import env_config as env_conf

LOG = log.getLogger(__name__)

@base.ObjectRegistry.register
class Dormitory(base.BaseObject):

    VERSION = '1.0'
    dbapi = dbapi.get_instance()

    fields = {
        'id': fields.IntegerField(nullable=False), 
        'name': fields.StringField(nullable=True), 
    }

    @staticmethod
    def _from_db_object(dormitory, db_dormitory):
        """Converts a database entity to a formal object."""
        for field in dormitory.fields:
            dormitory[field] = db_dormitory[field]
        dormitory.obj_reset_changes()
        return dormitory

    @staticmethod
    def _from_db_object_list(db_objects, cls, context):
        """Converts a list of database entities to a list of formal objects."""
        return [Dormitory._from_db_object(cls(context), obj)
                for obj in db_objects]

    @base.remotable_classmethod
    def list(cls, context, filters=None, limit=3000, marker=1,
             sort_key='id', sort_dir='asc'):
        """Return a list of Dormitory objects.

        :param context: Security context.
        :param limit: maximum number of resources to return in a single result.
        :param marker: pagination marker for large data sets.
        :param sort_key: column to sort results by.
        :param sort_dir: direction to sort. "asc" or "desc".
        :returns: a list of :class:`Dormitory` object.

        """
        #import pdb; pdb.set_trace()
        db_dormitorys = cls.dbapi.get_dormitory_list(
            context, limit=limit, marker=marker, sort_key=sort_key,
            sort_dir=sort_dir, filters=filters)
        total =  db_dormitorys.total
        return [Dormitory._from_db_object(cls(context), obj) for obj in db_dormitorys], total

    @base.remotable_classmethod
    def get_by_id(cls, context, id):
        db_dormitory = cls.dbapi.get_dormitory_by_id(context, id)
        return Dormitory._from_db_object(cls(context), db_dormitory)

    @base.remotable
    def create(self, context=None):
        values = self.obj_get_changes()

        db_dormitory = self.dbapi.create_dormitory(context, values)
        return self._from_db_object(self, db_dormitory)

    @base.remotable
    def save(self, context=None):
        """Save updates to this dormitory.

        Updates will be made column by column based on the result
        of self.what_changed().

        :param context: Security context. NOTE: This should only
                        be used internally by the indirection_api.
                        Unfortunately, RPC requires context as the first
                        argument, even though we don't use it.
                        A context should be set when instantiating the
                        object, e.g.: Dormitory(context)
        """
        updates = self.obj_get_changes()
        self.dbapi.update_dormitory(context, self.id, updates)
        self.obj_reset_changes()

    @base.remotable
    def delete(self, context=None):
        self.dbapi.delete_dormitory(context, self.id)   
