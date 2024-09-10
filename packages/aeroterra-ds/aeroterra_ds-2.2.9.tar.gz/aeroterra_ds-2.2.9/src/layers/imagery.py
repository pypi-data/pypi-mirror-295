from typing import Optional, Tuple, List, Union

import os
import shutil

import math
import numpy as np

import pandas as pd
import geopandas as gpd

from shapely.geometry import Polygon, MultiPolygon, box
from shapely.geometry.base import BaseGeometry

from arcgis.gis import GIS
from arcgis.raster import ImageryLayer
from arcgis.geometry.filters import intersects

from geometry.change_crs import change_box_crs, change_crs
from geometry.checks import is_bbox, is_number, is_polygon_like
from geometry.geometry import create_geo_json

from rasters.handler import join_tiffs, is_tiff

from exceptions.type_checker import type_checker

from gis_typing.gis_types import CRS_TYPE, BBOX_TYPE

from .common import create_geo_filter_envelope
from .layers import parse_features_to_gdf

@type_checker
def get_imagery_layer(gis: GIS,
                      link: Optional[str] = None,
                      layer_id: Optional[str] = None):
    """
    It returns an Imagery Layer item associated to the given gis session.
    
    Parameters:
        - gis: GIS Session to get the iamgery layer
        - link (Optional): URL to read the Imagery Layer from.
        - layer_id (Optional): Layer ID if the layer is stored as an item.
    
    """
    if link is not None:
        return ImageryLayer(link, gis)
    elif layer_id is not None:
        return gis.content.get(layer_id).layers[0]
    
    raise Exception("You must provide a Link or a Layer ID")

@type_checker
def get_size_limit(layer: ImageryLayer):
    """
    Given an imagery layer, it returns the max valid size for download

    Parameters:
        layer: ImageryLayer object to check
    """
    try:
        max_size = layer._lazy_properties.maxImageWidth
        if layer._lazy_properties.maxImageHeight < max_size:
            max_size = layer._lazy_properties.maxImageHeight

        return max_size
    except:
        return 4000


def decimal_position(number: float):
    """
    Given a float numberber it returns the position of the first decimal.

    Parameters:
        - number: The number to check the decimal position for
    """
    number = abs(number)

    if number == int(number):
        return 0

    number = number - int(number)
    power_of_10 = -math.floor(math.log10(number))
    
    return power_of_10

@type_checker
def clip_imagery(layer: ImageryLayer,
                 bounds: Union[Polygon, MultiPolygon, BBOX_TYPE],
                 crs: CRS_TYPE,
                 folder: str,
                 size: Optional[Tuple[int, int]] = None,
                 delete_clips: bool = False,
                 quality: float = 1,
                 join: bool = True,
                 bands: Optional[List[int]] = None,
                 file: str = "joined.tif",
                 complete_borders: bool =False):
    """
    Given an imagery layer, it clips the image to gets the best possible
    (or the wanted) quality in TIFF format in a given bound.

    Parameters:
        - layer: ImageryLayer item to download from.
        - bounds: (Multi)Polygon or bbox of the area wanted to be downloaded. 
        - crs: CRS of the given bbox.
        - folder: Path to the folder where to store the clips.
        - size (Optional): Size of the crops to ask for. If the value given is
            None, it'll use the biggest possible size. By default, is in None.
        - delete_clips (Optional): If it should delete the clips one finished
            the cliping process. By default, is in False.
        - quality (Optional): Quality to download the images from. 
            1 being 100% equal to the real one. By default at 1.
        - join (Optional): bool indicating if it should join the tiffs in a 
            singular image at the end. By default in true.
        - bands (Optional): List of bands to download. If None, it'll
            download all bands. By default in None.
        - file (Optional): Name for the joined file. The file will be stored
            inside the folder with the given name. By default in "joined.tif"
        - complete_borders(Optional): When set in true, all the clips will be the same size.
            If false, the borders will be cut to fit the bounds perfectly. By default in False.
    """
    box_like = is_bbox(bounds)
    pol_like = is_polygon_like(bounds)
    if not pol_like and not box_like:
        raise Exception("Please Provide A Valid BBOX (x_min, y_min, x_max, y_max)")
    
    pol = bounds
    if not pol_like and box_like:
        pol = box(bounds)
    bounds = pol.bounds

    if bands is not None:
        for i in range(len(bands)):
            if not is_number(bands[i]):
                raise Exception(f"All Bands IDs must be number like [{bands}]")
            bands[i] = int(bands[i])
    
    if join and not is_tiff(file):
        raise Exception("If Asked for joined images, must provide a valid TIFF file")

    if size is None:
        base_size = get_size_limit(layer) // 2
        size = (base_size, base_size)
    
    image_crs = layer._lazy_properties.spatialReference["latestWkid"]

    bounds = change_box_crs(bounds, crs, image_crs)
    pol = change_crs(pol, crs, image_crs)
    start = (bounds[0], bounds[1])
    end = (bounds[2], bounds[3])

    max_width = size[0]
    max_height = size[1]

    coord_width = abs(end[0] - start[0])
    coord_height = abs(end[1] - start[1])

    multiply_value = 10 ** (decimal_position(layer._lazy_properties.pixelSizeX) + 3)
    pixel_size_x = math.ceil(layer._lazy_properties.pixelSizeX * int(multiply_value)) / float(multiply_value)
    pixel_size_x = math.ceil((pixel_size_x / quality)* int(multiply_value)) / float(multiply_value)

    multiply_value = 10 ** (decimal_position(layer._lazy_properties.pixelSizeY) + 3)
    pixel_size_y = math.ceil(layer._lazy_properties.pixelSizeY * int(multiply_value)) / float(multiply_value)
    pixel_size_y = math.ceil((pixel_size_y / quality)* int(multiply_value)) / float(multiply_value)
    
    width = coord_width // pixel_size_x
    height = coord_height // pixel_size_y

    coords_per_pix_width = coord_width / width
    coords_per_pix_height = coord_height / height

    if not complete_borders:
        limites_lon = np.append(np.arange(0, width, max_width), width)
        limites_lat = np.append(np.arange(0, height, max_height), height)
    else:
        limites_lon = np.arange(0, width, max_width)
        if limites_lon[-1] < width:
            limites_lon = np.append(limites_lon, limites_lon[-1] + max_width)

        limites_lat = np.arange(0, height, max_height)
        if limites_lat[-1] < height:
            limites_lat = np.append(limites_lat, limites_lat[-1] + max_height)

    
    if not os.path.isdir(folder):
        os.makedirs(folder)
    
    clips_folder = f"{folder}/clips/"
    if os.path.isdir(clips_folder):
        shutil.rmtree(clips_folder)
    
    if not os.path.isdir(clips_folder):
        os.makedirs(clips_folder)
    
    for i in range(len(limites_lon)-1):
        start_lon = start[0] + limites_lon[i] * coords_per_pix_width
        end_lon = start[0] + limites_lon[i+1] * coords_per_pix_width

        for j in range(len(limites_lat)-1):
            start_lat = start[1] + limites_lat[j] * coords_per_pix_height
            end_lat = start[1] + limites_lat[j+1] * coords_per_pix_height
            down_box = box(start_lon, start_lat, end_lon, end_lat)
            if not pol.intersects(down_box):
                continue
            bbox = f"{start_lon}, {start_lat}, {end_lon}, {end_lat}"
            size = (limites_lon[i+1] - limites_lon[i], limites_lat[j+1] - limites_lat[j])
            clip_file = f"clip_{i}_{j}.tif"
            layer.export_image(bbox= bbox,
                                band_ids = bands,
                                export_format="tiff",
                                size = size,
                                adjust_aspect_ratio=False,
                                f="image",
                                save_folder=clips_folder,
                                save_file=clip_file)
    if join:
        file = f"{folder}/{file}"
        join_tiffs(file, clips_folder)
    
    if delete_clips:
        shutil.rmtree(clips_folder)   


@type_checker
def get_imagery_tiles(layer: ImageryLayer,
                      geometry_filter: BaseGeometry,
                      geometry_crs: CRS_TYPE,
                      query: str = "1=1",
                      out_crs: Optional[CRS_TYPE] = None):
    """
    Given a imagery layer and a geometry, it returns all the tiles geometries
    that intersects with it and matches the query if given.

    Parameters:
        - layer: Layer to check from.
        - geometry: Geometry to check for.
        - geometry_crs: CRS of the given geometry.
        - query (Optional): Query for the attributes to match. By
            default in '1=1'
        - out_crs (Optional): The crs to receive the geometries in
    """
    geo_filter = create_geo_filter_envelope(geometry_filter, geometry_crs)
    if out_crs is None:
        out_crs = layer._lazy_properties.spatialReference["latestWkid"]

    total_data = None
    try:
        new_data = layer.query(where = query, geometry_filter=geo_filter, out_sr=out_crs)
        new_data = parse_features_to_gdf(new_data)
        while len(new_data) > 0:
            if total_data is None:
                total_data = new_data.copy()
            else:
                total_data = pd.concat([total_data, new_data])

            new_data = layer.query(where = query, geometry_filter=geo_filter, out_sr=out_crs, result_offset=len(total_data))
            new_data = parse_features_to_gdf(new_data)
    except Exception as err:
        if str(err).find("Invalid") >= 0:
            raise Exception(f"Invalid Query. Query Done: where = {query}, geometry_filter={geo_filter}, out_sr={out_crs}")
        else:
            raise err
    
    total_data = total_data.rename(columns = {"SHAPE": "geometry"})

    gdf_result = gpd.GeoDataFrame(total_data, geometry="geometry", crs=out_crs)

    filter_polygon = change_crs(geometry_filter, geometry_crs, out_crs)
    gdf_result = gdf_result[gdf_result["geometry"].intersects(filter_polygon)]

    return gdf_result