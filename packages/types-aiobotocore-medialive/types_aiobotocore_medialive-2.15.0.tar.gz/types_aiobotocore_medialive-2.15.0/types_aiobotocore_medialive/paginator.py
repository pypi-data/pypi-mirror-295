"""
Type annotations for medialive service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_medialive.client import MediaLiveClient
    from types_aiobotocore_medialive.paginator import (
        DescribeSchedulePaginator,
        ListChannelsPaginator,
        ListCloudWatchAlarmTemplateGroupsPaginator,
        ListCloudWatchAlarmTemplatesPaginator,
        ListEventBridgeRuleTemplateGroupsPaginator,
        ListEventBridgeRuleTemplatesPaginator,
        ListInputDeviceTransfersPaginator,
        ListInputDevicesPaginator,
        ListInputSecurityGroupsPaginator,
        ListInputsPaginator,
        ListMultiplexProgramsPaginator,
        ListMultiplexesPaginator,
        ListOfferingsPaginator,
        ListReservationsPaginator,
        ListSignalMapsPaginator,
    )

    session = get_session()
    with session.create_client("medialive") as client:
        client: MediaLiveClient

        describe_schedule_paginator: DescribeSchedulePaginator = client.get_paginator("describe_schedule")
        list_channels_paginator: ListChannelsPaginator = client.get_paginator("list_channels")
        list_cloud_watch_alarm_template_groups_paginator: ListCloudWatchAlarmTemplateGroupsPaginator = client.get_paginator("list_cloud_watch_alarm_template_groups")
        list_cloud_watch_alarm_templates_paginator: ListCloudWatchAlarmTemplatesPaginator = client.get_paginator("list_cloud_watch_alarm_templates")
        list_event_bridge_rule_template_groups_paginator: ListEventBridgeRuleTemplateGroupsPaginator = client.get_paginator("list_event_bridge_rule_template_groups")
        list_event_bridge_rule_templates_paginator: ListEventBridgeRuleTemplatesPaginator = client.get_paginator("list_event_bridge_rule_templates")
        list_input_device_transfers_paginator: ListInputDeviceTransfersPaginator = client.get_paginator("list_input_device_transfers")
        list_input_devices_paginator: ListInputDevicesPaginator = client.get_paginator("list_input_devices")
        list_input_security_groups_paginator: ListInputSecurityGroupsPaginator = client.get_paginator("list_input_security_groups")
        list_inputs_paginator: ListInputsPaginator = client.get_paginator("list_inputs")
        list_multiplex_programs_paginator: ListMultiplexProgramsPaginator = client.get_paginator("list_multiplex_programs")
        list_multiplexes_paginator: ListMultiplexesPaginator = client.get_paginator("list_multiplexes")
        list_offerings_paginator: ListOfferingsPaginator = client.get_paginator("list_offerings")
        list_reservations_paginator: ListReservationsPaginator = client.get_paginator("list_reservations")
        list_signal_maps_paginator: ListSignalMapsPaginator = client.get_paginator("list_signal_maps")
    ```
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    DescribeScheduleRequestDescribeSchedulePaginateTypeDef,
    DescribeScheduleResponseTypeDef,
    ListChannelsRequestListChannelsPaginateTypeDef,
    ListChannelsResponseTypeDef,
    ListCloudWatchAlarmTemplateGroupsRequestListCloudWatchAlarmTemplateGroupsPaginateTypeDef,
    ListCloudWatchAlarmTemplateGroupsResponseTypeDef,
    ListCloudWatchAlarmTemplatesRequestListCloudWatchAlarmTemplatesPaginateTypeDef,
    ListCloudWatchAlarmTemplatesResponseTypeDef,
    ListEventBridgeRuleTemplateGroupsRequestListEventBridgeRuleTemplateGroupsPaginateTypeDef,
    ListEventBridgeRuleTemplateGroupsResponseTypeDef,
    ListEventBridgeRuleTemplatesRequestListEventBridgeRuleTemplatesPaginateTypeDef,
    ListEventBridgeRuleTemplatesResponseTypeDef,
    ListInputDevicesRequestListInputDevicesPaginateTypeDef,
    ListInputDevicesResponseTypeDef,
    ListInputDeviceTransfersRequestListInputDeviceTransfersPaginateTypeDef,
    ListInputDeviceTransfersResponseTypeDef,
    ListInputSecurityGroupsRequestListInputSecurityGroupsPaginateTypeDef,
    ListInputSecurityGroupsResponseTypeDef,
    ListInputsRequestListInputsPaginateTypeDef,
    ListInputsResponseTypeDef,
    ListMultiplexesRequestListMultiplexesPaginateTypeDef,
    ListMultiplexesResponseTypeDef,
    ListMultiplexProgramsRequestListMultiplexProgramsPaginateTypeDef,
    ListMultiplexProgramsResponseTypeDef,
    ListOfferingsRequestListOfferingsPaginateTypeDef,
    ListOfferingsResponseTypeDef,
    ListReservationsRequestListReservationsPaginateTypeDef,
    ListReservationsResponseTypeDef,
    ListSignalMapsRequestListSignalMapsPaginateTypeDef,
    ListSignalMapsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeSchedulePaginator",
    "ListChannelsPaginator",
    "ListCloudWatchAlarmTemplateGroupsPaginator",
    "ListCloudWatchAlarmTemplatesPaginator",
    "ListEventBridgeRuleTemplateGroupsPaginator",
    "ListEventBridgeRuleTemplatesPaginator",
    "ListInputDeviceTransfersPaginator",
    "ListInputDevicesPaginator",
    "ListInputSecurityGroupsPaginator",
    "ListInputsPaginator",
    "ListMultiplexProgramsPaginator",
    "ListMultiplexesPaginator",
    "ListOfferingsPaginator",
    "ListReservationsPaginator",
    "ListSignalMapsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeSchedulePaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.DescribeSchedule)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#describeschedulepaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeScheduleRequestDescribeSchedulePaginateTypeDef]
    ) -> AsyncIterator[DescribeScheduleResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.DescribeSchedule.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#describeschedulepaginator)
        """


class ListChannelsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.ListChannels)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listchannelspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListChannelsRequestListChannelsPaginateTypeDef]
    ) -> AsyncIterator[ListChannelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.ListChannels.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listchannelspaginator)
        """


class ListCloudWatchAlarmTemplateGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.ListCloudWatchAlarmTemplateGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listcloudwatchalarmtemplategroupspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListCloudWatchAlarmTemplateGroupsRequestListCloudWatchAlarmTemplateGroupsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListCloudWatchAlarmTemplateGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.ListCloudWatchAlarmTemplateGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listcloudwatchalarmtemplategroupspaginator)
        """


class ListCloudWatchAlarmTemplatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.ListCloudWatchAlarmTemplates)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listcloudwatchalarmtemplatespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListCloudWatchAlarmTemplatesRequestListCloudWatchAlarmTemplatesPaginateTypeDef
        ],
    ) -> AsyncIterator[ListCloudWatchAlarmTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.ListCloudWatchAlarmTemplates.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listcloudwatchalarmtemplatespaginator)
        """


class ListEventBridgeRuleTemplateGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.ListEventBridgeRuleTemplateGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listeventbridgeruletemplategroupspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListEventBridgeRuleTemplateGroupsRequestListEventBridgeRuleTemplateGroupsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListEventBridgeRuleTemplateGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.ListEventBridgeRuleTemplateGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listeventbridgeruletemplategroupspaginator)
        """


class ListEventBridgeRuleTemplatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.ListEventBridgeRuleTemplates)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listeventbridgeruletemplatespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListEventBridgeRuleTemplatesRequestListEventBridgeRuleTemplatesPaginateTypeDef
        ],
    ) -> AsyncIterator[ListEventBridgeRuleTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.ListEventBridgeRuleTemplates.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listeventbridgeruletemplatespaginator)
        """


class ListInputDeviceTransfersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.ListInputDeviceTransfers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listinputdevicetransferspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListInputDeviceTransfersRequestListInputDeviceTransfersPaginateTypeDef],
    ) -> AsyncIterator[ListInputDeviceTransfersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.ListInputDeviceTransfers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listinputdevicetransferspaginator)
        """


class ListInputDevicesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.ListInputDevices)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listinputdevicespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListInputDevicesRequestListInputDevicesPaginateTypeDef]
    ) -> AsyncIterator[ListInputDevicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.ListInputDevices.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listinputdevicespaginator)
        """


class ListInputSecurityGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.ListInputSecurityGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listinputsecuritygroupspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListInputSecurityGroupsRequestListInputSecurityGroupsPaginateTypeDef]
    ) -> AsyncIterator[ListInputSecurityGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.ListInputSecurityGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listinputsecuritygroupspaginator)
        """


class ListInputsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.ListInputs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listinputspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListInputsRequestListInputsPaginateTypeDef]
    ) -> AsyncIterator[ListInputsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.ListInputs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listinputspaginator)
        """


class ListMultiplexProgramsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.ListMultiplexPrograms)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listmultiplexprogramspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListMultiplexProgramsRequestListMultiplexProgramsPaginateTypeDef]
    ) -> AsyncIterator[ListMultiplexProgramsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.ListMultiplexPrograms.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listmultiplexprogramspaginator)
        """


class ListMultiplexesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.ListMultiplexes)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listmultiplexespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListMultiplexesRequestListMultiplexesPaginateTypeDef]
    ) -> AsyncIterator[ListMultiplexesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.ListMultiplexes.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listmultiplexespaginator)
        """


class ListOfferingsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.ListOfferings)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listofferingspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListOfferingsRequestListOfferingsPaginateTypeDef]
    ) -> AsyncIterator[ListOfferingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.ListOfferings.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listofferingspaginator)
        """


class ListReservationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.ListReservations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listreservationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListReservationsRequestListReservationsPaginateTypeDef]
    ) -> AsyncIterator[ListReservationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.ListReservations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listreservationspaginator)
        """


class ListSignalMapsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.ListSignalMaps)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listsignalmapspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListSignalMapsRequestListSignalMapsPaginateTypeDef]
    ) -> AsyncIterator[ListSignalMapsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.ListSignalMaps.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listsignalmapspaginator)
        """
