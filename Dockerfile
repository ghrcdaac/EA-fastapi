FROM ghcr.io/osgeo/gdal:ubuntu-small-3.9.1
RUN apt-get update && apt-get -y install python3-pip --fix-missing
COPY requirements.txt .
COPY requirements-additional.txt .
# RUN ln -s /usr/include/hdf5/serial /usr/include/hdf5/include
# RUN export HDF5_DIR=/usr/include/hdf5
# RUN pip install versioned-hdf5 --break-system-packages
RUN apt-get -y install pkg-config libhdf5-dev
RUN apt-get -y install python3.12-venv
RUN pip install --no-binary=h5py h5py --break-system-packages
RUN pip install -r requirements.txt --break-system-packages
RUN pip install -r requirements-additional.txt --break-system-packages
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]