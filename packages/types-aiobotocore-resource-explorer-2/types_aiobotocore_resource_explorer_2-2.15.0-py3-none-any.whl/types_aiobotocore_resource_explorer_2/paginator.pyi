"""
Type annotations for resource-explorer-2 service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_explorer_2/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_resource_explorer_2.client import ResourceExplorerClient
    from types_aiobotocore_resource_explorer_2.paginator import (
        ListIndexesPaginator,
        ListIndexesForMembersPaginator,
        ListSupportedResourceTypesPaginator,
        ListViewsPaginator,
        SearchPaginator,
    )

    session = get_session()
    with session.create_client("resource-explorer-2") as client:
        client: ResourceExplorerClient

        list_indexes_paginator: ListIndexesPaginator = client.get_paginator("list_indexes")
        list_indexes_for_members_paginator: ListIndexesForMembersPaginator = client.get_paginator("list_indexes_for_members")
        list_supported_resource_types_paginator: ListSupportedResourceTypesPaginator = client.get_paginator("list_supported_resource_types")
        list_views_paginator: ListViewsPaginator = client.get_paginator("list_views")
        search_paginator: SearchPaginator = client.get_paginator("search")
    ```
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListIndexesForMembersInputListIndexesForMembersPaginateTypeDef,
    ListIndexesForMembersOutputTypeDef,
    ListIndexesInputListIndexesPaginateTypeDef,
    ListIndexesOutputTypeDef,
    ListSupportedResourceTypesInputListSupportedResourceTypesPaginateTypeDef,
    ListSupportedResourceTypesOutputTypeDef,
    ListViewsInputListViewsPaginateTypeDef,
    ListViewsOutputTypeDef,
    SearchInputSearchPaginateTypeDef,
    SearchOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListIndexesPaginator",
    "ListIndexesForMembersPaginator",
    "ListSupportedResourceTypesPaginator",
    "ListViewsPaginator",
    "SearchPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListIndexesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-explorer-2.html#ResourceExplorer.Paginator.ListIndexes)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_explorer_2/paginators/#listindexespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListIndexesInputListIndexesPaginateTypeDef]
    ) -> AsyncIterator[ListIndexesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-explorer-2.html#ResourceExplorer.Paginator.ListIndexes.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_explorer_2/paginators/#listindexespaginator)
        """

class ListIndexesForMembersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-explorer-2.html#ResourceExplorer.Paginator.ListIndexesForMembers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_explorer_2/paginators/#listindexesformemberspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListIndexesForMembersInputListIndexesForMembersPaginateTypeDef]
    ) -> AsyncIterator[ListIndexesForMembersOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-explorer-2.html#ResourceExplorer.Paginator.ListIndexesForMembers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_explorer_2/paginators/#listindexesformemberspaginator)
        """

class ListSupportedResourceTypesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-explorer-2.html#ResourceExplorer.Paginator.ListSupportedResourceTypes)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_explorer_2/paginators/#listsupportedresourcetypespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListSupportedResourceTypesInputListSupportedResourceTypesPaginateTypeDef],
    ) -> AsyncIterator[ListSupportedResourceTypesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-explorer-2.html#ResourceExplorer.Paginator.ListSupportedResourceTypes.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_explorer_2/paginators/#listsupportedresourcetypespaginator)
        """

class ListViewsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-explorer-2.html#ResourceExplorer.Paginator.ListViews)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_explorer_2/paginators/#listviewspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListViewsInputListViewsPaginateTypeDef]
    ) -> AsyncIterator[ListViewsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-explorer-2.html#ResourceExplorer.Paginator.ListViews.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_explorer_2/paginators/#listviewspaginator)
        """

class SearchPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-explorer-2.html#ResourceExplorer.Paginator.Search)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_explorer_2/paginators/#searchpaginator)
    """
    def paginate(
        self, **kwargs: Unpack[SearchInputSearchPaginateTypeDef]
    ) -> AsyncIterator[SearchOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-explorer-2.html#ResourceExplorer.Paginator.Search.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_explorer_2/paginators/#searchpaginator)
        """
