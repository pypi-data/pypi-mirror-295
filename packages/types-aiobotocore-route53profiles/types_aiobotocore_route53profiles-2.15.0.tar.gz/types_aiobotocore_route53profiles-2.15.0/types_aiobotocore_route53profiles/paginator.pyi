"""
Type annotations for route53profiles service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53profiles/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_route53profiles.client import Route53ProfilesClient
    from types_aiobotocore_route53profiles.paginator import (
        ListProfileAssociationsPaginator,
        ListProfileResourceAssociationsPaginator,
        ListProfilesPaginator,
    )

    session = get_session()
    with session.create_client("route53profiles") as client:
        client: Route53ProfilesClient

        list_profile_associations_paginator: ListProfileAssociationsPaginator = client.get_paginator("list_profile_associations")
        list_profile_resource_associations_paginator: ListProfileResourceAssociationsPaginator = client.get_paginator("list_profile_resource_associations")
        list_profiles_paginator: ListProfilesPaginator = client.get_paginator("list_profiles")
    ```
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListProfileAssociationsRequestListProfileAssociationsPaginateTypeDef,
    ListProfileAssociationsResponseTypeDef,
    ListProfileResourceAssociationsRequestListProfileResourceAssociationsPaginateTypeDef,
    ListProfileResourceAssociationsResponseTypeDef,
    ListProfilesRequestListProfilesPaginateTypeDef,
    ListProfilesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListProfileAssociationsPaginator",
    "ListProfileResourceAssociationsPaginator",
    "ListProfilesPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListProfileAssociationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles.html#Route53Profiles.Paginator.ListProfileAssociations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53profiles/paginators/#listprofileassociationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListProfileAssociationsRequestListProfileAssociationsPaginateTypeDef]
    ) -> AsyncIterator[ListProfileAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles.html#Route53Profiles.Paginator.ListProfileAssociations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53profiles/paginators/#listprofileassociationspaginator)
        """

class ListProfileResourceAssociationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles.html#Route53Profiles.Paginator.ListProfileResourceAssociations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53profiles/paginators/#listprofileresourceassociationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListProfileResourceAssociationsRequestListProfileResourceAssociationsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListProfileResourceAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles.html#Route53Profiles.Paginator.ListProfileResourceAssociations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53profiles/paginators/#listprofileresourceassociationspaginator)
        """

class ListProfilesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles.html#Route53Profiles.Paginator.ListProfiles)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53profiles/paginators/#listprofilespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListProfilesRequestListProfilesPaginateTypeDef]
    ) -> AsyncIterator[ListProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53profiles.html#Route53Profiles.Paginator.ListProfiles.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53profiles/paginators/#listprofilespaginator)
        """
