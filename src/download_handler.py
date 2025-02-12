import earthaccess as ea
from src.utils.pangeo_forge_utils import handlePangeoForge
from src.utils.earthaccess_utils import handleEarthAccess
from src.utils.utils import callWithNonNoneArgs
import asyncio

from src.websocket_handler import ConnectionManager

from src.models.status_model import JobStatus, Status, JobType
    
def download_handler(current_job, short_name = None, date_range = None, concept_id = None, bounding_box = None, manager: ConnectionManager = None, isPangeoForge = False):
    """
    Handles the download process for data based on specified parameters, supporting both EarthAccess and pangeo-forge workflows.

    Args:
        current_job (Job): The current job object containing information about the job.
        short_name (str): Short name identifier for the dataset.
        date_range (str): String specifying the date range for the dataset query.
        concept_id (str, optional): The unique identifier for the dataset, if applicable.
        bounding_box (tuple, optional): Tuple specifying the geographic bounding box for the dataset query.
        isPangeoForge (bool): Flag to determine if the job is for Pangeo Forge; otherwise, it's for Earth Access.

    This function sets the job status, performs a EarthAccess search with non-None parameters, 
    and processes results according to the specified workflow (Pangeo Forge or Earth Access). 
    It also handles broadcasting status updates through the specified connection manager.
    """
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
        current_job.completed = True
        asyncio.run(manager.broadcast(Status(jobType, current_job.uid, current_job.status)))
        return

    if (isPangeoForge):
        handlePangeoForge(results, current_job, manager)
    else:
        handleEarthAccess(results, current_job, manager)