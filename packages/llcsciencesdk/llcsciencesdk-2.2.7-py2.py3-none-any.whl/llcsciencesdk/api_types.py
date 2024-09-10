from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, TypedDict


class Geography(str, Enum):
    GLOBAL = "global"
    LOCAL = "local"


class MapJobProgress(TypedDict):
    percent_complete: float
    step_name: str
    started: bool
    finished: bool
    description: Optional[str]


class DetailedMapLayerResponse(TypedDict):
    map_layer_id: str
    layer_name: str
    categories: List[str]
    author: str
    source: str
    url: str
    raw_url: str
    url_query_params: str
    legend: str
    minZoom: int
    maxZoom: int
    thumbnail: str
    coverage: str
    epsg: str
    resolution: List[int]
    citation: Optional[str]
    usage_notes: Optional[str]
    bands: Optional[str]
    additional_meta_data: Optional[str]
    description: Optional[str]
    format: str
    planting_design_id: int


class SimplifiedMapLayerResponse(TypedDict):
    map_layer_id: str
    layer_name: str
    categories: List[str]
    thumbnail: str
    format: str
