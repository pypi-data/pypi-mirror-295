from rasterio.mask import mask as rasterio_mask
import rasterio
from rasterio.merge import merge
from rasterio.plot import show
from glob import glob
import os
import tempfile
import numpy as np
from pathlib import Path
import geopandas as gpd
from rasterio import mask


def mosaic(main_folder_path, sub_folder_list):
    print(main_folder_path)
    print('\n')
    print(sub_folder_list)
    
    temp_mosaic_dir = tempfile.mkdtemp()
    for folder in sub_folder_list:
        path = os.path.join(main_folder_path, folder)
        images_to_mosaic = glob(os.path.join(path, '*.tiff'))
        print('Images to mosaic:: \n',images_to_mosaic)

        img_to_mosaic = [rasterio.open(file) for file in images_to_mosaic]
        mosaic, out_trans = merge(img_to_mosaic)

        out_meta = img_to_mosaic[0].meta.copy()
        out_meta.update({"driver": "GTiff", "height": mosaic.shape[1], "width": mosaic.shape[2], "transform": out_trans})
        # Set the output CRS
        out_crs = img_to_mosaic[0].crs
        out_meta.update({"crs": out_crs})
        output_file = os.path.join(temp_mosaic_dir, f"{folder}.tif")
        with rasterio.open(output_file, "w", **out_meta) as dest:
            dest.write(mosaic)

    return temp_mosaic_dir

    

def composite_mosaic_image(mosaic_folder, dates):
    mosaic_image_list = glob(os.path.join(mosaic_folder, '*.tif'))
    mosaic_image_list = sorted(mosaic_image_list)
    print('\n')
    print(mosaic_image_list)

    base_image_list = []
    target_image_list = []

    if dates[0] < 2020 and dates[1] < 2020:
        base_image_list = mosaic_image_list[:2]
        target_image_list = mosaic_image_list[2:4]
    elif dates[0] < 2020 and dates[1] == 2020:
        base_image_list = mosaic_image_list[:2]
        target_image_list = mosaic_image_list[2:8]
    elif dates[0] < 2020 and dates[1] > 2020:
        base_image_list = mosaic_image_list[:2]
        target_image_list = mosaic_image_list[2:14]
    elif dates[0] == 2020 and dates[1] > 2020:
        base_image_list = mosaic_image_list[:6]
        target_image_list = mosaic_image_list[6:18]
    elif dates[0] > 2020 and dates[1] > 2020:
        base_image_list = mosaic_image_list[:12]
        target_image_list = mosaic_image_list[12:24]

    print(f'Base Images: {base_image_list}\n')
    print(f'Target Images: {target_image_list}\n')

    base_images = []
    target_images = []

    for file in base_image_list:
        with rasterio.open(file) as image:
            base_images.append(image.read().astype(np.float32))

    for file in target_image_list:
        with rasterio.open(file) as image:
            target_images.append(image.read().astype(np.float32))

    base_mean_composite = np.mean(base_images, axis=0)
    target_mean_composite = np.mean(target_images, axis=0)

    with rasterio.open(base_image_list[0]) as base, rasterio.open(target_image_list[0]) as target:
        base_meta = base.meta.copy()
        target_meta = target.meta.copy()

        # Update the metadata for data type to float32
        base_meta.update(dtype='float32', driver='GTiff')
        target_meta.update(dtype='float32', driver='GTiff')

        # Create temporary files
        with tempfile.NamedTemporaryFile(suffix='.tif', delete=False) as base_temp, \
             tempfile.NamedTemporaryFile(suffix='.tif', delete=False) as target_temp:
            
            base_composite_file = base_temp.name
            target_composite_file = target_temp.name

            with rasterio.open(base_composite_file, 'w', **base_meta) as dst_1:
                dst_1.write(base_mean_composite.astype(np.float32))

            with rasterio.open(target_composite_file, 'w', **target_meta) as dst_2:
                dst_2.write(target_mean_composite.astype(np.float32))

    return base_composite_file, target_composite_file
   
       


def clip_raster(image, clip_shapefile):
    name = Path(image).stem
    print(f'\nClipping {name} mosaic to extent')

    # Create a temporary file
    with tempfile.NamedTemporaryFile(suffix='.tif', delete=False) as temp_file:
        output_clipped_raster = temp_file.name

    with rasterio.open(image) as src:

        gdf = gpd.read_file(clip_shapefile)
        # Ensure the GeoDataFrame is in the same CRS as the raster
        gdf = gdf.to_crs(src.crs)
        shapes = gdf.geometry.values

        out_image, out_transform = rasterio_mask(src, shapes, crop=True)
        out_meta = src.meta.copy()
        out_meta.update({
            "driver": "GTiff",
            "height": out_image.shape[1],
            "width": out_image.shape[2],
            "transform": out_transform
        })

        # Write the clipped raster
        with rasterio.open(output_clipped_raster, "w", **out_meta) as dest:
            dest.write(out_image)

    return output_clipped_raster
