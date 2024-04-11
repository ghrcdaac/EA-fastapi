import boto3
import logging
import earthaccess as ea
import asyncio
import os
from src.models.status_model import JobType, Status, JobStatus

from config import cloudfrontUrl, s3BucketName, fileDownloadPath, aws_access_key_id, aws_secret_access_key

# upload file to S3 and return the S3 URL
def s3_upload_earthaccess(file, uid, manager):
    s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key)
    file_name = os.path.split(file)[1]
    key=f'{uid}/{file_name}'
    print(file, key)
    status = f"Uploading {file_name} to S3"
    asyncio.run(manager.broadcast(Status(JobType.EARTH_ACCESS, uid, status)))

    try:
        s3_client.upload_file(file, s3BucketName, key)
    except Exception as e:
        logging.exception(e)
        return ""

    return f"{cloudfrontUrl}/{key}"

def handleEarthAccess(results, current_job, manager):

    current_job.result_granules = results
    current_job.progress = 0

    # CHECK: ea should tell about calculating percentage, can't use external libraries as this is unique for each case.
    # might be available for s3 upload, % for downloading from ea should be given by ea
    remote_files = []
    for result in results:
        current_job.progress += 1
        current_job.status = f"In progress - downloading files {current_job.progress}/{len(results)}"
        asyncio.run(manager.broadcast(Status(JobType.EARTH_ACCESS, current_job.uid, current_job.status)))

        # download from CMR to a local path
        result_file = ea.download(granules=result,local_path=fileDownloadPath)
        response = s3_upload_earthaccess(result_file[0], current_job.uid, manager)
        if (len(response) == 0):
            current_job.status = "File could not be uploaded to S3"
            asyncio.run(manager.broadcast(Status(JobType.EARTH_ACCESS, current_job.uid, current_job.status)))
            current_job.completed = True
            return
        
        # Upload the downloaded file to S3 and get the S3 URL
        remote_files.append(response)
    
    current_job.files = remote_files
    current_job.completed = True
    current_job.status = JobStatus.JOB_COMPLETE
    asyncio.run(manager.broadcast(Status(JobType.EARTH_ACCESS, current_job.uid, current_job.status)))