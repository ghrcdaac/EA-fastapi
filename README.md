# ea-fastapi

In this repo, FastAPI is used as a wrapper around EarthAccess library. There are 4 endpoints defined which can be validated in Postman for tracking,
1. start_download - Downloads files from search result locally and uploads them to S3. Returns a unique job id of 8 characters.
2. status - Returns latest status of the job.
3. get_file_path - Returns S3 path of the uploaded granules.
4. get_metadata - Displays the metadata of granules.

## Pre-requisites

Accounts in AWS and EarthData are necessary for using this wrapper application. The credentials for these accounts should be entered in .env file.
Postman and Docker needs to be installed.

## Steps to Use

Run the following commands:

`docker compose build`

`docker compose up`

Once the Docker container is up and running, the following endpoints can be used to send GET/POST/PUT requests from http://0.0.0.0:8080/:

| Request type | Endpoint | Parameters |
| --- | --- | --- |
| GET | / | N/A |
| PUT | /start_download | short_name, date_range, bounding_box(coordinates can be entered manually or passed as a text in Request Body), concept_id(optional) |
| POST | /status | job_id |
| POST | /get_file_path | job_id |
| POST | /get_metadata | job_id |

For checking status in websocket, choose 'WebSocket' request type and enter ws://localhost:8080/ws.
Enter 'Disconnect' in Messages for disconnecting.
