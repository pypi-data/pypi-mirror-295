"""
Type annotations for timestream-influxdb service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_influxdb/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_timestream_influxdb.client import TimestreamInfluxDBClient

    session = get_session()
    async with session.create_client("timestream-influxdb") as client:
        client: TimestreamInfluxDBClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import ListDbInstancesPaginator, ListDbParameterGroupsPaginator
from .type_defs import (
    CreateDbInstanceInputRequestTypeDef,
    CreateDbInstanceOutputTypeDef,
    CreateDbParameterGroupInputRequestTypeDef,
    CreateDbParameterGroupOutputTypeDef,
    DeleteDbInstanceInputRequestTypeDef,
    DeleteDbInstanceOutputTypeDef,
    EmptyResponseMetadataTypeDef,
    GetDbInstanceInputRequestTypeDef,
    GetDbInstanceOutputTypeDef,
    GetDbParameterGroupInputRequestTypeDef,
    GetDbParameterGroupOutputTypeDef,
    ListDbInstancesInputRequestTypeDef,
    ListDbInstancesOutputTypeDef,
    ListDbParameterGroupsInputRequestTypeDef,
    ListDbParameterGroupsOutputTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateDbInstanceInputRequestTypeDef,
    UpdateDbInstanceOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("TimestreamInfluxDBClient",)


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


class TimestreamInfluxDBClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb.html#TimestreamInfluxDB.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_influxdb/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        TimestreamInfluxDBClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb.html#TimestreamInfluxDB.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_influxdb/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb.html#TimestreamInfluxDB.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_influxdb/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb.html#TimestreamInfluxDB.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_influxdb/client/#close)
        """

    async def create_db_instance(
        self, **kwargs: Unpack[CreateDbInstanceInputRequestTypeDef]
    ) -> CreateDbInstanceOutputTypeDef:
        """
        Creates a new Timestream for InfluxDB DB instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb.html#TimestreamInfluxDB.Client.create_db_instance)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_influxdb/client/#create_db_instance)
        """

    async def create_db_parameter_group(
        self, **kwargs: Unpack[CreateDbParameterGroupInputRequestTypeDef]
    ) -> CreateDbParameterGroupOutputTypeDef:
        """
        Creates a new Timestream for InfluxDB DB parameter group to associate with DB
        instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb.html#TimestreamInfluxDB.Client.create_db_parameter_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_influxdb/client/#create_db_parameter_group)
        """

    async def delete_db_instance(
        self, **kwargs: Unpack[DeleteDbInstanceInputRequestTypeDef]
    ) -> DeleteDbInstanceOutputTypeDef:
        """
        Deletes a Timestream for InfluxDB DB instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb.html#TimestreamInfluxDB.Client.delete_db_instance)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_influxdb/client/#delete_db_instance)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb.html#TimestreamInfluxDB.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_influxdb/client/#generate_presigned_url)
        """

    async def get_db_instance(
        self, **kwargs: Unpack[GetDbInstanceInputRequestTypeDef]
    ) -> GetDbInstanceOutputTypeDef:
        """
        Returns a Timestream for InfluxDB DB instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb.html#TimestreamInfluxDB.Client.get_db_instance)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_influxdb/client/#get_db_instance)
        """

    async def get_db_parameter_group(
        self, **kwargs: Unpack[GetDbParameterGroupInputRequestTypeDef]
    ) -> GetDbParameterGroupOutputTypeDef:
        """
        Returns a Timestream for InfluxDB DB parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb.html#TimestreamInfluxDB.Client.get_db_parameter_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_influxdb/client/#get_db_parameter_group)
        """

    async def list_db_instances(
        self, **kwargs: Unpack[ListDbInstancesInputRequestTypeDef]
    ) -> ListDbInstancesOutputTypeDef:
        """
        Returns a list of Timestream for InfluxDB DB instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb.html#TimestreamInfluxDB.Client.list_db_instances)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_influxdb/client/#list_db_instances)
        """

    async def list_db_parameter_groups(
        self, **kwargs: Unpack[ListDbParameterGroupsInputRequestTypeDef]
    ) -> ListDbParameterGroupsOutputTypeDef:
        """
        Returns a list of Timestream for InfluxDB DB parameter groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb.html#TimestreamInfluxDB.Client.list_db_parameter_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_influxdb/client/#list_db_parameter_groups)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        A list of tags applied to the resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb.html#TimestreamInfluxDB.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_influxdb/client/#list_tags_for_resource)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Tags are composed of a Key/Value pairs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb.html#TimestreamInfluxDB.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_influxdb/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes the tag from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb.html#TimestreamInfluxDB.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_influxdb/client/#untag_resource)
        """

    async def update_db_instance(
        self, **kwargs: Unpack[UpdateDbInstanceInputRequestTypeDef]
    ) -> UpdateDbInstanceOutputTypeDef:
        """
        Updates a Timestream for InfluxDB DB instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb.html#TimestreamInfluxDB.Client.update_db_instance)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_influxdb/client/#update_db_instance)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_db_instances"]
    ) -> ListDbInstancesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb.html#TimestreamInfluxDB.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_influxdb/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_db_parameter_groups"]
    ) -> ListDbParameterGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb.html#TimestreamInfluxDB.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_influxdb/client/#get_paginator)
        """

    async def __aenter__(self) -> "TimestreamInfluxDBClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb.html#TimestreamInfluxDB.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_influxdb/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-influxdb.html#TimestreamInfluxDB.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_timestream_influxdb/client/)
        """
