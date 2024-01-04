import random
from typing import Dict
from fastapi import Body, FastAPI, Query, WebSocket
import string

from src import *

from http import HTTPStatus
from fastapi import BackgroundTasks

# Dict as job storage
jobs: Dict[str, Job] = {}
app = FastAPI()

# Authenticate user and allow login
login_handler()

# Root endpoint
@app.get("/")
async def root():
    return await root_handler()

manager = ConnectionManager()

# Establish WebSocket connection
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    return await websocket_endpoint_handler(websocket, manager)

# Start a download job in the background
@app.put("/start_download", status_code=HTTPStatus.ACCEPTED)
async def start_download(background_tasks: BackgroundTasks, short_name: str | None = None, date_range: list = Query([]) , concept_id: str | None = None, bounding_box: list | None = Query(None), bounding_box_geojson: str | None = Body(None)):
   
    # Create a new Job instance and add it to the jobs dictionary
    current_job = Job()
    current_job.uid = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    jobs[current_job.uid] = current_job

    # Add the download job to the background tasks
    background_tasks.add_task(download_handler, current_job, short_name, tuple(date_range), concept_id, bounding_box, bounding_box_geojson, manager)
    return current_job.uid

# Check the status of a job
@app.post("/status")
async def status(uid: str):
    return await status_handler(uid, jobs)

# Get the files associated with a job
@app.post("/get_file_path")
async def get_file_path(uid: str):
    return await file_path_handler(uid, jobs)

# Display metadata associated with a job
@app.post("/get_metadata")
async def get_metadata(uid: str):
    return await metadata_handler(uid, jobs)
