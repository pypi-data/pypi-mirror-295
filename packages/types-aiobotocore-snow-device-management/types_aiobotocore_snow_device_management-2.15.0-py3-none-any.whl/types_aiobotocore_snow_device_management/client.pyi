"""
Type annotations for snow-device-management service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snow_device_management/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_snow_device_management.client import SnowDeviceManagementClient

    session = get_session()
    async with session.create_client("snow-device-management") as client:
        client: SnowDeviceManagementClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import (
    ListDeviceResourcesPaginator,
    ListDevicesPaginator,
    ListExecutionsPaginator,
    ListTasksPaginator,
)
from .type_defs import (
    CancelTaskInputRequestTypeDef,
    CancelTaskOutputTypeDef,
    CreateTaskInputRequestTypeDef,
    CreateTaskOutputTypeDef,
    DescribeDeviceEc2InputRequestTypeDef,
    DescribeDeviceEc2OutputTypeDef,
    DescribeDeviceInputRequestTypeDef,
    DescribeDeviceOutputTypeDef,
    DescribeExecutionInputRequestTypeDef,
    DescribeExecutionOutputTypeDef,
    DescribeTaskInputRequestTypeDef,
    DescribeTaskOutputTypeDef,
    EmptyResponseMetadataTypeDef,
    ListDeviceResourcesInputRequestTypeDef,
    ListDeviceResourcesOutputTypeDef,
    ListDevicesInputRequestTypeDef,
    ListDevicesOutputTypeDef,
    ListExecutionsInputRequestTypeDef,
    ListExecutionsOutputTypeDef,
    ListTagsForResourceInputRequestTypeDef,
    ListTagsForResourceOutputTypeDef,
    ListTasksInputRequestTypeDef,
    ListTasksOutputTypeDef,
    TagResourceInputRequestTypeDef,
    UntagResourceInputRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("SnowDeviceManagementClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class SnowDeviceManagementClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management.html#SnowDeviceManagement.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snow_device_management/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SnowDeviceManagementClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management.html#SnowDeviceManagement.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snow_device_management/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management.html#SnowDeviceManagement.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snow_device_management/client/#can_paginate)
        """

    async def cancel_task(
        self, **kwargs: Unpack[CancelTaskInputRequestTypeDef]
    ) -> CancelTaskOutputTypeDef:
        """
        Sends a cancel request for a specified task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management.html#SnowDeviceManagement.Client.cancel_task)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snow_device_management/client/#cancel_task)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management.html#SnowDeviceManagement.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snow_device_management/client/#close)
        """

    async def create_task(
        self, **kwargs: Unpack[CreateTaskInputRequestTypeDef]
    ) -> CreateTaskOutputTypeDef:
        """
        Instructs one or more devices to start a task, such as unlocking or rebooting.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management.html#SnowDeviceManagement.Client.create_task)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snow_device_management/client/#create_task)
        """

    async def describe_device(
        self, **kwargs: Unpack[DescribeDeviceInputRequestTypeDef]
    ) -> DescribeDeviceOutputTypeDef:
        """
        Checks device-specific information, such as the device type, software version,
        IP addresses, and lock
        status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management.html#SnowDeviceManagement.Client.describe_device)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snow_device_management/client/#describe_device)
        """

    async def describe_device_ec2_instances(
        self, **kwargs: Unpack[DescribeDeviceEc2InputRequestTypeDef]
    ) -> DescribeDeviceEc2OutputTypeDef:
        """
        Checks the current state of the Amazon EC2 instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management.html#SnowDeviceManagement.Client.describe_device_ec2_instances)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snow_device_management/client/#describe_device_ec2_instances)
        """

    async def describe_execution(
        self, **kwargs: Unpack[DescribeExecutionInputRequestTypeDef]
    ) -> DescribeExecutionOutputTypeDef:
        """
        Checks the status of a remote task running on one or more target devices.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management.html#SnowDeviceManagement.Client.describe_execution)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snow_device_management/client/#describe_execution)
        """

    async def describe_task(
        self, **kwargs: Unpack[DescribeTaskInputRequestTypeDef]
    ) -> DescribeTaskOutputTypeDef:
        """
        Checks the metadata for a given task on a device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management.html#SnowDeviceManagement.Client.describe_task)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snow_device_management/client/#describe_task)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management.html#SnowDeviceManagement.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snow_device_management/client/#generate_presigned_url)
        """

    async def list_device_resources(
        self, **kwargs: Unpack[ListDeviceResourcesInputRequestTypeDef]
    ) -> ListDeviceResourcesOutputTypeDef:
        """
        Returns a list of the Amazon Web Services resources available for a device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management.html#SnowDeviceManagement.Client.list_device_resources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snow_device_management/client/#list_device_resources)
        """

    async def list_devices(
        self, **kwargs: Unpack[ListDevicesInputRequestTypeDef]
    ) -> ListDevicesOutputTypeDef:
        """
        Returns a list of all devices on your Amazon Web Services account that have
        Amazon Web Services Snow Device Management enabled in the Amazon Web Services
        Region where the command is
        run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management.html#SnowDeviceManagement.Client.list_devices)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snow_device_management/client/#list_devices)
        """

    async def list_executions(
        self, **kwargs: Unpack[ListExecutionsInputRequestTypeDef]
    ) -> ListExecutionsOutputTypeDef:
        """
        Returns the status of tasks for one or more target devices.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management.html#SnowDeviceManagement.Client.list_executions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snow_device_management/client/#list_executions)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceInputRequestTypeDef]
    ) -> ListTagsForResourceOutputTypeDef:
        """
        Returns a list of tags for a managed device or task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management.html#SnowDeviceManagement.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snow_device_management/client/#list_tags_for_resource)
        """

    async def list_tasks(
        self, **kwargs: Unpack[ListTasksInputRequestTypeDef]
    ) -> ListTasksOutputTypeDef:
        """
        Returns a list of tasks that can be filtered by state.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management.html#SnowDeviceManagement.Client.list_tasks)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snow_device_management/client/#list_tasks)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds or replaces tags on a device or task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management.html#SnowDeviceManagement.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snow_device_management/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes a tag from a device or task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management.html#SnowDeviceManagement.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snow_device_management/client/#untag_resource)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_device_resources"]
    ) -> ListDeviceResourcesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management.html#SnowDeviceManagement.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snow_device_management/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_devices"]) -> ListDevicesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management.html#SnowDeviceManagement.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snow_device_management/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_executions"]) -> ListExecutionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management.html#SnowDeviceManagement.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snow_device_management/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_tasks"]) -> ListTasksPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management.html#SnowDeviceManagement.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snow_device_management/client/#get_paginator)
        """

    async def __aenter__(self) -> "SnowDeviceManagementClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management.html#SnowDeviceManagement.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snow_device_management/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snow-device-management.html#SnowDeviceManagement.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snow_device_management/client/)
        """
