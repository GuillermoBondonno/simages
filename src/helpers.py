import numpy as np
from osgeo import gdal_array, gdal
import sys
import rioxarray
from rioxarray.exceptions import NoDataInBounds
import geopandas as gpd
from shapely.geometry import Point, Polygon
from shapely import speedups
from os import getcwd

speedups.disable()


d = {
    # (min, max) : color RGB
    (0, 26+26*0):       (160, 25, 0),
    (26+26*0, 26+26*1): (165, 50, 0),
    (26+26*1, 26+26*2): (170, 75, 0),
    (26+26*2, 26+26*3): (175, 100, 0),
    (26+26*3, 26+26*4): (210, 150, 0),
    (26+26*4, 26+26*5): (255, 251, 0),
    (26+26*5, 26+26*6): (100, 210, 0),
    (26+26*6, 26+26*7): (80, 180, 0),
    (26+26*7, 26+26*8): (40, 130, 0),
    (26+26*8, 26+26*9): (18, 110, 0),
}

red_to_green_colormap = {}
for i in range(256):
    for tup in d.keys():
        if tup[1] > i >= tup[0]:
            red_to_green_colormap[i] = (
                d[tup][2], d[tup][1], d[tup][0])  # RGB TO BGR


def points_to_geojson(points):
    """
    Transforms points to geojson to pass it to the read_and_clip_band func

    """
    if np.array(points).shape[1] != 2:
        raise Exception

    point_list = [Point(p[0], p[1]) for p in points]
    polygon = Polygon([[p.x, p.y] for p in point_list])
    return gpd.GeoDataFrame({"geometry": [polygon]})['geometry']


def read_and_clip_band_array(band_path, geometry):
    """
    Crops a band based on a geojson geometry and returns a gdal dataset
    """
    try:
        with rioxarray.open_rasterio(band_path, crop=True) as band:
            band = band.rio.reproject("epsg:4326")
            clipped_band = band.rio.clip(geometry)

        return np.array(clipped_band)[0]
    except NoDataInBounds as nd:
        print("Bound outside of band surface area")
        return False
    except Exception as e:
        print(f"\n\n Other exception: {e}")
        raise e


def read_and_clip_band(band_path, geometry):
    """
    Crops a band based on a geojson geometry and returns a gdal dataset
    """
    try:
        with rioxarray.open_rasterio(band_path, crop=True) as band:
            band = band.rio.reproject("epsg:4326")
            clipped_band = band.rio.clip(geometry)

        # Transform to GDAL dataset
        gdal_band = gdal_array.OpenArray(np.array(clipped_band))
        return gdal_band
    except NoDataInBounds as nd:
        print("Bound outside of band surface area")
        return False
    except Exception as e:
        print(f"\n\n Other exception: {e}")
        raise e

# A function to create the output image


def createOutputImage(outFilename, inDataset):
    """Takes a band or dataset as input and returns a new empty one, unused"""
    # Define the image driver to be used
    # This defines the output file format (e.g., GeoTiff)
    driver = gdal.GetDriverByName("GTiff")
    # Check that this driver can create a new file.
    metadata = driver.GetMetadata()
    if gdal.DCAP_CREATE in metadata.keys() and metadata[gdal.DCAP_CREATE] == 'YES':
        print('Driver GTiff supports Create() method.')
    else:
        print('Driver GTIFF does not support Create()')
        sys.exit(-1)
    # Get the spatial information from the input file
    geoTransform = inDataset.GetGeoTransform()
    geoProjection = inDataset.GetProjection()
    # Create an output file of the same size as the inputted
    # image, but with only 1 output image band.
    newDataset = driver.Create(
        outFilename, inDataset.RasterXSize,     inDataset.RasterYSize, 1, gdal.GDT_Float32)
    # Define the spatial information for the new image.
    newDataset.SetGeoTransform(geoTransform)
    newDataset.SetProjection(geoProjection)
    return newDataset
