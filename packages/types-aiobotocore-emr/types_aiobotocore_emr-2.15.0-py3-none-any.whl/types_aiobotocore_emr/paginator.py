"""
Type annotations for emr service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_emr.client import EMRClient
    from types_aiobotocore_emr.paginator import (
        ListBootstrapActionsPaginator,
        ListClustersPaginator,
        ListInstanceFleetsPaginator,
        ListInstanceGroupsPaginator,
        ListInstancesPaginator,
        ListNotebookExecutionsPaginator,
        ListSecurityConfigurationsPaginator,
        ListStepsPaginator,
        ListStudioSessionMappingsPaginator,
        ListStudiosPaginator,
    )

    session = get_session()
    with session.create_client("emr") as client:
        client: EMRClient

        list_bootstrap_actions_paginator: ListBootstrapActionsPaginator = client.get_paginator("list_bootstrap_actions")
        list_clusters_paginator: ListClustersPaginator = client.get_paginator("list_clusters")
        list_instance_fleets_paginator: ListInstanceFleetsPaginator = client.get_paginator("list_instance_fleets")
        list_instance_groups_paginator: ListInstanceGroupsPaginator = client.get_paginator("list_instance_groups")
        list_instances_paginator: ListInstancesPaginator = client.get_paginator("list_instances")
        list_notebook_executions_paginator: ListNotebookExecutionsPaginator = client.get_paginator("list_notebook_executions")
        list_security_configurations_paginator: ListSecurityConfigurationsPaginator = client.get_paginator("list_security_configurations")
        list_steps_paginator: ListStepsPaginator = client.get_paginator("list_steps")
        list_studio_session_mappings_paginator: ListStudioSessionMappingsPaginator = client.get_paginator("list_studio_session_mappings")
        list_studios_paginator: ListStudiosPaginator = client.get_paginator("list_studios")
    ```
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListBootstrapActionsInputListBootstrapActionsPaginateTypeDef,
    ListBootstrapActionsOutputTypeDef,
    ListClustersInputListClustersPaginateTypeDef,
    ListClustersOutputTypeDef,
    ListInstanceFleetsInputListInstanceFleetsPaginateTypeDef,
    ListInstanceFleetsOutputTypeDef,
    ListInstanceGroupsInputListInstanceGroupsPaginateTypeDef,
    ListInstanceGroupsOutputTypeDef,
    ListInstancesInputListInstancesPaginateTypeDef,
    ListInstancesOutputTypeDef,
    ListNotebookExecutionsInputListNotebookExecutionsPaginateTypeDef,
    ListNotebookExecutionsOutputTypeDef,
    ListSecurityConfigurationsInputListSecurityConfigurationsPaginateTypeDef,
    ListSecurityConfigurationsOutputTypeDef,
    ListStepsInputListStepsPaginateTypeDef,
    ListStepsOutputTypeDef,
    ListStudioSessionMappingsInputListStudioSessionMappingsPaginateTypeDef,
    ListStudioSessionMappingsOutputTypeDef,
    ListStudiosInputListStudiosPaginateTypeDef,
    ListStudiosOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListBootstrapActionsPaginator",
    "ListClustersPaginator",
    "ListInstanceFleetsPaginator",
    "ListInstanceGroupsPaginator",
    "ListInstancesPaginator",
    "ListNotebookExecutionsPaginator",
    "ListSecurityConfigurationsPaginator",
    "ListStepsPaginator",
    "ListStudioSessionMappingsPaginator",
    "ListStudiosPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListBootstrapActionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Paginator.ListBootstrapActions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr/paginators/#listbootstrapactionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListBootstrapActionsInputListBootstrapActionsPaginateTypeDef]
    ) -> AsyncIterator[ListBootstrapActionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Paginator.ListBootstrapActions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr/paginators/#listbootstrapactionspaginator)
        """


class ListClustersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Paginator.ListClusters)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr/paginators/#listclusterspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListClustersInputListClustersPaginateTypeDef]
    ) -> AsyncIterator[ListClustersOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Paginator.ListClusters.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr/paginators/#listclusterspaginator)
        """


class ListInstanceFleetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Paginator.ListInstanceFleets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr/paginators/#listinstancefleetspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListInstanceFleetsInputListInstanceFleetsPaginateTypeDef]
    ) -> AsyncIterator[ListInstanceFleetsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Paginator.ListInstanceFleets.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr/paginators/#listinstancefleetspaginator)
        """


class ListInstanceGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Paginator.ListInstanceGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr/paginators/#listinstancegroupspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListInstanceGroupsInputListInstanceGroupsPaginateTypeDef]
    ) -> AsyncIterator[ListInstanceGroupsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Paginator.ListInstanceGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr/paginators/#listinstancegroupspaginator)
        """


class ListInstancesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Paginator.ListInstances)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr/paginators/#listinstancespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListInstancesInputListInstancesPaginateTypeDef]
    ) -> AsyncIterator[ListInstancesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Paginator.ListInstances.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr/paginators/#listinstancespaginator)
        """


class ListNotebookExecutionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Paginator.ListNotebookExecutions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr/paginators/#listnotebookexecutionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListNotebookExecutionsInputListNotebookExecutionsPaginateTypeDef]
    ) -> AsyncIterator[ListNotebookExecutionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Paginator.ListNotebookExecutions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr/paginators/#listnotebookexecutionspaginator)
        """


class ListSecurityConfigurationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Paginator.ListSecurityConfigurations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr/paginators/#listsecurityconfigurationspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListSecurityConfigurationsInputListSecurityConfigurationsPaginateTypeDef],
    ) -> AsyncIterator[ListSecurityConfigurationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Paginator.ListSecurityConfigurations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr/paginators/#listsecurityconfigurationspaginator)
        """


class ListStepsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Paginator.ListSteps)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr/paginators/#liststepspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListStepsInputListStepsPaginateTypeDef]
    ) -> AsyncIterator[ListStepsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Paginator.ListSteps.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr/paginators/#liststepspaginator)
        """


class ListStudioSessionMappingsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Paginator.ListStudioSessionMappings)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr/paginators/#liststudiosessionmappingspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListStudioSessionMappingsInputListStudioSessionMappingsPaginateTypeDef],
    ) -> AsyncIterator[ListStudioSessionMappingsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Paginator.ListStudioSessionMappings.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr/paginators/#liststudiosessionmappingspaginator)
        """


class ListStudiosPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Paginator.ListStudios)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr/paginators/#liststudiospaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListStudiosInputListStudiosPaginateTypeDef]
    ) -> AsyncIterator[ListStudiosOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Paginator.ListStudios.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr/paginators/#liststudiospaginator)
        """
