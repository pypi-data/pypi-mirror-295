"""
Type annotations for pcs service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_pcs.client import ParallelComputingServiceClient

    session = get_session()
    async with session.create_client("pcs") as client:
        client: ParallelComputingServiceClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import ListClustersPaginator, ListComputeNodeGroupsPaginator, ListQueuesPaginator
from .type_defs import (
    CreateClusterRequestRequestTypeDef,
    CreateClusterResponseTypeDef,
    CreateComputeNodeGroupRequestRequestTypeDef,
    CreateComputeNodeGroupResponseTypeDef,
    CreateQueueRequestRequestTypeDef,
    CreateQueueResponseTypeDef,
    DeleteClusterRequestRequestTypeDef,
    DeleteComputeNodeGroupRequestRequestTypeDef,
    DeleteQueueRequestRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    GetClusterRequestRequestTypeDef,
    GetClusterResponseTypeDef,
    GetComputeNodeGroupRequestRequestTypeDef,
    GetComputeNodeGroupResponseTypeDef,
    GetQueueRequestRequestTypeDef,
    GetQueueResponseTypeDef,
    ListClustersRequestRequestTypeDef,
    ListClustersResponseTypeDef,
    ListComputeNodeGroupsRequestRequestTypeDef,
    ListComputeNodeGroupsResponseTypeDef,
    ListQueuesRequestRequestTypeDef,
    ListQueuesResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    RegisterComputeNodeGroupInstanceRequestRequestTypeDef,
    RegisterComputeNodeGroupInstanceResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateComputeNodeGroupRequestRequestTypeDef,
    UpdateComputeNodeGroupResponseTypeDef,
    UpdateQueueRequestRequestTypeDef,
    UpdateQueueResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ParallelComputingServiceClient",)


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


class ParallelComputingServiceClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ParallelComputingServiceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/client/#close)
        """

    async def create_cluster(
        self, **kwargs: Unpack[CreateClusterRequestRequestTypeDef]
    ) -> CreateClusterResponseTypeDef:
        """
        Creates a cluster in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client.create_cluster)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/client/#create_cluster)
        """

    async def create_compute_node_group(
        self, **kwargs: Unpack[CreateComputeNodeGroupRequestRequestTypeDef]
    ) -> CreateComputeNodeGroupResponseTypeDef:
        """
        Creates a managed set of compute nodes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client.create_compute_node_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/client/#create_compute_node_group)
        """

    async def create_queue(
        self, **kwargs: Unpack[CreateQueueRequestRequestTypeDef]
    ) -> CreateQueueResponseTypeDef:
        """
        Creates a job queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client.create_queue)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/client/#create_queue)
        """

    async def delete_cluster(
        self, **kwargs: Unpack[DeleteClusterRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a cluster and all its linked resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client.delete_cluster)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/client/#delete_cluster)
        """

    async def delete_compute_node_group(
        self, **kwargs: Unpack[DeleteComputeNodeGroupRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a compute node group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client.delete_compute_node_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/client/#delete_compute_node_group)
        """

    async def delete_queue(
        self, **kwargs: Unpack[DeleteQueueRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a job queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client.delete_queue)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/client/#delete_queue)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/client/#generate_presigned_url)
        """

    async def get_cluster(
        self, **kwargs: Unpack[GetClusterRequestRequestTypeDef]
    ) -> GetClusterResponseTypeDef:
        """
        Returns detailed information about a running cluster in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client.get_cluster)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/client/#get_cluster)
        """

    async def get_compute_node_group(
        self, **kwargs: Unpack[GetComputeNodeGroupRequestRequestTypeDef]
    ) -> GetComputeNodeGroupResponseTypeDef:
        """
        Returns detailed information about a compute node group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client.get_compute_node_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/client/#get_compute_node_group)
        """

    async def get_queue(
        self, **kwargs: Unpack[GetQueueRequestRequestTypeDef]
    ) -> GetQueueResponseTypeDef:
        """
        Returns detailed information about a queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client.get_queue)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/client/#get_queue)
        """

    async def list_clusters(
        self, **kwargs: Unpack[ListClustersRequestRequestTypeDef]
    ) -> ListClustersResponseTypeDef:
        """
        Returns a list of running clusters in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client.list_clusters)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/client/#list_clusters)
        """

    async def list_compute_node_groups(
        self, **kwargs: Unpack[ListComputeNodeGroupsRequestRequestTypeDef]
    ) -> ListComputeNodeGroupsResponseTypeDef:
        """
        Returns a list of all compute node groups associated with a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client.list_compute_node_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/client/#list_compute_node_groups)
        """

    async def list_queues(
        self, **kwargs: Unpack[ListQueuesRequestRequestTypeDef]
    ) -> ListQueuesResponseTypeDef:
        """
        Returns a list of all queues associated with a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client.list_queues)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/client/#list_queues)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of all tags on an Amazon Web Services PCS resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/client/#list_tags_for_resource)
        """

    async def register_compute_node_group_instance(
        self, **kwargs: Unpack[RegisterComputeNodeGroupInstanceRequestRequestTypeDef]
    ) -> RegisterComputeNodeGroupInstanceResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client.register_compute_node_group_instance)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/client/#register_compute_node_group_instance)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds or edits tags on an Amazon Web Services PCS resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes tags from an Amazon Web Services PCS resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/client/#untag_resource)
        """

    async def update_compute_node_group(
        self, **kwargs: Unpack[UpdateComputeNodeGroupRequestRequestTypeDef]
    ) -> UpdateComputeNodeGroupResponseTypeDef:
        """
        Updates a compute node group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client.update_compute_node_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/client/#update_compute_node_group)
        """

    async def update_queue(
        self, **kwargs: Unpack[UpdateQueueRequestRequestTypeDef]
    ) -> UpdateQueueResponseTypeDef:
        """
        Updates the compute node group configuration of a queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client.update_queue)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/client/#update_queue)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_clusters"]) -> ListClustersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_compute_node_groups"]
    ) -> ListComputeNodeGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_queues"]) -> ListQueuesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/client/#get_paginator)
        """

    async def __aenter__(self) -> "ParallelComputingServiceClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pcs/client/)
        """
