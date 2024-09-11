"""
Type annotations for mediaconnect service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_mediaconnect.client import MediaConnectClient

    session = get_session()
    async with session.create_client("mediaconnect") as client:
        client: MediaConnectClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import (
    ListBridgesPaginator,
    ListEntitlementsPaginator,
    ListFlowsPaginator,
    ListGatewayInstancesPaginator,
    ListGatewaysPaginator,
    ListOfferingsPaginator,
    ListReservationsPaginator,
)
from .type_defs import (
    AddBridgeOutputsRequestRequestTypeDef,
    AddBridgeOutputsResponseTypeDef,
    AddBridgeSourcesRequestRequestTypeDef,
    AddBridgeSourcesResponseTypeDef,
    AddFlowMediaStreamsRequestRequestTypeDef,
    AddFlowMediaStreamsResponseTypeDef,
    AddFlowOutputsRequestRequestTypeDef,
    AddFlowOutputsResponseTypeDef,
    AddFlowSourcesRequestRequestTypeDef,
    AddFlowSourcesResponseTypeDef,
    AddFlowVpcInterfacesRequestRequestTypeDef,
    AddFlowVpcInterfacesResponseTypeDef,
    CreateBridgeRequestRequestTypeDef,
    CreateBridgeResponseTypeDef,
    CreateFlowRequestRequestTypeDef,
    CreateFlowResponseTypeDef,
    CreateGatewayRequestRequestTypeDef,
    CreateGatewayResponseTypeDef,
    DeleteBridgeRequestRequestTypeDef,
    DeleteBridgeResponseTypeDef,
    DeleteFlowRequestRequestTypeDef,
    DeleteFlowResponseTypeDef,
    DeleteGatewayRequestRequestTypeDef,
    DeleteGatewayResponseTypeDef,
    DeregisterGatewayInstanceRequestRequestTypeDef,
    DeregisterGatewayInstanceResponseTypeDef,
    DescribeBridgeRequestRequestTypeDef,
    DescribeBridgeResponseTypeDef,
    DescribeFlowRequestRequestTypeDef,
    DescribeFlowResponseTypeDef,
    DescribeFlowSourceMetadataRequestRequestTypeDef,
    DescribeFlowSourceMetadataResponseTypeDef,
    DescribeFlowSourceThumbnailRequestRequestTypeDef,
    DescribeFlowSourceThumbnailResponseTypeDef,
    DescribeGatewayInstanceRequestRequestTypeDef,
    DescribeGatewayInstanceResponseTypeDef,
    DescribeGatewayRequestRequestTypeDef,
    DescribeGatewayResponseTypeDef,
    DescribeOfferingRequestRequestTypeDef,
    DescribeOfferingResponseTypeDef,
    DescribeReservationRequestRequestTypeDef,
    DescribeReservationResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    GrantFlowEntitlementsRequestRequestTypeDef,
    GrantFlowEntitlementsResponseTypeDef,
    ListBridgesRequestRequestTypeDef,
    ListBridgesResponseTypeDef,
    ListEntitlementsRequestRequestTypeDef,
    ListEntitlementsResponseTypeDef,
    ListFlowsRequestRequestTypeDef,
    ListFlowsResponseTypeDef,
    ListGatewayInstancesRequestRequestTypeDef,
    ListGatewayInstancesResponseTypeDef,
    ListGatewaysRequestRequestTypeDef,
    ListGatewaysResponseTypeDef,
    ListOfferingsRequestRequestTypeDef,
    ListOfferingsResponseTypeDef,
    ListReservationsRequestRequestTypeDef,
    ListReservationsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PurchaseOfferingRequestRequestTypeDef,
    PurchaseOfferingResponseTypeDef,
    RemoveBridgeOutputRequestRequestTypeDef,
    RemoveBridgeOutputResponseTypeDef,
    RemoveBridgeSourceRequestRequestTypeDef,
    RemoveBridgeSourceResponseTypeDef,
    RemoveFlowMediaStreamRequestRequestTypeDef,
    RemoveFlowMediaStreamResponseTypeDef,
    RemoveFlowOutputRequestRequestTypeDef,
    RemoveFlowOutputResponseTypeDef,
    RemoveFlowSourceRequestRequestTypeDef,
    RemoveFlowSourceResponseTypeDef,
    RemoveFlowVpcInterfaceRequestRequestTypeDef,
    RemoveFlowVpcInterfaceResponseTypeDef,
    RevokeFlowEntitlementRequestRequestTypeDef,
    RevokeFlowEntitlementResponseTypeDef,
    StartFlowRequestRequestTypeDef,
    StartFlowResponseTypeDef,
    StopFlowRequestRequestTypeDef,
    StopFlowResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateBridgeOutputRequestRequestTypeDef,
    UpdateBridgeOutputResponseTypeDef,
    UpdateBridgeRequestRequestTypeDef,
    UpdateBridgeResponseTypeDef,
    UpdateBridgeSourceRequestRequestTypeDef,
    UpdateBridgeSourceResponseTypeDef,
    UpdateBridgeStateRequestRequestTypeDef,
    UpdateBridgeStateResponseTypeDef,
    UpdateFlowEntitlementRequestRequestTypeDef,
    UpdateFlowEntitlementResponseTypeDef,
    UpdateFlowMediaStreamRequestRequestTypeDef,
    UpdateFlowMediaStreamResponseTypeDef,
    UpdateFlowOutputRequestRequestTypeDef,
    UpdateFlowOutputResponseTypeDef,
    UpdateFlowRequestRequestTypeDef,
    UpdateFlowResponseTypeDef,
    UpdateFlowSourceRequestRequestTypeDef,
    UpdateFlowSourceResponseTypeDef,
    UpdateGatewayInstanceRequestRequestTypeDef,
    UpdateGatewayInstanceResponseTypeDef,
)
from .waiter import FlowActiveWaiter, FlowDeletedWaiter, FlowStandbyWaiter

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("MediaConnectClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AddFlowOutputs420Exception: Type[BotocoreClientError]
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    CreateBridge420Exception: Type[BotocoreClientError]
    CreateFlow420Exception: Type[BotocoreClientError]
    CreateGateway420Exception: Type[BotocoreClientError]
    ForbiddenException: Type[BotocoreClientError]
    GrantFlowEntitlements420Exception: Type[BotocoreClientError]
    InternalServerErrorException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]


class MediaConnectClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        MediaConnectClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#exceptions)
        """

    async def add_bridge_outputs(
        self, **kwargs: Unpack[AddBridgeOutputsRequestRequestTypeDef]
    ) -> AddBridgeOutputsResponseTypeDef:
        """
        Adds outputs to an existing bridge.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.add_bridge_outputs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#add_bridge_outputs)
        """

    async def add_bridge_sources(
        self, **kwargs: Unpack[AddBridgeSourcesRequestRequestTypeDef]
    ) -> AddBridgeSourcesResponseTypeDef:
        """
        Adds sources to an existing bridge.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.add_bridge_sources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#add_bridge_sources)
        """

    async def add_flow_media_streams(
        self, **kwargs: Unpack[AddFlowMediaStreamsRequestRequestTypeDef]
    ) -> AddFlowMediaStreamsResponseTypeDef:
        """
        Adds media streams to an existing flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.add_flow_media_streams)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#add_flow_media_streams)
        """

    async def add_flow_outputs(
        self, **kwargs: Unpack[AddFlowOutputsRequestRequestTypeDef]
    ) -> AddFlowOutputsResponseTypeDef:
        """
        Adds outputs to an existing flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.add_flow_outputs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#add_flow_outputs)
        """

    async def add_flow_sources(
        self, **kwargs: Unpack[AddFlowSourcesRequestRequestTypeDef]
    ) -> AddFlowSourcesResponseTypeDef:
        """
        Adds Sources to flow See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/mediaconnect-2018-11-14/AddFlowSources).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.add_flow_sources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#add_flow_sources)
        """

    async def add_flow_vpc_interfaces(
        self, **kwargs: Unpack[AddFlowVpcInterfacesRequestRequestTypeDef]
    ) -> AddFlowVpcInterfacesResponseTypeDef:
        """
        Adds VPC interfaces to flow See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/mediaconnect-2018-11-14/AddFlowVpcInterfaces).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.add_flow_vpc_interfaces)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#add_flow_vpc_interfaces)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#close)
        """

    async def create_bridge(
        self, **kwargs: Unpack[CreateBridgeRequestRequestTypeDef]
    ) -> CreateBridgeResponseTypeDef:
        """
        Creates a new bridge.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.create_bridge)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#create_bridge)
        """

    async def create_flow(
        self, **kwargs: Unpack[CreateFlowRequestRequestTypeDef]
    ) -> CreateFlowResponseTypeDef:
        """
        Creates a new flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.create_flow)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#create_flow)
        """

    async def create_gateway(
        self, **kwargs: Unpack[CreateGatewayRequestRequestTypeDef]
    ) -> CreateGatewayResponseTypeDef:
        """
        Creates a new gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.create_gateway)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#create_gateway)
        """

    async def delete_bridge(
        self, **kwargs: Unpack[DeleteBridgeRequestRequestTypeDef]
    ) -> DeleteBridgeResponseTypeDef:
        """
        Deletes a bridge.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.delete_bridge)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#delete_bridge)
        """

    async def delete_flow(
        self, **kwargs: Unpack[DeleteFlowRequestRequestTypeDef]
    ) -> DeleteFlowResponseTypeDef:
        """
        Deletes a flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.delete_flow)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#delete_flow)
        """

    async def delete_gateway(
        self, **kwargs: Unpack[DeleteGatewayRequestRequestTypeDef]
    ) -> DeleteGatewayResponseTypeDef:
        """
        Deletes a gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.delete_gateway)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#delete_gateway)
        """

    async def deregister_gateway_instance(
        self, **kwargs: Unpack[DeregisterGatewayInstanceRequestRequestTypeDef]
    ) -> DeregisterGatewayInstanceResponseTypeDef:
        """
        Deregisters an instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.deregister_gateway_instance)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#deregister_gateway_instance)
        """

    async def describe_bridge(
        self, **kwargs: Unpack[DescribeBridgeRequestRequestTypeDef]
    ) -> DescribeBridgeResponseTypeDef:
        """
        Displays the details of a bridge.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.describe_bridge)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#describe_bridge)
        """

    async def describe_flow(
        self, **kwargs: Unpack[DescribeFlowRequestRequestTypeDef]
    ) -> DescribeFlowResponseTypeDef:
        """
        Displays the details of a flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.describe_flow)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#describe_flow)
        """

    async def describe_flow_source_metadata(
        self, **kwargs: Unpack[DescribeFlowSourceMetadataRequestRequestTypeDef]
    ) -> DescribeFlowSourceMetadataResponseTypeDef:
        """
        Displays details of the flow's source stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.describe_flow_source_metadata)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#describe_flow_source_metadata)
        """

    async def describe_flow_source_thumbnail(
        self, **kwargs: Unpack[DescribeFlowSourceThumbnailRequestRequestTypeDef]
    ) -> DescribeFlowSourceThumbnailResponseTypeDef:
        """
        Displays the thumbnail details of a flow's source stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.describe_flow_source_thumbnail)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#describe_flow_source_thumbnail)
        """

    async def describe_gateway(
        self, **kwargs: Unpack[DescribeGatewayRequestRequestTypeDef]
    ) -> DescribeGatewayResponseTypeDef:
        """
        Displays the details of a gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.describe_gateway)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#describe_gateway)
        """

    async def describe_gateway_instance(
        self, **kwargs: Unpack[DescribeGatewayInstanceRequestRequestTypeDef]
    ) -> DescribeGatewayInstanceResponseTypeDef:
        """
        Displays the details of an instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.describe_gateway_instance)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#describe_gateway_instance)
        """

    async def describe_offering(
        self, **kwargs: Unpack[DescribeOfferingRequestRequestTypeDef]
    ) -> DescribeOfferingResponseTypeDef:
        """
        Displays the details of an offering.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.describe_offering)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#describe_offering)
        """

    async def describe_reservation(
        self, **kwargs: Unpack[DescribeReservationRequestRequestTypeDef]
    ) -> DescribeReservationResponseTypeDef:
        """
        Displays the details of a reservation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.describe_reservation)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#describe_reservation)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#generate_presigned_url)
        """

    async def grant_flow_entitlements(
        self, **kwargs: Unpack[GrantFlowEntitlementsRequestRequestTypeDef]
    ) -> GrantFlowEntitlementsResponseTypeDef:
        """
        Grants entitlements to an existing flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.grant_flow_entitlements)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#grant_flow_entitlements)
        """

    async def list_bridges(
        self, **kwargs: Unpack[ListBridgesRequestRequestTypeDef]
    ) -> ListBridgesResponseTypeDef:
        """
        Displays a list of bridges that are associated with this account and an
        optionally specified
        Arn.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.list_bridges)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#list_bridges)
        """

    async def list_entitlements(
        self, **kwargs: Unpack[ListEntitlementsRequestRequestTypeDef]
    ) -> ListEntitlementsResponseTypeDef:
        """
        Displays a list of all entitlements that have been granted to this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.list_entitlements)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#list_entitlements)
        """

    async def list_flows(
        self, **kwargs: Unpack[ListFlowsRequestRequestTypeDef]
    ) -> ListFlowsResponseTypeDef:
        """
        Displays a list of flows that are associated with this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.list_flows)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#list_flows)
        """

    async def list_gateway_instances(
        self, **kwargs: Unpack[ListGatewayInstancesRequestRequestTypeDef]
    ) -> ListGatewayInstancesResponseTypeDef:
        """
        Displays a list of instances associated with the AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.list_gateway_instances)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#list_gateway_instances)
        """

    async def list_gateways(
        self, **kwargs: Unpack[ListGatewaysRequestRequestTypeDef]
    ) -> ListGatewaysResponseTypeDef:
        """
        Displays a list of gateways that are associated with this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.list_gateways)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#list_gateways)
        """

    async def list_offerings(
        self, **kwargs: Unpack[ListOfferingsRequestRequestTypeDef]
    ) -> ListOfferingsResponseTypeDef:
        """
        Displays a list of all offerings that are available to this account in the
        current AWS
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.list_offerings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#list_offerings)
        """

    async def list_reservations(
        self, **kwargs: Unpack[ListReservationsRequestRequestTypeDef]
    ) -> ListReservationsResponseTypeDef:
        """
        Displays a list of all reservations that have been purchased by this account in
        the current AWS
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.list_reservations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#list_reservations)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        List all tags on an AWS Elemental MediaConnect resource See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/mediaconnect-2018-11-14/ListTagsForResource).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#list_tags_for_resource)
        """

    async def purchase_offering(
        self, **kwargs: Unpack[PurchaseOfferingRequestRequestTypeDef]
    ) -> PurchaseOfferingResponseTypeDef:
        """
        Submits a request to purchase an offering.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.purchase_offering)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#purchase_offering)
        """

    async def remove_bridge_output(
        self, **kwargs: Unpack[RemoveBridgeOutputRequestRequestTypeDef]
    ) -> RemoveBridgeOutputResponseTypeDef:
        """
        Removes an output from a bridge.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.remove_bridge_output)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#remove_bridge_output)
        """

    async def remove_bridge_source(
        self, **kwargs: Unpack[RemoveBridgeSourceRequestRequestTypeDef]
    ) -> RemoveBridgeSourceResponseTypeDef:
        """
        Removes a source from a bridge.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.remove_bridge_source)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#remove_bridge_source)
        """

    async def remove_flow_media_stream(
        self, **kwargs: Unpack[RemoveFlowMediaStreamRequestRequestTypeDef]
    ) -> RemoveFlowMediaStreamResponseTypeDef:
        """
        Removes a media stream from a flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.remove_flow_media_stream)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#remove_flow_media_stream)
        """

    async def remove_flow_output(
        self, **kwargs: Unpack[RemoveFlowOutputRequestRequestTypeDef]
    ) -> RemoveFlowOutputResponseTypeDef:
        """
        Removes an output from an existing flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.remove_flow_output)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#remove_flow_output)
        """

    async def remove_flow_source(
        self, **kwargs: Unpack[RemoveFlowSourceRequestRequestTypeDef]
    ) -> RemoveFlowSourceResponseTypeDef:
        """
        Removes a source from an existing flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.remove_flow_source)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#remove_flow_source)
        """

    async def remove_flow_vpc_interface(
        self, **kwargs: Unpack[RemoveFlowVpcInterfaceRequestRequestTypeDef]
    ) -> RemoveFlowVpcInterfaceResponseTypeDef:
        """
        Removes a VPC Interface from an existing flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.remove_flow_vpc_interface)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#remove_flow_vpc_interface)
        """

    async def revoke_flow_entitlement(
        self, **kwargs: Unpack[RevokeFlowEntitlementRequestRequestTypeDef]
    ) -> RevokeFlowEntitlementResponseTypeDef:
        """
        Revokes an entitlement from a flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.revoke_flow_entitlement)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#revoke_flow_entitlement)
        """

    async def start_flow(
        self, **kwargs: Unpack[StartFlowRequestRequestTypeDef]
    ) -> StartFlowResponseTypeDef:
        """
        Starts a flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.start_flow)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#start_flow)
        """

    async def stop_flow(
        self, **kwargs: Unpack[StopFlowRequestRequestTypeDef]
    ) -> StopFlowResponseTypeDef:
        """
        Stops a flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.stop_flow)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#stop_flow)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Associates the specified tags to a resource with the specified resourceArn.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes specified tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#untag_resource)
        """

    async def update_bridge(
        self, **kwargs: Unpack[UpdateBridgeRequestRequestTypeDef]
    ) -> UpdateBridgeResponseTypeDef:
        """
        Updates the bridge See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/mediaconnect-2018-11-14/UpdateBridge).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.update_bridge)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#update_bridge)
        """

    async def update_bridge_output(
        self, **kwargs: Unpack[UpdateBridgeOutputRequestRequestTypeDef]
    ) -> UpdateBridgeOutputResponseTypeDef:
        """
        Updates an existing bridge output.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.update_bridge_output)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#update_bridge_output)
        """

    async def update_bridge_source(
        self, **kwargs: Unpack[UpdateBridgeSourceRequestRequestTypeDef]
    ) -> UpdateBridgeSourceResponseTypeDef:
        """
        Updates an existing bridge source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.update_bridge_source)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#update_bridge_source)
        """

    async def update_bridge_state(
        self, **kwargs: Unpack[UpdateBridgeStateRequestRequestTypeDef]
    ) -> UpdateBridgeStateResponseTypeDef:
        """
        Updates the bridge state See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/mediaconnect-2018-11-14/UpdateBridgeState).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.update_bridge_state)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#update_bridge_state)
        """

    async def update_flow(
        self, **kwargs: Unpack[UpdateFlowRequestRequestTypeDef]
    ) -> UpdateFlowResponseTypeDef:
        """
        Updates flow See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/mediaconnect-2018-11-14/UpdateFlow).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.update_flow)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#update_flow)
        """

    async def update_flow_entitlement(
        self, **kwargs: Unpack[UpdateFlowEntitlementRequestRequestTypeDef]
    ) -> UpdateFlowEntitlementResponseTypeDef:
        """
        You can change an entitlement's description, subscribers, and encryption.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.update_flow_entitlement)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#update_flow_entitlement)
        """

    async def update_flow_media_stream(
        self, **kwargs: Unpack[UpdateFlowMediaStreamRequestRequestTypeDef]
    ) -> UpdateFlowMediaStreamResponseTypeDef:
        """
        Updates an existing media stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.update_flow_media_stream)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#update_flow_media_stream)
        """

    async def update_flow_output(
        self, **kwargs: Unpack[UpdateFlowOutputRequestRequestTypeDef]
    ) -> UpdateFlowOutputResponseTypeDef:
        """
        Updates an existing flow output.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.update_flow_output)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#update_flow_output)
        """

    async def update_flow_source(
        self, **kwargs: Unpack[UpdateFlowSourceRequestRequestTypeDef]
    ) -> UpdateFlowSourceResponseTypeDef:
        """
        Updates the source of a flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.update_flow_source)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#update_flow_source)
        """

    async def update_gateway_instance(
        self, **kwargs: Unpack[UpdateGatewayInstanceRequestRequestTypeDef]
    ) -> UpdateGatewayInstanceResponseTypeDef:
        """
        Updates the configuration of an existing Gateway Instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.update_gateway_instance)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#update_gateway_instance)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_bridges"]) -> ListBridgesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_entitlements"]
    ) -> ListEntitlementsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_flows"]) -> ListFlowsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_gateway_instances"]
    ) -> ListGatewayInstancesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_gateways"]) -> ListGatewaysPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_offerings"]) -> ListOfferingsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_reservations"]
    ) -> ListReservationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#get_paginator)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["flow_active"]) -> FlowActiveWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["flow_deleted"]) -> FlowDeletedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["flow_standby"]) -> FlowStandbyWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/#get_waiter)
        """

    async def __aenter__(self) -> "MediaConnectClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/client/)
        """
