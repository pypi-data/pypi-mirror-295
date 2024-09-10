from typing import List, Dict, Tuple, Optional, Union

import geopandas as gpd

from rtree import index

from shapely import unary_union

from shapely.geometry import Polygon, MultiPolygon, GeometryCollection
from shapely.geometry.base import BaseGeometry

from .dataframes import create_gdf_geometries
from .checks import is_polygon_like
from .filters import filter_collection

from exceptions.type_checker import type_checker

from gis_typing.gis_types import CRS_TYPE

@type_checker
def get_intersections(polygons: List[Union[Polygon, MultiPolygon]],
                      precise: bool =True):
    """
    Given a list of polygons it returns the positions of those that intersect each other

    Parameters:
        - polygons: List of polygons to check
        - precise: If intersection must be secured or if it could use rtree one
    
    Returns a dictionary with List positions as key and a list of other positions intersecting
    as value
    """
    idx = index.Index()
    intersected_polygons = {}

    for i, polygon in enumerate(polygons):
        idx.insert(i, polygon.bounds)
        intersected_polygons[i] = []

    for i, polygon1 in enumerate(polygons):
        intersections = []
        for j in idx.intersection(polygon1.bounds):
            if j <= i:
                continue
            if precise or polygon1.intersects(polygons[j]):
                intersections.append(j)
                intersected_polygons[j].append(i)
        intersected_polygons[i].extend(intersections)
    
    return intersected_polygons


@type_checker
def create_unique_lists(intersections: Dict[int, List[int]]):
    """
    Given a dictionary of intersections it returns the unique list of joined elements

    Parameters:
        - intersections: Dict of intersections. Key: Position of element, Value: List of intersections
    """
    visited = set()
    unique_links = []

    def dfs(node, current_link):
        visited.add(node)
        current_link.append(node)

        for neighbor in intersections.get(node, []):
            if neighbor not in visited:
                dfs(neighbor, current_link)

    for key in intersections.keys():
        if key not in visited:
            current_link = []
            dfs(key, current_link)
            unique_links.append(current_link)
    
    return unique_links


@type_checker
def join_by_intersections(polygons: gpd.GeoDataFrame,
                          values_column: Dict[str, Union[List[str], Tuple[str]]] = {},
                          precise: bool = True):
    """
    Given a GeoDataFrame with polygons, it returns new GeoDataFrame with the set
    of intersected polygons joined.

    Parameters:
        - polygons: GeoDataFrame to join
        - values_column: Dictionary indicating new columns to create with operations
            to do with the combination.
                {new_key: [operation_type, operation_column]}
                operation_types:
                    - sum
                    - count
                    - unique
                    - max
                    - min
            By default, an empty dic meaning no new column will be created
        - precise: If intersection must be secured or if it could use rtree one
    """
    geometry_column = polygons.geometry.name
    crs = polygons.crs
    pols_list = polygons[geometry_column].to_list()
    intersections = get_intersections(pols_list, precise=precise)
    links = create_unique_lists(intersections)
    
    polygons_final = []
    
    for link in links:
        if len(link) == 0:
            continue
        polygons_current = [pols_list[i] for i in link]
        polygon = unary_union(polygons_current)
        if isinstance(polygon, Polygon):
            polygon = MultiPolygon([polygon])
        
        values = {geometry_column: polygon}
        polygons_current = polygons.iloc[link]
        for new_key, operation in values_column.items():
            metric = None
            operation_action = operation[0].lower()
            operation_key = operation[1]
            if operation_action == "sum":
                metric = polygons_current[operation_key].sum()
            elif operation_action == "count":
                metric = polygons_current[operation_key].count()
            elif operation_action == "unique":
                metric = len(polygons_current[operation_key].unique())
            elif operation_action == "max":
                metric = polygons_current[operation_key].max()
            elif operation_action == "min":
                metric = polygons_current[operation_key].min()
            values[new_key] = metric

        polygons_final.append(values)

    return gpd.GeoDataFrame(polygons_final, geometry=geometry_column, crs=crs)


@type_checker
def get_polygons_hit(input_gdf: gpd.GeoDataFrame,
                     intersect_geoms,
                     intersect_crs: Optional[CRS_TYPE] = None,
                     area_perc: Optional[float] = None):
    """
    Returns a GDF filter from the input_gdf based on those that
    intersect with intersect_geoms

    Parameters:
        - input_gdf: GDF to get the base from
        - intersect_geoms: GeoDataframe/(Multi)Polygon/(Multi)Polygons List 
            where to get the geometries from
        - intersect_crs: CRS of the given intersect_geoms. In case the geoms are 
            a GDF the crs assigned to it will be used. If set to None, it'll be
            assumed the geometries are in the same crs as input_gdf. By default,
            in None.
        - area_perc: Percentage of the original polygon needed to be
            considered a valid intersection. If None, any intersection
            will be counted.
    """
    #TODO Add intersect_geoms dtypes
    if input_gdf.crs is None:
        raise Exception("Must Provide a CRS for the input_gdf")

    if intersect_crs is None:
        intersect_crs = input_gdf.crs

    intersect_gdf = create_gdf_geometries(intersect_geoms, intersect_crs)
    intersect_gdf = intersect_gdf.to_crs(input_gdf.crs)

    original_geoms = input_gdf.geometry.to_list()
    intersect_geoms = intersect_gdf.geometry.to_list()

    idx = index.Index()
    for i, polygon in enumerate(intersect_geoms):
        idx.insert(i, polygon.bounds)
    
    if area_perc >= 0.99 :
        area_perc = 0.99

    pols_keep = []
    for i, polygon in enumerate(original_geoms):
        area_needed = 0
        if area_perc is not None:
            area_needed = polygon.area * area_perc

        matches = False
        for j in idx.intersection(polygon.bounds):
            pol_intersection = polygon.intersection(intersect_geoms[j])

            if isinstance(pol_intersection, GeometryCollection):
                pol_intersection = filter_collection(pol_intersection, [is_polygon_like])
            
            if pol_intersection is None or pol_intersection.is_empty or not is_polygon_like(pol_intersection):
                continue

            if pol_intersection.area >= area_needed:
                matches = True
                break
        
        if matches:
            pols_keep.append(i)
    
    return input_gdf.iloc[pols_keep]


@type_checker
def get_total_bound(geometries: List[BaseGeometry]):
    """
    Returns the bounds (min_x, min_y, max_x, max_y) of a list of geometries
    
    Parameters:
        - geometries: list of geometries to get their total bound from
    """

    min_x = float("inf")
    min_y = float("inf")
    max_x = -float("inf")
    max_y = -float("inf")
    
    for geom in geometries:
        if geom is None:
            continue
        bounds = list(geom.bounds)
        if bounds[0] < min_x:
            min_x = bounds[0]
        if bounds[1] < min_y:
            min_y = bounds[1]
        if bounds[2] > max_x:
            max_x = bounds[2]
        if bounds[3] > max_y:
            max_y = bounds[3]
    
    return [min_x, min_y, max_x, max_y]
