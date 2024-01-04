import earthaccess as ea
import xarray as xr

async def metadata_handler(uid, jobs):
    # Check if the specified job UID exists in the jobs dictionary
    if uid in jobs:
        current_job = jobs[uid]
        print("current_job.result_granules: ", current_job.result_granules)
        #CHECK: s3url - give region; http_url(from result_granules.data?) - give provider
        #can't use fcx-downloader http url as it has no provider
        fileset = ea.open(current_job.result_granules)
        print("fileset: ", fileset)

        # Open through xarray
        current_job.data = xr.open_mfdataset(fileset, decode_times=False).to_dict(data=False)
        print("current_job.data ", current_job.data)
        return current_job.data
    else:
        return "Job not available"