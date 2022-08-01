import requests
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from sentinelhub import SHConfig
from sentinelhub import (
    CRS,
    BBox,
    DataCollection,
    DownloadRequest,
    MimeType,
    MosaickingOrder,
    SentinelHubDownloadClient,
    SentinelHubRequest,
    bbox_to_dimensions,
    WmsRequest,
    WebFeatureService
)
from geopy.geocoders import Nominatim
from datetime import datetime, timedelta
import os
import config

def get_img(date_in, date_out):
    #Identifiant de SentinelHub
    id_sentinel = config.id_sentinel
    pass_sentinel = config.pass_sentinel
    

    #Connexion SentinelHub
    config = SHConfig()
    config.instance_id = id_sentinel
    config.sh_client_id = id_sentinel
    config.sh_client_secret = pass_sentinel

    if not config.sh_client_id or not config.sh_client_secret:
        print("Warning! To use Process API, please provide the credentials (OAuth client ID and client secret).")

    betsiboka_coords_wgs84 = [2.518, 43.205, 4.194, 43.97]
    resolution = 100
    betsiboka_bbox = BBox(bbox=betsiboka_coords_wgs84, crs=CRS.WGS84)
    betsiboka_size = bbox_to_dimensions(betsiboka_bbox, resolution=resolution)

    print(f"Image shape at {resolution} m resolution: {betsiboka_size} pixels")
    
    evalscript_true_color = """
        //VERSION=3

        function setup() {
            return {
                input: [{
                     bands: ["B04", "B08", "CLM", "B11"]
                }],
                output: {
                    bands: 3,
                }
            };
        }

        function evaluatePixel(sample) {
            if(sample.CLM == 0){
                return [sample.B04, sample.B08, sample.B11];
                }
            return [NaN]
        }
        """

    request_true_color = SentinelHubRequest(
        evalscript=evalscript_true_color,
        input_data=[
            SentinelHubRequest.input_data(
                data_collection=DataCollection.SENTINEL2_L1C,
                time_interval=(date_in, date_out),
            )
        ],
        data_folder = "./Input/sentinel2/all/",
        responses=[SentinelHubRequest.output_response("default", MimeType.TIFF)],
        bbox=betsiboka_bbox,
        size=betsiboka_size,
        config=config,
    )
    request_true_color.get_data(save_data = True)
    name = find_files("response.tiff","./Input/sentinel2/all/")
    os.rename(name[0], f'./Input/sentinel2/{date_out}.tiff')



def find_files(filename, search_path):
   result = []
   for root, dir, files in os.walk(search_path):
      if filename in files:
         result.append(os.path.join(root, filename))
   return result

"""
date_in_test ="2022-07-20"
date_out_test = "2022-07-21"
get_img(date_in_test, date_out_test)
"""
