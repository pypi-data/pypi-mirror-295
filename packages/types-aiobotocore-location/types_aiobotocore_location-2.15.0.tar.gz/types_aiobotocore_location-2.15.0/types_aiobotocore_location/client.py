"""
Type annotations for location service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_location.client import LocationServiceClient

    session = get_session()
    async with session.create_client("location") as client:
        client: LocationServiceClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import (
    ForecastGeofenceEventsPaginator,
    GetDevicePositionHistoryPaginator,
    ListDevicePositionsPaginator,
    ListGeofenceCollectionsPaginator,
    ListGeofencesPaginator,
    ListKeysPaginator,
    ListMapsPaginator,
    ListPlaceIndexesPaginator,
    ListRouteCalculatorsPaginator,
    ListTrackerConsumersPaginator,
    ListTrackersPaginator,
)
from .type_defs import (
    AssociateTrackerConsumerRequestRequestTypeDef,
    BatchDeleteDevicePositionHistoryRequestRequestTypeDef,
    BatchDeleteDevicePositionHistoryResponseTypeDef,
    BatchDeleteGeofenceRequestRequestTypeDef,
    BatchDeleteGeofenceResponseTypeDef,
    BatchEvaluateGeofencesRequestRequestTypeDef,
    BatchEvaluateGeofencesResponseTypeDef,
    BatchGetDevicePositionRequestRequestTypeDef,
    BatchGetDevicePositionResponseTypeDef,
    BatchPutGeofenceRequestRequestTypeDef,
    BatchPutGeofenceResponseTypeDef,
    BatchUpdateDevicePositionRequestRequestTypeDef,
    BatchUpdateDevicePositionResponseTypeDef,
    CalculateRouteMatrixRequestRequestTypeDef,
    CalculateRouteMatrixResponseTypeDef,
    CalculateRouteRequestRequestTypeDef,
    CalculateRouteResponseTypeDef,
    CreateGeofenceCollectionRequestRequestTypeDef,
    CreateGeofenceCollectionResponseTypeDef,
    CreateKeyRequestRequestTypeDef,
    CreateKeyResponseTypeDef,
    CreateMapRequestRequestTypeDef,
    CreateMapResponseTypeDef,
    CreatePlaceIndexRequestRequestTypeDef,
    CreatePlaceIndexResponseTypeDef,
    CreateRouteCalculatorRequestRequestTypeDef,
    CreateRouteCalculatorResponseTypeDef,
    CreateTrackerRequestRequestTypeDef,
    CreateTrackerResponseTypeDef,
    DeleteGeofenceCollectionRequestRequestTypeDef,
    DeleteKeyRequestRequestTypeDef,
    DeleteMapRequestRequestTypeDef,
    DeletePlaceIndexRequestRequestTypeDef,
    DeleteRouteCalculatorRequestRequestTypeDef,
    DeleteTrackerRequestRequestTypeDef,
    DescribeGeofenceCollectionRequestRequestTypeDef,
    DescribeGeofenceCollectionResponseTypeDef,
    DescribeKeyRequestRequestTypeDef,
    DescribeKeyResponseTypeDef,
    DescribeMapRequestRequestTypeDef,
    DescribeMapResponseTypeDef,
    DescribePlaceIndexRequestRequestTypeDef,
    DescribePlaceIndexResponseTypeDef,
    DescribeRouteCalculatorRequestRequestTypeDef,
    DescribeRouteCalculatorResponseTypeDef,
    DescribeTrackerRequestRequestTypeDef,
    DescribeTrackerResponseTypeDef,
    DisassociateTrackerConsumerRequestRequestTypeDef,
    ForecastGeofenceEventsRequestRequestTypeDef,
    ForecastGeofenceEventsResponseTypeDef,
    GetDevicePositionHistoryRequestRequestTypeDef,
    GetDevicePositionHistoryResponseTypeDef,
    GetDevicePositionRequestRequestTypeDef,
    GetDevicePositionResponseTypeDef,
    GetGeofenceRequestRequestTypeDef,
    GetGeofenceResponseTypeDef,
    GetMapGlyphsRequestRequestTypeDef,
    GetMapGlyphsResponseTypeDef,
    GetMapSpritesRequestRequestTypeDef,
    GetMapSpritesResponseTypeDef,
    GetMapStyleDescriptorRequestRequestTypeDef,
    GetMapStyleDescriptorResponseTypeDef,
    GetMapTileRequestRequestTypeDef,
    GetMapTileResponseTypeDef,
    GetPlaceRequestRequestTypeDef,
    GetPlaceResponseTypeDef,
    ListDevicePositionsRequestRequestTypeDef,
    ListDevicePositionsResponseTypeDef,
    ListGeofenceCollectionsRequestRequestTypeDef,
    ListGeofenceCollectionsResponseTypeDef,
    ListGeofencesRequestRequestTypeDef,
    ListGeofencesResponseTypeDef,
    ListKeysRequestRequestTypeDef,
    ListKeysResponseTypeDef,
    ListMapsRequestRequestTypeDef,
    ListMapsResponseTypeDef,
    ListPlaceIndexesRequestRequestTypeDef,
    ListPlaceIndexesResponseTypeDef,
    ListRouteCalculatorsRequestRequestTypeDef,
    ListRouteCalculatorsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTrackerConsumersRequestRequestTypeDef,
    ListTrackerConsumersResponseTypeDef,
    ListTrackersRequestRequestTypeDef,
    ListTrackersResponseTypeDef,
    PutGeofenceRequestRequestTypeDef,
    PutGeofenceResponseTypeDef,
    SearchPlaceIndexForPositionRequestRequestTypeDef,
    SearchPlaceIndexForPositionResponseTypeDef,
    SearchPlaceIndexForSuggestionsRequestRequestTypeDef,
    SearchPlaceIndexForSuggestionsResponseTypeDef,
    SearchPlaceIndexForTextRequestRequestTypeDef,
    SearchPlaceIndexForTextResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateGeofenceCollectionRequestRequestTypeDef,
    UpdateGeofenceCollectionResponseTypeDef,
    UpdateKeyRequestRequestTypeDef,
    UpdateKeyResponseTypeDef,
    UpdateMapRequestRequestTypeDef,
    UpdateMapResponseTypeDef,
    UpdatePlaceIndexRequestRequestTypeDef,
    UpdatePlaceIndexResponseTypeDef,
    UpdateRouteCalculatorRequestRequestTypeDef,
    UpdateRouteCalculatorResponseTypeDef,
    UpdateTrackerRequestRequestTypeDef,
    UpdateTrackerResponseTypeDef,
    VerifyDevicePositionRequestRequestTypeDef,
    VerifyDevicePositionResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("LocationServiceClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class LocationServiceClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        LocationServiceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#exceptions)
        """

    async def associate_tracker_consumer(
        self, **kwargs: Unpack[AssociateTrackerConsumerRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates an association between a geofence collection and a tracker resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.associate_tracker_consumer)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#associate_tracker_consumer)
        """

    async def batch_delete_device_position_history(
        self, **kwargs: Unpack[BatchDeleteDevicePositionHistoryRequestRequestTypeDef]
    ) -> BatchDeleteDevicePositionHistoryResponseTypeDef:
        """
        Deletes the position history of one or more devices from a tracker resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.batch_delete_device_position_history)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#batch_delete_device_position_history)
        """

    async def batch_delete_geofence(
        self, **kwargs: Unpack[BatchDeleteGeofenceRequestRequestTypeDef]
    ) -> BatchDeleteGeofenceResponseTypeDef:
        """
        Deletes a batch of geofences from a geofence collection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.batch_delete_geofence)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#batch_delete_geofence)
        """

    async def batch_evaluate_geofences(
        self, **kwargs: Unpack[BatchEvaluateGeofencesRequestRequestTypeDef]
    ) -> BatchEvaluateGeofencesResponseTypeDef:
        """
        Evaluates device positions against the geofence geometries from a given
        geofence
        collection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.batch_evaluate_geofences)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#batch_evaluate_geofences)
        """

    async def batch_get_device_position(
        self, **kwargs: Unpack[BatchGetDevicePositionRequestRequestTypeDef]
    ) -> BatchGetDevicePositionResponseTypeDef:
        """
        Lists the latest device positions for requested devices.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.batch_get_device_position)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#batch_get_device_position)
        """

    async def batch_put_geofence(
        self, **kwargs: Unpack[BatchPutGeofenceRequestRequestTypeDef]
    ) -> BatchPutGeofenceResponseTypeDef:
        """
        A batch request for storing geofence geometries into a given geofence
        collection, or updates the geometry of an existing geofence if a geofence ID is
        included in the
        request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.batch_put_geofence)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#batch_put_geofence)
        """

    async def batch_update_device_position(
        self, **kwargs: Unpack[BatchUpdateDevicePositionRequestRequestTypeDef]
    ) -> BatchUpdateDevicePositionResponseTypeDef:
        """
        Uploads position update data for one or more devices to a tracker resource (up
        to 10 devices per
        batch).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.batch_update_device_position)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#batch_update_device_position)
        """

    async def calculate_route(
        self, **kwargs: Unpack[CalculateRouteRequestRequestTypeDef]
    ) -> CalculateRouteResponseTypeDef:
        """
        [Calculates a
        route](https://docs.aws.amazon.com/location/latest/developerguide/calculate-route.html)
        given the following required parameters: `DeparturePosition` and
        `DestinationPosition`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.calculate_route)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#calculate_route)
        """

    async def calculate_route_matrix(
        self, **kwargs: Unpack[CalculateRouteMatrixRequestRequestTypeDef]
    ) -> CalculateRouteMatrixResponseTypeDef:
        """
        [Calculates a route
        matrix](https://docs.aws.amazon.com/location/latest/developerguide/calculate-route-matrix.html)
        given the following required parameters: `DeparturePositions` and
        `DestinationPositions`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.calculate_route_matrix)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#calculate_route_matrix)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#close)
        """

    async def create_geofence_collection(
        self, **kwargs: Unpack[CreateGeofenceCollectionRequestRequestTypeDef]
    ) -> CreateGeofenceCollectionResponseTypeDef:
        """
        Creates a geofence collection, which manages and stores geofences.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.create_geofence_collection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#create_geofence_collection)
        """

    async def create_key(
        self, **kwargs: Unpack[CreateKeyRequestRequestTypeDef]
    ) -> CreateKeyResponseTypeDef:
        """
        Creates an API key resource in your Amazon Web Services account, which lets you
        grant actions for Amazon Location resources to the API key
        bearer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.create_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#create_key)
        """

    async def create_map(
        self, **kwargs: Unpack[CreateMapRequestRequestTypeDef]
    ) -> CreateMapResponseTypeDef:
        """
        Creates a map resource in your Amazon Web Services account, which provides map
        tiles of different styles sourced from global location data
        providers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.create_map)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#create_map)
        """

    async def create_place_index(
        self, **kwargs: Unpack[CreatePlaceIndexRequestRequestTypeDef]
    ) -> CreatePlaceIndexResponseTypeDef:
        """
        Creates a place index resource in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.create_place_index)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#create_place_index)
        """

    async def create_route_calculator(
        self, **kwargs: Unpack[CreateRouteCalculatorRequestRequestTypeDef]
    ) -> CreateRouteCalculatorResponseTypeDef:
        """
        Creates a route calculator resource in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.create_route_calculator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#create_route_calculator)
        """

    async def create_tracker(
        self, **kwargs: Unpack[CreateTrackerRequestRequestTypeDef]
    ) -> CreateTrackerResponseTypeDef:
        """
        Creates a tracker resource in your Amazon Web Services account, which lets you
        retrieve current and historical location of
        devices.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.create_tracker)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#create_tracker)
        """

    async def delete_geofence_collection(
        self, **kwargs: Unpack[DeleteGeofenceCollectionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a geofence collection from your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.delete_geofence_collection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#delete_geofence_collection)
        """

    async def delete_key(self, **kwargs: Unpack[DeleteKeyRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes the specified API key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.delete_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#delete_key)
        """

    async def delete_map(self, **kwargs: Unpack[DeleteMapRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes a map resource from your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.delete_map)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#delete_map)
        """

    async def delete_place_index(
        self, **kwargs: Unpack[DeletePlaceIndexRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a place index resource from your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.delete_place_index)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#delete_place_index)
        """

    async def delete_route_calculator(
        self, **kwargs: Unpack[DeleteRouteCalculatorRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a route calculator resource from your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.delete_route_calculator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#delete_route_calculator)
        """

    async def delete_tracker(
        self, **kwargs: Unpack[DeleteTrackerRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a tracker resource from your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.delete_tracker)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#delete_tracker)
        """

    async def describe_geofence_collection(
        self, **kwargs: Unpack[DescribeGeofenceCollectionRequestRequestTypeDef]
    ) -> DescribeGeofenceCollectionResponseTypeDef:
        """
        Retrieves the geofence collection details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.describe_geofence_collection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#describe_geofence_collection)
        """

    async def describe_key(
        self, **kwargs: Unpack[DescribeKeyRequestRequestTypeDef]
    ) -> DescribeKeyResponseTypeDef:
        """
        Retrieves the API key resource details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.describe_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#describe_key)
        """

    async def describe_map(
        self, **kwargs: Unpack[DescribeMapRequestRequestTypeDef]
    ) -> DescribeMapResponseTypeDef:
        """
        Retrieves the map resource details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.describe_map)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#describe_map)
        """

    async def describe_place_index(
        self, **kwargs: Unpack[DescribePlaceIndexRequestRequestTypeDef]
    ) -> DescribePlaceIndexResponseTypeDef:
        """
        Retrieves the place index resource details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.describe_place_index)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#describe_place_index)
        """

    async def describe_route_calculator(
        self, **kwargs: Unpack[DescribeRouteCalculatorRequestRequestTypeDef]
    ) -> DescribeRouteCalculatorResponseTypeDef:
        """
        Retrieves the route calculator resource details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.describe_route_calculator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#describe_route_calculator)
        """

    async def describe_tracker(
        self, **kwargs: Unpack[DescribeTrackerRequestRequestTypeDef]
    ) -> DescribeTrackerResponseTypeDef:
        """
        Retrieves the tracker resource details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.describe_tracker)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#describe_tracker)
        """

    async def disassociate_tracker_consumer(
        self, **kwargs: Unpack[DisassociateTrackerConsumerRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes the association between a tracker resource and a geofence collection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.disassociate_tracker_consumer)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#disassociate_tracker_consumer)
        """

    async def forecast_geofence_events(
        self, **kwargs: Unpack[ForecastGeofenceEventsRequestRequestTypeDef]
    ) -> ForecastGeofenceEventsResponseTypeDef:
        """
        Evaluates device positions against geofence geometries from a given geofence
        collection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.forecast_geofence_events)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#forecast_geofence_events)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#generate_presigned_url)
        """

    async def get_device_position(
        self, **kwargs: Unpack[GetDevicePositionRequestRequestTypeDef]
    ) -> GetDevicePositionResponseTypeDef:
        """
        Retrieves a device's most recent position according to its sample time.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.get_device_position)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#get_device_position)
        """

    async def get_device_position_history(
        self, **kwargs: Unpack[GetDevicePositionHistoryRequestRequestTypeDef]
    ) -> GetDevicePositionHistoryResponseTypeDef:
        """
        Retrieves the device position history from a tracker resource within a
        specified range of
        time.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.get_device_position_history)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#get_device_position_history)
        """

    async def get_geofence(
        self, **kwargs: Unpack[GetGeofenceRequestRequestTypeDef]
    ) -> GetGeofenceResponseTypeDef:
        """
        Retrieves the geofence details from a geofence collection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.get_geofence)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#get_geofence)
        """

    async def get_map_glyphs(
        self, **kwargs: Unpack[GetMapGlyphsRequestRequestTypeDef]
    ) -> GetMapGlyphsResponseTypeDef:
        """
        Retrieves glyphs used to display labels on a map.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.get_map_glyphs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#get_map_glyphs)
        """

    async def get_map_sprites(
        self, **kwargs: Unpack[GetMapSpritesRequestRequestTypeDef]
    ) -> GetMapSpritesResponseTypeDef:
        """
        Retrieves the sprite sheet corresponding to a map resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.get_map_sprites)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#get_map_sprites)
        """

    async def get_map_style_descriptor(
        self, **kwargs: Unpack[GetMapStyleDescriptorRequestRequestTypeDef]
    ) -> GetMapStyleDescriptorResponseTypeDef:
        """
        Retrieves the map style descriptor from a map resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.get_map_style_descriptor)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#get_map_style_descriptor)
        """

    async def get_map_tile(
        self, **kwargs: Unpack[GetMapTileRequestRequestTypeDef]
    ) -> GetMapTileResponseTypeDef:
        """
        Retrieves a vector data tile from the map resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.get_map_tile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#get_map_tile)
        """

    async def get_place(
        self, **kwargs: Unpack[GetPlaceRequestRequestTypeDef]
    ) -> GetPlaceResponseTypeDef:
        """
        Finds a place by its unique ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.get_place)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#get_place)
        """

    async def list_device_positions(
        self, **kwargs: Unpack[ListDevicePositionsRequestRequestTypeDef]
    ) -> ListDevicePositionsResponseTypeDef:
        """
        A batch request to retrieve all device positions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.list_device_positions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#list_device_positions)
        """

    async def list_geofence_collections(
        self, **kwargs: Unpack[ListGeofenceCollectionsRequestRequestTypeDef]
    ) -> ListGeofenceCollectionsResponseTypeDef:
        """
        Lists geofence collections in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.list_geofence_collections)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#list_geofence_collections)
        """

    async def list_geofences(
        self, **kwargs: Unpack[ListGeofencesRequestRequestTypeDef]
    ) -> ListGeofencesResponseTypeDef:
        """
        Lists geofences stored in a given geofence collection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.list_geofences)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#list_geofences)
        """

    async def list_keys(
        self, **kwargs: Unpack[ListKeysRequestRequestTypeDef]
    ) -> ListKeysResponseTypeDef:
        """
        Lists API key resources in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.list_keys)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#list_keys)
        """

    async def list_maps(
        self, **kwargs: Unpack[ListMapsRequestRequestTypeDef]
    ) -> ListMapsResponseTypeDef:
        """
        Lists map resources in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.list_maps)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#list_maps)
        """

    async def list_place_indexes(
        self, **kwargs: Unpack[ListPlaceIndexesRequestRequestTypeDef]
    ) -> ListPlaceIndexesResponseTypeDef:
        """
        Lists place index resources in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.list_place_indexes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#list_place_indexes)
        """

    async def list_route_calculators(
        self, **kwargs: Unpack[ListRouteCalculatorsRequestRequestTypeDef]
    ) -> ListRouteCalculatorsResponseTypeDef:
        """
        Lists route calculator resources in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.list_route_calculators)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#list_route_calculators)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of tags that are applied to the specified Amazon Location
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#list_tags_for_resource)
        """

    async def list_tracker_consumers(
        self, **kwargs: Unpack[ListTrackerConsumersRequestRequestTypeDef]
    ) -> ListTrackerConsumersResponseTypeDef:
        """
        Lists geofence collections currently associated to the given tracker resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.list_tracker_consumers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#list_tracker_consumers)
        """

    async def list_trackers(
        self, **kwargs: Unpack[ListTrackersRequestRequestTypeDef]
    ) -> ListTrackersResponseTypeDef:
        """
        Lists tracker resources in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.list_trackers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#list_trackers)
        """

    async def put_geofence(
        self, **kwargs: Unpack[PutGeofenceRequestRequestTypeDef]
    ) -> PutGeofenceResponseTypeDef:
        """
        Stores a geofence geometry in a given geofence collection, or updates the
        geometry of an existing geofence if a geofence ID is included in the
        request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.put_geofence)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#put_geofence)
        """

    async def search_place_index_for_position(
        self, **kwargs: Unpack[SearchPlaceIndexForPositionRequestRequestTypeDef]
    ) -> SearchPlaceIndexForPositionResponseTypeDef:
        """
        Reverse geocodes a given coordinate and returns a legible address.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.search_place_index_for_position)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#search_place_index_for_position)
        """

    async def search_place_index_for_suggestions(
        self, **kwargs: Unpack[SearchPlaceIndexForSuggestionsRequestRequestTypeDef]
    ) -> SearchPlaceIndexForSuggestionsResponseTypeDef:
        """
        Generates suggestions for addresses and points of interest based on partial or
        misspelled free-form
        text.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.search_place_index_for_suggestions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#search_place_index_for_suggestions)
        """

    async def search_place_index_for_text(
        self, **kwargs: Unpack[SearchPlaceIndexForTextRequestRequestTypeDef]
    ) -> SearchPlaceIndexForTextResponseTypeDef:
        """
        Geocodes free-form text, such as an address, name, city, or region to allow you
        to search for Places or points of
        interest.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.search_place_index_for_text)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#search_place_index_for_text)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Assigns one or more tags (key-value pairs) to the specified Amazon Location
        Service
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes one or more tags from the specified Amazon Location resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#untag_resource)
        """

    async def update_geofence_collection(
        self, **kwargs: Unpack[UpdateGeofenceCollectionRequestRequestTypeDef]
    ) -> UpdateGeofenceCollectionResponseTypeDef:
        """
        Updates the specified properties of a given geofence collection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.update_geofence_collection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#update_geofence_collection)
        """

    async def update_key(
        self, **kwargs: Unpack[UpdateKeyRequestRequestTypeDef]
    ) -> UpdateKeyResponseTypeDef:
        """
        Updates the specified properties of a given API key resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.update_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#update_key)
        """

    async def update_map(
        self, **kwargs: Unpack[UpdateMapRequestRequestTypeDef]
    ) -> UpdateMapResponseTypeDef:
        """
        Updates the specified properties of a given map resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.update_map)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#update_map)
        """

    async def update_place_index(
        self, **kwargs: Unpack[UpdatePlaceIndexRequestRequestTypeDef]
    ) -> UpdatePlaceIndexResponseTypeDef:
        """
        Updates the specified properties of a given place index resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.update_place_index)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#update_place_index)
        """

    async def update_route_calculator(
        self, **kwargs: Unpack[UpdateRouteCalculatorRequestRequestTypeDef]
    ) -> UpdateRouteCalculatorResponseTypeDef:
        """
        Updates the specified properties for a given route calculator resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.update_route_calculator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#update_route_calculator)
        """

    async def update_tracker(
        self, **kwargs: Unpack[UpdateTrackerRequestRequestTypeDef]
    ) -> UpdateTrackerResponseTypeDef:
        """
        Updates the specified properties of a given tracker resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.update_tracker)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#update_tracker)
        """

    async def verify_device_position(
        self, **kwargs: Unpack[VerifyDevicePositionRequestRequestTypeDef]
    ) -> VerifyDevicePositionResponseTypeDef:
        """
        Verifies the integrity of the device's position by determining if it was
        reported behind a proxy, and by comparing it to an inferred position estimated
        based on the device's
        state.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.verify_device_position)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#verify_device_position)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["forecast_geofence_events"]
    ) -> ForecastGeofenceEventsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_device_position_history"]
    ) -> GetDevicePositionHistoryPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_device_positions"]
    ) -> ListDevicePositionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_geofence_collections"]
    ) -> ListGeofenceCollectionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_geofences"]) -> ListGeofencesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_keys"]) -> ListKeysPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_maps"]) -> ListMapsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_place_indexes"]
    ) -> ListPlaceIndexesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_route_calculators"]
    ) -> ListRouteCalculatorsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_tracker_consumers"]
    ) -> ListTrackerConsumersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_trackers"]) -> ListTrackersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#get_paginator)
        """

    async def __aenter__(self) -> "LocationServiceClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/)
        """
