from oslo_versionedobjects import  fields

from oslo_log import log

from pig_manage.db import api as dbapi
from pig_manage.objects import base
from pig_manage import utils
from pig_manage import env_config as env_conf

LOG = log.getLogger(__name__)

@base.ObjectRegistry.register
class Sow(base.BaseObject):

    VERSION = '1.0'
    dbapi = dbapi.get_instance()

    fields = {
        'id': fields.IntegerField(nullable=False), 
        'ear_tag': fields.IntegerField(nullable=True), 
        'ear_lack': fields.IntegerField(nullable=True), 
        'birthday': fields.DateTimeField(nullable=True), 
        'entryday': fields.DateTimeField(nullable=True), 

        'dormitory_id': fields.IntegerField(nullable=True), 
        'category_id': fields.IntegerField(nullable=True), 
        'gestational_age': fields.IntegerField(nullable=True), 
        'accum_return': fields.IntegerField(nullable=True), 
        'state_id': fields.IntegerField(nullable=True), 
        'state_day': fields.IntegerField(nullable=True), 
        'source_id': fields.IntegerField(nullable=True), 
        'category': fields.StringField(nullable=True),
        'dormitory': fields.StringField(nullable=True),
        'source': fields.StringField(nullable=True),
        'state': fields.StringField(nullable=True),
    }

    @staticmethod
    def _from_db_object(sow, db_sow):
        """Converts a database entity to a formal object."""
        foreign_key = ['category', 'dormitory', 'source', 'state']
        for field in sow.fields:
            if field not in foreign_key:
                sow[field] = db_sow[field]
            elif field == 'category' and db_sow.category:
                sow[field] = db_sow.category.name
            elif field == 'dormitory' and db_sow.dormitory:
                sow[field] = db_sow.dormitory.name
            elif field == 'source' and db_sow.source:
                sow[field] = db_sow.source.name
            elif field == 'state' and db_sow.state:
                sow[field] = db_sow.state.name
        sow.obj_reset_changes()
        return sow

    @staticmethod
    def _from_db_object_list(db_objects, cls, context):
        """Converts a list of database entities to a list of formal objects."""
        return [Sow._from_db_object(cls(context), obj)
                for obj in db_objects]

    @base.remotable_classmethod
    def list(cls, context, filters=None, limit=3000, marker=1,
             sort_key='id', sort_dir='asc'):
        """Return a list of Sow objects.

        :param context: Security context.
        :param limit: maximum number of resources to return in a single result.
        :param marker: pagination marker for large data sets.
        :param sort_key: column to sort results by.
        :param sort_dir: direction to sort. "asc" or "desc".
        :returns: a list of :class:`Sow` object.

        """
        #import pdb; pdb.set_trace()
        db_sows = cls.dbapi.get_sow_list(
            context, limit=limit, marker=marker, sort_key=sort_key,
            sort_dir=sort_dir, filters=filters)
        return [Sow._from_db_object(cls(context), obj) for obj in db_sows]

    @base.remotable_classmethod
    def get_by_id(cls, context, id):
        db_sow = cls.dbapi.get_sow_by_id(context, id)
        return Sow._from_db_object(cls(context), db_sow)

    @base.remotable
    def create(self, context=None):
        values = self.obj_get_changes()

        db_sow = self.dbapi.create_sow(context, values)
        return self._from_db_object(self, db_sow)

    @base.remotable
    def save(self, context=None):
        """Save updates to this sow.

        Updates will be made column by column based on the result
        of self.what_changed().

        :param context: Security context. NOTE: This should only
                        be used internally by the indirection_api.
                        Unfortunately, RPC requires context as the first
                        argument, even though we don't use it.
                        A context should be set when instantiating the
                        object, e.g.: Sow(context)
        """
        updates = self.obj_get_changes()
        self.dbapi.update_sow(context, self.id, updates)
        self.obj_reset_changes()

    @base.remotable
    def delete(self, context=None):
        self.dbapi.delete_sow(context, self.id)   
