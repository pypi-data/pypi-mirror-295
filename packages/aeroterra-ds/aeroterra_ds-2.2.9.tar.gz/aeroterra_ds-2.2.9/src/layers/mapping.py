from typing import Optional, List

import requests
import json

from urllib.parse import quote

from arcgis.gis import GIS
from arcgis.mapping import WebMap

from geometry.checks import is_bbox
from geometry.change_crs import change_box_crs

from .gets import get_map
from .symbology import get_symbology_aux

from exceptions.type_checker import type_checker

from gis_typing.gis_types import CRS_TYPE, BBOX_TYPE


@type_checker
def get_map_extent_aux(map_item: WebMap,
                       crs: CRS_TYPE =4326):
    """
    Given a map, it returns the extent for it

    Parameters:
        map_item: WebMap item of the map to check
        crs (Optional): CRS in what to get the crs. By default in 4326
    """
    extent = map_item.item.extent
    min_x = min(extent[0][0], extent[1][0])
    max_x = max(extent[0][0], extent[1][0])
    min_y = min(extent[0][1], extent[1][1])
    max_y = max(extent[0][1], extent[1][1])
    extent = (min_x, min_y, max_x, max_y)

    base_url = map_item._gis.url
    token = map_item._gis._con.token
    if base_url.find("/home") >= 0:
        base_url = base_url.replace("/home", "")

    content_url = base_url + "sharing/rest/content/items/"
    content_url += map_item.item.id
    content_url += "/data"
    content_url += f"/?f=json&token={token}"

    data = requests.get(content_url)
    if data.status_code % 100 != 2:
        raise Exception("Couldn't Connect To The Item Information URL")

    data = data.json()
    crs = data.get("spatialReference", None)
    if crs is None:
        raise Exception("Spatial Reference Not Set")

    if "latestWkid" in crs:
        extent_crs = crs["latestWkid"]
    elif "wkid" in crs:
        extent_crs = crs["wkid"]
    else:
        raise Exception("Spatial Reference Not Set")
    
    return {'xmin': extent[0], 'ymin': extent[1], 'xmax': extent[2], 'ymax': extent[3], 'spatialReference': {'wkid': extent_crs}}

@type_checker
def get_map_extent(gis: GIS,
                   map_id: str,
                   crs: CRS_TYPE = 4326):
    """
    Given a map, it returns the extent for it

    Parameters:
        gis: GIS Item linked to the portal fo the map
        map_id: ID of the map where the map is saved
        crs (Optional): CRS in what to get the crs. By default in 4326
    """
    map_item = get_map(gis, map_id)

    return get_map_extent_aux(map_item, crs)

@type_checker
def set_map_extent_aux(map_item: WebMap,
                       extent_bbox: BBOX_TYPE,
                       extent_crs: CRS_TYPE,
                       save: bool = True):
    """
    Changes the home extent of a given map

    Parameters:
        - map_item: WebMap item of the map to check
        - extent_bbox: extent to set the map to (min_x, min_y, max_x, max_y).
        - extent_crs: CRS of the given extent_bbox.
        - save: If it should save on the real layer or just update the python item.
            By default in True.
    """    
    if not is_bbox(extent_bbox):
        raise Exception(f"{extent_bbox} Is Not A bbox")

    extent_bbox = change_box_crs(extent_bbox, extent_crs, 3857)
    extent_crs = 3857

    extent_degrees = change_box_crs(extent_bbox, extent_crs, 4326)

    base_url = map_item._gis.url
    token = map_item._gis._con.token
    if base_url.find("/home") >= 0:
        base_url = base_url.replace("/home", "")

    update_url = base_url + "sharing/rest/content/items/"
    update_url += map_item.item.id
    update_url += "/update"

    map_item.definition["initialState"] = {
        "viewpoint": {
            "targetGeometry": {
                "spatialReference": {
                    "latestWkid": 3857,
                    "wkid": 102100
                },
                "xmin": extent_bbox[0],
                "ymin": extent_bbox[1],
                "xmax": extent_bbox[2],
                "ymax": extent_bbox[3]
            }
        }
    }
    map_item.extent = [[extent_degrees[0], extent_degrees[1]],[extent_degrees[2], extent_degrees[3]]]
    map_item.item.update({"extent": [[extent_degrees[0], extent_degrees[1]],[extent_degrees[2], extent_degrees[3]]]})

    data = {}
    data["f"] = "json"
    data["token"] = token
    data["extent"] = f"{extent_degrees[0]}, {extent_degrees[1]}, {extent_degrees[2]}, {extent_degrees[3]}"
    data["text"] = quote(json.dumps(dict(map_item.definition)))

    data = requests.post(update_url, data=data)
    if data.status_code // 100 != 2:
        raise Exception("Couldn't Connect To The Item Update URL ")

    if save:
        map_item.update()

@type_checker
def set_map_extent(gis: GIS,
                   map_id: str,
                   extent_bbox: BBOX_TYPE,
                   extent_crs: CRS_TYPE):
    """
    Given a map, it set the extent for it

    Parameters:
        gis: GIS Item linked to the portal fo the map
        map_id: ID of the map where the map is saved
        - extent_bbox: extent to set the map to (min_x, min_y, max_x, max_y).
        - extent_crs: CRS of the given extent_bbox.
    """
    map_item = get_map(gis, map_id)

    return set_map_extent_aux(map_item, extent_bbox, extent_crs)


@type_checker
def get_basemap_aux(map_item: WebMap):
    """
    Given a map, it returns the basemap for it

    Parameters:
        - map_item: WebMap item of the map to check
    """
    return map_item.basemap.title


@type_checker
def get_basemap(gis: GIS,
                map_id: str):
    """
    Given a map, it returns the basemap for it

    Parameters:
        gis: GIS Item linked to the portal fo the map
        map_id: ID of the map where the map is saved
    """
    map_item = get_map(gis, map_id)

    return get_basemap_aux(map_item)


@type_checker
def set_basemap_aux(map_item: WebMap,
                    title: str,
                    update: bool = False):
    """
    Given a map, it returns the basemap for it

    Parameters:
        - map_item: WebMap item of the map to check
    """
    map_item.basemap = title

    if update:
        map_item.update()

@type_checker
def set_basemap(gis: GIS,
                map_id: str,
                title: str):
    """
    Given a map, it set the basemap for it

    Parameters:
        gis: GIS Item linked to the portal fo the map
        map_id: ID of the map where the map is saved
        title: title of the new basemap to use
    """
    map_item = get_map(gis, map_id)

    return set_basemap_aux(map_item, title, True)


@type_checker
def create_map(gis: GIS,
               name: str,
               snippet: Optional[str] = None,
               tags: Optional[List[str]] = None,
               extent_bbox: Optional[BBOX_TYPE] = None,
               extent_crs: Optional[CRS_TYPE] = None):
    """
    Creates an empty map

    Parameters:
        - gis: GIS Item to use to store the map
        - name: Name to save the map with
        - snippet (Optional): Text used to describe the map. If None, none will be 
            set. By default in None.
        - tags (Optional): Tags to add to the map item. If None, none will be set. By 
            default in None.
        - extent_bbox (Optional): extent to set the map to (min_x, min_y, max_x, max_y).
            If none, full map it'll be used. By default in None.
        - extent_crs (Optional): CRS of the given extent_bbox. Must provide if extent_bbox set.
    """
    if extent_bbox and not extent_crs:
        raise Exception(f"Must Provide extent_crs [{extent_crs}] if an extent given")
    
    if not is_bbox(extent_bbox):
        raise Exception(f"{extent_bbox} Is Not A bbox")

    wm = WebMap()
    wm._gis = gis
    wm._con = gis._con

    if snippet is None:
        snippet = "Not Set"
    
    if tags is None:
        tags = []
    
    if extent_bbox is None:
        extent_bbox = [-180, -90, 180, 90]
    else:
        extent_bbox = change_box_crs(extent_bbox, extent_crs, 4326)

    extent_crs = 4326

    webmap_item_properties = {'title': name,
             'snippet': snippet,
             'tags': tags,
             'extent': {'xmin': extent_bbox[0], 'ymin': extent_bbox[1], 'xmax': extent_bbox[2], 'ymax': extent_bbox[3], 'spatialReference': {'wkid': extent_crs}}
             }

    wm.save(webmap_item_properties)

    return wm


def rewrite_layer_aux(map_item: WebMap,
                  layer_title: str,
                  new_layer_id: str,
                  gis_new: Optional[GIS] = None,
                  gis_old: Optional[GIS] = None):
    """
    Given a map it redirects where a layer is consumed from.

    Parameters:
        - map_item: WebMap to change the layer from
        - layer_title: Title of the layer inside the map, used to find the
            layer to replace
        - new_layer_id: ID of the new source to use.
        - gis_new (Optional): GIS session to get the new layer from.
            If None is given, the one of the map will be used.
        - gis_old (Optional): GIS session to check the layes type matches.
            If None is given, the one of the map will be used.
            If the gis session can't access the layers type Will NOT be checked.
    """
    if gis_old is None:
        gis_old = map_item._gis
    if gis_new is None:
        gis_new = map_item._gis
    
    webmap = WebMap(map_item)
    
    new_layer = gis_new.content.get(new_layer_id)
    if new_layer is None:
        raise Exception(f"Layer {new_layer_id} Can't Be Found")
    
    map_layer = webmap.get_layer(title=layer_title)
    
    if map_layer is None:
        raise Exception(f"Layer {layer_title} Can't Be Found In Map")
    
    change_symbology = "drawingInfo" in map_layer.get("layerDefinition", {})
    read_symbology = None

    if "itemId" in map_layer:
        prev_layer_id = map_layer["itemId"]
        old_layer = gis_old.content.get(prev_layer_id)
        if old_layer is not None:
            if old_layer.type != new_layer.type:
                raise Exception(f"Old Layer ({old_layer.type}) And New Layer ({new_layer.type}) Need Matching Types")
            if change_symbology and hasattr(old_layer, "layers"):
                read_symbology = get_symbology_aux(old_layer.layers[0])
    else:
        url = map_layer["url"]
        #TODO: Check Type Through URL

    new_url = new_layer.url
    
    map_layer["itemId"] = new_layer_id
    map_layer["url"] = new_url
    if change_symbology and read_symbology is not None:
        def_before = map_layer.get("layerDefinition", {})
        def_before["drawingInfo"] = read_symbology
        map_layer["layerDefinition"] = def_before
    #TODO: Check If Symbology Is from Layer or from Map

    webmap.update_layer(dict(map_layer))
    webmap.update()


def rewrite_layer(gis: GIS,
                  map_id: str,
                  layer_title: str,
                  new_layer_id: str,
                  gis_new: Optional[GIS] = None,
                  gis_old: Optional[GIS] = None):
    """
    Given a map it redirects where a layer is consumed from.

    Parameters:
        - gis: GIS Item linked to the portal fo the map
        - map_id: ID of the map where the map is saved
        - layer_title: Title of the layer inside the map, used to find the
            layer to replace
        - new_layer_id: ID of the new source to use.
        - gis_new (Optional): GIS session to get the new layer from.
            If None is given, the one of the map will be used.
        - gis_old (Optional): GIS session to check the layes type matches.
            If None is given, the one of the map will be used.
            If the gis session can't access the layers type Will NOT be checked.
    """
    map_item = get_map(gis, map_id)

    return rewrite_layer_aux(map_item, layer_title, new_layer_id, gis_new, gis_old)