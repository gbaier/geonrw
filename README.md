Dataset description
===================

This repository contains processing scripts to create the [GeoNRW dataset](https://ieee-dataport.org/open-access/geonrw).
It also contains a script to generate corresponding TerraSAR-X high-resolution spotlight samples, provided you have the corresponding EEC (Enhanced Ellipsoid Corrected) acquisitions.

![Dataset Examples](../imgs/dataset_examples.jpg?raw=true)

The dataset consists of orthorectified aerial photographs, LiDAR derived digital elevation models, segmentation maps with 10 classes, acquired through the [open data program of the German state North Rhine-Westphalia](https://www.opengeodata.nrw.de/produkte/) and refined with OpenStreeMap, and TerraSAR-X high resolution spotlight acquisitions.
Please check the license information [Data licence Germany – attribution – Version 2.0](http://www.govdata.de/dl-de/by-2-0).
Preprocessing consists of resampling the 0.1m resolution photographs to 1m and taking the first LiDAR return while averaging within 1m² to arrive at the same resolution as the photographs.
The geocoded and terrain corrected TerraSAR-X spotlight Enhanced Ellipsoid Corrected (EEC) acquisitions are directly resampled to the same grid.

In total the dataset consists of 7782 tiles of aerial photographs, land cover maps and DEMs of size 1000 × 1000.
Since the TerraSAR-X archive does not contain data for all these tiles the SAR dataset is smaller and only consists of 2980 tiles.
Below you find the class statistics for the dataset with 7782 tiles.

![Dataset Statistics](../imgs/pie_plot.png)

We include a PyTorch dataloader with a tentative split into train and test set.



Creating the GeoNRW Dataset
===========================

All scripts are supposed to be run from the main directory.

1. Run **download_data.sh**
2. Setup new environment with necessary tools and libraries
> conda create --yes --name pdal --channel conda-forge pdal python-pdal tqdm
> conda activate pdal
3. Downsample orthophotos by running **downsample_rgbs.py**
4. Create DEM geotiffs from LiDAR points clouds by running **build_lidar_dem.py**
5. Rasterize landcover shapefiles with **rasterize_landcover.py**
6. Run **verify_dataset.py** to check the output.
   I had one missing LiDAR tile and had to delete the respective RGB and landcover map.


Creating the TerraSAR-X Tiles
=============================

All scripts are supposed to be run from the main directory.

1. Download all acquisitions listed in **tsx_aquisitions.txt** to the directory **download_tsx**
2. Run **proc_tsx.py**
