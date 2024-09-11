from typing import Optional
from pydantic import BaseModel


class MetaData(BaseModel):

    description: str      # descriptive name of the time series
    timeseries: str       # unique time series identification - needed to identity the timeseries that the data is part of
    origin: Optional[str] # origin time series identification (for traceability of transformations) -  maybe optional?
