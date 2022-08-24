import pathlib
import itertools

import PIL.Image
import tqdm

def test_size(root):
    """ test that all images are of size 1000x1000

    Args:
    root: dataset root

    """

    root = pathlib.Path(root)

    for img_path in tqdm.tqdm(sorted(root.glob('*/*.*'))):
        with PIL.Image.open(img_path) as img:
            if img.size != (1000, 1000):
                print('{} has wrong size of {}'.format(img_path, img.size))

def test_triplets(root):
    """ test that rgb, dem and seg are all there """
    def get_coords(img_path):
        return tuple((int(x) for x in img_path.stem.split('_')[:2]))

    root = pathlib.Path(root)
    for city in tqdm.tqdm(root.iterdir()):
        img_paths = sorted(city.glob('*.*'), key=get_coords)
        for key, group in itertools.groupby(img_paths, key=get_coords):
            group = list(group)
            if len(group) != 3 and len(group) != 4:
                print('missing a file in {}: {}'.format(city.name, [g.name for g in group]))

root = 'dataset'

print('Checking image dimensions')
test_size(root)

print('\nChecking missing files')
test_triplets(root)
