import argparse
import concurrent.futures
from collections import OrderedDict
import pathlib

from osgeo import ogr, gdal
import tqdm

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--nproc", default=4, type=int, help="number of processes")
parser.add_argument(
    "--dir",
    default=pathlib.Path(__file__).parents[0].absolute(),
    type=pathlib.Path,
    help="base directory of dataset, i.e. where are the downloaded files",
)
args = parser.parse_args()

VECTOR_DIR = args.dir / "landcover_map"
DATASET_DIR = args.dir / "dataset"

GDALFORMAT = "GTiff"
DATATYPE = gdal.GDT_Byte

BURN_IN_VALUES = OrderedDict(
    [
        ("forest", 1),
        ("water", 2),
        ("agricultural", 3),
        ("residential_commercial_industrial", 4),
        ("grassland_swamp_shrubbery", 5),
        ("railway_trainstation", 6),
        ("highway_squares", 7),
        ("airport_shipyard", 8),
        ("roads", 9),
        ("buildings", 10),
    ]
)

print(BURN_IN_VALUES)


def datasetimg2datasetlabel(rgb_image_path):
    """ 32337_5709_rgb.jp2 -> 32337_5709_seg.tif """
    parts = rgb_image_path.split("_")
    return "{}_{}_seg.tif".format(parts[0], parts[1])


def rasterize_landcovers(rgb_image_path):
    seg_name = datasetimg2datasetlabel(rgb_image_path.name)
    output_path = rgb_image_path.parents[0] / seg_name

    rgb_image = gdal.Open(str(rgb_image_path), gdal.GA_ReadOnly)
    label_mask = gdal.GetDriverByName(GDALFORMAT).Create(
        str(output_path), rgb_image.RasterXSize, rgb_image.RasterYSize, 1, DATATYPE,
    )

    label_mask.SetProjection(rgb_image.GetProjectionRef())
    label_mask.SetGeoTransform(rgb_image.GetGeoTransform())

    for lv, biv in BURN_IN_VALUES.items():
        shp_path = str(VECTOR_DIR / (lv + ".shp"))
        shape = ogr.Open(shp_path)
        gdal.RasterizeLayer(label_mask, [1], shape.GetLayer(), burn_values=[biv])

    # close files
    del rgb_image, label_mask


print("Rasterizing shapefiles")
rgb_image_paths = list(DATASET_DIR.glob("*/*rgb.jp2"))

with concurrent.futures.ProcessPoolExecutor(max_workers=args.nproc) as executor:
    futures = list(
        tqdm.tqdm(
            executor.map(rasterize_landcovers, rgb_image_paths),
            total=len(rgb_image_paths)
        )
    )
