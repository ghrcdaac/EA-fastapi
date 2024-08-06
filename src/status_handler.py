from src.models.status_model import JobStatus

async def status_handler(uid, jobs):
    """
    Asynchronously retrieves the status of a specified job.
    
    Args:
        uid (str): Unique identifier for the job.
        jobs (dict): Dictionary containing job details and statuses.
    
    Returns:
        The current status of the job if available; otherwise, returns a status indicating the job is not available.
    """
    if uid in jobs:
        return jobs[uid].status
    
    return JobStatus.NOT_AVAILABLE
    