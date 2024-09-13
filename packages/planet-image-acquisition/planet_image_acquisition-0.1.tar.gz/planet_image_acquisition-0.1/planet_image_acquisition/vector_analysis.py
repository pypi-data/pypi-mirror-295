import geopandas as gpd
import os
import tempfile
from shapely.geometry import box


def make_shapefile(xmin, ymin, xmax, ymax):
    print('Creating shapefile from the bounding box')
    bbox = box(xmin, ymin, xmax, ymax)
    gdf = gpd.GeoDataFrame({'geometry': [bbox]}, crs="EPSG:4326")
    temp_dir = tempfile.mkdtemp()
    shapefile_path = os.path.join(temp_dir, "bounding_box.shp")
    gdf.to_file(shapefile_path)

    return shapefile_path