import json

from oslo_db.sqlalchemy import models
import six.moves.urllib.parse as urlparse
from sqlalchemy import (ForeignKey, Column, Index, Integer, BigInteger, Enum, String, Float,
                        schema, Unicode, Text, SmallInteger, Boolean, DateTime, Date)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import orm
from sqlalchemy.orm import relationship
from pig_manage.db.sqlalchemy import types

from pig_manage import config as conf

CONF = conf.CONF

def table_args():
    engine_name = urlparse.urlparse(CONF.database.connection).scheme
    if engine_name == 'mysql':
        return {'mysql_engine': CONF.database.mysql_engine,
                'mysql_charset': "utf8"}
    return None


class Pig_manageBase(models.TimestampMixin,
                      models.ModelBase):

    metadata = None

    def as_dict(self):
        d = {}
        for c in self.__table__.columns:
            d[c.name] = self[c.name]
        return d

    def save(self, session=None):
        import pig_manage.db.sqlalchemy.api as db_api

        if session is None:
            session = db_api.get_session()

        super(Pig_manageBase, self).save(session)

Base = declarative_base(cls=Pig_manageBase)

class Category(Base, Pig_manageBase):
    """Represents category in pig farm."""
    __tablename__ = 'category'
    __table_args__ = (
        Index('category_id_idx', 'id'),
    )
    id = Column(BigInteger, nullable=False, primary_key=True)
    name = Column(String(36))

    deleted = Column(BigInteger, default=0)
    created_at = Column('created_at', DateTime)
    updated_at = Column('updated_at', DateTime)
    deleted_at = Column('deleted_at', DateTime)
    
class Dormitory(Base, Pig_manageBase):
    """Represents dormitory in pig farm."""
    __tablename__ = 'dormitory'
    __table_args__ = (
        Index('dormitory_id_idx', 'id'),
    )
    id = Column(BigInteger, nullable=False, primary_key=True)
    name = Column(String(36))

    deleted = Column(BigInteger, default=0)
    created_at = Column('created_at', DateTime)
    updated_at = Column('updated_at', DateTime)
    deleted_at = Column('deleted_at', DateTime)

class Source(Base, Pig_manageBase):
    """Represents source in pig farm."""
    __tablename__ = 'source'
    __table_args__ = (
        Index('source_id_idx', 'id'),
    )
    id = Column(BigInteger, nullable=False, primary_key=True)
    name = Column(String(36))

    deleted = Column(BigInteger, default=0)
    created_at = Column('created_at', DateTime)
    updated_at = Column('updated_at', DateTime)
    deleted_at = Column('deleted_at', DateTime)

class State(Base, Pig_manageBase):
    """Represents state in pig farm."""
    __tablename__ = 'state'
    __table_args__ = (
        Index('state_id_idx', 'id'),
    )
    id = Column(BigInteger, nullable=False, primary_key=True)
    name = Column(String(36))

    deleted = Column(BigInteger, default=0)
    created_at = Column('created_at', DateTime)
    updated_at = Column('updated_at', DateTime)
    deleted_at = Column('deleted_at', DateTime)

class ParturitionRecord(Base, Pig_manageBase):
    """Represents parturition_record in pig farm."""
    __tablename__ = 'parturition_record'
    __table_args__ = (
        Index('parturition_record_id_idx', 'id'),
    )
    id = Column(BigInteger, nullable=False, primary_key=True)
    sow_id = Column(BigInteger)
    piglet_num = Column(Integer)
    date = Column(DateTime, nullable=True)
    staff_id = Column(BigInteger)

    deleted = Column(BigInteger, default=0)
    created_at = Column('created_at', DateTime)
    updated_at = Column('updated_at', DateTime)
    deleted_at = Column('deleted_at', DateTime)

class Sow(Base, Pig_manageBase):
    """Represents sow in pig farm."""
    __tablename__ = 'sow'
    __table_args__ = (
        Index('sow_id_idx', 'id'),
    )

    id = Column(BigInteger, nullable=False, primary_key=True)
    ear_tag = Column(BigInteger)
    ear_lack = Column(BigInteger)
    birthday = Column(Date, nullable=True)
    entryday = Column(Date, nullable=True)

    dormitory_id = Column(BigInteger,ForeignKey(Dormitory.id))
    category_id = Column(Integer,ForeignKey(Category.id))
    gestational_age = Column(Integer)
    accum_return = Column(Integer)
    state_id = Column(Integer,ForeignKey(State.id))
    state_day = Column(Integer)
    source_id = Column(Integer,ForeignKey(Source.id))
    note = Column(String(255))
    deleted = Column(BigInteger, default=0)
    created_at = Column('created_at', DateTime)
    updated_at = Column('updated_at', DateTime)
    deleted_at = Column('deleted_at', DateTime)

    category = orm.relationship(Category, foreign_keys=category_id,
            primaryjoin='Sow.category_id == Category.id')
    dormitory = orm.relationship(Dormitory, foreign_keys=dormitory_id,
            primaryjoin='Sow.dormitory_id == Dormitory.id')
    source = orm.relationship(Source, foreign_keys=source_id,
            primaryjoin='Sow.source_id == Source.id')
    state = orm.relationship(State, foreign_keys=state_id,
            primaryjoin='Sow.state_id == State.id')
    #category = relationship('Category')
    #dormitory = relationship('Dormitory')
    #source = relationship('Source')
    #state = relationship('State')


class Boar(Base, Pig_manageBase):
    """Represents boar in pig farm."""
    __tablename__ = 'boar'
    __table_args__ = (
        Index('boar_id_idx', 'id'),
    )

    id = Column(BigInteger, nullable=False, primary_key=True)
    ear_tag = Column(BigInteger)
    ear_lack = Column(BigInteger)
    birthday = Column(Date, nullable=True)
    entryday = Column(Date, nullable=True)
    #dormitory_id = Column(BigInteger,ForeignKey(Dormitory.id))
    dormitory_id = Column(BigInteger, nullable=True)
    #category_id = Column(Integer,ForeignKey(Category.id))
    category_id = Column(Integer, nullable=True)
    breed_num = Column(Integer)
    breed_acceptability = Column(Float)
    #source_id = Column(Integer,ForeignKey(Source.id))
    source_id = Column(Integer, nullable=True)
    note = Column(String(255))
    created_at = Column('created_at', DateTime)
    updated_at = Column('updated_at', DateTime)
    deleted_at = Column('deleted_at', DateTime)
    #Category.boar_tag = relationship("Boar",order_by=Boar.id,back_populates="boar")
    deleted = Column(BigInteger, default=0)

    category = orm.relationship(Category, foreign_keys=category_id,
            primaryjoin='Boar.category_id == Category.id')
    dormitory = orm.relationship(Dormitory, foreign_keys=dormitory_id,
            primaryjoin='Boar.dormitory_id == Dormitory.id')
    source = orm.relationship(Source, foreign_keys=source_id,
            primaryjoin='Boar.source_id == Source.id')
    #category = relationship('Category')
    #dormitory = relationship('Dormitory')
    #source = relationship('Source')
