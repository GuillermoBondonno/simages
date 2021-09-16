from typing import Tuple, Float
import shapely
import geopandas as gpd
from sentinelsat import SentinelAPI, make_path_filter
import pandas as pd


user = '*********'
password = '*********'
api = SentinelAPI(user, password)


# UL (lng,lat) y BR
# Date format: '20210830'
def download_from_bounding_box(min_date, max_date, UL: Tuple[Float], BR: Tuple[Float]):
    """
    Toma una bbox (UL y BR) y una fecha y descarga el producto, retornando el path
    """
    points = [UL[0], UL[1], BR[0], BR[1]]
    polygon = shapely.geometry.box(*points, ccw=True)
    gdf = gpd.GeoDataFrame(pd.DataFrame({"geometry": [polygon]}))

    footprint = None
    for i in gdf["geometry"]:
        footprint = i

    products = api.query(footprint,
                         date=(min_date, max_date),
                         platformname='Sentinel-2',
                         processinglevel='Level-2A',
                         cloudcoverpercentage=(0, 3)
                         )

    products_gdf = api.to_geodataframe(products).sort_values(
        ['cloudcoverpercentage'], ascending=[True])
    print(f'Total de productos: {len(products_gdf.index)}')

    # TODO: Check that the footprint is indside out bounds or reasonably
    # ovelapping it

    nodefilter = make_path_filter("*_10m.jp2")

    for product_id in products_gdf['cloudcoverpercentage'].index:
        product_info = api.get_product_odata(product_id)
        online = product_info['Online']
        print(f"Product {product_id} online? : {online}")
        if online:
            print(f"Attempting to download {product_id} ...")
            try:
                path, product_info = api.download(
                    product_id, directory_path="downloaded_data", nodefilter=nodefilter)
                return True, path, product_id
                break
            except Exception as e:
                print(f'Exception when downloading {product_id} --> {e}')
