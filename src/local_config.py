# Let's put all our data on the same dir as this config file
from pathlib import Path
import os
HERE = Path(__file__).parent

DATA_PREFIX = HERE / 'data'
os.makedirs(DATA_PREFIX, exist_ok=True)

# Target output should be partitioned by job id
c.TargetStorage.fsspec_class = "fsspec.implementations.local.LocalFileSystem"
c.TargetStorage.root_path = f"{DATA_PREFIX}/{{job_name}}"

c.InputCacheStorage.fsspec_class = c.TargetStorage.fsspec_class
c.InputCacheStorage.fsspec_args = c.TargetStorage.fsspec_args

# Input data cache should *not* be partitioned by job id, as we want to get the datafile
# from the source only once
c.InputCacheStorage.root_path = f"{DATA_PREFIX}/cache/input"

c.MetadataCacheStorage.fsspec_class = c.TargetStorage.fsspec_class
c.MetadataCacheStorage.fsspec_args = c.TargetStorage.fsspec_args
# Metadata cache should be per job, as kwargs changing can change metadata
c.MetadataCacheStorage.root_path = f"{DATA_PREFIX}/{{job_name}}/cache/metadata"