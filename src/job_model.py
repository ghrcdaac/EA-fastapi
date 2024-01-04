from typing import List
from pydantic import BaseModel
import earthaccess as ea

class Job(BaseModel):
    # unique uid with length=8 can't be created with Pydantic model
    uid: str = ""
    status: str = "in_progress"
    progress: int = 0
    files: list[str] = []   # List of files downloaded
    data: list[str] = []    # Data within the files downloaded
    result_granules: List[ea.results.DataGranule] = []      # Store results of ea.search_data()

    # Type of result_granules is not in-built
    class Config:
        arbitrary_types_allowed = True