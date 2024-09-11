"""
Type annotations for iotfleethub service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleethub/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_iotfleethub.client import IoTFleetHubClient
    from types_aiobotocore_iotfleethub.paginator import (
        ListApplicationsPaginator,
    )

    session = get_session()
    with session.create_client("iotfleethub") as client:
        client: IoTFleetHubClient

        list_applications_paginator: ListApplicationsPaginator = client.get_paginator("list_applications")
    ```
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListApplicationsRequestListApplicationsPaginateTypeDef,
    ListApplicationsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListApplicationsPaginator",)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListApplicationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleethub.html#IoTFleetHub.Paginator.ListApplications)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleethub/paginators/#listapplicationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListApplicationsRequestListApplicationsPaginateTypeDef]
    ) -> AsyncIterator[ListApplicationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleethub.html#IoTFleetHub.Paginator.ListApplications.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleethub/paginators/#listapplicationspaginator)
        """
