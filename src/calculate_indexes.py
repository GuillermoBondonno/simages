from tqdm import tqdm
import struct
from osgeo import gdal
import numpy as np


def calculate_ndvi_array(red_band, nir_band):
    """
    Uses the red and near infrared band to calculate the natural dense vegetation index
    """
    print(f"\n\n  {red_band} \n\n")
    NDVIs = []
    result_array = []
    num_lines = red_band.shape[0]
    # Loop through each line in turn.
    print(f"Total de lineas: {num_lines}")
    for line in tqdm(range(num_lines)):
        # Read in data for the current line from the
        # image band representing the red wavelength

        red_tuple = red_band[line]

        nir_tuple = nir_band[line]
        # Loop through the columns within the image
        this_line_result = []
        for i in range(len(red_tuple)):
            # Calculate the NDVI for the current pixel.
            ndvi_lower = (nir_tuple[i] + red_tuple[i])
            ndvi_upper = (nir_tuple[i] - red_tuple[i])
            ndvi = 0
            # Be careful of zero divide
            if ndvi_lower == 0:
                ndvi = 0
            else:
                ndvi = ndvi_upper/ndvi_lower
            # Add the current pixel to the output line
            NDVIs.append(ndvi)
            this_line_result.append(ndvi)
        result_array.append(this_line_result)

    return np.array(result_array)


def calculate_ndvi(red_band, nir_band):
    """
    Uses the red and near infrared band to calculate the natural dense vegetation index
    """
    NDVIs = []
    result_array = []
    num_lines = red_band.RasterYSize
    # Loop through each line in turn.
    print(f"Total de lineas: {num_lines}")
    for line in tqdm(range(num_lines)):
        # Read in data for the current line from the
        # image band representing the red wavelength
        red_scanline = red_band.ReadRaster(
            0, line, red_band.RasterXSize, 1,             red_band.RasterXSize, 1, gdal.GDT_Float32)
        # Unpack the line of data to be read as floating point data
        red_tuple = struct.unpack('f' * red_band.RasterXSize, red_scanline)

        # Read in data for the current line from the
        # image band representing the NIR wavelength
        nir_scanline = nir_band.ReadRaster(
            0, line, nir_band.RasterXSize, 1,             nir_band.RasterXSize, 1, gdal.GDT_Float32)
        # Unpack the line of data to be read as floating point data
        nir_tuple = struct.unpack('f' * nir_band.RasterXSize, nir_scanline)
        # Loop through the columns within the image
        this_line_result = []
        for i in range(len(red_tuple)):
            # Calculate the NDVI for the current pixel.
            ndvi_lower = (nir_tuple[i] + red_tuple[i])
            ndvi_upper = (nir_tuple[i] - red_tuple[i])
            ndvi = 0
            # Be careful of zero divide
            if ndvi_lower == 0:
                ndvi = 0
            else:
                ndvi = ndvi_upper/ndvi_lower
            # Add the current pixel to the output line
            NDVIs.append(ndvi)
            this_line_result.append(ndvi)
        result_array.append(this_line_result)

    return np.array(result_array)
