import earthaccess as ea
from src.utils import callWithNonNoneArgs
import boto3
import os
import geopandas as gpd
import asyncio
import logging

from config import s3Url, s3ObjectUrl,s3BucketName, fileDownloadPath, aws_access_key_id, aws_secret_access_key
from src.websocket_handler import ConnectionManager

# TO-DO: s3_upload can be moved into a separate class like ConnectionManager in main.py
# so that any error while setting up S3 is taken care of in the beginning itself
# CHECK: The s3 status should be known only to the backend? The client in frontend need not know
# what's being done in s3

# upload file to S3 and return the S3 URL
def s3_upload(file, uid, status, manager):
    s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key)
    file_name = os.path.split(file)[1]
    key=f'{uid}/{file_name}'
    print(file, key)
    status = f"{uid}: uploading {file_name} to S3"
    asyncio.run(manager.broadcast(status))

    try:
        s3_client.upload_file(file, s3BucketName, key)
    except Exception as e:
        logging.exception(e)
        return ""

    return f"{s3ObjectUrl}/{key}"
    
def download_handler(current_job, short_name = None, date_range = None, concept_id = None, bounding_box = None, bounding_box_geojson = None, manager: ConnectionManager = None):
    current_job.status = f"{current_job.uid}: querying data"
    asyncio.run(manager.broadcast(current_job.status))

    # Assign bounding_box with geojson coordinates
    if(bounding_box is None):
        if(bounding_box_geojson is not None):
            gdf = gpd.read_file(bounding_box_geojson, driver='GeoJSON')
            xmin, ymin, xmax, ymax = gdf.total_bounds
            bounding_box = (xmin, ymin, xmax, ymax)
        
        else:
            bounding_box = (-180.0, -90.0, 180.0, 90.0)

    # Call the search_data function with non-None arguments
    results = callWithNonNoneArgs(ea.search_data,
    concept_id = concept_id,
    short_name=short_name,
    cloud_hosted=True,
    temporal=date_range,
    bounding_box=bounding_box,
    count = 3  #set count for testing purposes
    )

    current_job.result_granules = results
    current_job.progress = 0
    print("results ", results)

    if (results == []):
        current_job.progress = 100
        current_job.status = f"{current_job.uid}: No files to download"
        asyncio.run(manager.broadcast(current_job.status))
        return

    # CHECK: ea should tell about calculating percentage, can't use external libraries as this is unique for each case.
    # might be available for s3 upload, % for downloading from ea should be given by ea
    remote_files = []
    for result in results:
        current_job.progress += 1
        current_job.status = f"{current_job.uid}: in progress - downloading files {current_job.progress}/{len(results)}"
        asyncio.run(manager.broadcast(current_job.status))

        # download from CMR to a local path
        result_file = ea.download(granules=result,local_path=fileDownloadPath)
        print("result_file ", result_file)

        response = s3_upload(result_file[0], current_job.uid, current_job.status, manager)
        if (len(response) == 0):
            current_job.status = f"{current_job.uid}: File could not be uploaded to S3"
            asyncio.run(manager.broadcast(current_job.status))
            return
        # Upload the downloaded file to S3 and get the S3 URL
        remote_files.append(response)
    
    current_job.files = remote_files
    current_job.status = f"{current_job.uid}: Download completed"
    asyncio.run(manager.broadcast(current_job.status))
    print("remote files", remote_files)