import pathlib
import shutil

import numpy as np
import tqdm
import rasterio
import rasterio.mask
import rasterio.windows
from rasterio.warp import calculate_default_transform, reproject, Resampling


def read_bounds(paths):
    bounds = {}
    for path in paths:
        with rasterio.open(path, 'r') as src:
            bounds[path] = src.bounds
    return bounds


def get_overlapping_tsx_paths(rgb_bound, tsx_path_bound_dict):
    return [path for path, tsx_bound in tsx_path_bound_dict.items() if not rasterio.coords.disjoint_bounds(rgb_bound, tsx_bound)]

def reduce_bands(bands):
    band_acc = np.zeros_like(next(iter(bands)))
    count = np.zeros(band_acc.shape, dtype=np.int)
    for band in bands:
        mask = band > 0
        band_acc[mask] += band[mask]
        count[mask] += 1
    mask = band_acc > 0
    band_acc[mask] = band_acc[mask] / count[mask]
    return band_acc


def datasetimg2datasetsar(rgb_image_path):
    """ 32337_5709_rgb.jp2 -> 32337_5709_sar.tif """
    parts = rgb_image_path.split("_")
    return "{}_{}_sar.tif".format(parts[0], parts[1])

SCRIPT_PATH = pathlib.Path(__file__).absolute().parents[0]

# read the boundaries of all TSX acquisitions
TSX_PATHS = list(sorted((SCRIPT_PATH / 'download_tsx/').glob('dims_op_oc_dfd2_*/TSX-1.SAR.L1B/*/IMAGEDATA/*.tif')))
TSX_BOUNDS = read_bounds(TSX_PATHS)

# get all GeoNRW dataset samples
RGB_PATHS = list(sorted((SCRIPT_PATH / "dataset/").glob("*/*.jp2")))

for rgb_path in tqdm.tqdm(RGB_PATHS):
    # get metadata and obunds of RGB
    with rasterio.open(rgb_path, 'r') as rgb:
        kwargs = rgb.meta.copy()
        bounds = rgb.bounds

    # where to store the SAR image
    sar_name = datasetimg2datasetsar(rgb_path.name)

    # there can be multiple TSX tifs that partially include
    # the RGB sample
    tsx_paths = get_overlapping_tsx_paths(bounds, TSX_BOUNDS)

    if not tsx_paths:
        print("found no matching TSX file for {}".format(rgb_path))
    else:
        bands = []
        for tsx_path in tsx_paths:
            with rasterio.open(tsx_path, 'r') as tsx:
                tsx_meta = tsx.meta.copy()
                kwargs['count'] = tsx_meta['count']
                kwargs['driver'] = tsx_meta['driver']
                kwargs['dtype'] = tsx_meta['dtype']

                band = np.empty((kwargs['width'], kwargs['height']), dtype=tsx_meta['dtype'])
                reproject(
                    source=rasterio.band(tsx, 1),
                    destination=band,
                    src_transform=tsx.transform,
                    src_crs=tsx.crs,
                    dst_transform=rgb.transform,
                    dst_crs=rgb.crs,
                    resampling=Resampling.cubic)
                bands.append(band)
        band = reduce_bands(bands)
        # too many invalid pixels -> don't save this tile
        if np.mean(band == 0) > 0.3:
            print("less then 30% valid pixels for TSX file for {}. Skipping.".format(rgb_path))
            continue

        with rasterio.open(rgb_path.parents[0] / sar_name, 'w', **kwargs) as dst:
            dst.write(band, 1)
