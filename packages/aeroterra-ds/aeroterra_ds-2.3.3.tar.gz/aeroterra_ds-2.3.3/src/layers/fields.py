from typing import Optional, Dict, List, Union

from .common import add_field_aux, set_display_field_aux, delete_field_aux
from .gets import get_layer
 
from .layers import rename_fields_aux

from arcgis.gis import GIS
from exceptions.type_checker import type_checker


@type_checker
def add_field(gis: GIS,
              layer_id: str,
              name: Union[List[str], str],
              data_type: Union[List[str], str],
              alias: Optional[Union[List[str], str]] = None,
              number: Optional[int] = None):
    """
    Adds a field to the layer
    
    Parameters:
        - gis: GIS struct from the user that owns the layer
        - layer_id: Layer ID of the layer wanting to be modified
        - name: Name(s) of the field looking to be created
        - data_type: String(s) representing the data type of the field
            looking to be created
        - alias (Optional): Alias(es) of the field looking to be created. If None,
            it'll be the same as name
        - number (Optional): Layer Number inside the item. If not provided
            it'll be assumed the item should only have 1 layer
    """
    layer = get_layer(gis, layer_id, number)

    return add_field_aux(layer, name, data_type, alias)

@type_checker
def delete_field(gis: GIS,
                 layer_id: str,
                 name: Union[List[str], str],
                 number: Optional[int] = None):
    """
    Deletes a field from the layer
    
    Parameters:
        - gis: GIS struct from the user that owns the layer
        - layer_id: Layer ID of the layer wanting to be modified
        - name: Names of the field looking to be removed
        - number (Optional): Layer Number inside the item. If not provided
            it'll be assumed the item should only have 1 layer
    """
    layer = get_layer(gis, layer_id, number)

    return delete_field_aux(layer, name)


@type_checker
def rename_fields(gis: GIS,
                  layer_id: str,
                  change_names: Dict[str, str],
                  number: Optional[int] = None):
    """
    Renames a series of fields from a layer
    
    Parameters:
        - gis: GIS struct from the user that owns the layer
        - layer_id: Layer ID of the layer wanting to be modified
        - change_names: Dictionary to express the before_name and the new_name. {old: new}
        - number (Optional): Layer Number inside the item. If not provided
            it'll be assumed the item should only have 1 layer
    """
    layer = get_layer(gis, layer_id, number)
    
    return rename_fields_aux(layer, change_names)

@type_checker
def set_display_field(gis: GIS,
                      layer_id: str,
                      display_field: str,
                      number: Optional[int] = None):
    """
    Sets the display field to the ask field

    Parameters:
        - gis: GIS struct from the user that owns the layer
        - layer_id: Layer ID of the layer wanting to be modified
        - display_field: Name of the field looking to set as display_field
        - number (Optional): Layer Number inside the item. If not provided
            it'll be assumed the item should only have 1 layer
    """
    layer = get_layer(gis, layer_id, number)

    return set_display_field_aux(layer, display_field)