from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse, StreamingResponse, Response
from src.helpers import points_to_geojson, read_and_clip_band, read_and_clip_band_array, red_to_green_colormap
from src.calculate_indexes import calculate_ndvi, calculate_ndvi_array
import cv2
import numpy as np
import io
import logging
import base64
import time


router = APIRouter()
demo_path = "./demo_data/S2B_MSIL2A_20210826T135019_N0301_R024_T21HUB_20210826T181340.SAFE/GRANULE/L2A_T21HUB_A023359_20210826T135327/IMG_DATA/R10m"


@router.get("/ulx/{upper_left_lng}/uly/{upper_left_lat}/brx/{bottom_right_lng}/bry/{bottom_right_lat}")
async def load_from_demo(upper_left_lng: float, upper_left_lat: float, bottom_right_lng: float, bottom_right_lat: float) -> JSONResponse:
    """
    #### Demo endpoint to calculate en display NDVI index around Buenos Aires metropolitan area
    ##### example: 
            {
                "upper_left": (-58.548340, -34.604787),
                "bottom_right": (-58.519157, -34.620478)
            }
    """
    start = time.time()

    red_band_path = demo_path+"/T21HUB_20210826T135019_B04_10m.jp2"
    nir_band_path = demo_path+"/T21HUB_20210826T135019_B08_10m.jp2"

    # Fetch the last update from the database for this field
    last_updated = "2021-09-01"

    points = [(upper_left_lng, upper_left_lat),
              (bottom_right_lng, upper_left_lat),
              (bottom_right_lng, bottom_right_lat),
              (upper_left_lng, bottom_right_lat)]

    area_of_interest = points_to_geojson(
        points=points)

    red_band = read_and_clip_band(red_band_path, area_of_interest)
    if red_band == False:
        return JSONResponse(status_code=400,
                            content="Input area outside band surface area")

    nir_band = read_and_clip_band(nir_band_path, area_of_interest)

    # Assume that if data is found in red_band, it will also be found in nir_band

    ndvi_array = calculate_ndvi(red_band, nir_band)

    # assume 0 values are water and urban
    NDVI_index = round(np.average(ndvi_array[ndvi_array != 0]), 3)

    ndvi_array = (ndvi_array*255).astype(np.uint8)
    colormapped_array = np.array([[red_to_green_colormap[value]
                                   for value in line] for line in ndvi_array])

    res, im_png = cv2.imencode(".png", colormapped_array)

    return StreamingResponse(io.BytesIO(im_png.tobytes()), media_type="image/png", headers={"ndvi": str(NDVI_index),
                                                                                            "last_updated": last_updated})
