"""
Type annotations for resource-groups service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_resource_groups.client import ResourceGroupsClient

    session = get_session()
    async with session.create_client("resource-groups") as client:
        client: ResourceGroupsClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import ListGroupResourcesPaginator, ListGroupsPaginator, SearchResourcesPaginator
from .type_defs import (
    CreateGroupInputRequestTypeDef,
    CreateGroupOutputTypeDef,
    DeleteGroupInputRequestTypeDef,
    DeleteGroupOutputTypeDef,
    GetAccountSettingsOutputTypeDef,
    GetGroupConfigurationInputRequestTypeDef,
    GetGroupConfigurationOutputTypeDef,
    GetGroupInputRequestTypeDef,
    GetGroupOutputTypeDef,
    GetGroupQueryInputRequestTypeDef,
    GetGroupQueryOutputTypeDef,
    GetTagsInputRequestTypeDef,
    GetTagsOutputTypeDef,
    GroupResourcesInputRequestTypeDef,
    GroupResourcesOutputTypeDef,
    ListGroupResourcesInputRequestTypeDef,
    ListGroupResourcesOutputTypeDef,
    ListGroupsInputRequestTypeDef,
    ListGroupsOutputTypeDef,
    PutGroupConfigurationInputRequestTypeDef,
    SearchResourcesInputRequestTypeDef,
    SearchResourcesOutputTypeDef,
    TagInputRequestTypeDef,
    TagOutputTypeDef,
    UngroupResourcesInputRequestTypeDef,
    UngroupResourcesOutputTypeDef,
    UntagInputRequestTypeDef,
    UntagOutputTypeDef,
    UpdateAccountSettingsInputRequestTypeDef,
    UpdateAccountSettingsOutputTypeDef,
    UpdateGroupInputRequestTypeDef,
    UpdateGroupOutputTypeDef,
    UpdateGroupQueryInputRequestTypeDef,
    UpdateGroupQueryOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ResourceGroupsClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ForbiddenException: Type[BotocoreClientError]
    InternalServerErrorException: Type[BotocoreClientError]
    MethodNotAllowedException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]
    UnauthorizedException: Type[BotocoreClientError]


class ResourceGroupsClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ResourceGroupsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/#close)
        """

    async def create_group(
        self, **kwargs: Unpack[CreateGroupInputRequestTypeDef]
    ) -> CreateGroupOutputTypeDef:
        """
        Creates a resource group with the specified name and description.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Client.create_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/#create_group)
        """

    async def delete_group(
        self, **kwargs: Unpack[DeleteGroupInputRequestTypeDef]
    ) -> DeleteGroupOutputTypeDef:
        """
        Deletes the specified resource group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Client.delete_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/#delete_group)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/#generate_presigned_url)
        """

    async def get_account_settings(self) -> GetAccountSettingsOutputTypeDef:
        """
        Retrieves the current status of optional features in Resource Groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Client.get_account_settings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/#get_account_settings)
        """

    async def get_group(
        self, **kwargs: Unpack[GetGroupInputRequestTypeDef]
    ) -> GetGroupOutputTypeDef:
        """
        Returns information about a specified resource group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Client.get_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/#get_group)
        """

    async def get_group_configuration(
        self, **kwargs: Unpack[GetGroupConfigurationInputRequestTypeDef]
    ) -> GetGroupConfigurationOutputTypeDef:
        """
        Retrieves the service configuration associated with the specified resource
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Client.get_group_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/#get_group_configuration)
        """

    async def get_group_query(
        self, **kwargs: Unpack[GetGroupQueryInputRequestTypeDef]
    ) -> GetGroupQueryOutputTypeDef:
        """
        Retrieves the resource query associated with the specified resource group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Client.get_group_query)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/#get_group_query)
        """

    async def get_tags(self, **kwargs: Unpack[GetTagsInputRequestTypeDef]) -> GetTagsOutputTypeDef:
        """
        Returns a list of tags that are associated with a resource group, specified by
        an
        ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Client.get_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/#get_tags)
        """

    async def group_resources(
        self, **kwargs: Unpack[GroupResourcesInputRequestTypeDef]
    ) -> GroupResourcesOutputTypeDef:
        """
        Adds the specified resources to the specified group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Client.group_resources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/#group_resources)
        """

    async def list_group_resources(
        self, **kwargs: Unpack[ListGroupResourcesInputRequestTypeDef]
    ) -> ListGroupResourcesOutputTypeDef:
        """
        Returns a list of ARNs of the resources that are members of a specified
        resource
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Client.list_group_resources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/#list_group_resources)
        """

    async def list_groups(
        self, **kwargs: Unpack[ListGroupsInputRequestTypeDef]
    ) -> ListGroupsOutputTypeDef:
        """
        Returns a list of existing Resource Groups in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Client.list_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/#list_groups)
        """

    async def put_group_configuration(
        self, **kwargs: Unpack[PutGroupConfigurationInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Attaches a service configuration to the specified group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Client.put_group_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/#put_group_configuration)
        """

    async def search_resources(
        self, **kwargs: Unpack[SearchResourcesInputRequestTypeDef]
    ) -> SearchResourcesOutputTypeDef:
        """
        Returns a list of Amazon Web Services resource identifiers that matches the
        specified
        query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Client.search_resources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/#search_resources)
        """

    async def tag(self, **kwargs: Unpack[TagInputRequestTypeDef]) -> TagOutputTypeDef:
        """
        Adds tags to a resource group with the specified ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Client.tag)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/#tag)
        """

    async def ungroup_resources(
        self, **kwargs: Unpack[UngroupResourcesInputRequestTypeDef]
    ) -> UngroupResourcesOutputTypeDef:
        """
        Removes the specified resources from the specified group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Client.ungroup_resources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/#ungroup_resources)
        """

    async def untag(self, **kwargs: Unpack[UntagInputRequestTypeDef]) -> UntagOutputTypeDef:
        """
        Deletes tags from a specified resource group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Client.untag)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/#untag)
        """

    async def update_account_settings(
        self, **kwargs: Unpack[UpdateAccountSettingsInputRequestTypeDef]
    ) -> UpdateAccountSettingsOutputTypeDef:
        """
        Turns on or turns off optional features in Resource Groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Client.update_account_settings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/#update_account_settings)
        """

    async def update_group(
        self, **kwargs: Unpack[UpdateGroupInputRequestTypeDef]
    ) -> UpdateGroupOutputTypeDef:
        """
        Updates the description for an existing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Client.update_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/#update_group)
        """

    async def update_group_query(
        self, **kwargs: Unpack[UpdateGroupQueryInputRequestTypeDef]
    ) -> UpdateGroupQueryOutputTypeDef:
        """
        Updates the resource query of a group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Client.update_group_query)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/#update_group_query)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_group_resources"]
    ) -> ListGroupResourcesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_groups"]) -> ListGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["search_resources"]
    ) -> SearchResourcesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/#get_paginator)
        """

    async def __aenter__(self) -> "ResourceGroupsClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/)
        """
