from src.models.status_model import JobStatus

async def file_path_handler(uid, jobs):
    if uid not in jobs:
        return JobStatus.NOT_AVAILABLE
    
    if jobs[uid].completed == False:
        return JobStatus.IN_PROGRESS
    
    if len(jobs[uid].files) == 0:
        return JobStatus.NO_GRANULES
    
    return jobs[uid].files