from typing import List, Tuple

from arcgis.gis import GIS, Layer
from arcgis.features import FeatureLayer

from .gets import get_layer

from exceptions.type_checker import type_checker


@type_checker
def get_symbology_aux(layer: Layer):
    """
    Returns the symbology data of a given layer
    
    Parameters:
        - layer: Layer Item of the structure looking to be read
    """
    if isinstance(layer, FeatureLayer):
        return layer.properties.drawingInfo
    else:
        return None
    #TODO Get Different Types Symbology Stream: 

@type_checker
def create_unique_values_symbology(colors: List[Tuple[int, int, int, int]], 
                                   field: str,
                                   values: List[Tuple[str, str]],
                                   symbols: List[dict]):
    """
    Creates the dictionary of an unique value symbology.

    Parameters:
        - colors: List of colors (tuple of 4 values, RGB & transparency)
            of the unique values.
        - field: Name of the field to renderer from
        - values: List of tuples (Value, Label) to categorize the render
        - symbols: List of symbol dictionary (excl. Color) to assign to each value    
    """
    renderers = []
    
    for i, color in enumerate(colors):
        renderer_line = {}
        rend_symbol = {}
        rend_symbol["color"] = color
        symbol = symbols[i]
        for key, value in symbol.items():
            rend_symbol[key] = value
        
        renderer_line["symbol"] = rend_symbol
        renderer_line["value"] = values[i][0]
        renderer_line["label"] = values[i][1]
        
        renderers.append(renderer_line)

    renderer = {}
    renderer["field1"] = field
    renderer["defaultSymbol"] = None
    renderer["uniqueValueInfos"] = renderers
    renderer["type"] = "uniqueValue"

    return renderer

@type_checker
def reset_unique_values(gis: GIS,
                        layer_id: str,
                        colors: List[Tuple[int, int, int, int]], 
                        field: str,
                        values: List[Tuple[str, str]],
                        symbols: List[dict],
                        transparency: int = 0):
    """
    Updates the symbology of an asked layer.

    Parameters:
        - gis: GIS struct from the user that owns the layer
        - layer_id: Layer ID of the layer wanting to be modified
        - colors: List of colors (tuple of 4 values, RGB & transparency)
            of the unique values.
        - field: Name of the field to renderer from
        - values: List of tuples (Value, Label) to categorize the render
        - symbols: List of symbol dictionary (excl. Color) to assign to each value
        - transparecny (Optional): Total transparency of the layer, from 0 to 100.
    """
    layer = get_layer(gis, layer_id)
    new_renderer = create_unique_values_symbology(colors, field, values, symbols)
    
    update_dict = {"renderer": new_renderer}
    update_dict["transparency"] = transparency
    update_dict = {"drawingInfo": update_dict}

    status = layer.manager.update_definition(update_dict)

    if not status["success"]:
        raise Exception(f"Error Updating Symbology: {status}")