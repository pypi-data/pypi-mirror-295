from typing import Optional, List, Dict

import warnings

import json

import geopandas as gpd
import pandas as pd

import datetime

from shapely.geometry import Point, Polygon, LineString
from shapely.geometry.base import BaseGeometry

from arcgis.gis import GIS, Item
from arcgis.features import GeoAccessor, FeatureSet, Feature, FeatureLayer
from arcgis.geometry.filters import intersects
from arcgis.geometry import Geometry
#TODO: Remove GeoAccessor

from .common import ordinal, get_fields_aux, set_display_field_aux, add_field_aux, delete_field_aux, field_present_layer, get_objectid_field_aux, create_geo_filter_envelope
from .constants import ESRI_DATA_TYPES
from .gets import get_layer, get_item
from .properties import get_layer_crs_aux
from .symbology import get_symbology_aux
from .properties import get_pop_up, get_layer_geom_type_aux, get_items_amount_aux
from .checks import parse_response

from geometry.geometry import create_geo_json
from geometry.change_crs import change_crs
from geometry.change_crs import check_gdf_geometries

from exceptions.type_checker import type_checker, TypeException

from gis_typing.gis_types import CRS_TYPE

BATCH_AMOUNT = 1000


@type_checker
def rename_fields_aux(layer: FeatureLayer,
                      change_names: Dict[str, str]):
    """
    Renames a series of fields from a layer
    
    Parameters:
        - layer: Layer Item of the structure looking to be modified
        - change_names: Dictionary to express the before_name and the new_name. {old: new}
    """
    old_names = []
    data_types = {}
    fields = get_fields_aux(layer)
    for old_name in change_names.keys():
        data_type = None
        for field in fields:
            if field[0] == old_name:
                data_types[old_name] = field[2]
                old_names.append(old_name)
                break
    
    if len(old_names) == 0:
        raise Exception("No Valid Field Found To Change")

    object_id_field = get_objectid_field_aux(layer)

    fields_to_ask = [object_id_field]
    fields_to_ask.extend(old_names)

    old_data = read_full_layer_aux(layer)[fields_to_ask]
    
    new_names = []
    new_data_types = []
    alias = []
    for old_name, new_name in change_names.items():
        data_type = data_types.get(old_name)
        if data_type is None:
            continue
        new_data_types.append(data_type)
        new_names.append(new_name.lower())
        alias.append(new_name.lower())
        change_names[old_name] = new_name.lower()
    add_field_aux(layer, new_names, new_data_types, alias)
    layer._refresh()

    new_data = old_data.rename(columns=change_names)
    adds = update_layer_aux(layer, new_data, columns=new_names)
    delete_field_aux(layer, old_names)

    return adds


def parse_features_to_gdf(feature_set: FeatureSet,
                          geometry_column: str = "geometry"):
    """
    Given a set of features it transforms them to a gdf.

    Parameters:
        feature_set: Dict of features to transform
        geometry_column (Optional): The name to give to the geometry column
    """
    features = feature_set.features
    crs = feature_set._spatial_reference["latestWkid"]
    fields = feature_set._fields

    date_fields = []
    for field in fields:
        name = field["name"]
        dtype = field["type"]
        if dtype == "esriFieldTypeDate":
            date_fields.append(name)

    if len(features) == 0:
        columns = [field["name"] for field in fields]
        columns.append(geometry_column)
        gdf = gpd.GeoDataFrame(columns=columns, geometry=geometry_column, crs=crs)
    else:
        data = []
        for feature in features:
            geometry = feature.geometry
            geometry = Geometry(geometry)
            geometry = geometry.as_shapely
            attributes = dict(feature.attributes)
            for field in date_fields:
                if attributes[field] is not None:
                    attributes[field] = datetime.datetime.fromtimestamp(attributes[field] / 1000)
            attributes[geometry_column] = geometry
            data.append(attributes)
    
        gdf = gpd.GeoDataFrame(data, geometry=geometry_column, crs=crs)
    
    for field in fields:
        name = field["name"]
        dtype = field["type"]
        dtype = ESRI_DATA_TYPES.get(dtype)
        if dtype == "ObjectID":
            dtype = "int"
        if dtype == "GlobalID":
            dtype = "str"
        if dtype == "int":
            dtype = "Int64"
        if dtype == "geometry":
            continue

        if name not in date_fields:
            gdf[name] = gdf[name].astype(dtype)
        else:
            gdf[name] = pd.to_datetime(gdf[name])

    return gdf


def parse_out_fields(layer: FeatureLayer,
                    out_fields: Optional[List[str]] = None,
                    excl_fields: Optional[List[str]] = None):
    """
    Given a layer and a set fo out/excl. fields it retusn the out_fields
    list/str that matches the request.

    Parameters:
        - layer: Layer wanting to be asked
        - out_fields (Optional): List of fields names to recieve. If None, all will be returned.
        - excl_fields (Optional): List of fields names to exclude, if out_fields set it'll be ignored.
            If None, all will be returned.
    """
    if out_fields is None and excl_fields is None:
       return "*"

    fields = get_fields_aux(layer)

    if out_fields is None and excl_fields is not None:
        out_fields = [field[0] for field in fields]
        for field in excl_fields:
            if field in out_fields:
                out_fields.remove(field)
    else:
        keep_fields = []
        real_fields = [field[0] for field in fields]
        for field in out_fields:
            if field in real_fields:
                keep_fields.append(field)
            else:
                warnings.warn(f"{field} Not Existing In Layer, Not Using It")
        out_fields = keep_fields
    return out_fields


def check_fields(layer: FeatureLayer,
                 gdf: gpd.GeoDataFrame):
    """
    Check if the fields in a given GDF matches the data types of 
    a given layer.

    Parameters:
        - layer: Layer to check if matching
        - gdf: GeoDataFrame to comapre with
    """
    fields = get_fields_aux(layer)

    gdf_types = dict(gdf.dtypes)
    invalids = []
    for field in fields:
        if field[2].lower() == "objectid":
            continue

        data_type = gdf_types.get(field[1], None)
        if data_type is None:
            continue

        str_type = str(data_type).lower()
        if str_type.find("float") >= 0:
            str_type = "float"
        
        if str_type.find("int") >= 0:
            str_type = "int"
        
        if str_type.find("datetime") >= 0:
            str_type = "datetime"
        
        if str_type.find("object") >= 0:
            str_type = "str"

        if str_type != field[2].lower():
            invalids.append((field[1], (field[2], str_type)))
        
    if len(invalids) == 0:
        return
    else:
        error = "Invalid Error Types Provided"
        for invalid in invalids:
            error += f"\n - {invalid[0]} - Expected: {invalid[1][0]}. Received: {invalid[1][1]}"
        raise Exception(error)


def filter_columns_to_fields(layer: FeatureLayer,
                             gdf: gpd.GeoDataFrame):
    """
    Given a GDF it filters it to only the columns that matches
    the fields of a given layer.

    Parameters:
        - layer: Layer to check if matching
        - gdf: GeoDataFrame to comapre with
    """    
    fields = get_fields_aux(layer)
    fields_names = [field[1] for field in fields]
    columns = gdf.columns
    geom_column = gdf.geometry.name
    valid_columns = []
    for column in columns:
        if column in fields_names or column == geom_column:
            valid_columns.append(column)
    
    return valid_columns    


def update_pop_up(gis: GIS,
                  layer_id: str,
                  number: int,
                  pop_up_data: dict):
    """
    Given a popupInfo dictionary, it updates the layer PopUp info with it

    Parameters:
        - gis: GIS struct from the user that owns the layer
        - layer_id: Layer ID of the layer wanting to be read
        - number: Number layer of the layer wanting to be read. If
            not set, default at 0
        - pop_up_data: Dictionary representing the new pop up
    """
    layer_item = get_item(gis, layer_id)
    
    layers_data = layer_item.get_data()
    
    if "layers" not in layers_data:
        layers = layer_item.layers
        if number >= len(layers):
            raise Exception(f"Layer Number {number} Can't Be Found Inside Item {layer_id}")
        layers_data["layers"] = []
        layers_data["layers"].append({"popupInfo": pop_up_data, "id": number})
    else:
        layer_pos = None
        for i, layer in enumerate(layers_data["layers"]):
            if layer["id"] == number:
                layer_pos = i
                break

        if layer_pos is None:
            raise Exception(f"Layer Number {number} Can't Be Found Inside Item {layer_id}")

        layers_data["layers"][layer_pos]["popupInfo"] = pop_up_data
    
    update_dict = {"layers": layers_data["layers"]}
    update_dict = {"text": json.dumps(update_dict)}    

    return layer_item.update(update_dict)

@type_checker
def update_symbology_aux(layer: FeatureLayer,
                         symbology: dict):
    """
    Updates the symbology data of a given layer

    Parameters:
        - layer: Layer Item of the structure looking to be read
        - symbology: Dictionary to set as symbology of the layer
    """
    symbology_dict = {"drawingInfo": dict(symbology)}

    ret_val = layer.manager.update_definition(symbology_dict)
    layer._refresh()
    return ret_val

@type_checker
def update_symbology(gis: GIS,
                     layer_id: str,
                     symbology: dict,
                     number: Optional[int] = None):
    """
    Updates the symbology data of a given layer

    Parameters:
        - gis: GIS struct from the user that owns the layer
        - layer_id: Layer ID of the layer wanting to be read
        - symbology: Dictionary to set as symbology of the layer
        - number (Optional): Layer Number inside the item. If not provided
            it'll be assumed the item should only have 1 layer
    """
    layer = get_layer(gis, layer_id, number)
    
    return update_symbology_aux(layer, symbology)


def get_layer_in_list(layers_found: List[Item],
                      title: str):
    """
    Find Layer titled as title inside all the layers found
    
    Parameters:
        - layers_found: List of Items to check from
        - title: Title searched
    
    Returns None if not found, the item if found
    """
    for layer in layers_found:
        if layer.title == title:
            return layer
    
    return None


def change_gdf_to_layer_crs(gdf: gpd.GeoDataFrame,
                            layer: FeatureLayer):
    """
    Given a geodataframe it returns a new one with the crs of the given layer
    
    Parameters:
        - gdf: GeoDataFrame to change the crs
        - layer: Layer where to read the crs from
    
    Returns the sucess status of each add.
    """
    layer_crs = get_layer_crs_aux(layer)
    gdf_crs = gdf.crs
    if gdf_crs is None:
        raise Exception("GeoDataFrame Must Have A CRS Assigned")
    elif gdf_crs != layer_crs:
        invalid_geoms = check_gdf_geometries(gdf)
        if len(invalid_geoms) > 0:
            raise Exception(f"Invalid Geometries For The Given CRS\n{invalid_geoms}")
        new_gdf = gdf.to_crs(layer_crs, inplace=False)
        #TODO Valid Geometries
    else:
        new_gdf = gdf.copy()
    
    return new_gdf


def create_fake_line(layer: FeatureLayer,
                     empty_gdf: gpd.GeoDataFrame):
    """
    Given a GDF and its assigned layer, it returns a new GDF with one fake line

    Parameters:
        - layer: Layer to use to know which type of geom to add.
        - empty_gdf: GDF to clone the structure from
    """
    geometry_type = get_layer_geom_type_aux(layer)

    fake_geometry = None
    if geometry_type.lower().find("point") >= 0:
        fake_geometry = Point(0, 0)
    elif geometry_type.lower().find("line") >= 0:
        fake_geometry = LineString([(0, 0), (1, 1)])
    elif geometry_type.lower().find("polygon") >= 0:
        fake_geometry = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])

    fake_line = {}
    for name, dtype in dict(empty_gdf.dtypes).items():
        dtype = str(dtype)
        name = str(name)

        if dtype == "object":
            fake_line[name] = "fake"
        elif dtype.lower().find("int") >= 0:
            fake_line[name] = 1
        elif dtype.lower().find("float") >= 0:
            fake_line[name] = 0.1
        elif dtype.lower().find("datetime") >= 0:
            fake_line[name] = datetime.datetime.now()
        elif dtype.lower().find("geometry") >= 0:
            fake_line[name] = fake_geometry
    
    new_gdf = gpd.GeoDataFrame([fake_line], geometry = "SHAPE", crs=empty_gdf.crs)

    return GeoAccessor.from_geodataframe(new_gdf)


def get_valid_name(gis: GIS,
                   asked_name: str):
    """
    Given a GIS session and an asked name. It returns the
    first valid name for it. Adding '(nth Copy)' in the end of it.

    Parameters:
        gis: GIS sesssion to check for
        asked_name: Name to check availability for
    """
    og_name = asked_name
    new_name = asked_name
    names_matching = gis.content.search(f"title:{new_name}")
    i = 1
    while get_layer_in_list(names_matching, new_name) is not None:
        ord_i = ordinal(i)
        new_name = f"{og_name} ({ord_i} Copy)"
        names_matching = gis.content.search(f"title:{new_name}")
        i += 1
    
    return new_name


def get_cloning_data(layer: FeatureLayer,
                     copy_data: bool):
    """
    Given a feature layer. It returns the full data of it ready for 
    it to be used to clone the layer.

    Parameters:
        layer: FeatureLayer item to read from
        copy_data: If it should copy the data or just the structure
    """
    if copy_data:
        layer_content = read_full_layer_aux_sdf(layer)
    else:
        layer_content = create_empty_gdf_aux(layer)
        layer_content = GeoAccessor.from_geodataframe(layer_content)
    
    object_id = get_objectid_field_aux(layer)

    if len(layer_content) == 0:
        layer_content = create_empty_gdf_aux(layer)
        layer_content = GeoAccessor.from_geodataframe(layer_content)

    layer_content = layer_content.drop(columns=[object_id])
    if "SHAPE__Length" in layer_content.columns:
        layer_content = layer_content.drop(columns=["SHAPE__Length"])
    if "SHAPE__Area" in layer_content.columns:
        layer_content = layer_content.drop(columns=["SHAPE__Area"])

    fields_ordered = []
    fields_real = get_fields_aux(layer)
    fields_real = [field[0] for field in fields_real]
    for field in layer_content.columns:
        if field in fields_real:
            fields_ordered.append(field)
    if layer_content.geometry.name not in fields_ordered:
        fields_ordered.append(layer_content.geometry.name)
    layer_content = layer_content[fields_ordered]

    return layer_content

@type_checker
def clone_layer(og_gis: GIS,
                og_id: str,
                new_gis: GIS,
                new_name: Optional[str] = None,
                copy_data: bool = True,
                publish_batch: int = BATCH_AMOUNT,
                number: Optional[int] = None):
    """
    Copy the content from the layer with id og_id in the og_gis into a 
    new layer in the new_gis. The name will be conserved unless given a new one, 
    in case the name is already taken a versioning will be added to it.
    
    Parameters:
        - og_gis: GIS struct from an user that can read the original layer
        - og_id: id of the original layer
        - new_gis: GIS struct from the user that will own the new layer
        - new_name (Optional): Name to be assigned to the new layer, if None the
            original name will be conserved.
        - copy_data (Optional): Bool to indicate if it should copy all the data. By deafult,
            set in True. If false it'll copy only the structure
        - publish_batch (Optional): When publishing the new layers, how many rows
            to publish per batch. By default 1000
        - number (Optional): Layer Number inside the item. If not provided
            it'll be assumed the item should only have 1 layer
    Returns the new layer item.
    """
    if publish_batch <= 0 or not isinstance(publish_batch, int):
        raise Exception(f"Publish Batch must be a Positive Integer")

    old_layer = get_layer(og_gis, og_id, number)
    symbology = get_symbology_aux(old_layer)
    layer_content = get_cloning_data(old_layer, copy_data)

    title = og_gis.content.get(og_id).title
    if new_name is None:
        new_name = title

    new_name = get_valid_name(new_gis, new_name)

    empty = False
    if len(layer_content) == 0:
        empty = True
        layer_content = create_fake_line(old_layer, layer_content)

    new_item = create_layer(layer_content, new_gis, new_name, publish_batch=publish_batch, is_sdf=False)
    new_layer = new_item.layers[0]

    if empty:
        new_layer.manager.truncate()

    symbology_dict = {"drawingInfo": dict(symbology)}
    new_layer.manager.update_definition(symbology_dict)

    object_id = get_objectid_field_aux(new_layer)
    set_display_field_aux(new_layer, object_id)

    pop_up = get_pop_up(og_gis, og_id, number)
    update_pop_up(new_gis, new_item.id, 0, pop_up)

    new_layer._refresh()
    return new_item


def get_date_columns(gdf: gpd.GeoDataFrame):
    """
    Given a GDF it returns the columns with a datetime type

    Parameters:
        - gdf: GeoDataFrame to check
    """
    columns = []
    for column, data_type in dict(gdf.dtypes).items():
        if str(data_type).find("datetime") >= 0:
            columns.append(column)
    
    return columns


@type_checker
def create_layer(gdf: pd.DataFrame,
                 gis: GIS,
                 title: Optional[str] = None,
                 folder: Optional[str] = None,
                 publish_batch: int = BATCH_AMOUNT,
                 is_sdf: bool = False):
    """
    Given a geodataframe it creates a feature layer with its data in a new item
    
    Parameters:
        - gdf: GeoDataFrame to publish
        - gis: GIS struct from the user that will own the new layer
        - title (Optional): Name to be given to the layer
        - folder (Optional): Folder in the portal where to store the layer
        - publish_batch (Optional): When publishing the new layers, how many rows
        to publish per batch. By default 1000
        - is_sdf (Optional): If the given gdf is already an sdf.
    Returns the new layer item.
    """
    if publish_batch <= 0 or not isinstance(publish_batch, int):
        raise Exception(f"Publish Batch must be a Positive Integer")

    end = publish_batch
    if end > len(gdf):
        end = len(gdf)

    one_columned = False
    if len(gdf) == 1:
        gdf["aux"] = 1
        one_columned = True

    if not is_sdf:
        sdf = GeoAccessor.from_geodataframe(gdf[:end])
    else:
        sdf = gdf

    new_names = {}
    empty_cols = {}
    for col in sdf.columns:
        if col == "SHAPE":
            continue
        new_names[col] = col.lower()
        if sdf[col].isna().all():
            empty_cols[col.lower()] = str(sdf[col].dtype)

    sdf = sdf.rename(columns=new_names)
    if len(empty_cols) > 0:
        sdf = sdf.drop(columns=list(empty_cols.keys()))

    item = sdf.spatial.to_featurelayer(gis=gis, title=title, folder=folder)
    layer = item.layers[0]
    fields = get_fields_aux(layer)
    renames = {}
    offset = 1
    for i, column in enumerate(sdf.columns):
        if column == "SHAPE":
            offset = 0
            continue

        saved_name = fields[i + offset][0]
        if column != saved_name:
            renames[saved_name] = column
        
    if len(renames) > 0:
        rename_fields_aux(layer, renames)
    if len(empty_cols) > 0:
        add_field_aux(layer, list(empty_cols.keys()), list(empty_cols.values()))

    if end != len(gdf):
        add_to_layer_aux(layer, gdf[end:], publish_batch, is_sdf=is_sdf)

    object_id = get_objectid_field_aux(layer)
    set_display_field_aux(layer, object_id)

    if one_columned:
        delete_field_aux(layer, "aux")
    
    return item

@type_checker
def add_to_layer_aux(layer: FeatureLayer,
                     gdf: pd.DataFrame,
                     publish_batch: int = BATCH_AMOUNT,
                     is_sdf: bool = False):
    """
    Given a geodataframe it adds all its features to a layer
    
    Parameters:
        - layer: Layer Item of the structure looking to be copied
        - gdf: GeoDataFrame to publish
        - publish_batch (Optional): When publishing the new layers, how many rows
        to publish per batch. By default 1000
        - is_sdf (Optional): If the given gdf is already an sdf.
    Returns the sucess status of each add.
    """
    if publish_batch <= 0 or not isinstance(publish_batch, int):
        raise Exception(f"Publish Batch must be a Positive Integer")

    total = {"addResults": [], "updateResults": [], "deleteResults": []}
    if len(gdf) == 0:
        return parse_response(total)

    if not is_sdf:
        if not isinstance(gdf, gpd.GeoDataFrame):
            raise TypeException(f"If not SDF, must provide a GDF Not a {type(gdf)}")
        gdf = change_gdf_to_layer_crs(gdf, layer)
        check_fields(layer, gdf)
        valid_columns = filter_columns_to_fields(layer, gdf)
        gdf = gdf[valid_columns]
        sdf = GeoAccessor.from_geodataframe(gdf)
    else:
        #TODO: Do the same checks for SDF
        sdf = gdf

    date_columns = get_date_columns(sdf)
    object_id = get_objectid_field_aux(layer)

    for i in range(0, len(sdf), publish_batch):
        end = i + publish_batch
        if i > len(sdf):
            end = len(sdf)
        batch_response = layer.edit_features(adds = sdf[i: end])
        if len(date_columns) > 1:
            aux_sdf = sdf[i: end][date_columns]
            object_ids = [item["objectId"] for item in batch_response["addResults"]]
            aux_sdf[object_id] = object_ids
            update_layer_aux(layer, aux_sdf)

        total["addResults"].extend(batch_response["addResults"])
        total["updateResults"].extend(batch_response["updateResults"])
        total["deleteResults"].extend(batch_response["deleteResults"])

    #TODO: Parse Error Codes (Specially 10550, Invalid Geometry)
    return parse_response(total)

@type_checker
def add_to_layer(gdf: gpd.GeoDataFrame,
                 gis: GIS,
                 layer_id: str,
                 number: Optional[int] = None,
                 publish_batch: int = BATCH_AMOUNT):
    """
    Given a geodataframe it adds all its features to a layer
    
    Parameters:
        - gdf: GeoDataFrame to publish
        - gis: GIS struct from the user that owns the layer
        - layer_id: Layer ID of the layer wanting to be modified
        - number (Optional): Layer Number inside the item. If not provided
            it'll be assumed the item should only have 1 layer
        - publish_batch (Optional): When publishing the new layers, how many rows
        to publish per batch. By default 1000
    
    Returns the sucess status of each add.
    """
    layer = get_layer(gis, layer_id, number)

    return add_to_layer_aux(layer, gdf, publish_batch)

@type_checker
def update_layer_aux(layer: FeatureLayer,
                     gdf: pd.DataFrame,
                     columns: Optional[List[str]] = None,
                     excl_columns: Optional[List[str]] = None):
    """
    Given a (geo)dataframe it updates the features asked in columns to a layer
    
    Parameters:
        - layer: Layer Item of the structure looking to be copied
        - gdf: (Geo)DataFrame to publish
        - columns(Optional): strings of the names of the columns to update. If None, all columns will be updated
        - excl_columns (Optional): List of fields names to exclude, if columns set it'll be ignored.
            If None, all will be returned.
    
    Returns the sucess status of each add.
    """
    total = {"addResults": [], "updateResults": [], "deleteResults": []}
    if len(gdf) == 0:
        return parse_response(total)
    object_id_col = get_objectid_field_aux(layer)
    if isinstance(gdf, gpd.GeoDataFrame):
        geom_column = gdf.geometry.name
    else:
        geom_column = None

    if columns:
        if isinstance(columns, str):
            columns = [columns]
        columns = parse_out_fields(layer, columns, excl_columns)
        if len(columns) == 0:
            warnings.warn("Nothing changed as columns was empty")
            return
        if object_id_col not in columns:
            columns.append(object_id_col)
        gdf = gdf[columns]
    
    if object_id_col not in gdf.columns:
        raise Exception(f"{object_id_col} Must Be Present In GDF In Order To Know Which Line To Update")

    check_fields(layer, gdf)

    if geom_column in gdf.columns:
        valid_columns = filter_columns_to_fields(layer, gdf)
        gdf = gdf[valid_columns]
        gdf = change_gdf_to_layer_crs(gdf, layer)
        gdf = GeoAccessor.from_geodataframe(gdf, column_name=geom_column)
    
    if excl_columns is not None:
        keep_cols = list(gdf.columns)
        for column in excl_columns:
            if column in keep_cols:
                keep_cols.remove(column)
        gdf = gdf[keep_cols]

    feature_set = FeatureSet(features=[])
    for index, row in gdf.iterrows():
        data = row.to_dict()
        data[object_id_col] = int(data[object_id_col])
        if geom_column in gdf.columns:
            geo = data.pop(geom_column)
            feature = Feature(attributes=data, geometry=geo)
        else:
            feature = Feature(attributes=data, geometry=None)
            
        feature_set.features.append(feature)
        if len(feature_set) == 1000:
            batch_response = layer.edit_features(updates = feature_set)
            total["addResults"].extend(batch_response["addResults"])
            total["updateResults"].extend(batch_response["updateResults"])
            total["deleteResults"].extend(batch_response["deleteResults"])
            feature_set = FeatureSet(features=[])
    
    if len(feature_set) > 0:
        batch_response = layer.edit_features(updates = feature_set)
        total["addResults"].extend(batch_response["addResults"])
        total["updateResults"].extend(batch_response["updateResults"])
        total["deleteResults"].extend(batch_response["deleteResults"])

    return parse_response(total)

@type_checker
def update_layer(gdf: pd.DataFrame,
                 gis: GIS,
                 layer_id: str,
                 number: Optional[int] = None,
                 columns: Optional[List[str]] = None,
                 excl_columns: Optional[List[str]] = None):
    """
    Given a (geo)dataframe it updates the features asked in columns to a layer
    
    Parameters:
        - gdf: (Geo)DataFrame to publish
        - gis: GIS struct from the user that owns the layer
        - layer_id: Layer ID of the layer wanting to be modified
        - number (Optional): Layer Number inside the item. If not provided
            it'll be assumed the item should only have 1 layer
        - columns(Optional): strings of the names of the columns to update. If None, all columns will be updated
        - excl_columns (Optional): List of fields names to exclude, if columns set it'll be ignored.
            If None, all will be returned.
    
    Returns the sucess status of each add.
    """
    layer = get_layer(gis, layer_id, number)

    return update_layer_aux(layer, gdf, columns, excl_columns)

@type_checker
def empty_layer_aux(layer: FeatureLayer):
    """
    Empty the data from a layer
    
    Parameters:
        - layer: Layer Item of the structure looking to be copied
    
    Returns the sucess status of each add.
    """    
    return layer.manager.truncate()

@type_checker
def empty_layer(gis: GIS,
                layer_id: FeatureLayer,
                number: Optional[int] = None):
    """
    Empty the data from a layer
    
    Parameters:
        - gis: GIS struct from the user that owns the layer
        - layer_id: Layer ID of the layer wanting to be emptied
        - number (Optional): Layer Number inside the item. If not provided
            it'll be assumed the item should only have 1 layer
    
    Returns the sucess status of each add.
    """
    layer = get_layer(gis, layer_id, number)
    
    return layer.manager.truncate()


def create_empty_gdf_aux(layer: FeatureLayer,
                         crs: Optional[CRS_TYPE] = None):
    """
    Returns an empty geodataframe with the columns of a given layer
    
    Parameters:
        - layer: Layer Item of the structure looking to be copied
        - crs (Optional): CRS of the GeoDataFrame to be created. If None, 
            the one of the layer will be used
    """
    fields = get_fields_aux(layer)
    fields.append(("SHAPE", "SHAPE", "geometry"))

    columns = [field[0] for field in fields]
    if crs is None:
        crs = get_layer_crs_aux(layer)
    gdf = gpd.GeoDataFrame(columns=columns, geometry='SHAPE', crs=crs)
    for field in fields:
        col = field[1]
        dtype = field[2]
        if col == "SHAPE":
            continue
        if dtype == "ObjectID":
            dtype = "int"
        if dtype == "GlobalID":
            dtype = "str"

        if dtype != "datetime":
            gdf[col] = gdf[col].astype(dtype)
        else:
            gdf[col] = pd.to_datetime(gdf[col])

    return gdf


@type_checker
def create_empty_gdf(gis: GIS,
                     layer_id: str,
                     number: Optional[int] = None,
                     crs:Optional[CRS_TYPE] = None):
    """
    Returns an empty geodataframe with the columns of a given layer
    
    Parameters:
        - gis: GIS struct from the user that owns the layer
        - layer_id: Layer ID of the layer wanting to be emptied
        - number (Optional): Layer Number inside the item. If not provided
            it'll be assumed the item should only have 1 layer
        - crs (Optional): CRS of the GeoDataFrame to be created. If None, 
            the one of the layer will be used
    """
    layer = get_layer(gis, layer_id, number)
    
    return create_empty_gdf_aux(layer, crs)

@type_checker
def read_full_layer_aux_sdf(layer: FeatureLayer,
                            out_crs: Optional[CRS_TYPE] = None):
    """
    Returns the full data stored in an asked layer.
    
    Parameters:
        - layer: Layer wanting to be asked
        - out_crs (Optional): Wanted CRS of the returned GeoDataFrame. If not
            loaded, it'll be returned in the one of the layer.

    Returns a SDF
    """
    total_data = None
    if out_crs is None:
        out_crs = get_layer_crs_aux(layer)
    new_data = layer.query(out_sr=out_crs)
    new_data = parse_features_to_gdf(new_data)
    while len(new_data) > 0:
        if total_data is None:
            total_data = new_data.copy()
        else:
            total_data = pd.concat([total_data, new_data])

        new_data = layer.query(where = "1=1", out_sr=out_crs, result_offset=len(total_data))
        new_data = parse_features_to_gdf(new_data)

    if total_data is None:
        return new_data

    return total_data

@type_checker
def read_full_layer_aux(layer: FeatureLayer,
                        out_crs: Optional[CRS_TYPE] = None):
    """
    Returns the full data stored in an asked layer.
    
    Parameters:
        - layer: Layer wanting to be asked
        - out_crs (Optional): Wanted CRS of the returned GeoDataFrame. If not
            loaded, it'll be returned in the one of the layer.

    Returns a GeoDataFrame
    """
    if out_crs is None:
        out_crs = get_layer_crs_aux(layer)
    total_data = read_full_layer_aux_sdf(layer, out_crs=out_crs)
    total_data = total_data.rename(columns = {"SHAPE": "geometry"})
    return gpd.GeoDataFrame(total_data, geometry="geometry", crs=out_crs)

@type_checker
def read_full_layer(gis: GIS,
                    layer_id: str,
                    number: Optional[int] = None,
                    out_crs: Optional[CRS_TYPE] = None):
    """
    Returns the full data stored in an asked layer.
    
    Parameters:
        - gis: GIS struct from the user that owns the layer
        - layer_id: Layer ID of the layer wanting to be asked
        - number (Optional): Layer Number inside the item. If not provided
            it'll be assumed the item should only have 1 layer
        - out_crs (Optional): Wanted CRS of the returned GeoDataFrame. If not
            loaded, it'll be returned in the one of the layer.

    Returns a GeoDataFrame
    """
    layer = get_layer(gis, layer_id, number)

    return read_full_layer_aux(layer, out_crs)


@type_checker
def read_layer_gdf_aux(layer: FeatureLayer,
                       query: str = "1=1",
                       geometry_filter: Optional[BaseGeometry] = None,
                       geometry_crs: CRS_TYPE = 4326,
                       out_fields: Optional[List[str]] = None,
                       excl_fields: Optional[List[str]] = None,
                       out_crs: Optional[CRS_TYPE] = None,
                       geometry_post: bool = True):
    """
    Returns the full data stored in an asked layer.
    
    Parameters:
        - layer: Layer wanting to be asked
        - query (Optional): String representing a SQL query to filter the data to 
            to be read from the layer. If None, all the data will be providen.
        - geometry_filter (Optional): Shapely (Multi)Polygon to filter data geographically.
            If None, all the data will be providen.
        - geometry_crs (Optional): CRS of the given geometry_filer. If missing, 4326 will be assumed.
        - out_fields (Optional): List of fields names to recieve. If None, all will be returned.
        - excl_fields (Optional): List of fields names to exclude, if out_fields set it'll be ignored.
            If None, all will be returned.
        - out_crs (Optional): CRS of the returned gdf. If None, the crs of the layer will be used.
        - geometry_post (Optional): If the geometry filter exists, if it should be done after the layer query. True by default

    Returns a GeoDataFrame
    """
    geo_filter = None
    if geometry_filter is not None and not geometry_post:
        geo_filter = create_geo_filter_envelope(geometry_filter, geometry_crs)

    if out_crs is None:
        out_crs = get_layer_crs_aux(layer)

    object_id_col = get_objectid_field_aux(layer)
    
    basic_where = query
    return_only_geoms = False

    if out_fields is not None and len(out_fields) == 1 and (out_fields[0] == "SHAPE" or out_fields[0] == "geometry"):
        return_only_geoms = True
        out_fields = [object_id_col]

    out_fields = parse_out_fields(layer, out_fields, excl_fields)

    total_data = None
    try:
        new_data = layer.query(where = query, geometry_filter=geo_filter, out_fields=out_fields, out_sr=out_crs)
        new_data = parse_features_to_gdf(new_data)
        while len(new_data) > 0:
            if total_data is None:
                total_data = new_data.copy()
            else:
                total_data = pd.concat([total_data, new_data])

            new_data = layer.query(where = query, geometry_filter=geo_filter, out_fields=out_fields, out_sr=out_crs, result_offset=len(total_data))
            new_data = parse_features_to_gdf(new_data)
    except Exception as err:
        if str(err).find("Invalid") >= 0:
            raise Exception(f"Invalid Query. Query Done: where = {basic_where}, geometry_filter={geo_filter}, out_fields={out_fields}, out_sr={out_crs}")
        else:
            raise err
    
    if total_data is None:
        return new_data

    if out_fields != "*" and object_id_col not in out_fields:
        total_data = total_data.drop(columns=[object_id_col])

    total_data = total_data.rename(columns = {"SHAPE": "geometry"})

    gdf_result = gpd.GeoDataFrame(total_data, geometry="geometry", crs=out_crs)

    if geometry_filter is not None:
        filter_polygon = change_crs(geometry_filter, geometry_crs, out_crs)
        gdf_result = gdf_result[gdf_result["geometry"].intersects(filter_polygon)]

    if return_only_geoms:
        gdf_result = gdf_result["geometry"]

    return gdf_result

@type_checker
def read_layer_gdf(gis: GIS,
                   layer_id: str,
                   number: Optional[int] = None,
                   query: Optional[str] = "1=1",
                   geometry_filter: Optional[BaseGeometry] = None,
                   geometry_crs: int = 4326, 
                   out_fields: Optional[List[str]] = None,
                   excl_fields: Optional[List[str]] = None,
                   out_crs: Optional[CRS_TYPE] = None,
                   geometry_post: bool = True):
    """
    Returns the full data stored in an asked layer.
    
    Parameters:
        - gis: GIS struct from the user that owns the layer
        - layer_id: Layer ID of the layer wanting to be asked
        - number (Optional): Layer Number inside the item. If not provided
            it'll be assumed the item should only have 1 layer
        - query (Optional): String representing a SQL query to filter the data to 
            to be read from the layer. If None, all the data will be providen.
        - geometry_filter (Optional): Shapely (Multi)Polygon to filter data geographically.
            If None, all the data will be providen.
        - geometry_crs (Optional): CRS of the given geometry_filer. If missing, 4326 will be assumed.
        - out_fields (Optional): List of fields names to recieve. If None, all will be returned.
        - excl_fields (Optional): List of fields names to exclude, if out_fields set it'll be ignored.
            If None, all will be returned.
        - out_crs (Optional): CRS of the returned gdf. If None, the crs of the layer will be used.
        - geometry_post (Optional): If the geometry filter exists, if it should be done after the layer query. True by default

    Returns a GeoDataFrame
    """
    layer = get_layer(gis, layer_id, number)

    return read_layer_gdf_aux(layer, query, geometry_filter, geometry_crs, out_fields, excl_fields, out_crs, geometry_post)
    
@type_checker
def delete_features_aux(layer: FeatureLayer,
                        query: str = "1=1",
                        geometry_filter: Optional[BaseGeometry] = None, 
                        geometry_crs: CRS_TYPE =4326):
    """
    Delete Features based on a query
    
    Parameters:
        - layer: Layer wanting to be asked
        - query (Optional): String representing a SQL query to filter the data to 
            to be read from the layer. If None, all the data will be providen.
        - geometry_filter (Optional): Shapely (Multi)Polygon to filter data geographically.
            If None, all the data will be providen.
        - geometry_crs (Optional): CRS of the given geometry_filer. If missing, 4326 will be assumed.
    """
    geo_filter = None

    if query == "1=1" and geometry_filter is None:
        return layer.manager.truncate()

    if geometry_filter is not None:
        bounds = create_geo_json(geometry_filter, geometry_crs)
        geo_filter = intersects(bounds)

    return layer.delete_features(where=query, geometry_filter=geo_filter)

@type_checker
def delete_features(gis: GIS, 
                    layer_id: str,
                    number: Optional[int] = None,
                    query: str = "1=1",
                    geometry_filter: Optional[BaseGeometry] = None,
                    geometry_crs: int = 4326):
    """
    Delete Features based on a query
    
    Parameters:
        - gis: GIS struct from the user that owns the layer
        - layer_id: Layer ID of the layer wanting to be asked
        - number (Optional): Layer Number inside the item. If not provided
            it'll be assumed the item should only have 1 layer
        - query (Optional): String representing a SQL query to filter the data to 
            to be read from the layer. If None, all the data will be providen.
        - geometry_filter (Optional): Shapely (Multi)Polygon to filter data geographically.
            If None, all the data will be providen.
        - geometry_crs (Optional): CRS of the given geometry_filer. If missing, 4326 will be assumed.
    """
    layer = get_layer(gis, layer_id, number)

    return delete_features_aux(layer, query, geometry_filter, geometry_crs)

@type_checker
def get_items_amount_query(gis: GIS,
                           layer_id: str,
                           number: Optional[int] = None,
                           query: str = "1=1",
                           geometry_filter: Optional[BaseGeometry] = None,
                           geometry_crs: int = 4326):
    """
    Returns the amount of items saved in layer
    
    Parameters:
        - gis: GIS struct from the user that owns the layer
        - layer_id: Layer ID of the layer wanting to be read
        - number (Optional): Layer Number inside the item. If not provided
            it'll be assumed the item should only have 1 layer
        - query (Optional): String representing a SQL query to filter the data to 
            to be read from the layer. If None, all the data will be providen.
        - geometry_filter (Optional): Shapely (Multi)Polygon to filter data geographically.
            If None, all the data will be providen.
        - geometry_crs (Optional): CRS of the given geometry_filer. If missing, 4326 will be assumed.
    """
    layer = get_layer(gis, layer_id, number)
    
    return get_items_amount_aux(layer, query, geometry_filter, geometry_crs)

@type_checker
def rewrite_layer_aux(layer: FeatureLayer,
                      gdf: gpd.GeoDataFrame,
                      publish_batch: int = BATCH_AMOUNT):
    """
    Given a GDF and an asked layer, it'll empty the layer and add the gdf
    as all the new data in it.

    Parameters:
        - layer: Layer Item of the structure looking to be replaced
        - gdf: GeoDataFrame to replace the data with
        - publish_batch (Optional): When publishing the new layers, how many rows
            to publish per batch. By default 1000
    """

    empty_layer_aux(layer)
    return add_to_layer_aux(layer, gdf, publish_batch)

@type_checker
def rewrite_layer(gis: GIS,
                  layer_id: str,
                  gdf: gpd.GeoDataFrame,
                  number: Optional[int] = None,
                  publish_batch: int = BATCH_AMOUNT):
    """
    Given a GDF and an asked layer, it'll empty the layer and add the gdf
    as all the new data in it.

    Parameters:
        - gis: GIS struct from the user that owns the layer
        - layer_id: Layer ID of the layer wanting to be read
        - gdf: GeoDataFrame to replace the data with
        - number (Optional): Layer Number inside the item. If not provided
            it'll be assumed the item should only have 1 layer
        - publish_batch (Optional): When publishing the new layers, how many rows
            to publish per batch. By default 1000
    """
    layer = get_layer(gis, layer_id, number)

    return rewrite_layer_aux(layer, gdf, publish_batch)

@type_checker
def get_time_enable_aux(layer: FeatureLayer):
    """
    Given a layer it returns the time enable fields

    Parameters:
        layer: Layer item to check
    """
    try:
        info = layer.properties.timeInfo
    except AttributeError:
        return None, None
    if info is None:
        return None, None

    start = info.startTimeField
    end = info.endTimeField

    if end is None:
        return start, None
    else:
        return start, end

@type_checker
def get_time_enable(gis: GIS,
                    layer_id: str,
                    number: Optional[int] = None):
    """
    Given a layer it returns the time enable fields    

    Parameters:
        - gis: GIS struct from the user that owns the layer
        - layer_id: Layer ID of the layer wanting to be read
        - number (Optional): Layer Number inside the item. If not provided
            it'll be assumed the item should only have 1 layer
    """
    layer = get_layer(gis, layer_id, number)

    return get_time_enable_aux(layer)

@type_checker
def set_time_enable_aux(layer: FeatureLayer,
                        start: Optional[str],
                        end: Optional[str] = None):
    """
    Given a layer it set the time enable fields.

    Parameters:
        layer: Layer item to check
        start: field to use as start or only date enable field. If 
            None, it'll disable the time enable.
        end (Optional): field to use as end date enable field.
            If None, only start will be used and set as only
            date enbale field.
    """
    if start is None and end is None:
        info_dict = {"timeInfo": None}

    if not field_present_layer(layer, start):
        raise Exception(f"Field {start} Doesn't Exist")
    
    fields = get_fields_aux(layer)
    fields_types = {field[1]: field[2] for field in fields}

    start_type = fields_types(start, None)
    if start_type is None:
        raise Exception(f"Field {start} Doesn't Exist")
    elif start_type != "datetime":
        raise Exception(f"Field {start} Is Not Of Datetime Type")

    out_fields = [start]
    if end is not None:
        out_fields.append(end)
        if not field_present_layer(layer, end):
            raise Exception(f"Field {end} Doesn't Exist")
        end_type = fields_types(end, None)
        if end_type is None:
            raise Exception(f"Field {end} Doesn't Exist")
        elif end_type != "datetime":
            raise Exception(f"Field {end} Is Not Of Datetime Type")

    time_info = {}
    time_info["startTimeField"] = start
    time_info["trackIdField"] = None
    time_info["exportOptions"] = {
            "timeOffsetUnits": "esriTimeUnitsUnknown",
            "timeDataCumulative": False,
            "useTime": False,
            "timeOffset": 0
    }
    time_info["endTimeField"] = end
    time_info["timeInterval"] = 0,
    object_id_col = get_objectid_field_aux(layer)
    new_data = layer.query(out_fields = out_fields)
    first_date = datetime.datetime.now().timestamp()
    end_date = 0
    while len(new_data) > 0:
        first_date_aux = min([feature.attributes[start] for feature in new_data.features])
        first_date = min([first_date, first_date_aux])

        if end is None:
            end_date_aux = max([feature.attributes[start] for feature in new_data.features])
        else:
            end_date_aux = max([feature.attributes[end] for feature in new_data.features])
        end_date = min([end_date, end_date_aux])

        if total_data is None:
            total_data = new_data.copy()
        else:
            total_data = pd.concat([total_data, new_data])

        last_time = max([feature.attributes[object_id_col] for feature in new_data.features])
        new_where = f"{object_id_col} > {last_time}"
        new_data = layer.query(where = new_where, out_fields = out_fields)

    time_info["timeExtent"] = [
        first_date,
        end_date
    ],

    time_info["timeReference"] = {
            "respectsDaylightSaving": False,
            "timeZone": "UTC"
        }
    
    time_info["hasLiveData"] = False
    time_info["timeIntervalUnits"] = None
    info_dict = {"timeInfo": time_info}
    return layer.manager.update_definition(info_dict)

@type_checker
def set_time_enable(gis: GIS,
                    layer_id: str,
                    start: Optional[str],
                    end: Optional[str] = None,
                    number: Optional[int] = None):
    """
    Given a layer it set the time enable fields

    Parameters:
        - gis: GIS struct from the user that owns the layer
        - layer_id: Layer ID of the layer wanting to be read
        - start: field to use as start or only date enable field
        - end (Optional): field to use as end date enable field.
            If None, only start will be used and set as only
            date enbale field.
        - number (Optional): Layer Number inside the item. If not provided
            it'll be assumed the item should only have 1 layer
    """
    layer = get_layer(gis, layer_id, number)

    return set_time_enable_aux(layer, start, end)