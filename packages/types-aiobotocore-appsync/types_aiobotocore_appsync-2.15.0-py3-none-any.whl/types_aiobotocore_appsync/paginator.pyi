"""
Type annotations for appsync service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_appsync.client import AppSyncClient
    from types_aiobotocore_appsync.paginator import (
        ListApiKeysPaginator,
        ListDataSourcesPaginator,
        ListDomainNamesPaginator,
        ListFunctionsPaginator,
        ListGraphqlApisPaginator,
        ListResolversPaginator,
        ListResolversByFunctionPaginator,
        ListSourceApiAssociationsPaginator,
        ListTypesPaginator,
        ListTypesByAssociationPaginator,
    )

    session = get_session()
    with session.create_client("appsync") as client:
        client: AppSyncClient

        list_api_keys_paginator: ListApiKeysPaginator = client.get_paginator("list_api_keys")
        list_data_sources_paginator: ListDataSourcesPaginator = client.get_paginator("list_data_sources")
        list_domain_names_paginator: ListDomainNamesPaginator = client.get_paginator("list_domain_names")
        list_functions_paginator: ListFunctionsPaginator = client.get_paginator("list_functions")
        list_graphql_apis_paginator: ListGraphqlApisPaginator = client.get_paginator("list_graphql_apis")
        list_resolvers_paginator: ListResolversPaginator = client.get_paginator("list_resolvers")
        list_resolvers_by_function_paginator: ListResolversByFunctionPaginator = client.get_paginator("list_resolvers_by_function")
        list_source_api_associations_paginator: ListSourceApiAssociationsPaginator = client.get_paginator("list_source_api_associations")
        list_types_paginator: ListTypesPaginator = client.get_paginator("list_types")
        list_types_by_association_paginator: ListTypesByAssociationPaginator = client.get_paginator("list_types_by_association")
    ```
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListApiKeysRequestListApiKeysPaginateTypeDef,
    ListApiKeysResponseTypeDef,
    ListDataSourcesRequestListDataSourcesPaginateTypeDef,
    ListDataSourcesResponseTypeDef,
    ListDomainNamesRequestListDomainNamesPaginateTypeDef,
    ListDomainNamesResponseTypeDef,
    ListFunctionsRequestListFunctionsPaginateTypeDef,
    ListFunctionsResponseTypeDef,
    ListGraphqlApisRequestListGraphqlApisPaginateTypeDef,
    ListGraphqlApisResponseTypeDef,
    ListResolversByFunctionRequestListResolversByFunctionPaginateTypeDef,
    ListResolversByFunctionResponseTypeDef,
    ListResolversRequestListResolversPaginateTypeDef,
    ListResolversResponseTypeDef,
    ListSourceApiAssociationsRequestListSourceApiAssociationsPaginateTypeDef,
    ListSourceApiAssociationsResponseTypeDef,
    ListTypesByAssociationRequestListTypesByAssociationPaginateTypeDef,
    ListTypesByAssociationResponseTypeDef,
    ListTypesRequestListTypesPaginateTypeDef,
    ListTypesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListApiKeysPaginator",
    "ListDataSourcesPaginator",
    "ListDomainNamesPaginator",
    "ListFunctionsPaginator",
    "ListGraphqlApisPaginator",
    "ListResolversPaginator",
    "ListResolversByFunctionPaginator",
    "ListSourceApiAssociationsPaginator",
    "ListTypesPaginator",
    "ListTypesByAssociationPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListApiKeysPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Paginator.ListApiKeys)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/paginators/#listapikeyspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListApiKeysRequestListApiKeysPaginateTypeDef]
    ) -> AsyncIterator[ListApiKeysResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Paginator.ListApiKeys.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/paginators/#listapikeyspaginator)
        """

class ListDataSourcesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Paginator.ListDataSources)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/paginators/#listdatasourcespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDataSourcesRequestListDataSourcesPaginateTypeDef]
    ) -> AsyncIterator[ListDataSourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Paginator.ListDataSources.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/paginators/#listdatasourcespaginator)
        """

class ListDomainNamesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Paginator.ListDomainNames)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/paginators/#listdomainnamespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDomainNamesRequestListDomainNamesPaginateTypeDef]
    ) -> AsyncIterator[ListDomainNamesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Paginator.ListDomainNames.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/paginators/#listdomainnamespaginator)
        """

class ListFunctionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Paginator.ListFunctions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/paginators/#listfunctionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListFunctionsRequestListFunctionsPaginateTypeDef]
    ) -> AsyncIterator[ListFunctionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Paginator.ListFunctions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/paginators/#listfunctionspaginator)
        """

class ListGraphqlApisPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Paginator.ListGraphqlApis)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/paginators/#listgraphqlapispaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListGraphqlApisRequestListGraphqlApisPaginateTypeDef]
    ) -> AsyncIterator[ListGraphqlApisResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Paginator.ListGraphqlApis.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/paginators/#listgraphqlapispaginator)
        """

class ListResolversPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Paginator.ListResolvers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/paginators/#listresolverspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListResolversRequestListResolversPaginateTypeDef]
    ) -> AsyncIterator[ListResolversResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Paginator.ListResolvers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/paginators/#listresolverspaginator)
        """

class ListResolversByFunctionPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Paginator.ListResolversByFunction)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/paginators/#listresolversbyfunctionpaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListResolversByFunctionRequestListResolversByFunctionPaginateTypeDef]
    ) -> AsyncIterator[ListResolversByFunctionResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Paginator.ListResolversByFunction.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/paginators/#listresolversbyfunctionpaginator)
        """

class ListSourceApiAssociationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Paginator.ListSourceApiAssociations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/paginators/#listsourceapiassociationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListSourceApiAssociationsRequestListSourceApiAssociationsPaginateTypeDef],
    ) -> AsyncIterator[ListSourceApiAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Paginator.ListSourceApiAssociations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/paginators/#listsourceapiassociationspaginator)
        """

class ListTypesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Paginator.ListTypes)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/paginators/#listtypespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTypesRequestListTypesPaginateTypeDef]
    ) -> AsyncIterator[ListTypesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Paginator.ListTypes.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/paginators/#listtypespaginator)
        """

class ListTypesByAssociationPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Paginator.ListTypesByAssociation)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/paginators/#listtypesbyassociationpaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTypesByAssociationRequestListTypesByAssociationPaginateTypeDef]
    ) -> AsyncIterator[ListTypesByAssociationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appsync.html#AppSync.Paginator.ListTypesByAssociation.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appsync/paginators/#listtypesbyassociationpaginator)
        """
