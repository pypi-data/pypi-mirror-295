from typing import Optional

from arcgis.gis import GIS
from arcgis.mapping import WebMap

from .constants import FEATURE_LAYER_TYPE, WEBMAP_ITEM_TYPE
from .common import ordinal


from exceptions.type_checker import type_checker


@type_checker
def get_item(gis: GIS,
             item_id: str):
    """
    Find Item from its id
    
    Parameters:
        - gis: GIS object logged in where to search from
        - item_id: ID of the asked item
    
    Returns the item object inside the service
    """
    gis_item = gis.content.get(item_id)
    if gis_item is None:
        raise Exception(f"Layer (Id: {item_id}) Can't Be Found")
    
    return gis_item

@type_checker
def get_layer(gis: GIS,
              layer_id: str,
              number: Optional[int] = None):
    """
    Find Layer from its id
    
    Parameters:
        - gis: GIS object logged in where to search from
        - layer_id: ID of the asked layer
        - number (Optional): Layer Number inside the item. If not provided
            it'll be assumed the item should only have 1 layer
    
    Returns the layer object inside the service
    """
    layer_item = get_item(gis, layer_id)
    if layer_item.type != FEATURE_LAYER_TYPE:
        raise Exception(f"Given Item Is Not A Feature Layer Type But A {layer_item.type}")
    
    layers = layer_item.layers
    if layers is None:
        raise Exception(f"Layer (Id: {layer_id}) Has NO Layers")
    if len(layers) > 1 and number is None:
        raise Exception(f"Layer (Id: {layer_id}) Has Too Many Layers ({layers})")
    elif len(layers) == 0:
        raise Exception(f"Layer (Id: {layer_id}) Has NO Layers")
    
    if number is None:
        return layers[0]
    
    if len(layers) < number:
        ord_num = ordinal(number)
        raise Exception(f"Layer (Id: {layer_id}) Has Not Enough Layers To Get the {ord_num} One [{len(layers)} < {number}]")

    return layers[number]

@type_checker
def get_map(gis: GIS,
            map_id: str):
    """
    Given a GIS session and a map_id, it returns the WebMap item
    associated to said id

    Parameters:
        - gis: GIS Item of the given map
        - map_id: Id of the item with the map
    """
    map_item = get_item(gis, map_id)
    if map_item.type != WEBMAP_ITEM_TYPE:
        raise Exception(f"Given Item Is Not A Feature Layer Type But A {map_item.type}")
    
    return WebMap(map_item)
