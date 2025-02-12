from typing import List, Dict
from pydantic import BaseModel
import earthaccess as ea
import json

class Coord(BaseModel):
    dims: List[str]
    attrs: Dict[str, str]
    dtype: str
    shape: List[int]

class Metadata(BaseModel):
    coords: Dict[str, Coord]

class Job(BaseModel):
    # unique uid with length=8 can't be created with Pydantic model
    uid: str = ""
    status: str = "in_progress"
    progress: int = 0
    completed: bool = False
    files: list[str] = []   # List of files downloaded
    data: Metadata = {}
    result_granules: List[ea.results.DataGranule] = []      # Store results of ea.search_data()

    # Type of result_granules is not in-built
    class Config:
        arbitrary_types_allowed = True