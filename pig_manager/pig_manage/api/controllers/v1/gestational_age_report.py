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


class GestationalAgeReportsController(rest.RestController):
    """REST Gestational Age Report for Default section"""

    def __init__(self):
        super(GestationalAgeReportsController, self).__init__()
        self.dbapi = dbapi.get_instance()

    @expose.expose(wtypes.text)
    def get_all(self):
        #all_records = self.dbapi.count_sow_by_filter(
        #    pecan.request.context)
        #total_num = len(all_records)

        result = []
        calc_limitation = 12
        upper_limitation = 7

        for num in range(0, calc_limitation):
            filters = {'gestational_age': num}
            records_num = self.dbapi.count_sow_by_filter(
                pecan.request.context, filters)
            if num < upper_limitation:
                record = {}
                record['gestational_age'] = num
                record['count'] = records_num
                result.append(record)
            elif num == upper_limitation:
                record = {}
                record['gestational_age'] = upper_limitation
                record['count'] = records_num
            else:
                record['count'] += records_num
        result.append(record)

        total_num = sum([record['count'] for record in result])
        for record in result:
            if total_num > 0:
                record['rate'] = record['count'] / float(total_num) 
            else:
                record['rate'] = 0
             
        return {'gestational_age_reports': result}
