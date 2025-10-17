import datetime
import json


class DateJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return {"value": o.strftime("%Y-%m-%d %H:%M:%S"), "__datetime__": True}
        elif isinstance(o, datetime.date):
            return {"value": o.strftime("%Y-%m-%d"), "__date__": True}

        return json.JSONEncoder.default(self, o)


def as_date_datetime(dct) -> datetime.datetime | datetime.date | dict:
    if "__datetime__" in dct:
        return datetime.datetime.strptime(dct["value"], "%Y-%m-%d %H:%M:%S")

    if "__date__" in dct:
        return datetime.datetime.strptime(dct["value"], "%Y-%m-%d %H:%M:%S").date()

    return dct
