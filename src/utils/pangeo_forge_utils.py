import asyncio
import os
from pathlib import Path
import subprocess
import s3fs
from config import cloudfrontUrl, s3BucketName, aws_access_key_id, aws_secret_access_key

from src.models.status_model import JobType, Status, JobStatus

def s3_upload_pangeoforge(dir, uid, manager):
    status = f"Uploading {dir} to S3"
    asyncio.run(manager.broadcast(Status(JobType.PANGEO_FORGE, uid, status)))

    s3_file = s3fs.S3FileSystem(anon=False, key=aws_access_key_id, secret=aws_secret_access_key)
    s3_path = f"{s3BucketName}/{uid}"
    s3_file.put(dir, s3_path, recursive=True) 

    return f"{cloudfrontUrl}/{uid}"

def handlePangeoForge(results, current_job, manager):

    data_link_list = []
    dir_path = f"{Path(__file__).parent.parent.absolute().as_posix()}/feedstock"

    for granule in results:
        for asset in granule.data_links():
            if (".nc" in asset):
                data_link_list.append(asset)
    
    with open(f"{dir_path}/url_list.txt", 'w') as f:
        for line in data_link_list:
            f.write(f"{line}\n")
    
    current_job.status = "Granules found, generating zarr files"
    asyncio.run(manager.broadcast(Status(JobType.PANGEO_FORGE, current_job.uid, current_job.status)))

    DIR = Path(__file__).parent.parent.absolute().as_posix()
    bake_script = f"{DIR}/bake.sh"
    zarr_path = f"{DIR}/data/{current_job.uid}/zarr"

    cmd = ["sh", bake_script]
    env = os.environ.copy() | {
        "REPO": f"{DIR}",
        "CONFIG_FILE": f"{DIR}/local_config.py",
        "JOB_NAME": current_job.uid,
    }

    # show live output
    proc = subprocess.Popen(cmd, stdout = subprocess.PIPE, env=env, text=True)
    while (line := proc.stdout.readline()) != "":
        print(line)

    if(len(os.listdir(zarr_path)) > 0):
        upload_path = os.path.dirname(zarr_path)
        current_job.status = "Generated zarr files"
        asyncio.run(manager.broadcast(Status(JobType.PANGEO_FORGE, current_job.uid, current_job.status)))
        response = s3_upload_pangeoforge(upload_path, current_job.uid, manager)
        if (len(response) == 0):
            current_job.status = "Failed uploading zarr to S3"
            asyncio.run(manager.broadcast(Status(JobType.PANGEO_FORGE, current_job.uid, current_job.status)))
            current_job.completed = True
            return
    else:
        current_job.status = "Zarr files could not be generated"
        current_job.completed = True
        asyncio.run(manager.broadcast(Status(JobType.PANGEO_FORGE, current_job.uid, current_job.status)))
        return
    
    remote_files = [] #similar to EA as FE expects array not string path
    remote_files.append(response)
    current_job.files = remote_files
    current_job.completed = True
    current_job.status = JobStatus.JOB_COMPLETE
    asyncio.run(manager.broadcast(Status(JobType.PANGEO_FORGE, current_job.uid, current_job.status)))