from json import JSONEncoder, dumps
from datetime import date, datetime
from uuid import NAMESPACE_DNS, uuid3


class DateTimeEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()

        return JSONEncoder.default(self, obj)


def dict_to_uuid(data):
    return str(uuid3(NAMESPACE_DNS, dumps(data, cls=DateTimeEncoder, sort_keys=True)))