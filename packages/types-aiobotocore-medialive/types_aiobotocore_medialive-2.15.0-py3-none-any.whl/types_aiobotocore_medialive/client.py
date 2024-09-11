"""
Type annotations for medialive service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_medialive.client import MediaLiveClient

    session = get_session()
    async with session.create_client("medialive") as client:
        client: MediaLiveClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import (
    DescribeSchedulePaginator,
    ListChannelsPaginator,
    ListCloudWatchAlarmTemplateGroupsPaginator,
    ListCloudWatchAlarmTemplatesPaginator,
    ListEventBridgeRuleTemplateGroupsPaginator,
    ListEventBridgeRuleTemplatesPaginator,
    ListInputDevicesPaginator,
    ListInputDeviceTransfersPaginator,
    ListInputSecurityGroupsPaginator,
    ListInputsPaginator,
    ListMultiplexesPaginator,
    ListMultiplexProgramsPaginator,
    ListOfferingsPaginator,
    ListReservationsPaginator,
    ListSignalMapsPaginator,
)
from .type_defs import (
    AcceptInputDeviceTransferRequestRequestTypeDef,
    BatchDeleteRequestRequestTypeDef,
    BatchDeleteResponseTypeDef,
    BatchStartRequestRequestTypeDef,
    BatchStartResponseTypeDef,
    BatchStopRequestRequestTypeDef,
    BatchStopResponseTypeDef,
    BatchUpdateScheduleRequestRequestTypeDef,
    BatchUpdateScheduleResponseTypeDef,
    CancelInputDeviceTransferRequestRequestTypeDef,
    ClaimDeviceRequestRequestTypeDef,
    CreateChannelRequestRequestTypeDef,
    CreateChannelResponseTypeDef,
    CreateCloudWatchAlarmTemplateGroupRequestRequestTypeDef,
    CreateCloudWatchAlarmTemplateGroupResponseTypeDef,
    CreateCloudWatchAlarmTemplateRequestRequestTypeDef,
    CreateCloudWatchAlarmTemplateResponseTypeDef,
    CreateEventBridgeRuleTemplateGroupRequestRequestTypeDef,
    CreateEventBridgeRuleTemplateGroupResponseTypeDef,
    CreateEventBridgeRuleTemplateRequestRequestTypeDef,
    CreateEventBridgeRuleTemplateResponseTypeDef,
    CreateInputRequestRequestTypeDef,
    CreateInputResponseTypeDef,
    CreateInputSecurityGroupRequestRequestTypeDef,
    CreateInputSecurityGroupResponseTypeDef,
    CreateMultiplexProgramRequestRequestTypeDef,
    CreateMultiplexProgramResponseTypeDef,
    CreateMultiplexRequestRequestTypeDef,
    CreateMultiplexResponseTypeDef,
    CreatePartnerInputRequestRequestTypeDef,
    CreatePartnerInputResponseTypeDef,
    CreateSignalMapRequestRequestTypeDef,
    CreateSignalMapResponseTypeDef,
    CreateTagsRequestRequestTypeDef,
    DeleteChannelRequestRequestTypeDef,
    DeleteChannelResponseTypeDef,
    DeleteCloudWatchAlarmTemplateGroupRequestRequestTypeDef,
    DeleteCloudWatchAlarmTemplateRequestRequestTypeDef,
    DeleteEventBridgeRuleTemplateGroupRequestRequestTypeDef,
    DeleteEventBridgeRuleTemplateRequestRequestTypeDef,
    DeleteInputRequestRequestTypeDef,
    DeleteInputSecurityGroupRequestRequestTypeDef,
    DeleteMultiplexProgramRequestRequestTypeDef,
    DeleteMultiplexProgramResponseTypeDef,
    DeleteMultiplexRequestRequestTypeDef,
    DeleteMultiplexResponseTypeDef,
    DeleteReservationRequestRequestTypeDef,
    DeleteReservationResponseTypeDef,
    DeleteScheduleRequestRequestTypeDef,
    DeleteSignalMapRequestRequestTypeDef,
    DeleteTagsRequestRequestTypeDef,
    DescribeAccountConfigurationResponseTypeDef,
    DescribeChannelRequestRequestTypeDef,
    DescribeChannelResponseTypeDef,
    DescribeInputDeviceRequestRequestTypeDef,
    DescribeInputDeviceResponseTypeDef,
    DescribeInputDeviceThumbnailRequestRequestTypeDef,
    DescribeInputDeviceThumbnailResponseTypeDef,
    DescribeInputRequestRequestTypeDef,
    DescribeInputResponseTypeDef,
    DescribeInputSecurityGroupRequestRequestTypeDef,
    DescribeInputSecurityGroupResponseTypeDef,
    DescribeMultiplexProgramRequestRequestTypeDef,
    DescribeMultiplexProgramResponseTypeDef,
    DescribeMultiplexRequestRequestTypeDef,
    DescribeMultiplexResponseTypeDef,
    DescribeOfferingRequestRequestTypeDef,
    DescribeOfferingResponseTypeDef,
    DescribeReservationRequestRequestTypeDef,
    DescribeReservationResponseTypeDef,
    DescribeScheduleRequestRequestTypeDef,
    DescribeScheduleResponseTypeDef,
    DescribeThumbnailsRequestRequestTypeDef,
    DescribeThumbnailsResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    GetCloudWatchAlarmTemplateGroupRequestRequestTypeDef,
    GetCloudWatchAlarmTemplateGroupResponseTypeDef,
    GetCloudWatchAlarmTemplateRequestRequestTypeDef,
    GetCloudWatchAlarmTemplateResponseTypeDef,
    GetEventBridgeRuleTemplateGroupRequestRequestTypeDef,
    GetEventBridgeRuleTemplateGroupResponseTypeDef,
    GetEventBridgeRuleTemplateRequestRequestTypeDef,
    GetEventBridgeRuleTemplateResponseTypeDef,
    GetSignalMapRequestRequestTypeDef,
    GetSignalMapResponseTypeDef,
    ListChannelsRequestRequestTypeDef,
    ListChannelsResponseTypeDef,
    ListCloudWatchAlarmTemplateGroupsRequestRequestTypeDef,
    ListCloudWatchAlarmTemplateGroupsResponseTypeDef,
    ListCloudWatchAlarmTemplatesRequestRequestTypeDef,
    ListCloudWatchAlarmTemplatesResponseTypeDef,
    ListEventBridgeRuleTemplateGroupsRequestRequestTypeDef,
    ListEventBridgeRuleTemplateGroupsResponseTypeDef,
    ListEventBridgeRuleTemplatesRequestRequestTypeDef,
    ListEventBridgeRuleTemplatesResponseTypeDef,
    ListInputDevicesRequestRequestTypeDef,
    ListInputDevicesResponseTypeDef,
    ListInputDeviceTransfersRequestRequestTypeDef,
    ListInputDeviceTransfersResponseTypeDef,
    ListInputSecurityGroupsRequestRequestTypeDef,
    ListInputSecurityGroupsResponseTypeDef,
    ListInputsRequestRequestTypeDef,
    ListInputsResponseTypeDef,
    ListMultiplexesRequestRequestTypeDef,
    ListMultiplexesResponseTypeDef,
    ListMultiplexProgramsRequestRequestTypeDef,
    ListMultiplexProgramsResponseTypeDef,
    ListOfferingsRequestRequestTypeDef,
    ListOfferingsResponseTypeDef,
    ListReservationsRequestRequestTypeDef,
    ListReservationsResponseTypeDef,
    ListSignalMapsRequestRequestTypeDef,
    ListSignalMapsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PurchaseOfferingRequestRequestTypeDef,
    PurchaseOfferingResponseTypeDef,
    RebootInputDeviceRequestRequestTypeDef,
    RejectInputDeviceTransferRequestRequestTypeDef,
    RestartChannelPipelinesRequestRequestTypeDef,
    RestartChannelPipelinesResponseTypeDef,
    StartChannelRequestRequestTypeDef,
    StartChannelResponseTypeDef,
    StartDeleteMonitorDeploymentRequestRequestTypeDef,
    StartDeleteMonitorDeploymentResponseTypeDef,
    StartInputDeviceMaintenanceWindowRequestRequestTypeDef,
    StartInputDeviceRequestRequestTypeDef,
    StartMonitorDeploymentRequestRequestTypeDef,
    StartMonitorDeploymentResponseTypeDef,
    StartMultiplexRequestRequestTypeDef,
    StartMultiplexResponseTypeDef,
    StartUpdateSignalMapRequestRequestTypeDef,
    StartUpdateSignalMapResponseTypeDef,
    StopChannelRequestRequestTypeDef,
    StopChannelResponseTypeDef,
    StopInputDeviceRequestRequestTypeDef,
    StopMultiplexRequestRequestTypeDef,
    StopMultiplexResponseTypeDef,
    TransferInputDeviceRequestRequestTypeDef,
    UpdateAccountConfigurationRequestRequestTypeDef,
    UpdateAccountConfigurationResponseTypeDef,
    UpdateChannelClassRequestRequestTypeDef,
    UpdateChannelClassResponseTypeDef,
    UpdateChannelRequestRequestTypeDef,
    UpdateChannelResponseTypeDef,
    UpdateCloudWatchAlarmTemplateGroupRequestRequestTypeDef,
    UpdateCloudWatchAlarmTemplateGroupResponseTypeDef,
    UpdateCloudWatchAlarmTemplateRequestRequestTypeDef,
    UpdateCloudWatchAlarmTemplateResponseTypeDef,
    UpdateEventBridgeRuleTemplateGroupRequestRequestTypeDef,
    UpdateEventBridgeRuleTemplateGroupResponseTypeDef,
    UpdateEventBridgeRuleTemplateRequestRequestTypeDef,
    UpdateEventBridgeRuleTemplateResponseTypeDef,
    UpdateInputDeviceRequestRequestTypeDef,
    UpdateInputDeviceResponseTypeDef,
    UpdateInputRequestRequestTypeDef,
    UpdateInputResponseTypeDef,
    UpdateInputSecurityGroupRequestRequestTypeDef,
    UpdateInputSecurityGroupResponseTypeDef,
    UpdateMultiplexProgramRequestRequestTypeDef,
    UpdateMultiplexProgramResponseTypeDef,
    UpdateMultiplexRequestRequestTypeDef,
    UpdateMultiplexResponseTypeDef,
    UpdateReservationRequestRequestTypeDef,
    UpdateReservationResponseTypeDef,
)
from .waiter import (
    ChannelCreatedWaiter,
    ChannelDeletedWaiter,
    ChannelRunningWaiter,
    ChannelStoppedWaiter,
    InputAttachedWaiter,
    InputDeletedWaiter,
    InputDetachedWaiter,
    MultiplexCreatedWaiter,
    MultiplexDeletedWaiter,
    MultiplexRunningWaiter,
    MultiplexStoppedWaiter,
    SignalMapCreatedWaiter,
    SignalMapMonitorDeletedWaiter,
    SignalMapMonitorDeployedWaiter,
    SignalMapUpdatedWaiter,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("MediaLiveClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    BadGatewayException: Type[BotocoreClientError]
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    ForbiddenException: Type[BotocoreClientError]
    GatewayTimeoutException: Type[BotocoreClientError]
    InternalServerErrorException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]
    UnprocessableEntityException: Type[BotocoreClientError]


class MediaLiveClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        MediaLiveClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#exceptions)
        """

    async def accept_input_device_transfer(
        self, **kwargs: Unpack[AcceptInputDeviceTransferRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Accept an incoming input device transfer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.accept_input_device_transfer)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#accept_input_device_transfer)
        """

    async def batch_delete(
        self, **kwargs: Unpack[BatchDeleteRequestRequestTypeDef]
    ) -> BatchDeleteResponseTypeDef:
        """
        Starts delete of resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.batch_delete)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#batch_delete)
        """

    async def batch_start(
        self, **kwargs: Unpack[BatchStartRequestRequestTypeDef]
    ) -> BatchStartResponseTypeDef:
        """
        Starts existing resources See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/medialive-2017-10-14/BatchStart).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.batch_start)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#batch_start)
        """

    async def batch_stop(
        self, **kwargs: Unpack[BatchStopRequestRequestTypeDef]
    ) -> BatchStopResponseTypeDef:
        """
        Stops running resources See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/medialive-2017-10-14/BatchStop).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.batch_stop)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#batch_stop)
        """

    async def batch_update_schedule(
        self, **kwargs: Unpack[BatchUpdateScheduleRequestRequestTypeDef]
    ) -> BatchUpdateScheduleResponseTypeDef:
        """
        Update a channel schedule See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/medialive-2017-10-14/BatchUpdateSchedule).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.batch_update_schedule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#batch_update_schedule)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#can_paginate)
        """

    async def cancel_input_device_transfer(
        self, **kwargs: Unpack[CancelInputDeviceTransferRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Cancel an input device transfer that you have requested.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.cancel_input_device_transfer)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#cancel_input_device_transfer)
        """

    async def claim_device(
        self, **kwargs: Unpack[ClaimDeviceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Send a request to claim an AWS Elemental device that you have purchased from a
        third-party
        vendor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.claim_device)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#claim_device)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#close)
        """

    async def create_channel(
        self, **kwargs: Unpack[CreateChannelRequestRequestTypeDef]
    ) -> CreateChannelResponseTypeDef:
        """
        Creates a new channel See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/medialive-2017-10-14/CreateChannel).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.create_channel)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#create_channel)
        """

    async def create_cloud_watch_alarm_template(
        self, **kwargs: Unpack[CreateCloudWatchAlarmTemplateRequestRequestTypeDef]
    ) -> CreateCloudWatchAlarmTemplateResponseTypeDef:
        """
        Creates a cloudwatch alarm template to dynamically generate cloudwatch metric
        alarms on targeted resource
        types.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.create_cloud_watch_alarm_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#create_cloud_watch_alarm_template)
        """

    async def create_cloud_watch_alarm_template_group(
        self, **kwargs: Unpack[CreateCloudWatchAlarmTemplateGroupRequestRequestTypeDef]
    ) -> CreateCloudWatchAlarmTemplateGroupResponseTypeDef:
        """
        Creates a cloudwatch alarm template group to group your cloudwatch alarm
        templates and to attach to signal maps for dynamically creating
        alarms.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.create_cloud_watch_alarm_template_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#create_cloud_watch_alarm_template_group)
        """

    async def create_event_bridge_rule_template(
        self, **kwargs: Unpack[CreateEventBridgeRuleTemplateRequestRequestTypeDef]
    ) -> CreateEventBridgeRuleTemplateResponseTypeDef:
        """
        Creates an eventbridge rule template to monitor events and send notifications
        to your targeted
        resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.create_event_bridge_rule_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#create_event_bridge_rule_template)
        """

    async def create_event_bridge_rule_template_group(
        self, **kwargs: Unpack[CreateEventBridgeRuleTemplateGroupRequestRequestTypeDef]
    ) -> CreateEventBridgeRuleTemplateGroupResponseTypeDef:
        """
        Creates an eventbridge rule template group to group your eventbridge rule
        templates and to attach to signal maps for dynamically creating notification
        rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.create_event_bridge_rule_template_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#create_event_bridge_rule_template_group)
        """

    async def create_input(
        self, **kwargs: Unpack[CreateInputRequestRequestTypeDef]
    ) -> CreateInputResponseTypeDef:
        """
        Create an input See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/medialive-2017-10-14/CreateInput).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.create_input)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#create_input)
        """

    async def create_input_security_group(
        self, **kwargs: Unpack[CreateInputSecurityGroupRequestRequestTypeDef]
    ) -> CreateInputSecurityGroupResponseTypeDef:
        """
        Creates a Input Security Group See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/medialive-2017-10-14/CreateInputSecurityGroup).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.create_input_security_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#create_input_security_group)
        """

    async def create_multiplex(
        self, **kwargs: Unpack[CreateMultiplexRequestRequestTypeDef]
    ) -> CreateMultiplexResponseTypeDef:
        """
        Create a new multiplex.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.create_multiplex)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#create_multiplex)
        """

    async def create_multiplex_program(
        self, **kwargs: Unpack[CreateMultiplexProgramRequestRequestTypeDef]
    ) -> CreateMultiplexProgramResponseTypeDef:
        """
        Create a new program in the multiplex.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.create_multiplex_program)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#create_multiplex_program)
        """

    async def create_partner_input(
        self, **kwargs: Unpack[CreatePartnerInputRequestRequestTypeDef]
    ) -> CreatePartnerInputResponseTypeDef:
        """
        Create a partner input See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/medialive-2017-10-14/CreatePartnerInput).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.create_partner_input)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#create_partner_input)
        """

    async def create_signal_map(
        self, **kwargs: Unpack[CreateSignalMapRequestRequestTypeDef]
    ) -> CreateSignalMapResponseTypeDef:
        """
        Initiates the creation of a new signal map.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.create_signal_map)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#create_signal_map)
        """

    async def create_tags(
        self, **kwargs: Unpack[CreateTagsRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Create tags for a resource See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/medialive-2017-10-14/CreateTags).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#create_tags)
        """

    async def delete_channel(
        self, **kwargs: Unpack[DeleteChannelRequestRequestTypeDef]
    ) -> DeleteChannelResponseTypeDef:
        """
        Starts deletion of channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.delete_channel)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#delete_channel)
        """

    async def delete_cloud_watch_alarm_template(
        self, **kwargs: Unpack[DeleteCloudWatchAlarmTemplateRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a cloudwatch alarm template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.delete_cloud_watch_alarm_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#delete_cloud_watch_alarm_template)
        """

    async def delete_cloud_watch_alarm_template_group(
        self, **kwargs: Unpack[DeleteCloudWatchAlarmTemplateGroupRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a cloudwatch alarm template group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.delete_cloud_watch_alarm_template_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#delete_cloud_watch_alarm_template_group)
        """

    async def delete_event_bridge_rule_template(
        self, **kwargs: Unpack[DeleteEventBridgeRuleTemplateRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an eventbridge rule template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.delete_event_bridge_rule_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#delete_event_bridge_rule_template)
        """

    async def delete_event_bridge_rule_template_group(
        self, **kwargs: Unpack[DeleteEventBridgeRuleTemplateGroupRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an eventbridge rule template group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.delete_event_bridge_rule_template_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#delete_event_bridge_rule_template_group)
        """

    async def delete_input(
        self, **kwargs: Unpack[DeleteInputRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the input end point See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/medialive-2017-10-14/DeleteInput).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.delete_input)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#delete_input)
        """

    async def delete_input_security_group(
        self, **kwargs: Unpack[DeleteInputSecurityGroupRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an Input Security Group See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/medialive-2017-10-14/DeleteInputSecurityGroup).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.delete_input_security_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#delete_input_security_group)
        """

    async def delete_multiplex(
        self, **kwargs: Unpack[DeleteMultiplexRequestRequestTypeDef]
    ) -> DeleteMultiplexResponseTypeDef:
        """
        Delete a multiplex.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.delete_multiplex)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#delete_multiplex)
        """

    async def delete_multiplex_program(
        self, **kwargs: Unpack[DeleteMultiplexProgramRequestRequestTypeDef]
    ) -> DeleteMultiplexProgramResponseTypeDef:
        """
        Delete a program from a multiplex.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.delete_multiplex_program)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#delete_multiplex_program)
        """

    async def delete_reservation(
        self, **kwargs: Unpack[DeleteReservationRequestRequestTypeDef]
    ) -> DeleteReservationResponseTypeDef:
        """
        Delete an expired reservation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.delete_reservation)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#delete_reservation)
        """

    async def delete_schedule(
        self, **kwargs: Unpack[DeleteScheduleRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Delete all schedule actions on a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.delete_schedule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#delete_schedule)
        """

    async def delete_signal_map(
        self, **kwargs: Unpack[DeleteSignalMapRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified signal map.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.delete_signal_map)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#delete_signal_map)
        """

    async def delete_tags(
        self, **kwargs: Unpack[DeleteTagsRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes tags for a resource See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/medialive-2017-10-14/DeleteTags).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.delete_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#delete_tags)
        """

    async def describe_account_configuration(self) -> DescribeAccountConfigurationResponseTypeDef:
        """
        Describe account configuration See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/medialive-2017-10-14/DescribeAccountConfiguration).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.describe_account_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#describe_account_configuration)
        """

    async def describe_channel(
        self, **kwargs: Unpack[DescribeChannelRequestRequestTypeDef]
    ) -> DescribeChannelResponseTypeDef:
        """
        Gets details about a channel See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/medialive-2017-10-14/DescribeChannel).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.describe_channel)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#describe_channel)
        """

    async def describe_input(
        self, **kwargs: Unpack[DescribeInputRequestRequestTypeDef]
    ) -> DescribeInputResponseTypeDef:
        """
        Produces details about an input See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/medialive-2017-10-14/DescribeInput).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.describe_input)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#describe_input)
        """

    async def describe_input_device(
        self, **kwargs: Unpack[DescribeInputDeviceRequestRequestTypeDef]
    ) -> DescribeInputDeviceResponseTypeDef:
        """
        Gets the details for the input device See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/medialive-2017-10-14/DescribeInputDevice).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.describe_input_device)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#describe_input_device)
        """

    async def describe_input_device_thumbnail(
        self, **kwargs: Unpack[DescribeInputDeviceThumbnailRequestRequestTypeDef]
    ) -> DescribeInputDeviceThumbnailResponseTypeDef:
        """
        Get the latest thumbnail data for the input device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.describe_input_device_thumbnail)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#describe_input_device_thumbnail)
        """

    async def describe_input_security_group(
        self, **kwargs: Unpack[DescribeInputSecurityGroupRequestRequestTypeDef]
    ) -> DescribeInputSecurityGroupResponseTypeDef:
        """
        Produces a summary of an Input Security Group See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/medialive-2017-10-14/DescribeInputSecurityGroup).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.describe_input_security_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#describe_input_security_group)
        """

    async def describe_multiplex(
        self, **kwargs: Unpack[DescribeMultiplexRequestRequestTypeDef]
    ) -> DescribeMultiplexResponseTypeDef:
        """
        Gets details about a multiplex.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.describe_multiplex)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#describe_multiplex)
        """

    async def describe_multiplex_program(
        self, **kwargs: Unpack[DescribeMultiplexProgramRequestRequestTypeDef]
    ) -> DescribeMultiplexProgramResponseTypeDef:
        """
        Get the details for a program in a multiplex.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.describe_multiplex_program)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#describe_multiplex_program)
        """

    async def describe_offering(
        self, **kwargs: Unpack[DescribeOfferingRequestRequestTypeDef]
    ) -> DescribeOfferingResponseTypeDef:
        """
        Get details for an offering.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.describe_offering)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#describe_offering)
        """

    async def describe_reservation(
        self, **kwargs: Unpack[DescribeReservationRequestRequestTypeDef]
    ) -> DescribeReservationResponseTypeDef:
        """
        Get details for a reservation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.describe_reservation)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#describe_reservation)
        """

    async def describe_schedule(
        self, **kwargs: Unpack[DescribeScheduleRequestRequestTypeDef]
    ) -> DescribeScheduleResponseTypeDef:
        """
        Get a channel schedule See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/medialive-2017-10-14/DescribeSchedule).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.describe_schedule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#describe_schedule)
        """

    async def describe_thumbnails(
        self, **kwargs: Unpack[DescribeThumbnailsRequestRequestTypeDef]
    ) -> DescribeThumbnailsResponseTypeDef:
        """
        Describe the latest thumbnails data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.describe_thumbnails)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#describe_thumbnails)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#generate_presigned_url)
        """

    async def get_cloud_watch_alarm_template(
        self, **kwargs: Unpack[GetCloudWatchAlarmTemplateRequestRequestTypeDef]
    ) -> GetCloudWatchAlarmTemplateResponseTypeDef:
        """
        Retrieves the specified cloudwatch alarm template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.get_cloud_watch_alarm_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#get_cloud_watch_alarm_template)
        """

    async def get_cloud_watch_alarm_template_group(
        self, **kwargs: Unpack[GetCloudWatchAlarmTemplateGroupRequestRequestTypeDef]
    ) -> GetCloudWatchAlarmTemplateGroupResponseTypeDef:
        """
        Retrieves the specified cloudwatch alarm template group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.get_cloud_watch_alarm_template_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#get_cloud_watch_alarm_template_group)
        """

    async def get_event_bridge_rule_template(
        self, **kwargs: Unpack[GetEventBridgeRuleTemplateRequestRequestTypeDef]
    ) -> GetEventBridgeRuleTemplateResponseTypeDef:
        """
        Retrieves the specified eventbridge rule template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.get_event_bridge_rule_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#get_event_bridge_rule_template)
        """

    async def get_event_bridge_rule_template_group(
        self, **kwargs: Unpack[GetEventBridgeRuleTemplateGroupRequestRequestTypeDef]
    ) -> GetEventBridgeRuleTemplateGroupResponseTypeDef:
        """
        Retrieves the specified eventbridge rule template group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.get_event_bridge_rule_template_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#get_event_bridge_rule_template_group)
        """

    async def get_signal_map(
        self, **kwargs: Unpack[GetSignalMapRequestRequestTypeDef]
    ) -> GetSignalMapResponseTypeDef:
        """
        Retrieves the specified signal map.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.get_signal_map)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#get_signal_map)
        """

    async def list_channels(
        self, **kwargs: Unpack[ListChannelsRequestRequestTypeDef]
    ) -> ListChannelsResponseTypeDef:
        """
        Produces list of channels that have been created See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/medialive-2017-10-14/ListChannels).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.list_channels)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#list_channels)
        """

    async def list_cloud_watch_alarm_template_groups(
        self, **kwargs: Unpack[ListCloudWatchAlarmTemplateGroupsRequestRequestTypeDef]
    ) -> ListCloudWatchAlarmTemplateGroupsResponseTypeDef:
        """
        Lists cloudwatch alarm template groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.list_cloud_watch_alarm_template_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#list_cloud_watch_alarm_template_groups)
        """

    async def list_cloud_watch_alarm_templates(
        self, **kwargs: Unpack[ListCloudWatchAlarmTemplatesRequestRequestTypeDef]
    ) -> ListCloudWatchAlarmTemplatesResponseTypeDef:
        """
        Lists cloudwatch alarm templates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.list_cloud_watch_alarm_templates)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#list_cloud_watch_alarm_templates)
        """

    async def list_event_bridge_rule_template_groups(
        self, **kwargs: Unpack[ListEventBridgeRuleTemplateGroupsRequestRequestTypeDef]
    ) -> ListEventBridgeRuleTemplateGroupsResponseTypeDef:
        """
        Lists eventbridge rule template groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.list_event_bridge_rule_template_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#list_event_bridge_rule_template_groups)
        """

    async def list_event_bridge_rule_templates(
        self, **kwargs: Unpack[ListEventBridgeRuleTemplatesRequestRequestTypeDef]
    ) -> ListEventBridgeRuleTemplatesResponseTypeDef:
        """
        Lists eventbridge rule templates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.list_event_bridge_rule_templates)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#list_event_bridge_rule_templates)
        """

    async def list_input_device_transfers(
        self, **kwargs: Unpack[ListInputDeviceTransfersRequestRequestTypeDef]
    ) -> ListInputDeviceTransfersResponseTypeDef:
        """
        List input devices that are currently being transferred.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.list_input_device_transfers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#list_input_device_transfers)
        """

    async def list_input_devices(
        self, **kwargs: Unpack[ListInputDevicesRequestRequestTypeDef]
    ) -> ListInputDevicesResponseTypeDef:
        """
        List input devices See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/medialive-2017-10-14/ListInputDevices).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.list_input_devices)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#list_input_devices)
        """

    async def list_input_security_groups(
        self, **kwargs: Unpack[ListInputSecurityGroupsRequestRequestTypeDef]
    ) -> ListInputSecurityGroupsResponseTypeDef:
        """
        Produces a list of Input Security Groups for an account See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/medialive-2017-10-14/ListInputSecurityGroups).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.list_input_security_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#list_input_security_groups)
        """

    async def list_inputs(
        self, **kwargs: Unpack[ListInputsRequestRequestTypeDef]
    ) -> ListInputsResponseTypeDef:
        """
        Produces list of inputs that have been created See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/medialive-2017-10-14/ListInputs).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.list_inputs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#list_inputs)
        """

    async def list_multiplex_programs(
        self, **kwargs: Unpack[ListMultiplexProgramsRequestRequestTypeDef]
    ) -> ListMultiplexProgramsResponseTypeDef:
        """
        List the programs that currently exist for a specific multiplex.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.list_multiplex_programs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#list_multiplex_programs)
        """

    async def list_multiplexes(
        self, **kwargs: Unpack[ListMultiplexesRequestRequestTypeDef]
    ) -> ListMultiplexesResponseTypeDef:
        """
        Retrieve a list of the existing multiplexes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.list_multiplexes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#list_multiplexes)
        """

    async def list_offerings(
        self, **kwargs: Unpack[ListOfferingsRequestRequestTypeDef]
    ) -> ListOfferingsResponseTypeDef:
        """
        List offerings available for purchase.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.list_offerings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#list_offerings)
        """

    async def list_reservations(
        self, **kwargs: Unpack[ListReservationsRequestRequestTypeDef]
    ) -> ListReservationsResponseTypeDef:
        """
        List purchased reservations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.list_reservations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#list_reservations)
        """

    async def list_signal_maps(
        self, **kwargs: Unpack[ListSignalMapsRequestRequestTypeDef]
    ) -> ListSignalMapsResponseTypeDef:
        """
        Lists signal maps.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.list_signal_maps)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#list_signal_maps)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Produces list of tags that have been created for a resource See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/medialive-2017-10-14/ListTagsForResource).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#list_tags_for_resource)
        """

    async def purchase_offering(
        self, **kwargs: Unpack[PurchaseOfferingRequestRequestTypeDef]
    ) -> PurchaseOfferingResponseTypeDef:
        """
        Purchase an offering and create a reservation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.purchase_offering)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#purchase_offering)
        """

    async def reboot_input_device(
        self, **kwargs: Unpack[RebootInputDeviceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Send a reboot command to the specified input device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.reboot_input_device)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#reboot_input_device)
        """

    async def reject_input_device_transfer(
        self, **kwargs: Unpack[RejectInputDeviceTransferRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Reject the transfer of the specified input device to your AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.reject_input_device_transfer)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#reject_input_device_transfer)
        """

    async def restart_channel_pipelines(
        self, **kwargs: Unpack[RestartChannelPipelinesRequestRequestTypeDef]
    ) -> RestartChannelPipelinesResponseTypeDef:
        """
        Restart pipelines in one channel that is currently running.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.restart_channel_pipelines)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#restart_channel_pipelines)
        """

    async def start_channel(
        self, **kwargs: Unpack[StartChannelRequestRequestTypeDef]
    ) -> StartChannelResponseTypeDef:
        """
        Starts an existing channel See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/medialive-2017-10-14/StartChannel).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.start_channel)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#start_channel)
        """

    async def start_delete_monitor_deployment(
        self, **kwargs: Unpack[StartDeleteMonitorDeploymentRequestRequestTypeDef]
    ) -> StartDeleteMonitorDeploymentResponseTypeDef:
        """
        Initiates a deployment to delete the monitor of the specified signal map.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.start_delete_monitor_deployment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#start_delete_monitor_deployment)
        """

    async def start_input_device(
        self, **kwargs: Unpack[StartInputDeviceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Start an input device that is attached to a MediaConnect flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.start_input_device)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#start_input_device)
        """

    async def start_input_device_maintenance_window(
        self, **kwargs: Unpack[StartInputDeviceMaintenanceWindowRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Start a maintenance window for the specified input device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.start_input_device_maintenance_window)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#start_input_device_maintenance_window)
        """

    async def start_monitor_deployment(
        self, **kwargs: Unpack[StartMonitorDeploymentRequestRequestTypeDef]
    ) -> StartMonitorDeploymentResponseTypeDef:
        """
        Initiates a deployment to deploy the latest monitor of the specified signal map.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.start_monitor_deployment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#start_monitor_deployment)
        """

    async def start_multiplex(
        self, **kwargs: Unpack[StartMultiplexRequestRequestTypeDef]
    ) -> StartMultiplexResponseTypeDef:
        """
        Start (run) the multiplex.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.start_multiplex)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#start_multiplex)
        """

    async def start_update_signal_map(
        self, **kwargs: Unpack[StartUpdateSignalMapRequestRequestTypeDef]
    ) -> StartUpdateSignalMapResponseTypeDef:
        """
        Initiates an update for the specified signal map.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.start_update_signal_map)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#start_update_signal_map)
        """

    async def stop_channel(
        self, **kwargs: Unpack[StopChannelRequestRequestTypeDef]
    ) -> StopChannelResponseTypeDef:
        """
        Stops a running channel See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/medialive-2017-10-14/StopChannel).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.stop_channel)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#stop_channel)
        """

    async def stop_input_device(
        self, **kwargs: Unpack[StopInputDeviceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Stop an input device that is attached to a MediaConnect flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.stop_input_device)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#stop_input_device)
        """

    async def stop_multiplex(
        self, **kwargs: Unpack[StopMultiplexRequestRequestTypeDef]
    ) -> StopMultiplexResponseTypeDef:
        """
        Stops a running multiplex.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.stop_multiplex)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#stop_multiplex)
        """

    async def transfer_input_device(
        self, **kwargs: Unpack[TransferInputDeviceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Start an input device transfer to another AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.transfer_input_device)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#transfer_input_device)
        """

    async def update_account_configuration(
        self, **kwargs: Unpack[UpdateAccountConfigurationRequestRequestTypeDef]
    ) -> UpdateAccountConfigurationResponseTypeDef:
        """
        Update account configuration See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/medialive-2017-10-14/UpdateAccountConfiguration).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.update_account_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#update_account_configuration)
        """

    async def update_channel(
        self, **kwargs: Unpack[UpdateChannelRequestRequestTypeDef]
    ) -> UpdateChannelResponseTypeDef:
        """
        Updates a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.update_channel)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#update_channel)
        """

    async def update_channel_class(
        self, **kwargs: Unpack[UpdateChannelClassRequestRequestTypeDef]
    ) -> UpdateChannelClassResponseTypeDef:
        """
        Changes the class of the channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.update_channel_class)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#update_channel_class)
        """

    async def update_cloud_watch_alarm_template(
        self, **kwargs: Unpack[UpdateCloudWatchAlarmTemplateRequestRequestTypeDef]
    ) -> UpdateCloudWatchAlarmTemplateResponseTypeDef:
        """
        Updates the specified cloudwatch alarm template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.update_cloud_watch_alarm_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#update_cloud_watch_alarm_template)
        """

    async def update_cloud_watch_alarm_template_group(
        self, **kwargs: Unpack[UpdateCloudWatchAlarmTemplateGroupRequestRequestTypeDef]
    ) -> UpdateCloudWatchAlarmTemplateGroupResponseTypeDef:
        """
        Updates the specified cloudwatch alarm template group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.update_cloud_watch_alarm_template_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#update_cloud_watch_alarm_template_group)
        """

    async def update_event_bridge_rule_template(
        self, **kwargs: Unpack[UpdateEventBridgeRuleTemplateRequestRequestTypeDef]
    ) -> UpdateEventBridgeRuleTemplateResponseTypeDef:
        """
        Updates the specified eventbridge rule template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.update_event_bridge_rule_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#update_event_bridge_rule_template)
        """

    async def update_event_bridge_rule_template_group(
        self, **kwargs: Unpack[UpdateEventBridgeRuleTemplateGroupRequestRequestTypeDef]
    ) -> UpdateEventBridgeRuleTemplateGroupResponseTypeDef:
        """
        Updates the specified eventbridge rule template group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.update_event_bridge_rule_template_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#update_event_bridge_rule_template_group)
        """

    async def update_input(
        self, **kwargs: Unpack[UpdateInputRequestRequestTypeDef]
    ) -> UpdateInputResponseTypeDef:
        """
        Updates an input.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.update_input)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#update_input)
        """

    async def update_input_device(
        self, **kwargs: Unpack[UpdateInputDeviceRequestRequestTypeDef]
    ) -> UpdateInputDeviceResponseTypeDef:
        """
        Updates the parameters for the input device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.update_input_device)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#update_input_device)
        """

    async def update_input_security_group(
        self, **kwargs: Unpack[UpdateInputSecurityGroupRequestRequestTypeDef]
    ) -> UpdateInputSecurityGroupResponseTypeDef:
        """
        Update an Input Security Group's Whilelists.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.update_input_security_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#update_input_security_group)
        """

    async def update_multiplex(
        self, **kwargs: Unpack[UpdateMultiplexRequestRequestTypeDef]
    ) -> UpdateMultiplexResponseTypeDef:
        """
        Updates a multiplex.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.update_multiplex)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#update_multiplex)
        """

    async def update_multiplex_program(
        self, **kwargs: Unpack[UpdateMultiplexProgramRequestRequestTypeDef]
    ) -> UpdateMultiplexProgramResponseTypeDef:
        """
        Update a program in a multiplex.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.update_multiplex_program)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#update_multiplex_program)
        """

    async def update_reservation(
        self, **kwargs: Unpack[UpdateReservationRequestRequestTypeDef]
    ) -> UpdateReservationResponseTypeDef:
        """
        Update reservation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.update_reservation)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#update_reservation)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_schedule"]
    ) -> DescribeSchedulePaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_channels"]) -> ListChannelsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_cloud_watch_alarm_template_groups"]
    ) -> ListCloudWatchAlarmTemplateGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_cloud_watch_alarm_templates"]
    ) -> ListCloudWatchAlarmTemplatesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_event_bridge_rule_template_groups"]
    ) -> ListEventBridgeRuleTemplateGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_event_bridge_rule_templates"]
    ) -> ListEventBridgeRuleTemplatesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_input_device_transfers"]
    ) -> ListInputDeviceTransfersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_input_devices"]
    ) -> ListInputDevicesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_input_security_groups"]
    ) -> ListInputSecurityGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_inputs"]) -> ListInputsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_multiplex_programs"]
    ) -> ListMultiplexProgramsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_multiplexes"]
    ) -> ListMultiplexesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_offerings"]) -> ListOfferingsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_reservations"]
    ) -> ListReservationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_signal_maps"]) -> ListSignalMapsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#get_paginator)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["channel_created"]) -> ChannelCreatedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["channel_deleted"]) -> ChannelDeletedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["channel_running"]) -> ChannelRunningWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["channel_stopped"]) -> ChannelStoppedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["input_attached"]) -> InputAttachedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["input_deleted"]) -> InputDeletedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["input_detached"]) -> InputDetachedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["multiplex_created"]) -> MultiplexCreatedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["multiplex_deleted"]) -> MultiplexDeletedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["multiplex_running"]) -> MultiplexRunningWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["multiplex_stopped"]) -> MultiplexStoppedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["signal_map_created"]) -> SignalMapCreatedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["signal_map_monitor_deleted"]
    ) -> SignalMapMonitorDeletedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["signal_map_monitor_deployed"]
    ) -> SignalMapMonitorDeployedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["signal_map_updated"]) -> SignalMapUpdatedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/#get_waiter)
        """

    async def __aenter__(self) -> "MediaLiveClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/client/)
        """
