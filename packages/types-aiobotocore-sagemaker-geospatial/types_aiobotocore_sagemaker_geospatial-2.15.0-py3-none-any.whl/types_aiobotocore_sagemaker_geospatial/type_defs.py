"""
Type annotations for sagemaker-geospatial service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_geospatial/type_defs/)

Usage::

    ```python
    from types_aiobotocore_sagemaker_geospatial.type_defs import MultiPolygonGeometryInputOutputTypeDef

    data: MultiPolygonGeometryInputOutputTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence, Union

from aiobotocore.response import StreamingBody

from .literals import (
    AlgorithmNameGeoMosaicType,
    AlgorithmNameResamplingType,
    ComparisonOperatorType,
    DataCollectionTypeType,
    EarthObservationJobErrorTypeType,
    EarthObservationJobExportStatusType,
    EarthObservationJobStatusType,
    ExportErrorTypeType,
    GroupByType,
    OutputTypeType,
    PredefinedResolutionType,
    SortOrderType,
    TargetOptionsType,
    TemporalStatisticsType,
    VectorEnrichmentJobErrorTypeType,
    VectorEnrichmentJobExportErrorTypeType,
    VectorEnrichmentJobExportStatusType,
    VectorEnrichmentJobStatusType,
    VectorEnrichmentJobTypeType,
    ZonalStatisticsType,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 12):
    from typing import NotRequired
else:
    from typing_extensions import NotRequired
if sys.version_info >= (3, 12):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "MultiPolygonGeometryInputOutputTypeDef",
    "PolygonGeometryInputOutputTypeDef",
    "MultiPolygonGeometryInputTypeDef",
    "PolygonGeometryInputTypeDef",
    "AssetValueTypeDef",
    "CloudRemovalConfigInputOutputTypeDef",
    "CloudRemovalConfigInputTypeDef",
    "OperationTypeDef",
    "DeleteEarthObservationJobInputRequestTypeDef",
    "DeleteVectorEnrichmentJobInputRequestTypeDef",
    "EarthObservationJobErrorDetailsTypeDef",
    "EoCloudCoverInputTypeDef",
    "ResponseMetadataTypeDef",
    "ExportErrorDetailsOutputTypeDef",
    "ExportS3DataInputTypeDef",
    "VectorEnrichmentJobS3DataTypeDef",
    "FilterTypeDef",
    "GeoMosaicConfigInputOutputTypeDef",
    "GeoMosaicConfigInputTypeDef",
    "GeometryTypeDef",
    "GetEarthObservationJobInputRequestTypeDef",
    "OutputBandTypeDef",
    "GetRasterDataCollectionInputRequestTypeDef",
    "GetTileInputRequestTypeDef",
    "GetVectorEnrichmentJobInputRequestTypeDef",
    "VectorEnrichmentJobErrorDetailsTypeDef",
    "VectorEnrichmentJobExportErrorDetailsTypeDef",
    "PropertiesTypeDef",
    "TemporalStatisticsConfigInputOutputTypeDef",
    "ZonalStatisticsConfigInputOutputTypeDef",
    "TemporalStatisticsConfigInputTypeDef",
    "ZonalStatisticsConfigInputTypeDef",
    "LandsatCloudCoverLandInputTypeDef",
    "PaginatorConfigTypeDef",
    "ListEarthObservationJobInputRequestTypeDef",
    "ListEarthObservationJobOutputConfigTypeDef",
    "ListRasterDataCollectionsInputRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListVectorEnrichmentJobInputRequestTypeDef",
    "ListVectorEnrichmentJobOutputConfigTypeDef",
    "MapMatchingConfigTypeDef",
    "UserDefinedTypeDef",
    "PlatformInputTypeDef",
    "ViewOffNadirInputTypeDef",
    "ViewSunAzimuthInputTypeDef",
    "ViewSunElevationInputTypeDef",
    "TimeRangeFilterOutputTypeDef",
    "ReverseGeocodingConfigTypeDef",
    "StopEarthObservationJobInputRequestTypeDef",
    "StopVectorEnrichmentJobInputRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "AreaOfInterestGeometryOutputTypeDef",
    "AreaOfInterestGeometryTypeDef",
    "CustomIndicesInputOutputTypeDef",
    "CustomIndicesInputTypeDef",
    "GetTileOutputTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ExportErrorDetailsTypeDef",
    "OutputConfigInputTypeDef",
    "ExportVectorEnrichmentJobOutputConfigTypeDef",
    "VectorEnrichmentJobDataSourceConfigInputTypeDef",
    "GetRasterDataCollectionOutputTypeDef",
    "RasterDataCollectionMetadataTypeDef",
    "ItemSourceTypeDef",
    "ListEarthObservationJobInputListEarthObservationJobsPaginateTypeDef",
    "ListRasterDataCollectionsInputListRasterDataCollectionsPaginateTypeDef",
    "ListVectorEnrichmentJobInputListVectorEnrichmentJobsPaginateTypeDef",
    "ListEarthObservationJobOutputTypeDef",
    "ListVectorEnrichmentJobOutputTypeDef",
    "OutputResolutionResamplingInputTypeDef",
    "OutputResolutionStackInputTypeDef",
    "PropertyTypeDef",
    "VectorEnrichmentJobConfigTypeDef",
    "TimeRangeFilterInputTypeDef",
    "AreaOfInterestOutputTypeDef",
    "AreaOfInterestTypeDef",
    "BandMathConfigInputOutputTypeDef",
    "BandMathConfigInputTypeDef",
    "ExportEarthObservationJobInputRequestTypeDef",
    "ExportEarthObservationJobOutputTypeDef",
    "ExportVectorEnrichmentJobInputRequestTypeDef",
    "ExportVectorEnrichmentJobOutputTypeDef",
    "VectorEnrichmentJobInputConfigTypeDef",
    "ListRasterDataCollectionsOutputTypeDef",
    "SearchRasterDataCollectionOutputTypeDef",
    "ResamplingConfigInputOutputTypeDef",
    "ResamplingConfigInputTypeDef",
    "StackConfigInputOutputTypeDef",
    "StackConfigInputTypeDef",
    "PropertyFilterTypeDef",
    "GetVectorEnrichmentJobOutputTypeDef",
    "StartVectorEnrichmentJobInputRequestTypeDef",
    "StartVectorEnrichmentJobOutputTypeDef",
    "JobConfigInputOutputTypeDef",
    "JobConfigInputTypeDef",
    "PropertyFiltersOutputTypeDef",
    "PropertyFiltersTypeDef",
    "RasterDataCollectionQueryOutputTypeDef",
    "RasterDataCollectionQueryInputTypeDef",
    "RasterDataCollectionQueryWithBandFilterInputTypeDef",
    "InputConfigOutputTypeDef",
    "InputConfigInputTypeDef",
    "SearchRasterDataCollectionInputRequestTypeDef",
    "GetEarthObservationJobOutputTypeDef",
    "StartEarthObservationJobOutputTypeDef",
    "StartEarthObservationJobInputRequestTypeDef",
)

MultiPolygonGeometryInputOutputTypeDef = TypedDict(
    "MultiPolygonGeometryInputOutputTypeDef",
    {
        "Coordinates": List[List[List[List[float]]]],
    },
)
PolygonGeometryInputOutputTypeDef = TypedDict(
    "PolygonGeometryInputOutputTypeDef",
    {
        "Coordinates": List[List[List[float]]],
    },
)
MultiPolygonGeometryInputTypeDef = TypedDict(
    "MultiPolygonGeometryInputTypeDef",
    {
        "Coordinates": Sequence[Sequence[Sequence[Sequence[float]]]],
    },
)
PolygonGeometryInputTypeDef = TypedDict(
    "PolygonGeometryInputTypeDef",
    {
        "Coordinates": Sequence[Sequence[Sequence[float]]],
    },
)
AssetValueTypeDef = TypedDict(
    "AssetValueTypeDef",
    {
        "Href": NotRequired[str],
    },
)
CloudRemovalConfigInputOutputTypeDef = TypedDict(
    "CloudRemovalConfigInputOutputTypeDef",
    {
        "AlgorithmName": NotRequired[Literal["INTERPOLATION"]],
        "InterpolationValue": NotRequired[str],
        "TargetBands": NotRequired[List[str]],
    },
)
CloudRemovalConfigInputTypeDef = TypedDict(
    "CloudRemovalConfigInputTypeDef",
    {
        "AlgorithmName": NotRequired[Literal["INTERPOLATION"]],
        "InterpolationValue": NotRequired[str],
        "TargetBands": NotRequired[Sequence[str]],
    },
)
OperationTypeDef = TypedDict(
    "OperationTypeDef",
    {
        "Equation": str,
        "Name": str,
        "OutputType": NotRequired[OutputTypeType],
    },
)
DeleteEarthObservationJobInputRequestTypeDef = TypedDict(
    "DeleteEarthObservationJobInputRequestTypeDef",
    {
        "Arn": str,
    },
)
DeleteVectorEnrichmentJobInputRequestTypeDef = TypedDict(
    "DeleteVectorEnrichmentJobInputRequestTypeDef",
    {
        "Arn": str,
    },
)
EarthObservationJobErrorDetailsTypeDef = TypedDict(
    "EarthObservationJobErrorDetailsTypeDef",
    {
        "Message": NotRequired[str],
        "Type": NotRequired[EarthObservationJobErrorTypeType],
    },
)
EoCloudCoverInputTypeDef = TypedDict(
    "EoCloudCoverInputTypeDef",
    {
        "LowerBound": float,
        "UpperBound": float,
    },
)
ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
        "HostId": NotRequired[str],
    },
)
ExportErrorDetailsOutputTypeDef = TypedDict(
    "ExportErrorDetailsOutputTypeDef",
    {
        "Message": NotRequired[str],
        "Type": NotRequired[ExportErrorTypeType],
    },
)
ExportS3DataInputTypeDef = TypedDict(
    "ExportS3DataInputTypeDef",
    {
        "S3Uri": str,
        "KmsKeyId": NotRequired[str],
    },
)
VectorEnrichmentJobS3DataTypeDef = TypedDict(
    "VectorEnrichmentJobS3DataTypeDef",
    {
        "S3Uri": str,
        "KmsKeyId": NotRequired[str],
    },
)
FilterTypeDef = TypedDict(
    "FilterTypeDef",
    {
        "Name": str,
        "Type": str,
        "Maximum": NotRequired[float],
        "Minimum": NotRequired[float],
    },
)
GeoMosaicConfigInputOutputTypeDef = TypedDict(
    "GeoMosaicConfigInputOutputTypeDef",
    {
        "AlgorithmName": NotRequired[AlgorithmNameGeoMosaicType],
        "TargetBands": NotRequired[List[str]],
    },
)
GeoMosaicConfigInputTypeDef = TypedDict(
    "GeoMosaicConfigInputTypeDef",
    {
        "AlgorithmName": NotRequired[AlgorithmNameGeoMosaicType],
        "TargetBands": NotRequired[Sequence[str]],
    },
)
GeometryTypeDef = TypedDict(
    "GeometryTypeDef",
    {
        "Coordinates": List[List[List[float]]],
        "Type": str,
    },
)
GetEarthObservationJobInputRequestTypeDef = TypedDict(
    "GetEarthObservationJobInputRequestTypeDef",
    {
        "Arn": str,
    },
)
OutputBandTypeDef = TypedDict(
    "OutputBandTypeDef",
    {
        "BandName": str,
        "OutputDataType": OutputTypeType,
    },
)
GetRasterDataCollectionInputRequestTypeDef = TypedDict(
    "GetRasterDataCollectionInputRequestTypeDef",
    {
        "Arn": str,
    },
)
GetTileInputRequestTypeDef = TypedDict(
    "GetTileInputRequestTypeDef",
    {
        "Arn": str,
        "ImageAssets": Sequence[str],
        "Target": TargetOptionsType,
        "x": int,
        "y": int,
        "z": int,
        "ExecutionRoleArn": NotRequired[str],
        "ImageMask": NotRequired[bool],
        "OutputDataType": NotRequired[OutputTypeType],
        "OutputFormat": NotRequired[str],
        "PropertyFilters": NotRequired[str],
        "TimeRangeFilter": NotRequired[str],
    },
)
GetVectorEnrichmentJobInputRequestTypeDef = TypedDict(
    "GetVectorEnrichmentJobInputRequestTypeDef",
    {
        "Arn": str,
    },
)
VectorEnrichmentJobErrorDetailsTypeDef = TypedDict(
    "VectorEnrichmentJobErrorDetailsTypeDef",
    {
        "ErrorMessage": NotRequired[str],
        "ErrorType": NotRequired[VectorEnrichmentJobErrorTypeType],
    },
)
VectorEnrichmentJobExportErrorDetailsTypeDef = TypedDict(
    "VectorEnrichmentJobExportErrorDetailsTypeDef",
    {
        "Message": NotRequired[str],
        "Type": NotRequired[VectorEnrichmentJobExportErrorTypeType],
    },
)
PropertiesTypeDef = TypedDict(
    "PropertiesTypeDef",
    {
        "EoCloudCover": NotRequired[float],
        "LandsatCloudCoverLand": NotRequired[float],
        "Platform": NotRequired[str],
        "ViewOffNadir": NotRequired[float],
        "ViewSunAzimuth": NotRequired[float],
        "ViewSunElevation": NotRequired[float],
    },
)
TemporalStatisticsConfigInputOutputTypeDef = TypedDict(
    "TemporalStatisticsConfigInputOutputTypeDef",
    {
        "Statistics": List[TemporalStatisticsType],
        "GroupBy": NotRequired[GroupByType],
        "TargetBands": NotRequired[List[str]],
    },
)
ZonalStatisticsConfigInputOutputTypeDef = TypedDict(
    "ZonalStatisticsConfigInputOutputTypeDef",
    {
        "Statistics": List[ZonalStatisticsType],
        "ZoneS3Path": str,
        "TargetBands": NotRequired[List[str]],
        "ZoneS3PathKmsKeyId": NotRequired[str],
    },
)
TemporalStatisticsConfigInputTypeDef = TypedDict(
    "TemporalStatisticsConfigInputTypeDef",
    {
        "Statistics": Sequence[TemporalStatisticsType],
        "GroupBy": NotRequired[GroupByType],
        "TargetBands": NotRequired[Sequence[str]],
    },
)
ZonalStatisticsConfigInputTypeDef = TypedDict(
    "ZonalStatisticsConfigInputTypeDef",
    {
        "Statistics": Sequence[ZonalStatisticsType],
        "ZoneS3Path": str,
        "TargetBands": NotRequired[Sequence[str]],
        "ZoneS3PathKmsKeyId": NotRequired[str],
    },
)
LandsatCloudCoverLandInputTypeDef = TypedDict(
    "LandsatCloudCoverLandInputTypeDef",
    {
        "LowerBound": float,
        "UpperBound": float,
    },
)
PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": NotRequired[int],
        "PageSize": NotRequired[int],
        "StartingToken": NotRequired[str],
    },
)
ListEarthObservationJobInputRequestTypeDef = TypedDict(
    "ListEarthObservationJobInputRequestTypeDef",
    {
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
        "SortBy": NotRequired[str],
        "SortOrder": NotRequired[SortOrderType],
        "StatusEquals": NotRequired[EarthObservationJobStatusType],
    },
)
ListEarthObservationJobOutputConfigTypeDef = TypedDict(
    "ListEarthObservationJobOutputConfigTypeDef",
    {
        "Arn": str,
        "CreationTime": datetime,
        "DurationInSeconds": int,
        "Name": str,
        "OperationType": str,
        "Status": EarthObservationJobStatusType,
        "Tags": NotRequired[Dict[str, str]],
    },
)
ListRasterDataCollectionsInputRequestTypeDef = TypedDict(
    "ListRasterDataCollectionsInputRequestTypeDef",
    {
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)
ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)
ListVectorEnrichmentJobInputRequestTypeDef = TypedDict(
    "ListVectorEnrichmentJobInputRequestTypeDef",
    {
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
        "SortBy": NotRequired[str],
        "SortOrder": NotRequired[SortOrderType],
        "StatusEquals": NotRequired[str],
    },
)
ListVectorEnrichmentJobOutputConfigTypeDef = TypedDict(
    "ListVectorEnrichmentJobOutputConfigTypeDef",
    {
        "Arn": str,
        "CreationTime": datetime,
        "DurationInSeconds": int,
        "Name": str,
        "Status": VectorEnrichmentJobStatusType,
        "Type": VectorEnrichmentJobTypeType,
        "Tags": NotRequired[Dict[str, str]],
    },
)
MapMatchingConfigTypeDef = TypedDict(
    "MapMatchingConfigTypeDef",
    {
        "IdAttributeName": str,
        "TimestampAttributeName": str,
        "XAttributeName": str,
        "YAttributeName": str,
    },
)
UserDefinedTypeDef = TypedDict(
    "UserDefinedTypeDef",
    {
        "Unit": Literal["METERS"],
        "Value": float,
    },
)
PlatformInputTypeDef = TypedDict(
    "PlatformInputTypeDef",
    {
        "Value": str,
        "ComparisonOperator": NotRequired[ComparisonOperatorType],
    },
)
ViewOffNadirInputTypeDef = TypedDict(
    "ViewOffNadirInputTypeDef",
    {
        "LowerBound": float,
        "UpperBound": float,
    },
)
ViewSunAzimuthInputTypeDef = TypedDict(
    "ViewSunAzimuthInputTypeDef",
    {
        "LowerBound": float,
        "UpperBound": float,
    },
)
ViewSunElevationInputTypeDef = TypedDict(
    "ViewSunElevationInputTypeDef",
    {
        "LowerBound": float,
        "UpperBound": float,
    },
)
TimeRangeFilterOutputTypeDef = TypedDict(
    "TimeRangeFilterOutputTypeDef",
    {
        "EndTime": datetime,
        "StartTime": datetime,
    },
)
ReverseGeocodingConfigTypeDef = TypedDict(
    "ReverseGeocodingConfigTypeDef",
    {
        "XAttributeName": str,
        "YAttributeName": str,
    },
)
StopEarthObservationJobInputRequestTypeDef = TypedDict(
    "StopEarthObservationJobInputRequestTypeDef",
    {
        "Arn": str,
    },
)
StopVectorEnrichmentJobInputRequestTypeDef = TypedDict(
    "StopVectorEnrichmentJobInputRequestTypeDef",
    {
        "Arn": str,
    },
)
TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Mapping[str, str],
    },
)
TimestampTypeDef = Union[datetime, str]
UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)
AreaOfInterestGeometryOutputTypeDef = TypedDict(
    "AreaOfInterestGeometryOutputTypeDef",
    {
        "MultiPolygonGeometry": NotRequired[MultiPolygonGeometryInputOutputTypeDef],
        "PolygonGeometry": NotRequired[PolygonGeometryInputOutputTypeDef],
    },
)
AreaOfInterestGeometryTypeDef = TypedDict(
    "AreaOfInterestGeometryTypeDef",
    {
        "MultiPolygonGeometry": NotRequired[MultiPolygonGeometryInputTypeDef],
        "PolygonGeometry": NotRequired[PolygonGeometryInputTypeDef],
    },
)
CustomIndicesInputOutputTypeDef = TypedDict(
    "CustomIndicesInputOutputTypeDef",
    {
        "Operations": NotRequired[List[OperationTypeDef]],
    },
)
CustomIndicesInputTypeDef = TypedDict(
    "CustomIndicesInputTypeDef",
    {
        "Operations": NotRequired[Sequence[OperationTypeDef]],
    },
)
GetTileOutputTypeDef = TypedDict(
    "GetTileOutputTypeDef",
    {
        "BinaryFile": StreamingBody,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ExportErrorDetailsTypeDef = TypedDict(
    "ExportErrorDetailsTypeDef",
    {
        "ExportResults": NotRequired[ExportErrorDetailsOutputTypeDef],
        "ExportSourceImages": NotRequired[ExportErrorDetailsOutputTypeDef],
    },
)
OutputConfigInputTypeDef = TypedDict(
    "OutputConfigInputTypeDef",
    {
        "S3Data": ExportS3DataInputTypeDef,
    },
)
ExportVectorEnrichmentJobOutputConfigTypeDef = TypedDict(
    "ExportVectorEnrichmentJobOutputConfigTypeDef",
    {
        "S3Data": VectorEnrichmentJobS3DataTypeDef,
    },
)
VectorEnrichmentJobDataSourceConfigInputTypeDef = TypedDict(
    "VectorEnrichmentJobDataSourceConfigInputTypeDef",
    {
        "S3Data": NotRequired[VectorEnrichmentJobS3DataTypeDef],
    },
)
GetRasterDataCollectionOutputTypeDef = TypedDict(
    "GetRasterDataCollectionOutputTypeDef",
    {
        "Arn": str,
        "Description": str,
        "DescriptionPageUrl": str,
        "ImageSourceBands": List[str],
        "Name": str,
        "SupportedFilters": List[FilterTypeDef],
        "Tags": Dict[str, str],
        "Type": DataCollectionTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
RasterDataCollectionMetadataTypeDef = TypedDict(
    "RasterDataCollectionMetadataTypeDef",
    {
        "Arn": str,
        "Description": str,
        "Name": str,
        "SupportedFilters": List[FilterTypeDef],
        "Type": DataCollectionTypeType,
        "DescriptionPageUrl": NotRequired[str],
        "Tags": NotRequired[Dict[str, str]],
    },
)
ItemSourceTypeDef = TypedDict(
    "ItemSourceTypeDef",
    {
        "DateTime": datetime,
        "Geometry": GeometryTypeDef,
        "Id": str,
        "Assets": NotRequired[Dict[str, AssetValueTypeDef]],
        "Properties": NotRequired[PropertiesTypeDef],
    },
)
ListEarthObservationJobInputListEarthObservationJobsPaginateTypeDef = TypedDict(
    "ListEarthObservationJobInputListEarthObservationJobsPaginateTypeDef",
    {
        "SortBy": NotRequired[str],
        "SortOrder": NotRequired[SortOrderType],
        "StatusEquals": NotRequired[EarthObservationJobStatusType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListRasterDataCollectionsInputListRasterDataCollectionsPaginateTypeDef = TypedDict(
    "ListRasterDataCollectionsInputListRasterDataCollectionsPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListVectorEnrichmentJobInputListVectorEnrichmentJobsPaginateTypeDef = TypedDict(
    "ListVectorEnrichmentJobInputListVectorEnrichmentJobsPaginateTypeDef",
    {
        "SortBy": NotRequired[str],
        "SortOrder": NotRequired[SortOrderType],
        "StatusEquals": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListEarthObservationJobOutputTypeDef = TypedDict(
    "ListEarthObservationJobOutputTypeDef",
    {
        "EarthObservationJobSummaries": List[ListEarthObservationJobOutputConfigTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
ListVectorEnrichmentJobOutputTypeDef = TypedDict(
    "ListVectorEnrichmentJobOutputTypeDef",
    {
        "VectorEnrichmentJobSummaries": List[ListVectorEnrichmentJobOutputConfigTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
OutputResolutionResamplingInputTypeDef = TypedDict(
    "OutputResolutionResamplingInputTypeDef",
    {
        "UserDefined": UserDefinedTypeDef,
    },
)
OutputResolutionStackInputTypeDef = TypedDict(
    "OutputResolutionStackInputTypeDef",
    {
        "Predefined": NotRequired[PredefinedResolutionType],
        "UserDefined": NotRequired[UserDefinedTypeDef],
    },
)
PropertyTypeDef = TypedDict(
    "PropertyTypeDef",
    {
        "EoCloudCover": NotRequired[EoCloudCoverInputTypeDef],
        "LandsatCloudCoverLand": NotRequired[LandsatCloudCoverLandInputTypeDef],
        "Platform": NotRequired[PlatformInputTypeDef],
        "ViewOffNadir": NotRequired[ViewOffNadirInputTypeDef],
        "ViewSunAzimuth": NotRequired[ViewSunAzimuthInputTypeDef],
        "ViewSunElevation": NotRequired[ViewSunElevationInputTypeDef],
    },
)
VectorEnrichmentJobConfigTypeDef = TypedDict(
    "VectorEnrichmentJobConfigTypeDef",
    {
        "MapMatchingConfig": NotRequired[MapMatchingConfigTypeDef],
        "ReverseGeocodingConfig": NotRequired[ReverseGeocodingConfigTypeDef],
    },
)
TimeRangeFilterInputTypeDef = TypedDict(
    "TimeRangeFilterInputTypeDef",
    {
        "EndTime": TimestampTypeDef,
        "StartTime": TimestampTypeDef,
    },
)
AreaOfInterestOutputTypeDef = TypedDict(
    "AreaOfInterestOutputTypeDef",
    {
        "AreaOfInterestGeometry": NotRequired[AreaOfInterestGeometryOutputTypeDef],
    },
)
AreaOfInterestTypeDef = TypedDict(
    "AreaOfInterestTypeDef",
    {
        "AreaOfInterestGeometry": NotRequired[AreaOfInterestGeometryTypeDef],
    },
)
BandMathConfigInputOutputTypeDef = TypedDict(
    "BandMathConfigInputOutputTypeDef",
    {
        "CustomIndices": NotRequired[CustomIndicesInputOutputTypeDef],
        "PredefinedIndices": NotRequired[List[str]],
    },
)
BandMathConfigInputTypeDef = TypedDict(
    "BandMathConfigInputTypeDef",
    {
        "CustomIndices": NotRequired[CustomIndicesInputTypeDef],
        "PredefinedIndices": NotRequired[Sequence[str]],
    },
)
ExportEarthObservationJobInputRequestTypeDef = TypedDict(
    "ExportEarthObservationJobInputRequestTypeDef",
    {
        "Arn": str,
        "ExecutionRoleArn": str,
        "OutputConfig": OutputConfigInputTypeDef,
        "ClientToken": NotRequired[str],
        "ExportSourceImages": NotRequired[bool],
    },
)
ExportEarthObservationJobOutputTypeDef = TypedDict(
    "ExportEarthObservationJobOutputTypeDef",
    {
        "Arn": str,
        "CreationTime": datetime,
        "ExecutionRoleArn": str,
        "ExportSourceImages": bool,
        "ExportStatus": EarthObservationJobExportStatusType,
        "OutputConfig": OutputConfigInputTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ExportVectorEnrichmentJobInputRequestTypeDef = TypedDict(
    "ExportVectorEnrichmentJobInputRequestTypeDef",
    {
        "Arn": str,
        "ExecutionRoleArn": str,
        "OutputConfig": ExportVectorEnrichmentJobOutputConfigTypeDef,
        "ClientToken": NotRequired[str],
    },
)
ExportVectorEnrichmentJobOutputTypeDef = TypedDict(
    "ExportVectorEnrichmentJobOutputTypeDef",
    {
        "Arn": str,
        "CreationTime": datetime,
        "ExecutionRoleArn": str,
        "ExportStatus": VectorEnrichmentJobExportStatusType,
        "OutputConfig": ExportVectorEnrichmentJobOutputConfigTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
VectorEnrichmentJobInputConfigTypeDef = TypedDict(
    "VectorEnrichmentJobInputConfigTypeDef",
    {
        "DataSourceConfig": VectorEnrichmentJobDataSourceConfigInputTypeDef,
        "DocumentType": Literal["CSV"],
    },
)
ListRasterDataCollectionsOutputTypeDef = TypedDict(
    "ListRasterDataCollectionsOutputTypeDef",
    {
        "RasterDataCollectionSummaries": List[RasterDataCollectionMetadataTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
SearchRasterDataCollectionOutputTypeDef = TypedDict(
    "SearchRasterDataCollectionOutputTypeDef",
    {
        "ApproximateResultCount": int,
        "Items": List[ItemSourceTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
ResamplingConfigInputOutputTypeDef = TypedDict(
    "ResamplingConfigInputOutputTypeDef",
    {
        "OutputResolution": OutputResolutionResamplingInputTypeDef,
        "AlgorithmName": NotRequired[AlgorithmNameResamplingType],
        "TargetBands": NotRequired[List[str]],
    },
)
ResamplingConfigInputTypeDef = TypedDict(
    "ResamplingConfigInputTypeDef",
    {
        "OutputResolution": OutputResolutionResamplingInputTypeDef,
        "AlgorithmName": NotRequired[AlgorithmNameResamplingType],
        "TargetBands": NotRequired[Sequence[str]],
    },
)
StackConfigInputOutputTypeDef = TypedDict(
    "StackConfigInputOutputTypeDef",
    {
        "OutputResolution": NotRequired[OutputResolutionStackInputTypeDef],
        "TargetBands": NotRequired[List[str]],
    },
)
StackConfigInputTypeDef = TypedDict(
    "StackConfigInputTypeDef",
    {
        "OutputResolution": NotRequired[OutputResolutionStackInputTypeDef],
        "TargetBands": NotRequired[Sequence[str]],
    },
)
PropertyFilterTypeDef = TypedDict(
    "PropertyFilterTypeDef",
    {
        "Property": PropertyTypeDef,
    },
)
GetVectorEnrichmentJobOutputTypeDef = TypedDict(
    "GetVectorEnrichmentJobOutputTypeDef",
    {
        "Arn": str,
        "CreationTime": datetime,
        "DurationInSeconds": int,
        "ErrorDetails": VectorEnrichmentJobErrorDetailsTypeDef,
        "ExecutionRoleArn": str,
        "ExportErrorDetails": VectorEnrichmentJobExportErrorDetailsTypeDef,
        "ExportStatus": VectorEnrichmentJobExportStatusType,
        "InputConfig": VectorEnrichmentJobInputConfigTypeDef,
        "JobConfig": VectorEnrichmentJobConfigTypeDef,
        "KmsKeyId": str,
        "Name": str,
        "Status": VectorEnrichmentJobStatusType,
        "Tags": Dict[str, str],
        "Type": VectorEnrichmentJobTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
StartVectorEnrichmentJobInputRequestTypeDef = TypedDict(
    "StartVectorEnrichmentJobInputRequestTypeDef",
    {
        "ExecutionRoleArn": str,
        "InputConfig": VectorEnrichmentJobInputConfigTypeDef,
        "JobConfig": VectorEnrichmentJobConfigTypeDef,
        "Name": str,
        "ClientToken": NotRequired[str],
        "KmsKeyId": NotRequired[str],
        "Tags": NotRequired[Mapping[str, str]],
    },
)
StartVectorEnrichmentJobOutputTypeDef = TypedDict(
    "StartVectorEnrichmentJobOutputTypeDef",
    {
        "Arn": str,
        "CreationTime": datetime,
        "DurationInSeconds": int,
        "ExecutionRoleArn": str,
        "InputConfig": VectorEnrichmentJobInputConfigTypeDef,
        "JobConfig": VectorEnrichmentJobConfigTypeDef,
        "KmsKeyId": str,
        "Name": str,
        "Status": VectorEnrichmentJobStatusType,
        "Tags": Dict[str, str],
        "Type": VectorEnrichmentJobTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
JobConfigInputOutputTypeDef = TypedDict(
    "JobConfigInputOutputTypeDef",
    {
        "BandMathConfig": NotRequired[BandMathConfigInputOutputTypeDef],
        "CloudMaskingConfig": NotRequired[Dict[str, Any]],
        "CloudRemovalConfig": NotRequired[CloudRemovalConfigInputOutputTypeDef],
        "GeoMosaicConfig": NotRequired[GeoMosaicConfigInputOutputTypeDef],
        "LandCoverSegmentationConfig": NotRequired[Dict[str, Any]],
        "ResamplingConfig": NotRequired[ResamplingConfigInputOutputTypeDef],
        "StackConfig": NotRequired[StackConfigInputOutputTypeDef],
        "TemporalStatisticsConfig": NotRequired[TemporalStatisticsConfigInputOutputTypeDef],
        "ZonalStatisticsConfig": NotRequired[ZonalStatisticsConfigInputOutputTypeDef],
    },
)
JobConfigInputTypeDef = TypedDict(
    "JobConfigInputTypeDef",
    {
        "BandMathConfig": NotRequired[BandMathConfigInputTypeDef],
        "CloudMaskingConfig": NotRequired[Mapping[str, Any]],
        "CloudRemovalConfig": NotRequired[CloudRemovalConfigInputTypeDef],
        "GeoMosaicConfig": NotRequired[GeoMosaicConfigInputTypeDef],
        "LandCoverSegmentationConfig": NotRequired[Mapping[str, Any]],
        "ResamplingConfig": NotRequired[ResamplingConfigInputTypeDef],
        "StackConfig": NotRequired[StackConfigInputTypeDef],
        "TemporalStatisticsConfig": NotRequired[TemporalStatisticsConfigInputTypeDef],
        "ZonalStatisticsConfig": NotRequired[ZonalStatisticsConfigInputTypeDef],
    },
)
PropertyFiltersOutputTypeDef = TypedDict(
    "PropertyFiltersOutputTypeDef",
    {
        "LogicalOperator": NotRequired[Literal["AND"]],
        "Properties": NotRequired[List[PropertyFilterTypeDef]],
    },
)
PropertyFiltersTypeDef = TypedDict(
    "PropertyFiltersTypeDef",
    {
        "LogicalOperator": NotRequired[Literal["AND"]],
        "Properties": NotRequired[Sequence[PropertyFilterTypeDef]],
    },
)
RasterDataCollectionQueryOutputTypeDef = TypedDict(
    "RasterDataCollectionQueryOutputTypeDef",
    {
        "RasterDataCollectionArn": str,
        "RasterDataCollectionName": str,
        "TimeRangeFilter": TimeRangeFilterOutputTypeDef,
        "AreaOfInterest": NotRequired[AreaOfInterestOutputTypeDef],
        "PropertyFilters": NotRequired[PropertyFiltersOutputTypeDef],
    },
)
RasterDataCollectionQueryInputTypeDef = TypedDict(
    "RasterDataCollectionQueryInputTypeDef",
    {
        "RasterDataCollectionArn": str,
        "TimeRangeFilter": TimeRangeFilterInputTypeDef,
        "AreaOfInterest": NotRequired[AreaOfInterestTypeDef],
        "PropertyFilters": NotRequired[PropertyFiltersTypeDef],
    },
)
RasterDataCollectionQueryWithBandFilterInputTypeDef = TypedDict(
    "RasterDataCollectionQueryWithBandFilterInputTypeDef",
    {
        "TimeRangeFilter": TimeRangeFilterInputTypeDef,
        "AreaOfInterest": NotRequired[AreaOfInterestTypeDef],
        "BandFilter": NotRequired[Sequence[str]],
        "PropertyFilters": NotRequired[PropertyFiltersTypeDef],
    },
)
InputConfigOutputTypeDef = TypedDict(
    "InputConfigOutputTypeDef",
    {
        "PreviousEarthObservationJobArn": NotRequired[str],
        "RasterDataCollectionQuery": NotRequired[RasterDataCollectionQueryOutputTypeDef],
    },
)
InputConfigInputTypeDef = TypedDict(
    "InputConfigInputTypeDef",
    {
        "PreviousEarthObservationJobArn": NotRequired[str],
        "RasterDataCollectionQuery": NotRequired[RasterDataCollectionQueryInputTypeDef],
    },
)
SearchRasterDataCollectionInputRequestTypeDef = TypedDict(
    "SearchRasterDataCollectionInputRequestTypeDef",
    {
        "Arn": str,
        "RasterDataCollectionQuery": RasterDataCollectionQueryWithBandFilterInputTypeDef,
        "NextToken": NotRequired[str],
    },
)
GetEarthObservationJobOutputTypeDef = TypedDict(
    "GetEarthObservationJobOutputTypeDef",
    {
        "Arn": str,
        "CreationTime": datetime,
        "DurationInSeconds": int,
        "ErrorDetails": EarthObservationJobErrorDetailsTypeDef,
        "ExecutionRoleArn": str,
        "ExportErrorDetails": ExportErrorDetailsTypeDef,
        "ExportStatus": EarthObservationJobExportStatusType,
        "InputConfig": InputConfigOutputTypeDef,
        "JobConfig": JobConfigInputOutputTypeDef,
        "KmsKeyId": str,
        "Name": str,
        "OutputBands": List[OutputBandTypeDef],
        "Status": EarthObservationJobStatusType,
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
StartEarthObservationJobOutputTypeDef = TypedDict(
    "StartEarthObservationJobOutputTypeDef",
    {
        "Arn": str,
        "CreationTime": datetime,
        "DurationInSeconds": int,
        "ExecutionRoleArn": str,
        "InputConfig": InputConfigOutputTypeDef,
        "JobConfig": JobConfigInputOutputTypeDef,
        "KmsKeyId": str,
        "Name": str,
        "Status": EarthObservationJobStatusType,
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
StartEarthObservationJobInputRequestTypeDef = TypedDict(
    "StartEarthObservationJobInputRequestTypeDef",
    {
        "ExecutionRoleArn": str,
        "InputConfig": InputConfigInputTypeDef,
        "JobConfig": JobConfigInputTypeDef,
        "Name": str,
        "ClientToken": NotRequired[str],
        "KmsKeyId": NotRequired[str],
        "Tags": NotRequired[Mapping[str, str]],
    },
)
