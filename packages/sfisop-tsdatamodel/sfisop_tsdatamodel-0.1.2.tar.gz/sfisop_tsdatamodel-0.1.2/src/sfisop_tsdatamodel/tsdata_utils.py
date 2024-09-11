import pydantic
import json

from sfisop_tsdatamodel.timeseriesdata import TimeSeriesData

class ValidateException(Exception):

    def __init__(self, msg: str):
        self.message = msg

    def __str__(self):
        return self.message


def validate_ts_json_data(ts_json_data: str) -> bool:

    try:
        json_item = json.loads(ts_json_data)

    except json.JSONDecodeError as exc:
        raise ValidateException(f'JSONDecodeError: Invalid JSON: {exc.msg}, line {exc.lineno}, column {exc.colno}')

    try:
        TimeSeriesData(**json_item)

    except pydantic.ValidationError as exc:
        raise ValidateException(f'TimeSeriesData Pydantic ValidationError: Invalid schema: {exc}')

    return True


def from_json_obj(ts_json_obj) -> TimeSeriesData:
    return TimeSeriesData.parse_obj(ts_json_obj) # TODO: handle validation exception

def from_json_data(ts_json_data: str) -> TimeSeriesData:
    return TimeSeriesData.parse_raw(ts_json_data) # TODO: handle validation exception
