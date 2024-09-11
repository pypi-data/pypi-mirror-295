"""
Type annotations for glue service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_glue.client import GlueClient
    from types_aiobotocore_glue.paginator import (
        GetClassifiersPaginator,
        GetConnectionsPaginator,
        GetCrawlerMetricsPaginator,
        GetCrawlersPaginator,
        GetDatabasesPaginator,
        GetDevEndpointsPaginator,
        GetJobRunsPaginator,
        GetJobsPaginator,
        GetPartitionIndexesPaginator,
        GetPartitionsPaginator,
        GetResourcePoliciesPaginator,
        GetSecurityConfigurationsPaginator,
        GetTableVersionsPaginator,
        GetTablesPaginator,
        GetTriggersPaginator,
        GetUserDefinedFunctionsPaginator,
        GetWorkflowRunsPaginator,
        ListBlueprintsPaginator,
        ListJobsPaginator,
        ListRegistriesPaginator,
        ListSchemaVersionsPaginator,
        ListSchemasPaginator,
        ListTriggersPaginator,
        ListUsageProfilesPaginator,
        ListWorkflowsPaginator,
    )

    session = get_session()
    with session.create_client("glue") as client:
        client: GlueClient

        get_classifiers_paginator: GetClassifiersPaginator = client.get_paginator("get_classifiers")
        get_connections_paginator: GetConnectionsPaginator = client.get_paginator("get_connections")
        get_crawler_metrics_paginator: GetCrawlerMetricsPaginator = client.get_paginator("get_crawler_metrics")
        get_crawlers_paginator: GetCrawlersPaginator = client.get_paginator("get_crawlers")
        get_databases_paginator: GetDatabasesPaginator = client.get_paginator("get_databases")
        get_dev_endpoints_paginator: GetDevEndpointsPaginator = client.get_paginator("get_dev_endpoints")
        get_job_runs_paginator: GetJobRunsPaginator = client.get_paginator("get_job_runs")
        get_jobs_paginator: GetJobsPaginator = client.get_paginator("get_jobs")
        get_partition_indexes_paginator: GetPartitionIndexesPaginator = client.get_paginator("get_partition_indexes")
        get_partitions_paginator: GetPartitionsPaginator = client.get_paginator("get_partitions")
        get_resource_policies_paginator: GetResourcePoliciesPaginator = client.get_paginator("get_resource_policies")
        get_security_configurations_paginator: GetSecurityConfigurationsPaginator = client.get_paginator("get_security_configurations")
        get_table_versions_paginator: GetTableVersionsPaginator = client.get_paginator("get_table_versions")
        get_tables_paginator: GetTablesPaginator = client.get_paginator("get_tables")
        get_triggers_paginator: GetTriggersPaginator = client.get_paginator("get_triggers")
        get_user_defined_functions_paginator: GetUserDefinedFunctionsPaginator = client.get_paginator("get_user_defined_functions")
        get_workflow_runs_paginator: GetWorkflowRunsPaginator = client.get_paginator("get_workflow_runs")
        list_blueprints_paginator: ListBlueprintsPaginator = client.get_paginator("list_blueprints")
        list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
        list_registries_paginator: ListRegistriesPaginator = client.get_paginator("list_registries")
        list_schema_versions_paginator: ListSchemaVersionsPaginator = client.get_paginator("list_schema_versions")
        list_schemas_paginator: ListSchemasPaginator = client.get_paginator("list_schemas")
        list_triggers_paginator: ListTriggersPaginator = client.get_paginator("list_triggers")
        list_usage_profiles_paginator: ListUsageProfilesPaginator = client.get_paginator("list_usage_profiles")
        list_workflows_paginator: ListWorkflowsPaginator = client.get_paginator("list_workflows")
    ```
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    GetClassifiersRequestGetClassifiersPaginateTypeDef,
    GetClassifiersResponseTypeDef,
    GetConnectionsRequestGetConnectionsPaginateTypeDef,
    GetConnectionsResponseTypeDef,
    GetCrawlerMetricsRequestGetCrawlerMetricsPaginateTypeDef,
    GetCrawlerMetricsResponseTypeDef,
    GetCrawlersRequestGetCrawlersPaginateTypeDef,
    GetCrawlersResponseTypeDef,
    GetDatabasesRequestGetDatabasesPaginateTypeDef,
    GetDatabasesResponseTypeDef,
    GetDevEndpointsRequestGetDevEndpointsPaginateTypeDef,
    GetDevEndpointsResponseTypeDef,
    GetJobRunsRequestGetJobRunsPaginateTypeDef,
    GetJobRunsResponseTypeDef,
    GetJobsRequestGetJobsPaginateTypeDef,
    GetJobsResponseTypeDef,
    GetPartitionIndexesRequestGetPartitionIndexesPaginateTypeDef,
    GetPartitionIndexesResponseTypeDef,
    GetPartitionsRequestGetPartitionsPaginateTypeDef,
    GetPartitionsResponseTypeDef,
    GetResourcePoliciesRequestGetResourcePoliciesPaginateTypeDef,
    GetResourcePoliciesResponseTypeDef,
    GetSecurityConfigurationsRequestGetSecurityConfigurationsPaginateTypeDef,
    GetSecurityConfigurationsResponseTypeDef,
    GetTablesRequestGetTablesPaginateTypeDef,
    GetTablesResponseTypeDef,
    GetTableVersionsRequestGetTableVersionsPaginateTypeDef,
    GetTableVersionsResponseTypeDef,
    GetTriggersRequestGetTriggersPaginateTypeDef,
    GetTriggersResponseTypeDef,
    GetUserDefinedFunctionsRequestGetUserDefinedFunctionsPaginateTypeDef,
    GetUserDefinedFunctionsResponseTypeDef,
    GetWorkflowRunsRequestGetWorkflowRunsPaginateTypeDef,
    GetWorkflowRunsResponseTypeDef,
    ListBlueprintsRequestListBlueprintsPaginateTypeDef,
    ListBlueprintsResponseTypeDef,
    ListJobsRequestListJobsPaginateTypeDef,
    ListJobsResponseTypeDef,
    ListRegistriesInputListRegistriesPaginateTypeDef,
    ListRegistriesResponseTypeDef,
    ListSchemasInputListSchemasPaginateTypeDef,
    ListSchemasResponseTypeDef,
    ListSchemaVersionsInputListSchemaVersionsPaginateTypeDef,
    ListSchemaVersionsResponseTypeDef,
    ListTriggersRequestListTriggersPaginateTypeDef,
    ListTriggersResponseTypeDef,
    ListUsageProfilesRequestListUsageProfilesPaginateTypeDef,
    ListUsageProfilesResponseTypeDef,
    ListWorkflowsRequestListWorkflowsPaginateTypeDef,
    ListWorkflowsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "GetClassifiersPaginator",
    "GetConnectionsPaginator",
    "GetCrawlerMetricsPaginator",
    "GetCrawlersPaginator",
    "GetDatabasesPaginator",
    "GetDevEndpointsPaginator",
    "GetJobRunsPaginator",
    "GetJobsPaginator",
    "GetPartitionIndexesPaginator",
    "GetPartitionsPaginator",
    "GetResourcePoliciesPaginator",
    "GetSecurityConfigurationsPaginator",
    "GetTableVersionsPaginator",
    "GetTablesPaginator",
    "GetTriggersPaginator",
    "GetUserDefinedFunctionsPaginator",
    "GetWorkflowRunsPaginator",
    "ListBlueprintsPaginator",
    "ListJobsPaginator",
    "ListRegistriesPaginator",
    "ListSchemaVersionsPaginator",
    "ListSchemasPaginator",
    "ListTriggersPaginator",
    "ListUsageProfilesPaginator",
    "ListWorkflowsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class GetClassifiersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Paginator.GetClassifiers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/paginators/#getclassifierspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetClassifiersRequestGetClassifiersPaginateTypeDef]
    ) -> AsyncIterator[GetClassifiersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Paginator.GetClassifiers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/paginators/#getclassifierspaginator)
        """

class GetConnectionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Paginator.GetConnections)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/paginators/#getconnectionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetConnectionsRequestGetConnectionsPaginateTypeDef]
    ) -> AsyncIterator[GetConnectionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Paginator.GetConnections.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/paginators/#getconnectionspaginator)
        """

class GetCrawlerMetricsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Paginator.GetCrawlerMetrics)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/paginators/#getcrawlermetricspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetCrawlerMetricsRequestGetCrawlerMetricsPaginateTypeDef]
    ) -> AsyncIterator[GetCrawlerMetricsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Paginator.GetCrawlerMetrics.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/paginators/#getcrawlermetricspaginator)
        """

class GetCrawlersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Paginator.GetCrawlers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/paginators/#getcrawlerspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetCrawlersRequestGetCrawlersPaginateTypeDef]
    ) -> AsyncIterator[GetCrawlersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Paginator.GetCrawlers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/paginators/#getcrawlerspaginator)
        """

class GetDatabasesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Paginator.GetDatabases)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/paginators/#getdatabasespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetDatabasesRequestGetDatabasesPaginateTypeDef]
    ) -> AsyncIterator[GetDatabasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Paginator.GetDatabases.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/paginators/#getdatabasespaginator)
        """

class GetDevEndpointsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Paginator.GetDevEndpoints)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/paginators/#getdevendpointspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetDevEndpointsRequestGetDevEndpointsPaginateTypeDef]
    ) -> AsyncIterator[GetDevEndpointsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Paginator.GetDevEndpoints.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/paginators/#getdevendpointspaginator)
        """

class GetJobRunsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Paginator.GetJobRuns)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/paginators/#getjobrunspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetJobRunsRequestGetJobRunsPaginateTypeDef]
    ) -> AsyncIterator[GetJobRunsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Paginator.GetJobRuns.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/paginators/#getjobrunspaginator)
        """

class GetJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Paginator.GetJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/paginators/#getjobspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetJobsRequestGetJobsPaginateTypeDef]
    ) -> AsyncIterator[GetJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Paginator.GetJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/paginators/#getjobspaginator)
        """

class GetPartitionIndexesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Paginator.GetPartitionIndexes)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/paginators/#getpartitionindexespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetPartitionIndexesRequestGetPartitionIndexesPaginateTypeDef]
    ) -> AsyncIterator[GetPartitionIndexesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Paginator.GetPartitionIndexes.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/paginators/#getpartitionindexespaginator)
        """

class GetPartitionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Paginator.GetPartitions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/paginators/#getpartitionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetPartitionsRequestGetPartitionsPaginateTypeDef]
    ) -> AsyncIterator[GetPartitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Paginator.GetPartitions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/paginators/#getpartitionspaginator)
        """

class GetResourcePoliciesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Paginator.GetResourcePolicies)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/paginators/#getresourcepoliciespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetResourcePoliciesRequestGetResourcePoliciesPaginateTypeDef]
    ) -> AsyncIterator[GetResourcePoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Paginator.GetResourcePolicies.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/paginators/#getresourcepoliciespaginator)
        """

class GetSecurityConfigurationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Paginator.GetSecurityConfigurations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/paginators/#getsecurityconfigurationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[GetSecurityConfigurationsRequestGetSecurityConfigurationsPaginateTypeDef],
    ) -> AsyncIterator[GetSecurityConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Paginator.GetSecurityConfigurations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/paginators/#getsecurityconfigurationspaginator)
        """

class GetTableVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Paginator.GetTableVersions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/paginators/#gettableversionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetTableVersionsRequestGetTableVersionsPaginateTypeDef]
    ) -> AsyncIterator[GetTableVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Paginator.GetTableVersions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/paginators/#gettableversionspaginator)
        """

class GetTablesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Paginator.GetTables)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/paginators/#gettablespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetTablesRequestGetTablesPaginateTypeDef]
    ) -> AsyncIterator[GetTablesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Paginator.GetTables.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/paginators/#gettablespaginator)
        """

class GetTriggersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Paginator.GetTriggers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/paginators/#gettriggerspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetTriggersRequestGetTriggersPaginateTypeDef]
    ) -> AsyncIterator[GetTriggersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Paginator.GetTriggers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/paginators/#gettriggerspaginator)
        """

class GetUserDefinedFunctionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Paginator.GetUserDefinedFunctions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/paginators/#getuserdefinedfunctionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetUserDefinedFunctionsRequestGetUserDefinedFunctionsPaginateTypeDef]
    ) -> AsyncIterator[GetUserDefinedFunctionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Paginator.GetUserDefinedFunctions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/paginators/#getuserdefinedfunctionspaginator)
        """

class GetWorkflowRunsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Paginator.GetWorkflowRuns)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/paginators/#getworkflowrunspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetWorkflowRunsRequestGetWorkflowRunsPaginateTypeDef]
    ) -> AsyncIterator[GetWorkflowRunsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Paginator.GetWorkflowRuns.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/paginators/#getworkflowrunspaginator)
        """

class ListBlueprintsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Paginator.ListBlueprints)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/paginators/#listblueprintspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListBlueprintsRequestListBlueprintsPaginateTypeDef]
    ) -> AsyncIterator[ListBlueprintsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Paginator.ListBlueprints.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/paginators/#listblueprintspaginator)
        """

class ListJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Paginator.ListJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/paginators/#listjobspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListJobsRequestListJobsPaginateTypeDef]
    ) -> AsyncIterator[ListJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Paginator.ListJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/paginators/#listjobspaginator)
        """

class ListRegistriesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Paginator.ListRegistries)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/paginators/#listregistriespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListRegistriesInputListRegistriesPaginateTypeDef]
    ) -> AsyncIterator[ListRegistriesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Paginator.ListRegistries.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/paginators/#listregistriespaginator)
        """

class ListSchemaVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Paginator.ListSchemaVersions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/paginators/#listschemaversionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSchemaVersionsInputListSchemaVersionsPaginateTypeDef]
    ) -> AsyncIterator[ListSchemaVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Paginator.ListSchemaVersions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/paginators/#listschemaversionspaginator)
        """

class ListSchemasPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Paginator.ListSchemas)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/paginators/#listschemaspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSchemasInputListSchemasPaginateTypeDef]
    ) -> AsyncIterator[ListSchemasResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Paginator.ListSchemas.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/paginators/#listschemaspaginator)
        """

class ListTriggersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Paginator.ListTriggers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/paginators/#listtriggerspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTriggersRequestListTriggersPaginateTypeDef]
    ) -> AsyncIterator[ListTriggersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Paginator.ListTriggers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/paginators/#listtriggerspaginator)
        """

class ListUsageProfilesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Paginator.ListUsageProfiles)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/paginators/#listusageprofilespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListUsageProfilesRequestListUsageProfilesPaginateTypeDef]
    ) -> AsyncIterator[ListUsageProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Paginator.ListUsageProfiles.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/paginators/#listusageprofilespaginator)
        """

class ListWorkflowsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Paginator.ListWorkflows)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/paginators/#listworkflowspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListWorkflowsRequestListWorkflowsPaginateTypeDef]
    ) -> AsyncIterator[ListWorkflowsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Paginator.ListWorkflows.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/paginators/#listworkflowspaginator)
        """
