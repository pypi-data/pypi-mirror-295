from typing import Any, Optional, List

#import sfisop_tsdatamodel.timeseriesdata
from pydantic import BaseModel

from sfisop_tsdatamodel.metadata import *


class Location(BaseModel):

    latitude: float
    longitude: float


class Observation(BaseModel):

    source: Optional[str]   # description of observation source
    source_id: str          # unique identification of observation source (sensor)
    parameter: str          # standardised parameter name
    value: Any
    unit: str                # standardised unit
    qualityCodes: List[int]  # standardized quality code


class DataPoint(BaseModel):

    dp_id: Optional[str]    # unique identification of data point within timeseries
    source: Optional[str]   # description of data point source
    source_id: str          # unique identification of data point source (sensor hub)
    location: Optional[Location]
    time: str               # ISO8601 specification of data point time
    observations: List[Observation]


class TimeSeriesData(BaseModel):

    format: str             # identification of format (SMARTOCEAN_Vx)
    metadata: MetaData
    data: List[DataPoint]

    def to_json_data(self) -> str:
        return self.json()

    def to_json_obj(self):
        return self.dict()



