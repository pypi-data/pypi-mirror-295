from types import FunctionType
from typing import Optional, List
import datetime

from geodesic.utils import DeferredImport
from boson.boson_core_pb2 import (
    DatasetInfoRequest,
    DatasetInfoResponse,
    PixelsRequest,
    RasterResponse,
    SearchRequest,
    SearchResponse,
    Properties,
)
from google.protobuf.timestamp_pb2 import Timestamp
from boson.features_pb2 import CollectionMsg, ExtentMsg, SpatialExtentMsg, TemporalExtentMsg
from boson.conversion import (
    search_request_to_kwargs,
    pixels_request_to_kwargs,
    feature_collection_to_proto,
    numpy_to_raster_response,
    dict_to_pagination,
    struct_to_dict,
)

gpd = DeferredImport("geopandas")
types_to_check = [dict, int, float, type(None)]
try:
    from geopandas import GeoDataFrame

    types_to_check.append(GeoDataFrame)
except ImportError:
    pass

types_to_check = tuple(types_to_check)


class BaseProvider:
    def __init__(
        self,
        name: str = "remote",
        alias: str = "Remote Boson Provider",
        description: str = "a remote Boson provider",
        license: str = "(unknown)",
        extent: Optional[dict] = None,
        search_func: Optional[FunctionType] = None,
        pixels_func: Optional[FunctionType] = None,
        queryables_func: Optional[FunctionType] = None,
        fields_func: Optional[FunctionType] = None,
        dataset_info_func: Optional[FunctionType] = None,
    ) -> None:
        self.name = name
        self.alias = alias
        self.description = description
        self.license = license
        self.extent = extent
        if self.extent is None:
            self.extent = {
                "spatial": {"bbox": [[-180.0, -70.0, 180.0, 70.0]]},
                "temporal": {"interval": [[None, None]]},
            }

        if search_func is not None and not callable(search_func):
            raise ValueError("search_func must be a callable or None")

        self.search_func = search_func

        if pixels_func is not None and not callable(pixels_func):
            raise ValueError("pixels_func must be a callable or None")
        self.pixels_func = pixels_func

        if queryables_func is not None and not callable(queryables_func):
            raise ValueError("queryables_func must be a callable or None")
        self.queryables_func = queryables_func

        if fields_func is not None and not callable(fields_func):
            raise ValueError("fields_func must be a callable or None")
        self.fields_func = fields_func

        if dataset_info_func is not None and not callable(dataset_info_func):
            raise ValueError("dataset_info_func must be a callable or None")
        self.dataset_info_func = dataset_info_func

        super().__init__()

    def dataset_info(self, req: DatasetInfoRequest) -> DatasetInfoResponse:
        provider_props = struct_to_dict(req.provider_properties)
        if self.dataset_info_func is not None:
            return self.dataset_info_func(provider_properties=provider_props)

        queryables = {}
        if self.queryables_func is not None:
            queryables_dict = self.queryables_func(provider_properties=provider_props)
            for collection, properties in queryables_dict.items():
                queryables[collection] = Properties(properties=properties)

        fields = {}
        if self.fields_func is not None:
            fields_dict = self.fields_func(provider_properties=provider_props)
            for collection, properties in fields_dict.items():
                fields[collection] = Properties(properties=properties)

        return DatasetInfoResponse(
            name=self.name,
            alias=self.alias,
            description=self.description,
            links=[],
            conforms_to=[
                "https://api.stacspec.org/v1.0.0/core",
                "https://api.stacspec.org/v1.0.0/item-search",
                "https://api.stacspec.org/v1.0.0/ogcapi-features",
                "https://api.stacspec.org/v1.0.0/collections",
                "http://www.opengis.net/spec/ogcapi-features-1/1.0/conf/core",
                "http://www.opengis.net/spec/ogcapi-features-1/1.0/conf/oas30",
                "http://www.opengis.net/spec/ogcapi-features-1/1.0/conf/geojson",
            ],
            overall_extent=self._extent_msg(),
            queryables=queryables,
            fields=fields,
            collections=[CollectionMsg(**self._collection())],
        )

    def _parse_interval(self, interval) -> List[Timestamp]:
        timestamps = []
        for x in interval:
            if x is None:
                timestamps.append(Timestamp())
            elif isinstance(x, datetime.datetime):
                t = Timestamp()
                t.FromDatetime(x)
                timestamps.append(t)
            else:
                timestamps.append(x)

        return timestamps

    def _extent_msg(self) -> ExtentMsg:
        bboxes = self.extent.get("bbox", [[-180, -70, 180, 70]])
        intervals = self.extent.get("interval", [[None, None]])

        bbox_msgs = [SpatialExtentMsg(bbox=bbox) for bbox in bboxes]
        interval_msgs = [
            TemporalExtentMsg(interval=self._parse_interval(interval)) for interval in intervals
        ]

        return ExtentMsg(spatial=bbox_msgs, temporal=interval_msgs)

    def _collection(self) -> dict:
        return {
            "version": "v1.0.0",
            "id": self.name,
            "title": self.alias,
            "description": self.description,
            "license": self.license,
            "extent": self._extent_msg(),
        }

    def pixels(self, request: PixelsRequest) -> RasterResponse:
        pixels_kwargs = pixels_request_to_kwargs(request)

        x = self.pixels_func(**pixels_kwargs)

        return numpy_to_raster_response(x)

    def search(self, request: SearchRequest) -> SearchResponse:
        search_kwargs = search_request_to_kwargs(request)
        res = self.search_func(**search_kwargs)
        pagination = {}

        if isinstance(res, types_to_check):
            fc = res
        elif len(res) == 2:
            fc, pagination = res

        # Check for a count response
        if request.count_only:
            if isinstance(fc, (int, float)):
                return SearchResponse(count=int(fc))
            return SearchResponse()

        fc_proto = feature_collection_to_proto(fc)
        return SearchResponse(
            feature_collection=fc_proto, pagination=dict_to_pagination(pagination)
        )
