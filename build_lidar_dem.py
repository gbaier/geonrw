import argparse
import concurrent.futures
import pathlib
from tempfile import TemporaryDirectory
from zipfile import ZipFile
import io

import cv2
import pdal
import rasterio
import numpy as np
import tqdm
import util


parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--nproc", default=4, type=int, help="number of processes")
parser.add_argument(
    "--dir",
    default=pathlib.Path(__file__).parents[0].absolute(),
    type=pathlib.Path,
    help="base directory of dataset, i.e. where are the downloaded files",
)
args = parser.parse_args()


pipeline_template = """
{{
  "pipeline":[
    {{
        "filename":"{}",
        "override_srs":"EPSG:5555",
        "type": "readers.las"
    }},
    {{
        "type":"filters.returns",
        "groups":"first,only"
    }},
    {{
        "filename":"{}",
        "gdaldriver":"GTiff",
        "output_type":"mean",
        "resolution":"1.0",
        "origin_x": {},
        "origin_y": {},
        "width":"1000",
        "height":"1000",
        "data_type":"float",
        "type": "writers.gdal"
    }}
  ]
}}"""


def zip2cityname(zip_name):
    """ returns the name of a city from the top filename

    E.g. 3dm_l_las_05112000_Duisburg_EPSG25832_XYZ.zip -> duisburg

    """

    return util.deumlautify(zip_name.split('_')[4].lower())


def laz2coords(laz_file):
    """ groups xyz_filenames by their coordinates

    E.g. dom1l-fp_32348_5703_1_nw.xyz by (32348, 5703)
    E.g. 3dm_32_459_5757_1_nw.laz (32459, 5703)

    The zip archives containes to types of point clouds
    1. fp for first pulse
    2. aw for filled water

    These must be merge in lates processing steps

    """
    parts = laz_file.split('_')
    return tuple((int(p) for p in parts[2:4]))


def inpaint_lidar_holes(tif_file):
    """ fill lidar holes """
    inpaint_radius = 3
    with rasterio.open(tif_file, "r") as src:
        profile = src.profile
        dem = np.array(src.read(1))

    mask = (dem < 1)
    dem[mask] = 0

    # opencv requires uint8 input
    dem = cv2.inpaint(dem, mask.astype(np.uint8), inpaint_radius, cv2.INPAINT_NS)

    with rasterio.open(tif_file, "w", **profile) as dst:
        dst.write(dem, 1)


def unzip_rasterize_inpaint(zip_path):
    city_name = zip2cityname(zip_path.name)
    out_dir = args.dir / "dataset" / city_name
    with ZipFile(zip_path, 'r') as zipfl:
        with TemporaryDirectory() as tmpdir:
            for laz_file in zipfl.namelist():
                zipfl.extract(laz_file, tmpdir)

                coords = laz2coords(laz_file)

                out_path = out_dir / '{}_{}_dem.tif'.format(*coords)
                in_path = pathlib.Path(tmpdir) / laz_file

                # join both first pulse (fp) and filled water (aw) to one xyz file
                pipeline = pipeline_template.format(in_path, out_path, 1000 * (coords[0] % 1000), 1000*coords[1])
                pipeline = pdal.Pipeline(pipeline)
                pipeline.validate()
                pipeline.execute()
                inpaint_lidar_holes(out_path)
                in_path.unlink()


zip_files = list((args.dir / "download").glob('3dm_l_las_*.zip'))

with concurrent.futures.ProcessPoolExecutor(max_workers=args.nproc) as executor:
    futures = list(
        tqdm.tqdm(executor.map(unzip_rasterize_inpaint, zip_files), total=len(zip_files))
    )
