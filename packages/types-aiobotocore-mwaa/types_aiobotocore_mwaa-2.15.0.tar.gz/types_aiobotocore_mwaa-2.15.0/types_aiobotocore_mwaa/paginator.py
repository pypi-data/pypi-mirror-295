"""
Type annotations for mwaa service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mwaa/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_mwaa.client import MWAAClient
    from types_aiobotocore_mwaa.paginator import (
        ListEnvironmentsPaginator,
    )

    session = get_session()
    with session.create_client("mwaa") as client:
        client: MWAAClient

        list_environments_paginator: ListEnvironmentsPaginator = client.get_paginator("list_environments")
    ```
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListEnvironmentsInputListEnvironmentsPaginateTypeDef,
    ListEnvironmentsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListEnvironmentsPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListEnvironmentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mwaa.html#MWAA.Paginator.ListEnvironments)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mwaa/paginators/#listenvironmentspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListEnvironmentsInputListEnvironmentsPaginateTypeDef]
    ) -> AsyncIterator[ListEnvironmentsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mwaa.html#MWAA.Paginator.ListEnvironments.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mwaa/paginators/#listenvironmentspaginator)
        """
