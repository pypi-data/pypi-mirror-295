"""
Type annotations for mediapackage service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_mediapackage.client import MediaPackageClient

    session = get_session()
    async with session.create_client("mediapackage") as client:
        client: MediaPackageClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import ListChannelsPaginator, ListHarvestJobsPaginator, ListOriginEndpointsPaginator
from .type_defs import (
    ConfigureLogsRequestRequestTypeDef,
    ConfigureLogsResponseTypeDef,
    CreateChannelRequestRequestTypeDef,
    CreateChannelResponseTypeDef,
    CreateHarvestJobRequestRequestTypeDef,
    CreateHarvestJobResponseTypeDef,
    CreateOriginEndpointRequestRequestTypeDef,
    CreateOriginEndpointResponseTypeDef,
    DeleteChannelRequestRequestTypeDef,
    DeleteOriginEndpointRequestRequestTypeDef,
    DescribeChannelRequestRequestTypeDef,
    DescribeChannelResponseTypeDef,
    DescribeHarvestJobRequestRequestTypeDef,
    DescribeHarvestJobResponseTypeDef,
    DescribeOriginEndpointRequestRequestTypeDef,
    DescribeOriginEndpointResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    ListChannelsRequestRequestTypeDef,
    ListChannelsResponseTypeDef,
    ListHarvestJobsRequestRequestTypeDef,
    ListHarvestJobsResponseTypeDef,
    ListOriginEndpointsRequestRequestTypeDef,
    ListOriginEndpointsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    RotateChannelCredentialsRequestRequestTypeDef,
    RotateChannelCredentialsResponseTypeDef,
    RotateIngestEndpointCredentialsRequestRequestTypeDef,
    RotateIngestEndpointCredentialsResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateChannelRequestRequestTypeDef,
    UpdateChannelResponseTypeDef,
    UpdateOriginEndpointRequestRequestTypeDef,
    UpdateOriginEndpointResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("MediaPackageClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    ForbiddenException: Type[BotocoreClientError]
    InternalServerErrorException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]
    UnprocessableEntityException: Type[BotocoreClientError]


class MediaPackageClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage.html#MediaPackage.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        MediaPackageClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage.html#MediaPackage.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage.html#MediaPackage.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage.html#MediaPackage.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/#close)
        """

    async def configure_logs(
        self, **kwargs: Unpack[ConfigureLogsRequestRequestTypeDef]
    ) -> ConfigureLogsResponseTypeDef:
        """
        Changes the Channel's properities to configure log subscription See also: [AWS
        API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/mediapackage-2017-10-12/ConfigureLogs).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage.html#MediaPackage.Client.configure_logs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/#configure_logs)
        """

    async def create_channel(
        self, **kwargs: Unpack[CreateChannelRequestRequestTypeDef]
    ) -> CreateChannelResponseTypeDef:
        """
        Creates a new Channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage.html#MediaPackage.Client.create_channel)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/#create_channel)
        """

    async def create_harvest_job(
        self, **kwargs: Unpack[CreateHarvestJobRequestRequestTypeDef]
    ) -> CreateHarvestJobResponseTypeDef:
        """
        Creates a new HarvestJob record.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage.html#MediaPackage.Client.create_harvest_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/#create_harvest_job)
        """

    async def create_origin_endpoint(
        self, **kwargs: Unpack[CreateOriginEndpointRequestRequestTypeDef]
    ) -> CreateOriginEndpointResponseTypeDef:
        """
        Creates a new OriginEndpoint record.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage.html#MediaPackage.Client.create_origin_endpoint)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/#create_origin_endpoint)
        """

    async def delete_channel(
        self, **kwargs: Unpack[DeleteChannelRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an existing Channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage.html#MediaPackage.Client.delete_channel)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/#delete_channel)
        """

    async def delete_origin_endpoint(
        self, **kwargs: Unpack[DeleteOriginEndpointRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an existing OriginEndpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage.html#MediaPackage.Client.delete_origin_endpoint)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/#delete_origin_endpoint)
        """

    async def describe_channel(
        self, **kwargs: Unpack[DescribeChannelRequestRequestTypeDef]
    ) -> DescribeChannelResponseTypeDef:
        """
        Gets details about a Channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage.html#MediaPackage.Client.describe_channel)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/#describe_channel)
        """

    async def describe_harvest_job(
        self, **kwargs: Unpack[DescribeHarvestJobRequestRequestTypeDef]
    ) -> DescribeHarvestJobResponseTypeDef:
        """
        Gets details about an existing HarvestJob.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage.html#MediaPackage.Client.describe_harvest_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/#describe_harvest_job)
        """

    async def describe_origin_endpoint(
        self, **kwargs: Unpack[DescribeOriginEndpointRequestRequestTypeDef]
    ) -> DescribeOriginEndpointResponseTypeDef:
        """
        Gets details about an existing OriginEndpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage.html#MediaPackage.Client.describe_origin_endpoint)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/#describe_origin_endpoint)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage.html#MediaPackage.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/#generate_presigned_url)
        """

    async def list_channels(
        self, **kwargs: Unpack[ListChannelsRequestRequestTypeDef]
    ) -> ListChannelsResponseTypeDef:
        """
        Returns a collection of Channels.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage.html#MediaPackage.Client.list_channels)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/#list_channels)
        """

    async def list_harvest_jobs(
        self, **kwargs: Unpack[ListHarvestJobsRequestRequestTypeDef]
    ) -> ListHarvestJobsResponseTypeDef:
        """
        Returns a collection of HarvestJob records.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage.html#MediaPackage.Client.list_harvest_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/#list_harvest_jobs)
        """

    async def list_origin_endpoints(
        self, **kwargs: Unpack[ListOriginEndpointsRequestRequestTypeDef]
    ) -> ListOriginEndpointsResponseTypeDef:
        """
        Returns a collection of OriginEndpoint records.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage.html#MediaPackage.Client.list_origin_endpoints)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/#list_origin_endpoints)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/mediapackage-2017-10-12/ListTagsForResource).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage.html#MediaPackage.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/#list_tags_for_resource)
        """

    async def rotate_channel_credentials(
        self, **kwargs: Unpack[RotateChannelCredentialsRequestRequestTypeDef]
    ) -> RotateChannelCredentialsResponseTypeDef:
        """
        Changes the Channel's first IngestEndpoint's username and password.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage.html#MediaPackage.Client.rotate_channel_credentials)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/#rotate_channel_credentials)
        """

    async def rotate_ingest_endpoint_credentials(
        self, **kwargs: Unpack[RotateIngestEndpointCredentialsRequestRequestTypeDef]
    ) -> RotateIngestEndpointCredentialsResponseTypeDef:
        """
        Rotate the IngestEndpoint's username and password, as specified by the
        IngestEndpoint's
        id.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage.html#MediaPackage.Client.rotate_ingest_endpoint_credentials)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/#rotate_ingest_endpoint_credentials)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/mediapackage-2017-10-12/TagResource).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage.html#MediaPackage.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/mediapackage-2017-10-12/UntagResource).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage.html#MediaPackage.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/#untag_resource)
        """

    async def update_channel(
        self, **kwargs: Unpack[UpdateChannelRequestRequestTypeDef]
    ) -> UpdateChannelResponseTypeDef:
        """
        Updates an existing Channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage.html#MediaPackage.Client.update_channel)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/#update_channel)
        """

    async def update_origin_endpoint(
        self, **kwargs: Unpack[UpdateOriginEndpointRequestRequestTypeDef]
    ) -> UpdateOriginEndpointResponseTypeDef:
        """
        Updates an existing OriginEndpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage.html#MediaPackage.Client.update_origin_endpoint)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/#update_origin_endpoint)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_channels"]) -> ListChannelsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage.html#MediaPackage.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_harvest_jobs"]
    ) -> ListHarvestJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage.html#MediaPackage.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_origin_endpoints"]
    ) -> ListOriginEndpointsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage.html#MediaPackage.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/#get_paginator)
        """

    async def __aenter__(self) -> "MediaPackageClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage.html#MediaPackage.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage.html#MediaPackage.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/client/)
        """
