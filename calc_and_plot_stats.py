import pathlib

from PIL import Image
import numpy as np
import tqdm

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects

matplotlib.use("Agg")  # headless plotting

######################
#                    #
# Count class labels #
#                    #
######################

classes = [
    "Forest",
    "Water",
    "Agricultural",
    "Urban",
    "Grassland",
    "Railway",
    "Highway",
    "Airport, shipyard",
    "Roads",
    "Buildings",
]


# will be a ordered dictionary
classes = {cl: 0 for cl in classes}

for seg_path in tqdm.tqdm(pathlib.Path.cwd().glob("dataset/*/*_seg.tif")):
    seg = np.array(Image.open(seg_path))
    for idx, class_name in enumerate(classes, 1):
        classes[class_name] += np.sum(seg == idx)

n_samples = sum(classes.values())

for class_name, count in classes.items():
    print("{:>20s} : {:0>7.6f}".format(class_name, count / n_samples))

############
#          #
# Plotting #
#          #
############

fig = plt.figure(figsize=(4.0, 2.5))
fig.subplots_adjust(left=0.01, right=0.6, bottom=0.01, top=0.88)


order = [
    "Forest",
    "Water",
    "Agricultural",
    "Railway",
    "Urban",
    "Highway",
    "Grassland",
    "Airport, shipyard",
    "Roads",
    "Buildings",
]

colors = [
    "#2ca02c",  # green for forest
    "#1f77b4",  # blue for water
    "#8c564b",  # brown for agricultural
    "#ff7f0e",  # orange for railway
    "#7f7f7f",  # gray urban
    "#9467bd",  # purple for highway
    "#bcbd22",  # olive for grassland
    "#17becf",  # cyan for airports and shipyards
    "#d62728",  # red for roads
    "#e377c2",  # pink for buildings
]

ratios = [classes[cl] / n_samples for cl in order]

kwargs = {
    "startangle": 90,
    "wedgeprops": dict(width=0.5),
    "colors": colors,
    "autopct": "%.1f%%",
    "pctdistance": 0.80,
    "textprops": {
        "color": "w",
        "path_effects": [
            path_effects.Stroke(linewidth=2.0, foreground="black"),
            path_effects.Normal(),
        ],
    },
}

ax = fig.add_subplot(1, 1, 1)
wedges, texts, autotexts = ax.pie(ratios, **kwargs)
ax.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.

fig.legend(
    wedges, order, loc="center right", borderaxespad=0.5,
)
fig.suptitle("Dataset statistics")

fig.savefig("pie_plot.pdf")
