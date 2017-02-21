"""Custom SQLAlchemy types."""

import netaddr
from oslo_utils import netutils
from sqlalchemy.dialects import postgresql
from sqlalchemy import types

from pig_manage import utils

class IPAddress(types.TypeDecorator):
    """An SQLAlchemy type representing an IP-address."""

    impl = types.String

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(postgresql.INET())
        else:
            return dialect.type_descriptor(types.String(39))

    def process_bind_param(self, value, dialect):
        """Process/Formats the value before insert it into the db."""
        if dialect.name == 'postgresql':
            return value
        # NOTE(maurosr): The purpose here is to convert ipv6 to the shortened
        # form, not validate it.
        elif netutils.is_valid_ipv6(value):
            return utils.get_shortened_ipv6(value)
        return value


class ListBlob(types.TypeDecorator):

    impl = types.String

    def process_bind_param(self, value, dialect):
        if value:
            value = ','.join(value)
        return value

    def process_result_value(self, value, dialect):
        if value:
            return value.strip().split(',')
        return value
