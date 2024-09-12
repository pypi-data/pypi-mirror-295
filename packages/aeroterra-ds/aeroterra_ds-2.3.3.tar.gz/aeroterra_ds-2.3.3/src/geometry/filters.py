from typing import Callable, Union, Optional, List

import geopandas as gpd

from itertools import combinations

from shapely.geometry import GeometryCollection, Polygon, MultiPolygon, LinearRing
from shapely.geometry.base import BaseGeometry
from shapely.ops import unary_union

from .checks import is_bbox, is_polygon_like, is_thin
from .change_crs import change_crs, change_box_crs

from exceptions.type_checker import type_checker

from gis_typing.gis_types import CRS_TYPE, BBOX_TYPE

@type_checker
def filter_collection(collection: GeometryCollection,
                      check_functions: Union[List[Callable[[BaseGeometry], bool]], Callable[[BaseGeometry], bool]],
                      join_geoms: bool = True):
    """
    Given a Geometry Collection filter out keeping all the 
    geometries that passes the given function.

    Parameters:
        - collection: GeometryCollection to split
        - check_function: List of functions to check the type of the 
            geometry. The function expect only 1 parameter, being 
            that the geometry to check.
        - join_geoms (Optional): If the filtered geometries should be joined
            to a only one. If not, a list of geometries will be returned
    """
    if not isinstance(check_functions, list):
        check_functions = [check_functions]

    response_geometries = []
    for geom in collection.geoms:
        for check in check_functions:
            if check(geom):
                response_geometries.append(geom)
    
    if join_geoms:
        return unary_union(response_geometries)
    else:
        return response_geometries

@type_checker
def filter_to_land(gdf: gpd.GeoDataFrame,
                   land_mask,
                   mask_crs: Optional[CRS_TYPE] = None):
    """
    Given a geodataframe it filters it to a given mask.

    Parameters:
        - gdf: The GeoDataFrame to filter
        - land_mask: Mask to use as filter.
            Could be a list of polygons, a GDF, a single polygon
            or a bound (min_x, min_y, max_x, max_y)
        - mask_crs: CRS of the given mask. If the mask is a gdf, the gdf crs
            will be used. Otherwise if this parameter is set in None it'll be
            assumed it's in the same crs as the gdf.
    """
    #TODO: Add Land Mask Type
    if isinstance(land_mask, gpd.GeoDataFrame):
        land_mask = land_mask.to_crs(gdf.crs)
    elif isinstance(land_mask, gpd.GeoSeries):
        land_mask = land_mask.to_crs(gdf.crs)
    elif is_bbox(land_mask):
        if mask_crs:
            land_mask = change_box_crs(land_mask, mask_crs, gdf.crs)
    elif is_polygon_like(land_mask):
        if mask_crs:
            land_mask = change_crs(land_mask, mask_crs, gdf.crs)
        land_mask = [land_mask]
    elif isinstance(land_mask, list):
        if len(land_mask) == 0:
            raise Exception("Can't Filter To An Empty List")
        if not is_polygon_like(land_mask[0]):
            raise Exception("Can't Filter From List Of Not Polygon-Like Geomtries")

        if mask_crs:
            land_mask = change_crs(land_mask, mask_crs, gdf.crs)
    else:
        raise Exception("Invalid Mask")
    
    land_mask = gpd.clip(land_mask, gdf.total_bounds)

    clipped_polygons = gpd.clip(gdf, land_mask, keep_geom_type=True)

    return clipped_polygons["geometry"].to_list()

@type_checker
def filter_thin_polygons(polygons: List[Union[Polygon, MultiPolygon]],
                         split_multi: bool = False,
                         filter_aspect: int = 21):
    """
    Given a list of (multi)polygons it returns a 
    new list with only the non thin polygons remaining.

    Parameters:
        - polygons: List of polygons-like figures to filter
        - split_multi (Optional): If multipolygons like geometries
            should be split into polygons or if the unification should
            remain. By default at False.
        - filter_aspect: Ratio of the Perimeter vs Area. 
            The bigger the value the more thinner polygons
            will be accepted. By default at 21, value from 
            an average equilateral polygon
    """
    final_polygons = []
    for geom in polygons:
        if isinstance(geom, Polygon):
            if not is_thin(geom, filter_aspect) and geom.area > 0:
                final_polygons.append(geom)
        elif isinstance(geom, MultiPolygon):
            new_geoms = []
            for sub_pol in geom.geoms:
                if isinstance(geom, Polygon) and not is_thin(sub_pol, filter_aspect) and geom.area > 0:
                    new_geoms.append(sub_pol)
            if split_multi:
                final_polygons.extend(new_geoms)
            else:
                final_polygons.append(MultiPolygon(new_geoms))

    return final_polygons


def generate_triangles(polygon):
    """
    Generate a list of all the triangles (shapely 
    polygons) that can be formed from the vertices
    of a given polygon that area also fully contained in it.

    Note: Doesn't work for holed polygons for now. The code
    won't break but hole(s) will be ignored

    Parameters:
        - polygon: Polygon to triangularize
    """
    if not is_polygon_like(polygon):
        raise Exception(f"Not A Valid Geometry To Triangularize [{polygon}]")

    vertices = list(polygon.exterior.coords)
    for hole in polygon.interiors:
        if isinstance(hole, Polygon):
            vertices.extend(list(hole.exterior.coords))
        elif isinstance(hole, LinearRing):
            vertices.extend(list(hole.coords))


    triangle_vertices = combinations(vertices, 3)
    
    triangles = []
    for vertices in triangle_vertices:
        try:
            triangle = Polygon(vertices)
            if polygon.contains(triangle):
                triangles.append(triangle)
        except:
            continue
    
    return triangles

@type_checker
def detect_and_cut_thin_parts(polygon,
                              filter_aspect: int = 100):
    """
    Detects and cuts thin parts from a Shapely polygon, 
    returning the new geometry. In case the geometry
    is not a polygon like one, an expection will be raised.

    Note: Doesn't work for holed polygons for now. The code
    won't break but hole(s) will be ignored

    Parameters:
        - polygon: Shapely Polygon object to split.
        - filter_aspect: Ratio of the Perimeter vs Area. 
            The bigger the value the more thinner polygons
            will be accepted. By default at 10, five times the value 
            of an average equilateral polygon
    """
    triangles = generate_triangles(polygon)
    if len(triangles) == 0:
        return polygon
    
    not_thin_triangles = []
    total_area = polygon.area
    same_area = total_area * 0.01
    
    for j, triangle in enumerate(triangles):
        intersection = triangle.difference(polygon)
        if intersection.area > same_area:
            continue

        if not is_thin(triangle, filter_aspect):
            not_thin_triangles.append(triangle)
    
    response = unary_union(not_thin_triangles)

    if is_polygon_like(response):
        return response
    elif isinstance(response, GeometryCollection):
        return filter_collection(response, is_polygon_like)
    else:
        return None