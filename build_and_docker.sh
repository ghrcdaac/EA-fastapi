docker build  -t fcx-fastapi .
docker stop fcx-fastapi-container
docker rm fcx-fastapi-container
docker run -d --name fcx-fastapi-container -p80:80 fcx-fastapi