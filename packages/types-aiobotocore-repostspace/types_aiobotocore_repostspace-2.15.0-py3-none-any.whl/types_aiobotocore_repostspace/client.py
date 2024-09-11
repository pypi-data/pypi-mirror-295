"""
Type annotations for repostspace service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_repostspace/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_repostspace.client import RePostPrivateClient

    session = get_session()
    async with session.create_client("repostspace") as client:
        client: RePostPrivateClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import ListSpacesPaginator
from .type_defs import (
    CreateSpaceInputRequestTypeDef,
    CreateSpaceOutputTypeDef,
    DeleteSpaceInputRequestTypeDef,
    DeregisterAdminInputRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    GetSpaceInputRequestTypeDef,
    GetSpaceOutputTypeDef,
    ListSpacesInputRequestTypeDef,
    ListSpacesOutputTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    RegisterAdminInputRequestTypeDef,
    SendInvitesInputRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateSpaceInputRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("RePostPrivateClient",)


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


class RePostPrivateClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/repostspace.html#RePostPrivate.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_repostspace/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        RePostPrivateClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/repostspace.html#RePostPrivate.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_repostspace/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/repostspace.html#RePostPrivate.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_repostspace/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/repostspace.html#RePostPrivate.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_repostspace/client/#close)
        """

    async def create_space(
        self, **kwargs: Unpack[CreateSpaceInputRequestTypeDef]
    ) -> CreateSpaceOutputTypeDef:
        """
        Creates an AWS re:Post Private private re:Post.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/repostspace.html#RePostPrivate.Client.create_space)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_repostspace/client/#create_space)
        """

    async def delete_space(
        self, **kwargs: Unpack[DeleteSpaceInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an AWS re:Post Private private re:Post.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/repostspace.html#RePostPrivate.Client.delete_space)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_repostspace/client/#delete_space)
        """

    async def deregister_admin(
        self, **kwargs: Unpack[DeregisterAdminInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes the user or group from the list of administrators of the private
        re:Post.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/repostspace.html#RePostPrivate.Client.deregister_admin)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_repostspace/client/#deregister_admin)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/repostspace.html#RePostPrivate.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_repostspace/client/#generate_presigned_url)
        """

    async def get_space(
        self, **kwargs: Unpack[GetSpaceInputRequestTypeDef]
    ) -> GetSpaceOutputTypeDef:
        """
        Displays information about the AWS re:Post Private private re:Post.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/repostspace.html#RePostPrivate.Client.get_space)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_repostspace/client/#get_space)
        """

    async def list_spaces(
        self, **kwargs: Unpack[ListSpacesInputRequestTypeDef]
    ) -> ListSpacesOutputTypeDef:
        """
        Returns a list of AWS re:Post Private private re:Posts in the account with some
        information about each private
        re:Post.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/repostspace.html#RePostPrivate.Client.list_spaces)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_repostspace/client/#list_spaces)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns the tags that are associated with the AWS re:Post Private resource
        specified by the
        resourceArn.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/repostspace.html#RePostPrivate.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_repostspace/client/#list_tags_for_resource)
        """

    async def register_admin(
        self, **kwargs: Unpack[RegisterAdminInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds a user or group to the list of administrators of the private re:Post.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/repostspace.html#RePostPrivate.Client.register_admin)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_repostspace/client/#register_admin)
        """

    async def send_invites(
        self, **kwargs: Unpack[SendInvitesInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Sends an invitation email to selected users and groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/repostspace.html#RePostPrivate.Client.send_invites)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_repostspace/client/#send_invites)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Associates tags with an AWS re:Post Private resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/repostspace.html#RePostPrivate.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_repostspace/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes the association of the tag with the AWS re:Post Private resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/repostspace.html#RePostPrivate.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_repostspace/client/#untag_resource)
        """

    async def update_space(
        self, **kwargs: Unpack[UpdateSpaceInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Modifies an existing AWS re:Post Private private re:Post.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/repostspace.html#RePostPrivate.Client.update_space)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_repostspace/client/#update_space)
        """

    def get_paginator(self, operation_name: Literal["list_spaces"]) -> ListSpacesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/repostspace.html#RePostPrivate.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_repostspace/client/#get_paginator)
        """

    async def __aenter__(self) -> "RePostPrivateClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/repostspace.html#RePostPrivate.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_repostspace/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/repostspace.html#RePostPrivate.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_repostspace/client/)
        """
