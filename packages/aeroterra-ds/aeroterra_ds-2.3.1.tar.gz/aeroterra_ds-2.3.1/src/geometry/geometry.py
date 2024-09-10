from shapely.geometry import Point, MultiPoint, LineString, MultiLineString, Polygon, MultiPolygon
from shapely.geometry.base import BaseGeometry

from arcgis.geometry import Geometry

from exceptions.type_checker import type_checker

from gis_typing.gis_types import CRS_TYPE

@type_checker
def create_geo_json_point(point: Point):
    """
    Given a shapely Point, it transforms the structure into a Json for ArcGIS
    
    Parameters:
        point: Shapely point to transform.
        crs: The CRS of the point to transform.
    
    Returns a dictionary
    """    
    geo_json = {}
    geo_json["x"] = point.x
    geo_json["y"] = point.y
    
    return geo_json

@type_checker
def create_geo_json_multipoint(multipoint: MultiPoint):
    """
    Given a shapely MultiPoint, it transforms the structure into a Json for ArcGIS

    Parameters:
        multipoint: Shapely MultiPoint to transform.
        crs: The CRS of the point to transform.

    Returns a dictionary
    """        
    geo_json = {}
    points = []
    for point in multipoint.geoms:
        aux_point = (point.x, point.y)
        points.append(aux_point)
    geo_json["points"] = points
    
    return geo_json

@type_checker
def create_geo_json_line(linestring: LineString):
    """
    Given a shapely LineString, it transforms the structure into a Json for ArcGIS

    Parameters:
        linestring: Shapely LineString to transform.
        crs: The CRS of the point to transform.

    Returns a dictionary
    """    
    geo_json = {}
    paths = []
    for point in linestring.coords:
        paths.append(point)
    geo_json["paths"] = [paths]
    
    return geo_json

@type_checker
def create_geo_json_multiline(multiline: MultiLineString):
    """
    Given a shapely MultiLineString, it transforms the structure into a Json for ArcGIS

    Parameters:
        multiline: Shapely MultiLineString to transform.
        crs: The CRS of the point to transform.

    Returns a dictionary
    """    
    geo_json = {}
    paths = []
    for line in multiline.geoms:
        aux_path = []
        for point in line.coords:
            aux_path.append(point)
        paths.append(aux_path)
    geo_json["paths"] = paths
    
    return geo_json

@type_checker
def create_geo_json_polygon(polygon: Polygon):
    """
    Given a shapely Polygon, it transforms the structure into a Json for ArcGIS

    Parameters:
        polygon: Shapely Polygon to transform.
        crs: The CRS of the point to transform.

    Returns a dictionary
    """    
    geo_json = {}
    external_ring = []
    for point in reversed(polygon.exterior.coords):
        external_ring.append(point)

    rings = [external_ring]
    for hole in polygon.interiors:
        aux_ring = []
        for point in reversed(hole.coords):
            aux_ring.append(point)
        rings.append(aux_ring)

    geo_json["rings"] = [rings]
    
    return geo_json

@type_checker
def create_geo_json_multipolygon(multipolygon: MultiPolygon):
    """
    Given a shapely MultiPolygon, it transforms the structure into a Json for ArcGIS

    Parameters:
        multipolygon: Shapely MultiPolygon to transform.
        crs: The CRS of the point to transform.

    Returns a dictionary
    """    
    geo_json = {}
    rings = []
    for polygon in multipolygon.geoms:
        pol_ring = []
        external_ring = []
        for point in reversed(polygon.exterior.coords):
            external_ring.append(point)
        pol_ring.append(external_ring)

        for hole in polygon.interiors:
            aux_ring = []
            for point in reversed(hole.coords):
                aux_ring.append(point)
            pol_ring.append(aux_ring)
        rings.append(pol_ring)

    geo_json["rings"] = rings
    
    return geo_json

@type_checker
def create_geo_json(geometry: BaseGeometry,
                    crs: CRS_TYPE):
    """
    Given a shapely geometry, it transforms the structure into a Json for ArcGIS
    
    Parameters:
        geometry: Shapely geometry to transform.
        crs: The CRS of the geometry to transform.
    
    Returns a dictionary
    """
    geo_json = None
    
    if isinstance(geometry, Point):
        geo_json = create_geo_json_point(geometry)
    elif isinstance(geometry, MultiPoint):
        geo_json = create_geo_json_multipoint(geometry)
    elif isinstance(geometry, LineString):
        geo_json = create_geo_json_line(geometry)
    elif isinstance(geometry, MultiLineString):
        geo_json = create_geo_json_multiline(geometry)
    elif isinstance(geometry, Polygon):
        geo_json = create_geo_json_polygon(geometry)
    elif isinstance(geometry, MultiPolygon):
        geo_json = create_geo_json_multipolygon(geometry)
    
    if geo_json is None:
        raise Exception("Couldn't Find A Valid Geometry Type")
    
    #TODO: Cast Other Types of CRS to int
    geo_json["spatialReference"] = {"wkid": crs}

    return geo_json

@type_checker
def get_arcgis_geometry(geometry: BaseGeometry,
                        crs: CRS_TYPE):
    """
    Given a shapely geometry, it transforms the structure into an arcgis Geometry
    
    Parameters:
        geometry: Shapely geometry to transform.
        crs: The CRS of the geometry to transform.
    
    Returns a dictionary
    """
    geo_json = create_geo_json(geometry, crs)
    return Geometry(geo_json)


@type_checker
def from_arcgis_to_shapely_polygon(arcgis_json: dict):
    if "rings" not in arcgis_json:
        raise Exception("Not a Polygon")

    rings = arcgis_json["rings"]
    
    polygons = []
    for ring in rings:
        if len(ring) == 1:
            polygons.append(Polygon(ring[0]))
        else:
            polygons.append(Polygon(ring[0], ring[1:]))

    return MultiPolygon(polygons)
