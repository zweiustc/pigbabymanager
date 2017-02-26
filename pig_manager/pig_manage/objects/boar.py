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

        'dormitory_id': fields.IntegerField(nullable=True), 
        'category_id': fields.IntegerField(nullable=True), 

        'breed_num': fields.IntegerField(nullable=True), 
        'breed_acceptability': fields.FloatField(nullable=True), 
        #'state_id': fields.IntegerField(nullable=True), 
        #'state_day': fields.IntegerField(nullable=True), 
        'source_id': fields.IntegerField(nullable=True), 
    }

    @staticmethod
    def _from_db_object(boar, db_boar):
        """Converts a database entity to a formal object."""
        for field in boar.fields:
            boar[field] = db_boar[field]
        boar.obj_reset_changes()
        return boar

    @staticmethod
    def _from_db_object_list(db_objects, cls, context):
        """Converts a list of database entities to a list of formal objects."""
        return [Boar._from_db_object(cls(context), obj)
                for obj in db_objects]

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
        #import pdb; pdb.set_trace()
        db_boars = cls.dbapi.get_boar_list(
            context, limit=limit, marker=marker, sort_key=sort_key,
            sort_dir=sort_dir, filters=filters)
        return Boar._from_db_object_list(db_boars, cls,
                                          context)
