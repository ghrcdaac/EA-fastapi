FROM osgeo/gdal:ubuntu-small-latest
RUN apt-get update && apt-get -y install python3-pip --fix-missing
WORKDIR /app
COPY requirements.txt .
COPY requirements1.txt .
RUN pip install -r requirements.txt
RUN pip install -r requirements1.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]