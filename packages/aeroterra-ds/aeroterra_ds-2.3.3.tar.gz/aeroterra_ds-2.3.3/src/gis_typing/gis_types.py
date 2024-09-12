from typing import Union, Tuple, List

from pyproj import CRS
from rasterio.crs import CRS as RST_CRS

NUMBER_TYPE = Union[float, int]

CRS_TYPE = Union[str, dict, int, Tuple[str, str], CRS, RST_CRS]
BBOX_TYPE = Union[List[NUMBER_TYPE], Tuple[NUMBER_TYPE]]