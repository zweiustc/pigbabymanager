from oslo_versionedobjects import  fields

from oslo_log import log

from pig_manage.db import api as dbapi
from pig_manage.objects import base
from pig_manage import utils
from pig_manage import env_config as env_conf

LOG = log.getLogger(__name__)

@base.ObjectRegistry.register
class Boar(base.BaseObject):

    VERSION = '1.0'
    dbapi = dbapi.get_instance()

    fields = {
        'id': fields.IntegerField(nullable=False), 
        'ear_tag': fields.IntegerField(nullable=True), 
        'ear_lack': fields.IntegerField(nullable=True), 
        'birthday': fields.DateTimeField(nullable=True), 
        'entryday': fields.DateTimeField(nullable=True), 
        #'birthday': fields.StringField(nullable=True), 
        #'entryday': fields.StringField(nullable=True), 

        'dormitory_id': fields.IntegerField(nullable=True), 
        'category_id': fields.IntegerField(nullable=True), 

        'breed_num': fields.IntegerField(nullable=True), 
        'breed_acceptability': fields.FloatField(nullable=True), 
        #'state_id': fields.IntegerField(nullable=True), 
        #'state_day': fields.IntegerField(nullable=True), 
        'source_id': fields.IntegerField(nullable=True), 
        'category': fields.StringField(nullable=True),
        'dormitory': fields.StringField(nullable=True),
        'source': fields.StringField(nullable=True),
    }

    @staticmethod
    def _from_db_object(boar, db_boar):
        """Converts a database entity to a formal object."""
        foreign_key = ['category', 'dormitory', 'source']
        for field in boar.fields:
            if field not in foreign_key:
                boar[field] = db_boar[field]
            elif field == 'category' and db_boar.category:
                boar[field] = db_boar.category.name
            elif field == 'dormitory' and db_boar.dormitory:
                boar[field] = db_boar.dormitory.name
            elif field == 'source' and db_boar.source:
                boar[field] = db_boar.source.name
        boar.obj_reset_changes()
        return boar

    @staticmethod
    def _from_db_object_list(db_objects, cls, context):
        """Converts a list of database entities to a list of formal objects."""
        return [Boar._from_db_object(cls(context), obj)
                for obj in db_objects]

    @base.remotable_classmethod
    def list(cls, context, filters=None, limit=3000, marker=1,
             sort_key='id', sort_dir='asc'):
        """Return a list of Boar objects.

        :param context: Security context.
        :param limit: maximum number of resources to return in a single result.
        :param marker: pagination marker for large data sets.
        :param sort_key: column to sort results by.
        :param sort_dir: direction to sort. "asc" or "desc".
        :returns: a list of :class:`Boar` object.

        """
        db_boars = cls.dbapi.get_boar_list(
            context, limit=limit, marker=marker, sort_key=sort_key,
            sort_dir=sort_dir, filters=filters)

        #import pdb; pdb.set_trace()
        return [Boar._from_db_object(cls(context), obj) for obj in db_boars]


    @base.remotable_classmethod
    def get_by_id(cls, context, id):
        db_boar = cls.dbapi.get_boar_by_id(context, id)
        return Boar._from_db_object(cls(context), db_boar)

    @base.remotable
    def create(self, context=None):
        values = self.obj_get_changes()

        db_boar = self.dbapi.create_boar(context, values)
        return self._from_db_object(self, db_boar)

    @base.remotable
    def save(self, context=None):
        """Save updates to this boar.

        Updates will be made column by column based on the result
        of self.what_changed().

        :param context: Security context. NOTE: This should only
                        be used internally by the indirection_api.
                        Unfortunately, RPC requires context as the first
                        argument, even though we don't use it.
                        A context should be set when instantiating the
                        object, e.g.: Boar(context)
        """
        updates = self.obj_get_changes()
        self.dbapi.update_boar(context, self.id, updates)
        self.obj_reset_changes()

    @base.remotable
    def delete(self, context=None):
        self.dbapi.delete_boar(context, self.id)
