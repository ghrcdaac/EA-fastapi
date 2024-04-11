from src.models.status_model import JobStatus

async def status_handler(uid, jobs):
    if uid in jobs:
        return jobs[uid].status
    
    return JobStatus.NOT_AVAILABLE
    