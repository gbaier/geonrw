import PIL
print(PIL.__version__)
print(PIL.__file__)

# headless
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib as mpl
import tqdm
import numpy as np

import pytorch.nrw



#landcover color map
# see matplotlib.colors.TABLEAU_COLORS
lcov_cmap = mpl.colors.ListedColormap([
   '#2ca02c', # matplotlib green for forest
   '#1f77b4', # matplotlib blue for water
   '#8c564b', # matplotlib brown for agricultural
   '#7f7f7f', # matplotlib gray residential_commercial_industrial
   '#bcbd22', # matplotlib olive for grassland_swamp_shrubbery
   '#ff7f0e', # matplotlib orange for railway_trainstation
   '#9467bd', # matplotlib purple for highway_squares
   '#17becf', # matplotlib cyan for airport_shipyard
   '#d62728', # matplotlib red for roads
   '#e377c2', # matplotlib pink for buildings
])

def vis_sample(sample):
    fig = plt.figure(figsize=(8, 2.3))

    sample = {k: np.array(v) for k, v in sample.items()}

    fig.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.92, wspace=0.05)

    ax_rgb = fig.add_subplot(1, 4, 1)
    ax_rgb.imshow(sample['rgb'])
    ax_rgb.set_title('RGB')
    ax_rgb.axis('off')

    ax_sar = fig.add_subplot(1, 4, 2)
    ax_sar.imshow(np.log(sample['sar']), cmap='gray')
    ax_sar.set_title('SAR')
    ax_sar.axis('off')

    ax_dem = fig.add_subplot(1, 4, 3)
    dem = sample['dem']
    dem -= dem.min()
    dem /= dem.max()
    ax_dem.imshow(dem, cmap='viridis')
    ax_dem.set_title('DEM')
    ax_dem.axis('off')

    ax_seg = fig.add_subplot(1, 4, 4)
    ax_seg.imshow(sample['seg'], cmap=lcov_cmap, vmin=1, vmax=10)
    ax_seg.set_title('Land cover')
    ax_seg.axis('off')

    return fig


dset = pytorch.nrw.NRW('dataset', split='test')
print(dset)

for idx in tqdm.tqdm(range(0, len(dset))):
    sample = dset[idx]
    fig = vis_sample(sample)
    fig.savefig('visualized/vis_{:0>4d}.jpg'.format(idx), dpi=150)
    plt.close(fig)
