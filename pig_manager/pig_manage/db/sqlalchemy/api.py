from oslo_db import exception as db_exc
from oslo_db.sqlalchemy import session as db_session
from oslo_db.sqlalchemy import utils as db_utils
from oslo_utils import strutils
from oslo_utils import timeutils
from oslo_utils import uuidutils
from sqlalchemy.orm.exc import MultipleResultsFound
from sqlalchemy.orm.exc import NoResultFound

from pig_manage.common import exception
from pig_manage.db import api
from pig_manage.db.sqlalchemy import models
from pig_manage import config as conf

CONF = conf.CONF

_FACADE = None


def _create_facade_lazily():
    global _FACADE
    if _FACADE is None:
        _FACADE = db_session.EngineFacade.from_config(CONF)
    return _FACADE


def get_engine():
    facade = _create_facade_lazily()
    return facade.get_engine()


def get_session(**kwargs):
    facade = _create_facade_lazily()
    return facade.get_session(**kwargs)


def get_backend():
    """The backend is this module itself."""
    return Connection()


def model_query(model, *args, **kwargs):
    """Query helper for simpler session usage.

    :param session: if present, the session to use
    """

    session = kwargs.get('session') or get_session()
    query = session.query(model, *args)
    return query

class Connection(api.Connection):
    """SqlAlchemy connection."""

    def __init__(self):
        pass

    def get_sow_list(self, context, filters=None, limit=None,
                              marker=None,
                              sort_key=None, sort_dir=None):
        #import pdb; pdb.set_trace()
        filters = filters or {}
        #deleted = filters.get('deleted', None)
        #if deleted is None:
        #    filters['deleted'] = False
        query = model_query(models.Sow)
        if filters and isinstance(filters, dict):
            query = query.filter_by(**filters)
        return query.all()

    def get_boar_list(self, context, filters=None, limit=None,
                              marker=None,
                              sort_key=None, sort_dir=None):
        query = model_query(models.Boar)
        if filters and isinstance(filters, dict):
            query = query.filter_by(**filters)
        return query.all()
