async def status_handler(uid, jobs):
    if uid in jobs:
        return jobs[uid].status
    else:
        return "Job not available"
    