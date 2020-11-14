import argparse
import concurrent.futures
import pathlib
from zipfile import ZipFile

import tqdm
from osgeo import gdal
import os

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


def correct_ecs_byte(path):
    """ the enumerated color space is wrongly defined in all jpeg2000 files.

    This function replaces that exact byte with the correct value x10

    """

    color_spec = b"\x63\x6f\x6c\x72"  # color specification header type
    offset_to_colr = 10  # offset of ECS byte to color specification header
    with open(path, "r+b") as fp:
        bits = fp.read(120)
        color_spec_pos = bits.find(color_spec)
        fp.seek(color_spec_pos + offset_to_colr, os.SEEK_SET)
        fp.write(b"\x10")  # replace ECS with correct value

    return color_spec_pos


def dop2cityname(dop_name):
    """ returns the name of a city from the top filename

    E.g. dop_05112000_Duisburg_EPSG25832_JPEG2000.zip -> duisburg

    """

    return util.deumlautify(dop_name.split("_")[2].lower())


def zipimg2datasetimg(zip_jp2_name):
    """ F9_dop10rgbi_32343_5697_1_nw.jp2 -> rgb_32343_5697.jp2 """
    parts = zip_jp2_name.split("_")
    return "{}_{}_rgb.jp2".format(parts[2], parts[3])


FORMAT = "JP2OpenJPEG"


def unzip_and_resample(zip_path):
    out_dir = args.dir / "dataset" / dop2cityname(zip_path.name)
    out_dir.mkdir(exist_ok=True, parents=True)

    with ZipFile(zip_path) as zipfl:
        for jp2_file in zipfl.namelist():
            path = out_dir / zipimg2datasetimg(jp2_file)

            # virtual zip path
            vzip = "/vsizip/" + str(zip_path / jp2_file)

            gdal.Translate(
                str(path),
                vzip,
                width=1000,
                height=1000,
                format="JP2OpenJPEG",
                resampleAlg="lanczos",
            )
            correct_ecs_byte(path)


zip_files = list((args.dir / "download").glob("dop_*_JPEG2000.zip"))

with concurrent.futures.ProcessPoolExecutor(max_workers=args.nproc) as executor:
    futures = list(
        tqdm.tqdm(executor.map(unzip_and_resample, zip_files), total=len(zip_files))
    )
