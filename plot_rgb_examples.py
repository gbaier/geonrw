""" plots some examples of the dataset """

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from PIL import Image

matplotlib.use("Agg")  # headless plotting

paths = [
    "duesseldorf/340_5677",
    "duesseldorf/341_5676",
    "duesseldorf/342_5676",
    "duesseldorf/344_5675",
    "duesseldorf/346_5684",
    "duesseldorf/350_5682",
    "herne/379_5709",
]


#######################################
#                                     #
# Conversion of land cover map to RGB #
#                                     #
#######################################

lcov_cmap = matplotlib.colors.ListedColormap(
    [
        "#2ca02c",  # green for forest
        "#1f77b4",  # blue for water
        "#8c564b",  # brown for agricultural
        "#7f7f7f",  # gray urban
        "#bcbd22",  # olive for grassland
        "#ff7f0e",  # orange for railway
        "#9467bd",  # purple for highway
        "#17becf",  # cyan for airports and shipyards
        "#d62728",  # red for roads
        "#e377c2",  # pink for buildings
    ]
)
lcov_norm = matplotlib.colors.Normalize(vmin=1, vmax=10)


def seg2rgb(seg_map):
    """ converts segmentation map to a plotable RGB image """
    return lcov_cmap(lcov_norm(seg_map))[:, :, :3]


############
#          #
# Plotting #
#          #
############

def calc_figsize(paths):
    def add_padding(dim):
        pad = 0.01
        return dim + (dim - 1) * pad

    nrows = 3
    ncols = len(paths)
    return add_padding(ncols), add_padding(nrows)


fig = plt.figure(figsize=calc_figsize(paths))
fig.subplots_adjust(top=1.0, bottom=0.0, left=0.0, right=1.0, hspace=0.01, wspace=0.01)
grid = gridspec.GridSpec(ncols=len(paths), nrows=3, figure=fig)

for idx, path in enumerate(paths):
    rgb = Image.open("dataset/" + path + "_rgb.jp2").convert("RGB")
    ax_rgb = fig.add_subplot(grid[0, idx])
    ax_rgb.imshow(rgb)
    ax_rgb.axis("off")

    dem = np.array(Image.open("dataset/" + path + "_dem.tif"))
    ax_dem = fig.add_subplot(grid[1, idx])
    ax_dem.imshow(dem)
    ax_dem.axis("off")

    seg = np.array(Image.open("dataset/" + path + "_seg.tif"))
    ax_seg = fig.add_subplot(grid[2, idx])
    ax_seg.imshow(seg2rgb(seg))
    ax_seg.axis("off")

fig.savefig("dataset_rgb_examples.jpg", dpi=200)
