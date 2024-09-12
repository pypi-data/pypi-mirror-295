from typing import List

import pandas as pd


def parse_response_particular(response: List[dict]):
    has_error = False
    errors = []
    object_ids = []

    for i, item_response in enumerate(response):
        object_id = item_response["objectId"]
        object_ids.append(object_id)
        success = item_response["success"]
        if success:
            continue
        else:
            has_error = True
            errors.append((i, item_response["error"]))
        
    final_response = {}
    final_response["has_error"] = has_error
    final_response["errors"] = errors
    final_response["object_ids"] = object_ids

    return final_response


def parse_response(response: dict):
    adds = response["addResults"]
    if len(adds) > 0:
        return parse_response_particular(adds)

    updates = response["updateResults"]
    if len(updates) > 0:
        return parse_response_particular(updates)

    deletes = response["deleteResults"]
    return parse_response_particular(deletes)


def has_multiple_dates(gdf: pd.DataFrame):
    dates = 0
    for column, data_type in dict(gdf.dtypes).items():
        if str(data_type).find("datetime") >= 0:
            dates += 1
    
    return dates > 1