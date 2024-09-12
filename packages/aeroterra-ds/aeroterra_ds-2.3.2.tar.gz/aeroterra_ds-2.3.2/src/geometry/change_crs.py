from typing import Tuple, Union, List, Any, Dict


import pyproj
from shapely.geometry import Point, MultiPoint, LineString, MultiLineString, Polygon, MultiPolygon
from shapely.geometry.base import BaseGeometry
from shapely.ops import unary_union

from pandas import DataFrame
import geopandas as gpd

from .checks import is_point, bound_in_bound, is_bbox

from exceptions.type_checker import type_checker

from gis_typing.gis_types import NUMBER_TYPE, CRS_TYPE, BBOX_TYPE

POINT_TUPLE = Tuple[NUMBER_TYPE, NUMBER_TYPE]
GEOMETRIES_TYPE = Union[BaseGeometry, POINT_TUPLE]
CHANGE_CRS_OPTIONS = Union[GEOMETRIES_TYPE, List[GEOMETRIES_TYPE], Dict[Any, GEOMETRIES_TYPE], DataFrame]

@type_checker
def change_crs_polygon(polygon: Polygon,
                       src_crs: CRS_TYPE,
                       dst_crs: CRS_TYPE):
    """
    Change the CRS of a given polygon.

    Parameters:
        - polygon: Item to change the CRS from
        - src_crs: CRS of the given item
        - dst_crs: CRS to set to the bbox
    """
    if not isinstance(polygon, Polygon):
        raise Exception("Geometry Must Be A Polygon")
    
    src_origen = pyproj.CRS(src_crs)
    src_destino = pyproj.CRS(dst_crs)
    transformador = pyproj.Transformer.from_crs(src_origen, src_destino, always_xy=True)

    transformed_exterior = [transformador.transform(v[0], v[1]) for v in polygon.exterior.coords]
    transformed_interiors = [[transformador.transform(v[0], v[1]) for v in hole.coords] for hole in polygon.interiors]

    return Polygon(transformed_exterior, transformed_interiors)

@type_checker
def change_crs_tuple_point(point: POINT_TUPLE,
                           src_crs: CRS_TYPE,
                           dst_crs: CRS_TYPE):
    """
    Change the CRS of a given tuple understood as point.

    Parameters:
        - point: Item to change the CRS from
        - src_crs: CRS of the given item
        - dst_crs: CRS to set to the bbox
    """
    if not isinstance(point, tuple) and not isinstance(point, list):
        raise Exception("Geometry Must Be A List/Tuple")
    if len(point) != 2:
        raise Exception("Geometry Must Be A List/Tuple Of Length 2")

    src_origen = pyproj.CRS(src_crs)
    src_destino = pyproj.CRS(dst_crs)
    transformador = pyproj.Transformer.from_crs(src_origen, src_destino, always_xy=True)
    
    x=point[0]
    y=point[1]
    
    return transformador.transform(x, y)

@type_checker
def change_crs_point(point: Point,
                     src_crs: CRS_TYPE,
                     dst_crs: CRS_TYPE):
    """
    Change the CRS of a given point.

    Parameters:
        - point: Item to change the CRS from
        - src_crs: CRS of the given item
        - dst_crs: CRS to set to the bbox
    """
    if not isinstance(point, Point):
        raise Exception("Geometry Must Be A Point")

    src_origen = pyproj.CRS(src_crs)
    src_destino = pyproj.CRS(dst_crs)
    transformador = pyproj.Transformer.from_crs(src_origen, src_destino, always_xy=True)
    
    x=point.x
    y=point.y

    return Point(transformador.transform(x, y))

@type_checker
def change_crs_multipolygon(multi_polygon: MultiPolygon,
                            src_crs: CRS_TYPE,
                            dst_crs: CRS_TYPE):
    """
    Change the CRS of a given MultiPolygon.

    Parameters:
        - multi_polygon: Item to change the CRS from
        - src_crs: CRS of the given item
        - dst_crs: CRS to set to the bbox
    """
    if not isinstance(multi_polygon, MultiPolygon):
        raise Exception("Geometry Must Be A MultiPolygon")
    src_origen = pyproj.CRS(src_crs)
    src_destino = pyproj.CRS(dst_crs)
    transformador = pyproj.Transformer.from_crs(src_origen, src_destino, always_xy=True)

    multi_new = []
    
    for pol in multi_polygon.geoms:
        transformed_exterior = [transformador.transform(v[0], v[1]) for v in pol.exterior.coords]
        transformed_interiors = [[transformador.transform(v[0], v[1]) for v in hole.coords] for hole in pol.interiors]
        
        transformed_polygon = Polygon(transformed_exterior, transformed_interiors)
        multi_new.append(transformed_polygon)
    
    return unary_union(multi_new)

@type_checker
def change_crs_linestring(line: LineString,
                          src_crs: CRS_TYPE,
                          dst_crs: CRS_TYPE):
    """
    Change the CRS of a given LineString.

    Parameters:
        - line: Item to change the CRS from
        - src_crs: CRS of the given item
        - dst_crs: CRS to set to the bbox
    """
    if not isinstance(line, LineString):
        raise Exception("Geometry Must Be A LineString")
    src_origen = pyproj.CRS(src_crs)
    src_destino = pyproj.CRS(dst_crs)
    transformador = pyproj.Transformer.from_crs(src_origen, src_destino, always_xy=True)

    points = []
    for point in line.coords:
        points.append(transformador.transform(point[0], point[1]))
    
    return LineString(points)

@type_checker
def change_crs_multilinestring(multiline: MultiLineString,
                               src_crs: CRS_TYPE,
                               dst_crs: CRS_TYPE):
    """
    Change the CRS of a given MultiLineString.

    Parameters:
        - multiline: Item to change the CRS from
        - src_crs: CRS of the given item
        - dst_crs: CRS to set to the bbox
    """
    if not isinstance(multiline, MultiLineString):
        raise Exception("Geometry Must Be A MultiLineString")
    src_origen = pyproj.CRS(src_crs)
    src_destino = pyproj.CRS(dst_crs)
    transformador = pyproj.Transformer.from_crs(src_origen, src_destino, always_xy=True)

    lines = []
    for line in multiline.geoms:
        points = []
        for point in line.coords:
            points.append(transformador.transform(point[0], point[1]))
        lines.append(LineString(points))
    
    return MultiLineString(lines)


@type_checker
def change_crs(item: CHANGE_CRS_OPTIONS,
               src_crs,
               dst_crs):
    """
    Change the CRS of a given item. If the item is not
    a georeferenced item, it'll return the same item.

    Parameters:
        - item: Item to change the CRS from
        - src_crs: CRS of the given item
        - dst_crs: CRS to set to the bbox
    """
    if isinstance(item, Point):
        return change_crs_point(item, src_crs, dst_crs)
    if isinstance(item, Polygon):
        return change_crs_polygon(item, src_crs, dst_crs)
    if isinstance(item, MultiPolygon):
        return change_crs_multipolygon(item, src_crs, dst_crs)
    if isinstance(item, LineString):
        return change_crs_linestring(item, src_crs, dst_crs)
    if isinstance(item, MultiLineString):
        return change_crs_multilinestring(item, src_crs, dst_crs)
    if is_point(item):
        return change_crs_tuple_point(item, src_crs, dst_crs)
    
    if isinstance(item, list):
        if len(item) == 0:
            return item
        if is_point(item[0]) and not isinstance(item[0], Point):
            item = [Point(sub_item) for sub_item in item]
        new_gdf = gpd.GeoDataFrame({"geometry": item}, crs=src_crs)
        new_gdf = new_gdf.to_crs(dst_crs)
        return list(new_gdf["geometry"])
    
    if isinstance(item, dict):
        new_dict = item.copy()
        for key, sub_item in item.items():
            new_dict[key] = change_crs(sub_item, src_crs, dst_crs)
        return new_dict

    if isinstance(item, gpd.GeoDataFrame):
        item.crs = src_crs
        return item.to_crs(dst_crs)

    if isinstance(item, DataFrame):
        new_df = item.copy()
        return new_df.applymap(lambda x: change_crs(x, src_crs, dst_crs))
    
    return item

@type_checker
def change_box_crs(bbox: BBOX_TYPE,
                   bbox_crs: CRS_TYPE,
                   new_crs: CRS_TYPE):
    """
    Change the CRS of a given bounding box (min_x, min_y, max_x, max_y)

    Parameters:
        - bbox: Bounding Box to change the crs of
        - bbox_crs: CRS of the given bounding box
        - new_crs: CRS to set to the bbox
    """
    if bbox_crs == new_crs:
        return bbox

    lowest_point = (bbox[0], bbox[1])
    lowest_point = change_crs_tuple_point(lowest_point, bbox_crs, new_crs)
    highest_point = (bbox[2], bbox[3])
    highest_point = change_crs_tuple_point(highest_point, bbox_crs, new_crs)

    new_bbox = [lowest_point[0], lowest_point[1], highest_point[0], highest_point[1]]

    return new_bbox

@type_checker
def get_crs_extent(crs: CRS_TYPE):
    """
    Given any CRS, it returns the valid extent for it

    Parameters:
        - crs: CRS to get the extent from
    """
    basic_extent = (-180, -90, 180, 90)
    crs_extent = change_box_crs(basic_extent, 4326, crs)

    return crs_extent

@type_checker
def valid_geometry(geometry: BaseGeometry,
                   crs: CRS_TYPE):
    """
    Check if a geometry is inside the valid extent of a given crs

    Parameters:
        - geometry: Geometry to check if valid
        - crs: CRS of the given geometry
    """
    basic_extent = (-180, -90, 180, 90)
    crs_extent = change_box_crs(basic_extent, 4326, crs)

    geom_bound = geometry.bounds

    return bound_in_bound(geom_bound, crs_extent)

@type_checker
def check_gdf_geometries(gdf: gpd.GeoDataFrame):
    """
    Check that the geometry of a gdf are
    inside the valid extent of its crs.

    Returns a list of all the invalid ones.

    Parameters:
        - gdf: GDF to check
    """
    crs = gdf.crs
    if crs is None:
        raise Exception("GDF Must Have An Assigned CRS")
    basic_extent = (-180, -90, 180, 90)
    crs_extent = change_box_crs(basic_extent, 4326, crs)

    gdf_extent = gdf.total_bounds
    if bound_in_bound(gdf_extent, crs_extent):
        return []

    geom_column = gdf.geometry.name
    invalids_geometries = []
    for i, row in gdf.iterrows():
        geom = row[geom_column]
        geom_bound = geom.bounds
        if not bound_in_bound(geom_bound, crs_extent):
            invalids_geometries.append(i)
    
    return invalids_geometries