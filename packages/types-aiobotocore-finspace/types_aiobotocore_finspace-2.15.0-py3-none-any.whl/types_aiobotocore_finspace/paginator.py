"""
Type annotations for finspace service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_finspace.client import FinspaceClient
    from types_aiobotocore_finspace.paginator import (
        ListKxEnvironmentsPaginator,
    )

    session = get_session()
    with session.create_client("finspace") as client:
        client: FinspaceClient

        list_kx_environments_paginator: ListKxEnvironmentsPaginator = client.get_paginator("list_kx_environments")
    ```
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListKxEnvironmentsRequestListKxEnvironmentsPaginateTypeDef,
    ListKxEnvironmentsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListKxEnvironmentsPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListKxEnvironmentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Paginator.ListKxEnvironments)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/paginators/#listkxenvironmentspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListKxEnvironmentsRequestListKxEnvironmentsPaginateTypeDef]
    ) -> AsyncIterator[ListKxEnvironmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace.html#Finspace.Paginator.ListKxEnvironments.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/paginators/#listkxenvironmentspaginator)
        """
