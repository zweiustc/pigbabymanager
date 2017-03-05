import json

from oslo_db.sqlalchemy import models
import six.moves.urllib.parse as urlparse
from sqlalchemy import (ForeignKey, Column, Index, Integer, BigInteger, Enum, String, Float,
                        schema, Unicode, Text, SmallInteger, Boolean, DateTime)
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
        import kingcloudos.db.sqlalchemy.api as db_api

        if session is None:
            session = db_api.get_session()

        super(KingcloudosBase, self).save(session)

Base = declarative_base(cls=Pig_manageBase)

class Category(Base, Pig_manageBase):
    """Represents category in pig farm."""
    __tablename__ = 'category'
    __table_args__ = (
        Index('category_id_idx', 'id'),
    )
    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String(36))
    

class Sow(Base, Pig_manageBase):
    """Represents sow in pig farm."""
    __tablename__ = 'sow'
    __table_args__ = (
        Index('sow_id_idx', 'id'),
    )

    id = Column(BigInteger, nullable=False, primary_key=True)
    ear_tag = Column(BigInteger)
    ear_lack = Column(BigInteger)
    birthday = Column(DateTime, nullable=True)
    entryday = Column(DateTime, nullable=True)

    dormitory_id = Column(BigInteger)
    category_id = Column(Integer)
    gestational_age = Column(Integer)
    accum_return = Column(Integer)
    state_id = Column(Integer)
    state_day = Column(Integer)
    source_id = Column(Integer)
    note = Column(String(255))


class Boar(Base, Pig_manageBase):
    """Represents boar in pig farm."""
    __tablename__ = 'boar'
    __table_args__ = (
        Index('boar_id_idx', 'id'),
    )

    id = Column(BigInteger, nullable=False, primary_key=True)
    ear_tag = Column(BigInteger)
    ear_lack = Column(BigInteger)
    birthday = Column(DateTime, nullable=True)
    entryday = Column(DateTime, nullable=True)
    dormitory_id = Column(BigInteger)
    category_id = Column(Integer,ForeignKey(Category.id))
    breed_num = Column(Integer)
    breed_acceptability = Column(Float)
    source_id = Column(Integer)
    note = Column(String(255))
    category = relationship('Category')
#Category.boar_tag = relationship("Boar",order_by=Boar.id,back_populates="boar")
