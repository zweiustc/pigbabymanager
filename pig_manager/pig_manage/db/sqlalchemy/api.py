from oslo_db import exception as db_exc
from oslo_db.sqlalchemy import session as db_session
from oslo_db.sqlalchemy import utils as db_utils
from oslo_utils import strutils
from oslo_utils import timeutils
from oslo_utils import uuidutils
from sqlalchemy.orm.exc import MultipleResultsFound
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import joinedload

from pig_manage.common import exception
from pig_manage.db import api
from pig_manage.db.sqlalchemy import models
from pig_manage import config as conf
from pig_manage.objects.base import PageList

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
        filters = filters or {}
        deleted = filters.get('deleted', None)
        if deleted is None:
            filters['deleted'] = 0
        query = model_query(models.Sow)

        columns_to_join = ['category', 'dormitory', 'source',
                        'state']
        for column in columns_to_join:
            query = query.options(joinedload(column))

        if filters and isinstance(filters, dict):
            query = query.filter_by(**filters)

        query, total = db_utils.paginate_query_offset(query, models.Sow, limit=limit,
                                        offset=marker, sort_keys=[sort_key],
                    sort_dir=sort_dir)
        return PageList(query.all(), total)

    def get_sow_by_id(self, context, id):
        session = get_session()
        with session.begin():
            #query = model_query(models.Sow).filter_by(id=id)
            query = model_query(models.Sow)

            columns_to_join = ['category', 'dormitory', 'source',
                            'state']
            for column in columns_to_join:
                query = query.options(joinedload(column))

            try:
                query = query.filter_by(id=id)
                return query.one()
            except NoResultFound:
                raise exception.ResourceNotFound(name='Sow', id=id)

    def create_sow(self, context, values):
        session = get_session()
        with session.begin():
            sow = models.Sow()
            sow.update(values)
            try:
                sow.save(session=session)
            except db_exc.DBDuplicateEntry as exc:
                raise
            return sow

    def update_sow(self, context, id, updates):
        session = get_session()
        with session.begin():
            query = model_query(models.Sow, session=session)
            query = query.filter_by(id=id)
            try:
                ref = query.with_lockmode('update').one()
            except NoResultFound:
                raise exception.ResourceNotFound(name='sow',
                                                 id=id)
            ref.update(updates)
            return ref

    def delete_sow(self, context, id):
        session = get_session()
        with session.begin():
            query = model_query(models.Sow, session=session,
                    read_deleted="no")
            query = query.filter_by(id=id)
            try:
                query.soft_delete()
            except NoResultFound:
                raise exception.ResourceNotFound(name='sow',
                                                 id=id)

    def get_boar_list(self, context, filters=None, limit=None,
                              marker=None,
                              sort_key=None, sort_dir=None):
        filters = filters or {}
        deleted = filters.get('deleted', None)
        if deleted is None:
            filters['deleted'] = 0
        query = model_query(models.Boar)

        columns_to_join = ['category', 'dormitory', 'source']
        for column in columns_to_join:
            query = query.options(joinedload(column))

        if filters and isinstance(filters, dict):
            query = query.filter_by(**filters)
        return query.all()

    def get_boar_by_id(self, context, id):
        session = get_session()
        with session.begin():
            #query = model_query(models.Boar).filter_by(id=id)
            query = model_query(models.Boar)

            columns_to_join = ['category', 'dormitory', 'source']
            for column in columns_to_join:
                query = query.options(joinedload(column))

            try:
                query = query.filter_by(id=id)
                return query.one()
            except NoResultFound:
                raise exception.ResourceNotFound(name='boar', id=id)

    def create_boar(self, context, values):
        session = get_session()
        with session.begin():
            boar = models.Boar()
            boar.update(values)
            try:
                boar.save(session=session)
            except db_exc.DBDuplicateEntry as exc:
                raise
            return boar

    def update_boar(self, context, id, updates):
        session = get_session()
        with session.begin():
            query = model_query(models.Boar, session=session)
            query = query.filter_by(id=id)
            try:
                ref = query.with_lockmode('update').one()
            except NoResultFound:
                raise exception.ResourceNotFound(name='boar',
                                                 id=id)
            ref.update(updates)
            return ref

    def delete_boar(self, context, id):
        session = get_session()
        with session.begin():
            query = model_query(models.Boar, session=session,
                    read_deleted="no")
            query = query.filter_by(id=id)
            try:
                query.soft_delete()
            except NoResultFound:
                raise exception.ResourceNotFound(name='boar',
                                                 id=id)

    def get_parturition_record_list(self, context, filters=None, limit=None,
                marker=None,
                sort_key=None, sort_dir=None):
        filters = filters or {}
        deleted = filters.get('deleted', None)
        if deleted is None:
            filters['deleted'] = 0
        query = model_query(models.ParturitionRecord)

        if filters and isinstance(filters, dict):
            query = query.filter_by(**filters)
        return query.all()

    def count_sow_by_filter(self, context, filters=None):
        filters = filters or {}
        deleted = filters.get('deleted', None)
        if deleted is None:
            filters['deleted'] = 0
        query = model_query(models.Sow)

        if filters and isinstance(filters, dict):
            query = query.filter_by(**filters)
        return query.count()

    def get_dormitory_list(self, context, filters=None, limit=None,
                              marker=None,
                              sort_key=None, sort_dir=None):
        filters = filters or {}
        deleted = filters.get('deleted', None)
        if deleted is None:
            filters['deleted'] = 0
        query = model_query(models.Dormitory)

        fuzzy_name = None
        if filters and isinstance(filters, dict):
            if 'name' in filters.keys():
                fuzzy_name = '%' + filters['name'] + '%'
                filters.pop('name')
            query = query.filter_by(**filters)
        if fuzzy_name:
            query = query.filter(models.Dormitory.name.like(fuzzy_name))

        #total = query.count()

        query, total = db_utils.paginate_query_offset(query, models.Dormitory,
                    limit=limit, offset=marker, sort_keys=[sort_key],
                    sort_dir=sort_dir)
        return PageList(query.all(), total)

    def get_dormitory_by_id(self, context, id):
        session = get_session()
        with session.begin():
            #query = model_query(models.Dormitory).filter_by(id=id)
            query = model_query(models.Dormitory)

            try:
                query = query.filter_by(id=id)
                return query.one()
            except NoResultFound:
                raise exception.ResourceNotFound(name='Dormitory', id=id)

    def create_dormitory(self, context, values):
        session = get_session()
        with session.begin():
            dormitory = models.Dormitory()
            dormitory.update(values)
            try:
                dormitory.save(session=session)
            except db_exc.DBDuplicateEntry as exc:
                raise
            return dormitory

    def update_dormitory(self, context, id, updates):
        session = get_session()
        with session.begin():
            query = model_query(models.Dormitory, session=session)
            query = query.filter_by(id=id)
            try:
                ref = query.with_lockmode('update').one()
            except NoResultFound:
                raise exception.ResourceNotFound(name='dormitory',
                                                 id=id)
            ref.update(updates)
            return ref

    def delete_dormitory(self, context, id):
        session = get_session()
        with session.begin():
            query = model_query(models.Dormitory, session=session,
                    read_deleted="no")
            query = query.filter_by(id=id)
            try:
                query.soft_delete()
            except NoResultFound:
                raise exception.ResourceNotFound(name='dormitory',
                                                 id=id)

    def get_state_list(self, context, filters=None, limit=None,
                              marker=None,
                              sort_key=None, sort_dir=None):
        filters = filters or {}
        deleted = filters.get('deleted', None)
        if deleted is None:
            filters['deleted'] = 0
        query = model_query(models.State)

        fuzzy_name = None
        if filters and isinstance(filters, dict):
            if 'name' in filters.keys():
                fuzzy_name = '%' + filters['name'] + '%'
                filters.pop('name')
            query = query.filter_by(**filters)
        if fuzzy_name:
            query = query.filter(models.State.name.like(fuzzy_name))

        #total = query.count()

        query, total = db_utils.paginate_query_offset(query, models.State,
                    limit=limit, offset=marker, sort_keys=[sort_key],
                    sort_dir=sort_dir)
        return PageList(query.all(), total)

    def get_state_by_id(self, context, id):
        session = get_session()
        with session.begin():
            #query = model_query(models.State).filter_by(id=id)
            query = model_query(models.State)

            try:
                query = query.filter_by(id=id)
                return query.one()
            except NoResultFound:
                raise exception.ResourceNotFound(name='State', id=id)

    def create_state(self, context, values):
        session = get_session()
        with session.begin():
            state = models.State()
            state.update(values)
            try:
                state.save(session=session)
            except db_exc.DBDuplicateEntry as exc:
                raise
            return state

    def update_state(self, context, id, updates):
        session = get_session()
        with session.begin():
            query = model_query(models.State, session=session)
            query = query.filter_by(id=id)
            try:
                ref = query.with_lockmode('update').one()
            except NoResultFound:
                raise exception.ResourceNotFound(name='state',
                                                 id=id)
            ref.update(updates)
            return ref

    def delete_state(self, context, id):
        session = get_session()
        with session.begin():
            query = model_query(models.State, session=session,
                    read_deleted="no")
            query = query.filter_by(id=id)
            try:
                query.soft_delete()
            except NoResultFound:
                raise exception.ResourceNotFound(name='state',
                                                 id=id)

