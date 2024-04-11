import earthaccess as ea
from src.utils.pangeo_forge_utils import handlePangeoForge
from src.utils.earthaccess_utils import handleEarthAccess
from src.utils.utils import callWithNonNoneArgs
import asyncio

from src.websocket_handler import ConnectionManager

from src.models.status_model import JobStatus, Status, JobType
    
def download_handler(current_job, short_name = None, date_range = None, concept_id = None, bounding_box = None, manager: ConnectionManager = None, isPangeoForge = False):
    jobType = JobType.PANGEO_FORGE if isPangeoForge else JobType.EARTH_ACCESS
    current_job.status = "Querying data"
    asyncio.run(manager.broadcast(Status(jobType, current_job.uid, current_job.status)))

    # Assign bounding_box with geojson coordinates
    if(bounding_box is None):
        bounding_box = (-180.0, -90.0, 180.0, 90.0)
    else:
        bounding_box = tuple(bounding_box)

    results = callWithNonNoneArgs(ea.search_data,
        concept_id = concept_id,
        short_name=short_name,
        cloud_hosted=True,
        temporal=date_range,
        bounding_box=bounding_box,
        count=3
    )

    if (results == []):
        current_job.progress = 100
        current_job.status = JobStatus.NO_GRANULES
        asyncio.run(manager.broadcast(Status(jobType, current_job.uid, current_job.status)))
        return

    if (isPangeoForge):
        handlePangeoForge(results, current_job, manager)
    else:
        handleEarthAccess(results, current_job, manager)