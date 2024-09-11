"""
Type annotations for lakeformation service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_lakeformation.client import LakeFormationClient

    session = get_session()
    async with session.create_client("lakeformation") as client:
        client: LakeFormationClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import (
    GetWorkUnitsPaginator,
    ListDataCellsFilterPaginator,
    ListLFTagsPaginator,
    SearchDatabasesByLFTagsPaginator,
    SearchTablesByLFTagsPaginator,
)
from .type_defs import (
    AddLFTagsToResourceRequestRequestTypeDef,
    AddLFTagsToResourceResponseTypeDef,
    AssumeDecoratedRoleWithSAMLRequestRequestTypeDef,
    AssumeDecoratedRoleWithSAMLResponseTypeDef,
    BatchGrantPermissionsRequestRequestTypeDef,
    BatchGrantPermissionsResponseTypeDef,
    BatchRevokePermissionsRequestRequestTypeDef,
    BatchRevokePermissionsResponseTypeDef,
    CancelTransactionRequestRequestTypeDef,
    CommitTransactionRequestRequestTypeDef,
    CommitTransactionResponseTypeDef,
    CreateDataCellsFilterRequestRequestTypeDef,
    CreateLakeFormationIdentityCenterConfigurationRequestRequestTypeDef,
    CreateLakeFormationIdentityCenterConfigurationResponseTypeDef,
    CreateLakeFormationOptInRequestRequestTypeDef,
    CreateLFTagRequestRequestTypeDef,
    DeleteDataCellsFilterRequestRequestTypeDef,
    DeleteLakeFormationIdentityCenterConfigurationRequestRequestTypeDef,
    DeleteLakeFormationOptInRequestRequestTypeDef,
    DeleteLFTagRequestRequestTypeDef,
    DeleteObjectsOnCancelRequestRequestTypeDef,
    DeregisterResourceRequestRequestTypeDef,
    DescribeLakeFormationIdentityCenterConfigurationRequestRequestTypeDef,
    DescribeLakeFormationIdentityCenterConfigurationResponseTypeDef,
    DescribeResourceRequestRequestTypeDef,
    DescribeResourceResponseTypeDef,
    DescribeTransactionRequestRequestTypeDef,
    DescribeTransactionResponseTypeDef,
    ExtendTransactionRequestRequestTypeDef,
    GetDataCellsFilterRequestRequestTypeDef,
    GetDataCellsFilterResponseTypeDef,
    GetDataLakePrincipalResponseTypeDef,
    GetDataLakeSettingsRequestRequestTypeDef,
    GetDataLakeSettingsResponseTypeDef,
    GetEffectivePermissionsForPathRequestRequestTypeDef,
    GetEffectivePermissionsForPathResponseTypeDef,
    GetLFTagRequestRequestTypeDef,
    GetLFTagResponseTypeDef,
    GetQueryStateRequestRequestTypeDef,
    GetQueryStateResponseTypeDef,
    GetQueryStatisticsRequestRequestTypeDef,
    GetQueryStatisticsResponseTypeDef,
    GetResourceLFTagsRequestRequestTypeDef,
    GetResourceLFTagsResponseTypeDef,
    GetTableObjectsRequestRequestTypeDef,
    GetTableObjectsResponseTypeDef,
    GetTemporaryGluePartitionCredentialsRequestRequestTypeDef,
    GetTemporaryGluePartitionCredentialsResponseTypeDef,
    GetTemporaryGlueTableCredentialsRequestRequestTypeDef,
    GetTemporaryGlueTableCredentialsResponseTypeDef,
    GetWorkUnitResultsRequestRequestTypeDef,
    GetWorkUnitResultsResponseTypeDef,
    GetWorkUnitsRequestRequestTypeDef,
    GetWorkUnitsResponseTypeDef,
    GrantPermissionsRequestRequestTypeDef,
    ListDataCellsFilterRequestRequestTypeDef,
    ListDataCellsFilterResponseTypeDef,
    ListLakeFormationOptInsRequestRequestTypeDef,
    ListLakeFormationOptInsResponseTypeDef,
    ListLFTagsRequestRequestTypeDef,
    ListLFTagsResponseTypeDef,
    ListPermissionsRequestRequestTypeDef,
    ListPermissionsResponseTypeDef,
    ListResourcesRequestRequestTypeDef,
    ListResourcesResponseTypeDef,
    ListTableStorageOptimizersRequestRequestTypeDef,
    ListTableStorageOptimizersResponseTypeDef,
    ListTransactionsRequestRequestTypeDef,
    ListTransactionsResponseTypeDef,
    PutDataLakeSettingsRequestRequestTypeDef,
    RegisterResourceRequestRequestTypeDef,
    RemoveLFTagsFromResourceRequestRequestTypeDef,
    RemoveLFTagsFromResourceResponseTypeDef,
    RevokePermissionsRequestRequestTypeDef,
    SearchDatabasesByLFTagsRequestRequestTypeDef,
    SearchDatabasesByLFTagsResponseTypeDef,
    SearchTablesByLFTagsRequestRequestTypeDef,
    SearchTablesByLFTagsResponseTypeDef,
    StartQueryPlanningRequestRequestTypeDef,
    StartQueryPlanningResponseTypeDef,
    StartTransactionRequestRequestTypeDef,
    StartTransactionResponseTypeDef,
    UpdateDataCellsFilterRequestRequestTypeDef,
    UpdateLakeFormationIdentityCenterConfigurationRequestRequestTypeDef,
    UpdateLFTagRequestRequestTypeDef,
    UpdateResourceRequestRequestTypeDef,
    UpdateTableObjectsRequestRequestTypeDef,
    UpdateTableStorageOptimizerRequestRequestTypeDef,
    UpdateTableStorageOptimizerResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("LakeFormationClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    AlreadyExistsException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    EntityNotFoundException: Type[BotocoreClientError]
    ExpiredException: Type[BotocoreClientError]
    GlueEncryptionException: Type[BotocoreClientError]
    InternalServiceException: Type[BotocoreClientError]
    InvalidInputException: Type[BotocoreClientError]
    OperationTimeoutException: Type[BotocoreClientError]
    PermissionTypeMismatchException: Type[BotocoreClientError]
    ResourceNotReadyException: Type[BotocoreClientError]
    ResourceNumberLimitExceededException: Type[BotocoreClientError]
    StatisticsNotReadyYetException: Type[BotocoreClientError]
    ThrottledException: Type[BotocoreClientError]
    TransactionCanceledException: Type[BotocoreClientError]
    TransactionCommitInProgressException: Type[BotocoreClientError]
    TransactionCommittedException: Type[BotocoreClientError]
    WorkUnitsNotReadyYetException: Type[BotocoreClientError]


class LakeFormationClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        LakeFormationClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#exceptions)
        """

    async def add_lf_tags_to_resource(
        self, **kwargs: Unpack[AddLFTagsToResourceRequestRequestTypeDef]
    ) -> AddLFTagsToResourceResponseTypeDef:
        """
        Attaches one or more LF-tags to an existing resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.add_lf_tags_to_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#add_lf_tags_to_resource)
        """

    async def assume_decorated_role_with_saml(
        self, **kwargs: Unpack[AssumeDecoratedRoleWithSAMLRequestRequestTypeDef]
    ) -> AssumeDecoratedRoleWithSAMLResponseTypeDef:
        """
        Allows a caller to assume an IAM role decorated as the SAML user specified in
        the SAML assertion included in the
        request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.assume_decorated_role_with_saml)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#assume_decorated_role_with_saml)
        """

    async def batch_grant_permissions(
        self, **kwargs: Unpack[BatchGrantPermissionsRequestRequestTypeDef]
    ) -> BatchGrantPermissionsResponseTypeDef:
        """
        Batch operation to grant permissions to the principal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.batch_grant_permissions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#batch_grant_permissions)
        """

    async def batch_revoke_permissions(
        self, **kwargs: Unpack[BatchRevokePermissionsRequestRequestTypeDef]
    ) -> BatchRevokePermissionsResponseTypeDef:
        """
        Batch operation to revoke permissions from the principal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.batch_revoke_permissions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#batch_revoke_permissions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#can_paginate)
        """

    async def cancel_transaction(
        self, **kwargs: Unpack[CancelTransactionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Attempts to cancel the specified transaction.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.cancel_transaction)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#cancel_transaction)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#close)
        """

    async def commit_transaction(
        self, **kwargs: Unpack[CommitTransactionRequestRequestTypeDef]
    ) -> CommitTransactionResponseTypeDef:
        """
        Attempts to commit the specified transaction.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.commit_transaction)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#commit_transaction)
        """

    async def create_data_cells_filter(
        self, **kwargs: Unpack[CreateDataCellsFilterRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates a data cell filter to allow one to grant access to certain columns on
        certain
        rows.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.create_data_cells_filter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#create_data_cells_filter)
        """

    async def create_lake_formation_identity_center_configuration(
        self, **kwargs: Unpack[CreateLakeFormationIdentityCenterConfigurationRequestRequestTypeDef]
    ) -> CreateLakeFormationIdentityCenterConfigurationResponseTypeDef:
        """
        Creates an IAM Identity Center connection with Lake Formation to allow IAM
        Identity Center users and groups to access Data Catalog
        resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.create_lake_formation_identity_center_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#create_lake_formation_identity_center_configuration)
        """

    async def create_lake_formation_opt_in(
        self, **kwargs: Unpack[CreateLakeFormationOptInRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Enforce Lake Formation permissions for the given databases, tables, and
        principals.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.create_lake_formation_opt_in)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#create_lake_formation_opt_in)
        """

    async def create_lf_tag(
        self, **kwargs: Unpack[CreateLFTagRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates an LF-tag with the specified name and values.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.create_lf_tag)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#create_lf_tag)
        """

    async def delete_data_cells_filter(
        self, **kwargs: Unpack[DeleteDataCellsFilterRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a data cell filter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.delete_data_cells_filter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#delete_data_cells_filter)
        """

    async def delete_lake_formation_identity_center_configuration(
        self, **kwargs: Unpack[DeleteLakeFormationIdentityCenterConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an IAM Identity Center connection with Lake Formation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.delete_lake_formation_identity_center_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#delete_lake_formation_identity_center_configuration)
        """

    async def delete_lake_formation_opt_in(
        self, **kwargs: Unpack[DeleteLakeFormationOptInRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Remove the Lake Formation permissions enforcement of the given databases,
        tables, and
        principals.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.delete_lake_formation_opt_in)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#delete_lake_formation_opt_in)
        """

    async def delete_lf_tag(
        self, **kwargs: Unpack[DeleteLFTagRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified LF-tag given a key name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.delete_lf_tag)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#delete_lf_tag)
        """

    async def delete_objects_on_cancel(
        self, **kwargs: Unpack[DeleteObjectsOnCancelRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        For a specific governed table, provides a list of Amazon S3 objects that will
        be written during the current transaction and that can be automatically deleted
        if the transaction is
        canceled.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.delete_objects_on_cancel)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#delete_objects_on_cancel)
        """

    async def deregister_resource(
        self, **kwargs: Unpack[DeregisterResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deregisters the resource as managed by the Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.deregister_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#deregister_resource)
        """

    async def describe_lake_formation_identity_center_configuration(
        self,
        **kwargs: Unpack[DescribeLakeFormationIdentityCenterConfigurationRequestRequestTypeDef],
    ) -> DescribeLakeFormationIdentityCenterConfigurationResponseTypeDef:
        """
        Retrieves the instance ARN and application ARN for the connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.describe_lake_formation_identity_center_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#describe_lake_formation_identity_center_configuration)
        """

    async def describe_resource(
        self, **kwargs: Unpack[DescribeResourceRequestRequestTypeDef]
    ) -> DescribeResourceResponseTypeDef:
        """
        Retrieves the current data access role for the given resource registered in
        Lake
        Formation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.describe_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#describe_resource)
        """

    async def describe_transaction(
        self, **kwargs: Unpack[DescribeTransactionRequestRequestTypeDef]
    ) -> DescribeTransactionResponseTypeDef:
        """
        Returns the details of a single transaction.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.describe_transaction)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#describe_transaction)
        """

    async def extend_transaction(
        self, **kwargs: Unpack[ExtendTransactionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Indicates to the service that the specified transaction is still active and
        should not be treated as idle and
        aborted.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.extend_transaction)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#extend_transaction)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#generate_presigned_url)
        """

    async def get_data_cells_filter(
        self, **kwargs: Unpack[GetDataCellsFilterRequestRequestTypeDef]
    ) -> GetDataCellsFilterResponseTypeDef:
        """
        Returns a data cells filter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.get_data_cells_filter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#get_data_cells_filter)
        """

    async def get_data_lake_principal(self) -> GetDataLakePrincipalResponseTypeDef:
        """
        Returns the identity of the invoking principal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.get_data_lake_principal)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#get_data_lake_principal)
        """

    async def get_data_lake_settings(
        self, **kwargs: Unpack[GetDataLakeSettingsRequestRequestTypeDef]
    ) -> GetDataLakeSettingsResponseTypeDef:
        """
        Retrieves the list of the data lake administrators of a Lake Formation-managed
        data
        lake.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.get_data_lake_settings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#get_data_lake_settings)
        """

    async def get_effective_permissions_for_path(
        self, **kwargs: Unpack[GetEffectivePermissionsForPathRequestRequestTypeDef]
    ) -> GetEffectivePermissionsForPathResponseTypeDef:
        """
        Returns the Lake Formation permissions for a specified table or database
        resource located at a path in Amazon
        S3.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.get_effective_permissions_for_path)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#get_effective_permissions_for_path)
        """

    async def get_lf_tag(
        self, **kwargs: Unpack[GetLFTagRequestRequestTypeDef]
    ) -> GetLFTagResponseTypeDef:
        """
        Returns an LF-tag definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.get_lf_tag)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#get_lf_tag)
        """

    async def get_query_state(
        self, **kwargs: Unpack[GetQueryStateRequestRequestTypeDef]
    ) -> GetQueryStateResponseTypeDef:
        """
        Returns the state of a query previously submitted.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.get_query_state)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#get_query_state)
        """

    async def get_query_statistics(
        self, **kwargs: Unpack[GetQueryStatisticsRequestRequestTypeDef]
    ) -> GetQueryStatisticsResponseTypeDef:
        """
        Retrieves statistics on the planning and execution of a query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.get_query_statistics)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#get_query_statistics)
        """

    async def get_resource_lf_tags(
        self, **kwargs: Unpack[GetResourceLFTagsRequestRequestTypeDef]
    ) -> GetResourceLFTagsResponseTypeDef:
        """
        Returns the LF-tags applied to a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.get_resource_lf_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#get_resource_lf_tags)
        """

    async def get_table_objects(
        self, **kwargs: Unpack[GetTableObjectsRequestRequestTypeDef]
    ) -> GetTableObjectsResponseTypeDef:
        """
        Returns the set of Amazon S3 objects that make up the specified governed table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.get_table_objects)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#get_table_objects)
        """

    async def get_temporary_glue_partition_credentials(
        self, **kwargs: Unpack[GetTemporaryGluePartitionCredentialsRequestRequestTypeDef]
    ) -> GetTemporaryGluePartitionCredentialsResponseTypeDef:
        """
        This API is identical to `GetTemporaryTableCredentials` except that this is
        used when the target Data Catalog resource is of type
        Partition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.get_temporary_glue_partition_credentials)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#get_temporary_glue_partition_credentials)
        """

    async def get_temporary_glue_table_credentials(
        self, **kwargs: Unpack[GetTemporaryGlueTableCredentialsRequestRequestTypeDef]
    ) -> GetTemporaryGlueTableCredentialsResponseTypeDef:
        """
        Allows a caller in a secure environment to assume a role with permission to
        access Amazon
        S3.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.get_temporary_glue_table_credentials)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#get_temporary_glue_table_credentials)
        """

    async def get_work_unit_results(
        self, **kwargs: Unpack[GetWorkUnitResultsRequestRequestTypeDef]
    ) -> GetWorkUnitResultsResponseTypeDef:
        """
        Returns the work units resulting from the query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.get_work_unit_results)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#get_work_unit_results)
        """

    async def get_work_units(
        self, **kwargs: Unpack[GetWorkUnitsRequestRequestTypeDef]
    ) -> GetWorkUnitsResponseTypeDef:
        """
        Retrieves the work units generated by the `StartQueryPlanning` operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.get_work_units)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#get_work_units)
        """

    async def grant_permissions(
        self, **kwargs: Unpack[GrantPermissionsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Grants permissions to the principal to access metadata in the Data Catalog and
        data organized in underlying data storage such as Amazon
        S3.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.grant_permissions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#grant_permissions)
        """

    async def list_data_cells_filter(
        self, **kwargs: Unpack[ListDataCellsFilterRequestRequestTypeDef]
    ) -> ListDataCellsFilterResponseTypeDef:
        """
        Lists all the data cell filters on a table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.list_data_cells_filter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#list_data_cells_filter)
        """

    async def list_lake_formation_opt_ins(
        self, **kwargs: Unpack[ListLakeFormationOptInsRequestRequestTypeDef]
    ) -> ListLakeFormationOptInsResponseTypeDef:
        """
        Retrieve the current list of resources and principals that are opt in to
        enforce Lake Formation
        permissions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.list_lake_formation_opt_ins)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#list_lake_formation_opt_ins)
        """

    async def list_lf_tags(
        self, **kwargs: Unpack[ListLFTagsRequestRequestTypeDef]
    ) -> ListLFTagsResponseTypeDef:
        """
        Lists LF-tags that the requester has permission to view.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.list_lf_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#list_lf_tags)
        """

    async def list_permissions(
        self, **kwargs: Unpack[ListPermissionsRequestRequestTypeDef]
    ) -> ListPermissionsResponseTypeDef:
        """
        Returns a list of the principal permissions on the resource, filtered by the
        permissions of the
        caller.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.list_permissions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#list_permissions)
        """

    async def list_resources(
        self, **kwargs: Unpack[ListResourcesRequestRequestTypeDef]
    ) -> ListResourcesResponseTypeDef:
        """
        Lists the resources registered to be managed by the Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.list_resources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#list_resources)
        """

    async def list_table_storage_optimizers(
        self, **kwargs: Unpack[ListTableStorageOptimizersRequestRequestTypeDef]
    ) -> ListTableStorageOptimizersResponseTypeDef:
        """
        Returns the configuration of all storage optimizers associated with a specified
        table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.list_table_storage_optimizers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#list_table_storage_optimizers)
        """

    async def list_transactions(
        self, **kwargs: Unpack[ListTransactionsRequestRequestTypeDef]
    ) -> ListTransactionsResponseTypeDef:
        """
        Returns metadata about transactions and their status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.list_transactions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#list_transactions)
        """

    async def put_data_lake_settings(
        self, **kwargs: Unpack[PutDataLakeSettingsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Sets the list of data lake administrators who have admin privileges on all
        resources managed by Lake
        Formation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.put_data_lake_settings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#put_data_lake_settings)
        """

    async def register_resource(
        self, **kwargs: Unpack[RegisterResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Registers the resource as managed by the Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.register_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#register_resource)
        """

    async def remove_lf_tags_from_resource(
        self, **kwargs: Unpack[RemoveLFTagsFromResourceRequestRequestTypeDef]
    ) -> RemoveLFTagsFromResourceResponseTypeDef:
        """
        Removes an LF-tag from the resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.remove_lf_tags_from_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#remove_lf_tags_from_resource)
        """

    async def revoke_permissions(
        self, **kwargs: Unpack[RevokePermissionsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Revokes permissions to the principal to access metadata in the Data Catalog and
        data organized in underlying data storage such as Amazon
        S3.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.revoke_permissions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#revoke_permissions)
        """

    async def search_databases_by_lf_tags(
        self, **kwargs: Unpack[SearchDatabasesByLFTagsRequestRequestTypeDef]
    ) -> SearchDatabasesByLFTagsResponseTypeDef:
        """
        This operation allows a search on `DATABASE` resources by `TagCondition`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.search_databases_by_lf_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#search_databases_by_lf_tags)
        """

    async def search_tables_by_lf_tags(
        self, **kwargs: Unpack[SearchTablesByLFTagsRequestRequestTypeDef]
    ) -> SearchTablesByLFTagsResponseTypeDef:
        """
        This operation allows a search on `TABLE` resources by `LFTag`s.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.search_tables_by_lf_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#search_tables_by_lf_tags)
        """

    async def start_query_planning(
        self, **kwargs: Unpack[StartQueryPlanningRequestRequestTypeDef]
    ) -> StartQueryPlanningResponseTypeDef:
        """
        Submits a request to process a query statement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.start_query_planning)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#start_query_planning)
        """

    async def start_transaction(
        self, **kwargs: Unpack[StartTransactionRequestRequestTypeDef]
    ) -> StartTransactionResponseTypeDef:
        """
        Starts a new transaction and returns its transaction ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.start_transaction)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#start_transaction)
        """

    async def update_data_cells_filter(
        self, **kwargs: Unpack[UpdateDataCellsFilterRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates a data cell filter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.update_data_cells_filter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#update_data_cells_filter)
        """

    async def update_lake_formation_identity_center_configuration(
        self, **kwargs: Unpack[UpdateLakeFormationIdentityCenterConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the IAM Identity Center connection parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.update_lake_formation_identity_center_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#update_lake_formation_identity_center_configuration)
        """

    async def update_lf_tag(
        self, **kwargs: Unpack[UpdateLFTagRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the list of possible values for the specified LF-tag key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.update_lf_tag)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#update_lf_tag)
        """

    async def update_resource(
        self, **kwargs: Unpack[UpdateResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the data access role used for vending access to the given (registered)
        resource in Lake
        Formation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.update_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#update_resource)
        """

    async def update_table_objects(
        self, **kwargs: Unpack[UpdateTableObjectsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the manifest of Amazon S3 objects that make up the specified governed
        table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.update_table_objects)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#update_table_objects)
        """

    async def update_table_storage_optimizer(
        self, **kwargs: Unpack[UpdateTableStorageOptimizerRequestRequestTypeDef]
    ) -> UpdateTableStorageOptimizerResponseTypeDef:
        """
        Updates the configuration of the storage optimizers for a table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.update_table_storage_optimizer)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#update_table_storage_optimizer)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_work_units"]) -> GetWorkUnitsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_data_cells_filter"]
    ) -> ListDataCellsFilterPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_lf_tags"]) -> ListLFTagsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["search_databases_by_lf_tags"]
    ) -> SearchDatabasesByLFTagsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["search_tables_by_lf_tags"]
    ) -> SearchTablesByLFTagsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/#get_paginator)
        """

    async def __aenter__(self) -> "LakeFormationClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lakeformation/client/)
        """
