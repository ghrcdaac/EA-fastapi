import earthaccess as ea
import xarray as xr

from src.models.status_model import JobStatus

async def metadata_handler(uid, jobs):
    if uid not in jobs:
        return JobStatus.NOT_AVAILABLE
    
    if jobs[uid].completed == False:
        return JobStatus.IN_PROGRESS
    
    if len(jobs[uid].files) == 0:
        return JobStatus.NO_GRANULES
    
    current_job = jobs[uid]

    # Display metadata of one granule
    fileset = ea.open([current_job.result_granules[0]])

    # Open through xarray
    current_job.data = xr.open_mfdataset(fileset, decode_times=False).to_dict(data=False)

    return current_job.data