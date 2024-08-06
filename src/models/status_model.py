from enum import Enum
from dataclasses import dataclass

class JobType(str, Enum):
    EARTH_ACCESS = "EA"
    PANGEO_FORGE = "PF"

class JobStatus(str, Enum):
    NOT_AVAILABLE = "Job not available"
    IN_PROGRESS = "Job in progress"
    NO_GRANULES = "No granules found"
    JOB_COMPLETE = "Job completed"

@dataclass
class Status():
    jobType: JobType = JobType.EARTH_ACCESS
    uid: str = ""
    status: str = ""