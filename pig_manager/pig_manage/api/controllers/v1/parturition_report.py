import pecan
import webob
from pecan import rest
import wsme
from wsme import types as wtypes

from pig_manage.api import expose
from pig_manage.api.controllers import base
from pig_manage.api.controllers import collection
from pig_manage.common import exception

from pig_manage.db import api as dbapi

from pig_manage import objects


class ParturitionReportsController(rest.RestController):
    """REST Parturition Report for Default section"""

    def __init__(self):
        super(ParturitionReportsController, self).__init__()
        self.dbapi = dbapi.get_instance()

    @expose.expose(wtypes.text)
    def get_all(self):
        all_records = self.dbapi.get_parturition_record_list(
            pecan.request.context)
        total_num = len(all_records)

        result = []
        # add for more than biggest piglet_num
        calc_limitation = 7
        current_num = 0
        for num in range(0, calc_limitation):
            record = {}
            filters = {'piglet_num': num}
            records = self.dbapi.get_parturition_record_list(
                pecan.request.context, filters)
            record['piglet_num'] = num
            record['count'] = len(records)
            current_num += record['count']
            if total_num == 0:
                record['rate'] = 0
            else:
                record['rate'] = record['count'] / float(total_num) 

            result.append(record)

        # piglet_num bigger than upper limitation
        record['piglet_num'] = calc_limitation
        record['count'] = total_num - current_num
        record['rate'] = record['count'] / float(total_num)
        result.append(record)

        return {'parturition': result}
