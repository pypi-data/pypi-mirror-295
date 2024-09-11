# Timeseries data model

The purpose of the data model is to support the exchange of time series data in particular exchange of fragments of data assosiated with time series. 

The data model is implemented based on the Pydantic framework: https://docs.pydantic.dev/latest/

The utility functions implemented in the `tsdata_utils.py` and `timeseriesdata.py` is to be used for serialisation and de-serialisation of time series data.

# Standards

The `parameter` and `unit` in the `Observation` class is to follow the Copernicus Marine in-situ TAC physical parameters list:

https://archimer.ifremer.fr/doc/00422/53381/

The `qualityCodes` is to follow the recommendations for in-situ data Near Real Time Quality Control:

https://archimer.ifremer.fr/doc/00251/36230/


The `time` object variable in the `Datapoint` class is to follow the ISO8601 standard and include timezone information.

# Installation

```
python -m pip install -r requirements.txt
```

Setup `PYTHONPATH` to include the top-level folder:

```
export PYTHONPATH=<path to top-level folder>/datamodels/
```

# Testing

Run `pytest` in the `datamodels/tests` folder.


