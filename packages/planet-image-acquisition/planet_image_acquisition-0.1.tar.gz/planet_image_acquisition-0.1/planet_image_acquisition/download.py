import requests
import os
import urllib.request
import time
import geopandas as gpd
import tempfile
from shapely.geometry import box
from .vector_analysis import make_shapefile




def setup_session(api_key):
    session = requests.Session()
    session.auth = (api_key, "")
    return session

def run_session(date, bbox, temp_dir, api_key):
    API_URL = 'https://api.planet.com/basemaps/v1/mosaics'
    session = setup_session(api_key)
    print(session, 'session\n')
    
    parameters = {
        "name__is": 'planet_medres_normalized_analytic_{}_mosaic'.format(date),
    }

    res = session.get(API_URL, params=parameters)
    print(res, 'response\n')
    print("Session response code: ", res.status_code)
    
    mosaic = res.json()
    mosaic_id = mosaic['mosaics'][0]['id']
    
    search_parameters = {
        'bbox': bbox,
        'minimal': True
    }
    
    quads_url = "{}/{}/quads".format(API_URL, mosaic_id)
    res = session.get(quads_url, params=search_parameters, stream=True)
    
    quads = res.json()
    items = quads['items']
    
    for i in items:
        link = i['_links']['download']
        name = i['id'] + '.tiff'
        filename = os.path.join(temp_dir, name)
        
        print(name)
        if not os.path.isfile(filename):
            urllib.request.urlretrieve(link, filename)

def download_planet_images(bbox_gdf_path, dates, api_key):
    # xmin, ymin, xmax, ymax = spatial_extent
    # bbox_gdf_path = make_shapefile(xmin, ymin, xmax, ymax)
    bbox_gdf = gpd.read_file(bbox_gdf_path)
    
    bbox_gdf[['x_min', 'y_min', 'x_max', 'y_max']] = bbox_gdf.bounds
    bbox_gdf['string_bbox'] = (bbox_gdf['x_min'].astype(str) + "," 
                               + bbox_gdf['y_min'].astype(str) + "," 
                               + bbox_gdf['x_max'].astype(str) + "," 
                               + bbox_gdf['y_max'].astype(str))
    
    print(bbox_gdf['string_bbox'],'string ')
    parts_check = len(bbox_gdf)    
    bbox_gdf['pl_iter_id'] = bbox_gdf.index
    
    temp_dir = tempfile.mkdtemp()
    
    for row in bbox_gdf.itertuples():
        start = time.time()
        
        for date in dates:
            print(f"\nDownloading for {date}...")
            date_path = os.path.join(temp_dir, date)
            
            if not os.path.exists(date_path):
                os.makedirs(date_path)
            
            try:
                run_session(date, row.string_bbox, date_path, api_key)
                print(f"Download successful: {date}")
            except Exception as e:
                print(f"Download NOT successful: {date}")
                print(f"Error: {str(e)}")
        


    return temp_dir

# # Usage example:
# spatial_extent = (120.527,16.342,120.652,16.464)
# temp_dirs=download_images(spatial_extent, ['2018-12_2019-05',"2019-06_2019-11"], 'PLAKc718f94526fd4f15970f4ae2cf4c4076')


        
# Example: List all downloaded files
# for root, dirs, files in os.walk(temp_dir):
#     for file in files:
#         print(os.path.join(root,file))