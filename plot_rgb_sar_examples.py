import PIL

import matplotlib
matplotlib.use("Agg")  # headless plotting

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

import pytorch.nrw


dset = pytorch.nrw.NRW('dataset', split='test', include_sar=True)
print(dset)

idxs = [4, 15, 33, 71, 118, 173, 250]

fig = plt.figure(figsize=(2*len(idxs), 2*4))
fig.subplots_adjust(top=1.0, bottom=0.0, left=0.0, right=1.0, hspace=0.01, wspace=0.01)
grid = gridspec.GridSpec(ncols=len(idxs), nrows=4, figure=fig)

def vis_sample(sample, idx, grid):

    sample = {k: np.array(v) for k, v in sample.items()}

    ax_rgb = fig.add_subplot(grid[0, idx])
    ax_rgb.imshow(sample['rgb'])
    ax_rgb.axis('off')

    ax_sar = fig.add_subplot(grid[1, idx])
    ax_sar.imshow(dset.sar2rgb(sample['sar']))
    ax_sar.axis('off')

    ax_dem = fig.add_subplot(grid[2, idx])
    ax_dem.imshow(dset.depth2rgb(sample['dem']))
    ax_dem.axis('off')

    ax_seg = fig.add_subplot(grid[3, idx])
    ax_seg.imshow(dset.segm2rgb(sample['seg']))
    ax_seg.axis('off')

    return fig

for idx, img_idx in enumerate(idxs):
    vis_sample(dset[img_idx], idx, grid)

fig.savefig('dataset_examples.jpg', dpi=200)
plt.close(fig)
