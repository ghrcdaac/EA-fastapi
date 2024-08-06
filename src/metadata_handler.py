import earthaccess as ea
import xarray as xr

from src.models.status_model import JobStatus

async def metadata_handler(uid, jobs):
    """
    Asynchronously retrieves and processes the metadata for the specified job using EarthAccess API and xarray.
    
    Args:
        uid (str): Unique identifier for the job.
        jobs (dict): Dictionary of jobs which may contain granule results and other metadata.
    
    Returns:
        A dictionary containing processed metadata or a job status; or an error message if metadata cannot be parsed.
    """
    try:
        if uid not in jobs:
            return JobStatus.NOT_AVAILABLE
        
        if not jobs[uid].completed:
            return JobStatus.IN_PROGRESS
        
        if len(jobs[uid].files) == 0:
            return JobStatus.NO_GRANULES
        
        current_job = jobs[uid]

        # Display metadata of one granule
        fileset = ea.open([current_job.result_granules[0]])

        # Open through xarray
        current_job.data = xr.open_mfdataset(fileset, decode_times=False).to_dict(data=False)
        return current_job.data

    except Exception:
        return "Metadata could not be parsed, ensure that the files are in NetCDF format." 