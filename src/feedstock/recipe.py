import aiohttp
import apache_beam as beam
import os
import sys
from pathlib import Path

__file__ = "recipe.py"
DIR = Path(__file__).parent.absolute().as_posix()
sys.path.append(DIR)
from config import username, password

from pangeo_forge_recipes.patterns import ConcatDim, FilePattern
from pangeo_forge_recipes.transforms import OpenURLWithFSSpec, OpenWithXarray, StoreToZarr

urls_file_path = f"{Path(__file__).parent.absolute().as_posix()}/src/feedstock/url_list.txt"

outfile = open(urls_file_path, 'r')
lines = outfile.readlines()
count_lines = len(lines)
range_lines = range(count_lines)

os.remove(urls_file_path)

def make_url(time):
    return lines[time]
    
concat_dim = ConcatDim("time", range_lines)
pattern = FilePattern(make_url, concat_dim)

# for index, url in pattern.items():
#     print(url)

recipe = (
    beam.Create(pattern.items())
    | OpenURLWithFSSpec(open_kwargs={'client_kwargs': {"auth" : aiohttp.BasicAuth(username, password)}})
    | OpenWithXarray(file_type=pattern.file_type, xarray_open_kwargs={"decode_coords": "all"})
    | StoreToZarr(
        store_name="zarr",
        combine_dims=pattern.combine_dim_keys,
    )
)