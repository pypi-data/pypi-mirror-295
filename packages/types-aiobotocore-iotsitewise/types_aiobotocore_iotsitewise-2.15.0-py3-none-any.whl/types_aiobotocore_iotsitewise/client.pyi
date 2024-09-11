"""
Type annotations for iotsitewise service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_iotsitewise.client import IoTSiteWiseClient

    session = get_session()
    async with session.create_client("iotsitewise") as client:
        client: IoTSiteWiseClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import (
    ExecuteQueryPaginator,
    GetAssetPropertyAggregatesPaginator,
    GetAssetPropertyValueHistoryPaginator,
    GetInterpolatedAssetPropertyValuesPaginator,
    ListAccessPoliciesPaginator,
    ListActionsPaginator,
    ListAssetModelCompositeModelsPaginator,
    ListAssetModelPropertiesPaginator,
    ListAssetModelsPaginator,
    ListAssetPropertiesPaginator,
    ListAssetRelationshipsPaginator,
    ListAssetsPaginator,
    ListAssociatedAssetsPaginator,
    ListBulkImportJobsPaginator,
    ListCompositionRelationshipsPaginator,
    ListDashboardsPaginator,
    ListGatewaysPaginator,
    ListPortalsPaginator,
    ListProjectAssetsPaginator,
    ListProjectsPaginator,
    ListTimeSeriesPaginator,
)
from .type_defs import (
    AssociateAssetsRequestRequestTypeDef,
    AssociateTimeSeriesToAssetPropertyRequestRequestTypeDef,
    BatchAssociateProjectAssetsRequestRequestTypeDef,
    BatchAssociateProjectAssetsResponseTypeDef,
    BatchDisassociateProjectAssetsRequestRequestTypeDef,
    BatchDisassociateProjectAssetsResponseTypeDef,
    BatchGetAssetPropertyAggregatesRequestRequestTypeDef,
    BatchGetAssetPropertyAggregatesResponseTypeDef,
    BatchGetAssetPropertyValueHistoryRequestRequestTypeDef,
    BatchGetAssetPropertyValueHistoryResponseTypeDef,
    BatchGetAssetPropertyValueRequestRequestTypeDef,
    BatchGetAssetPropertyValueResponseTypeDef,
    BatchPutAssetPropertyValueRequestRequestTypeDef,
    BatchPutAssetPropertyValueResponseTypeDef,
    CreateAccessPolicyRequestRequestTypeDef,
    CreateAccessPolicyResponseTypeDef,
    CreateAssetModelCompositeModelRequestRequestTypeDef,
    CreateAssetModelCompositeModelResponseTypeDef,
    CreateAssetModelRequestRequestTypeDef,
    CreateAssetModelResponseTypeDef,
    CreateAssetRequestRequestTypeDef,
    CreateAssetResponseTypeDef,
    CreateBulkImportJobRequestRequestTypeDef,
    CreateBulkImportJobResponseTypeDef,
    CreateDashboardRequestRequestTypeDef,
    CreateDashboardResponseTypeDef,
    CreateGatewayRequestRequestTypeDef,
    CreateGatewayResponseTypeDef,
    CreatePortalRequestRequestTypeDef,
    CreatePortalResponseTypeDef,
    CreateProjectRequestRequestTypeDef,
    CreateProjectResponseTypeDef,
    DeleteAccessPolicyRequestRequestTypeDef,
    DeleteAssetModelCompositeModelRequestRequestTypeDef,
    DeleteAssetModelCompositeModelResponseTypeDef,
    DeleteAssetModelRequestRequestTypeDef,
    DeleteAssetModelResponseTypeDef,
    DeleteAssetRequestRequestTypeDef,
    DeleteAssetResponseTypeDef,
    DeleteDashboardRequestRequestTypeDef,
    DeleteGatewayRequestRequestTypeDef,
    DeletePortalRequestRequestTypeDef,
    DeletePortalResponseTypeDef,
    DeleteProjectRequestRequestTypeDef,
    DeleteTimeSeriesRequestRequestTypeDef,
    DescribeAccessPolicyRequestRequestTypeDef,
    DescribeAccessPolicyResponseTypeDef,
    DescribeActionRequestRequestTypeDef,
    DescribeActionResponseTypeDef,
    DescribeAssetCompositeModelRequestRequestTypeDef,
    DescribeAssetCompositeModelResponseTypeDef,
    DescribeAssetModelCompositeModelRequestRequestTypeDef,
    DescribeAssetModelCompositeModelResponseTypeDef,
    DescribeAssetModelRequestRequestTypeDef,
    DescribeAssetModelResponseTypeDef,
    DescribeAssetPropertyRequestRequestTypeDef,
    DescribeAssetPropertyResponseTypeDef,
    DescribeAssetRequestRequestTypeDef,
    DescribeAssetResponseTypeDef,
    DescribeBulkImportJobRequestRequestTypeDef,
    DescribeBulkImportJobResponseTypeDef,
    DescribeDashboardRequestRequestTypeDef,
    DescribeDashboardResponseTypeDef,
    DescribeDefaultEncryptionConfigurationResponseTypeDef,
    DescribeGatewayCapabilityConfigurationRequestRequestTypeDef,
    DescribeGatewayCapabilityConfigurationResponseTypeDef,
    DescribeGatewayRequestRequestTypeDef,
    DescribeGatewayResponseTypeDef,
    DescribeLoggingOptionsResponseTypeDef,
    DescribePortalRequestRequestTypeDef,
    DescribePortalResponseTypeDef,
    DescribeProjectRequestRequestTypeDef,
    DescribeProjectResponseTypeDef,
    DescribeStorageConfigurationResponseTypeDef,
    DescribeTimeSeriesRequestRequestTypeDef,
    DescribeTimeSeriesResponseTypeDef,
    DisassociateAssetsRequestRequestTypeDef,
    DisassociateTimeSeriesFromAssetPropertyRequestRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    ExecuteActionRequestRequestTypeDef,
    ExecuteActionResponseTypeDef,
    ExecuteQueryRequestRequestTypeDef,
    ExecuteQueryResponseTypeDef,
    GetAssetPropertyAggregatesRequestRequestTypeDef,
    GetAssetPropertyAggregatesResponseTypeDef,
    GetAssetPropertyValueHistoryRequestRequestTypeDef,
    GetAssetPropertyValueHistoryResponseTypeDef,
    GetAssetPropertyValueRequestRequestTypeDef,
    GetAssetPropertyValueResponseTypeDef,
    GetInterpolatedAssetPropertyValuesRequestRequestTypeDef,
    GetInterpolatedAssetPropertyValuesResponseTypeDef,
    ListAccessPoliciesRequestRequestTypeDef,
    ListAccessPoliciesResponseTypeDef,
    ListActionsRequestRequestTypeDef,
    ListActionsResponseTypeDef,
    ListAssetModelCompositeModelsRequestRequestTypeDef,
    ListAssetModelCompositeModelsResponseTypeDef,
    ListAssetModelPropertiesRequestRequestTypeDef,
    ListAssetModelPropertiesResponseTypeDef,
    ListAssetModelsRequestRequestTypeDef,
    ListAssetModelsResponseTypeDef,
    ListAssetPropertiesRequestRequestTypeDef,
    ListAssetPropertiesResponseTypeDef,
    ListAssetRelationshipsRequestRequestTypeDef,
    ListAssetRelationshipsResponseTypeDef,
    ListAssetsRequestRequestTypeDef,
    ListAssetsResponseTypeDef,
    ListAssociatedAssetsRequestRequestTypeDef,
    ListAssociatedAssetsResponseTypeDef,
    ListBulkImportJobsRequestRequestTypeDef,
    ListBulkImportJobsResponseTypeDef,
    ListCompositionRelationshipsRequestRequestTypeDef,
    ListCompositionRelationshipsResponseTypeDef,
    ListDashboardsRequestRequestTypeDef,
    ListDashboardsResponseTypeDef,
    ListGatewaysRequestRequestTypeDef,
    ListGatewaysResponseTypeDef,
    ListPortalsRequestRequestTypeDef,
    ListPortalsResponseTypeDef,
    ListProjectAssetsRequestRequestTypeDef,
    ListProjectAssetsResponseTypeDef,
    ListProjectsRequestRequestTypeDef,
    ListProjectsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTimeSeriesRequestRequestTypeDef,
    ListTimeSeriesResponseTypeDef,
    PutDefaultEncryptionConfigurationRequestRequestTypeDef,
    PutDefaultEncryptionConfigurationResponseTypeDef,
    PutLoggingOptionsRequestRequestTypeDef,
    PutStorageConfigurationRequestRequestTypeDef,
    PutStorageConfigurationResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateAccessPolicyRequestRequestTypeDef,
    UpdateAssetModelCompositeModelRequestRequestTypeDef,
    UpdateAssetModelCompositeModelResponseTypeDef,
    UpdateAssetModelRequestRequestTypeDef,
    UpdateAssetModelResponseTypeDef,
    UpdateAssetPropertyRequestRequestTypeDef,
    UpdateAssetRequestRequestTypeDef,
    UpdateAssetResponseTypeDef,
    UpdateDashboardRequestRequestTypeDef,
    UpdateGatewayCapabilityConfigurationRequestRequestTypeDef,
    UpdateGatewayCapabilityConfigurationResponseTypeDef,
    UpdateGatewayRequestRequestTypeDef,
    UpdatePortalRequestRequestTypeDef,
    UpdatePortalResponseTypeDef,
    UpdateProjectRequestRequestTypeDef,
)
from .waiter import (
    AssetActiveWaiter,
    AssetModelActiveWaiter,
    AssetModelNotExistsWaiter,
    AssetNotExistsWaiter,
    PortalActiveWaiter,
    PortalNotExistsWaiter,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("IoTSiteWiseClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictingOperationException: Type[BotocoreClientError]
    InternalFailureException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    PreconditionFailedException: Type[BotocoreClientError]
    QueryTimeoutException: Type[BotocoreClientError]
    ResourceAlreadyExistsException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]
    UnauthorizedException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class IoTSiteWiseClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        IoTSiteWiseClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#exceptions)
        """

    async def associate_assets(
        self, **kwargs: Unpack[AssociateAssetsRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Associates a child asset with the given parent asset through a hierarchy
        defined in the parent asset's
        model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.associate_assets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#associate_assets)
        """

    async def associate_time_series_to_asset_property(
        self, **kwargs: Unpack[AssociateTimeSeriesToAssetPropertyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Associates a time series (data stream) with an asset property.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.associate_time_series_to_asset_property)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#associate_time_series_to_asset_property)
        """

    async def batch_associate_project_assets(
        self, **kwargs: Unpack[BatchAssociateProjectAssetsRequestRequestTypeDef]
    ) -> BatchAssociateProjectAssetsResponseTypeDef:
        """
        Associates a group (batch) of assets with an IoT SiteWise Monitor project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.batch_associate_project_assets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#batch_associate_project_assets)
        """

    async def batch_disassociate_project_assets(
        self, **kwargs: Unpack[BatchDisassociateProjectAssetsRequestRequestTypeDef]
    ) -> BatchDisassociateProjectAssetsResponseTypeDef:
        """
        Disassociates a group (batch) of assets from an IoT SiteWise Monitor project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.batch_disassociate_project_assets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#batch_disassociate_project_assets)
        """

    async def batch_get_asset_property_aggregates(
        self, **kwargs: Unpack[BatchGetAssetPropertyAggregatesRequestRequestTypeDef]
    ) -> BatchGetAssetPropertyAggregatesResponseTypeDef:
        """
        Gets aggregated values (for example, average, minimum, and maximum) for one or
        more asset
        properties.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.batch_get_asset_property_aggregates)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#batch_get_asset_property_aggregates)
        """

    async def batch_get_asset_property_value(
        self, **kwargs: Unpack[BatchGetAssetPropertyValueRequestRequestTypeDef]
    ) -> BatchGetAssetPropertyValueResponseTypeDef:
        """
        Gets the current value for one or more asset properties.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.batch_get_asset_property_value)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#batch_get_asset_property_value)
        """

    async def batch_get_asset_property_value_history(
        self, **kwargs: Unpack[BatchGetAssetPropertyValueHistoryRequestRequestTypeDef]
    ) -> BatchGetAssetPropertyValueHistoryResponseTypeDef:
        """
        Gets the historical values for one or more asset properties.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.batch_get_asset_property_value_history)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#batch_get_asset_property_value_history)
        """

    async def batch_put_asset_property_value(
        self, **kwargs: Unpack[BatchPutAssetPropertyValueRequestRequestTypeDef]
    ) -> BatchPutAssetPropertyValueResponseTypeDef:
        """
        Sends a list of asset property values to IoT SiteWise.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.batch_put_asset_property_value)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#batch_put_asset_property_value)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#close)
        """

    async def create_access_policy(
        self, **kwargs: Unpack[CreateAccessPolicyRequestRequestTypeDef]
    ) -> CreateAccessPolicyResponseTypeDef:
        """
        Creates an access policy that grants the specified identity (IAM Identity
        Center user, IAM Identity Center group, or IAM user) access to the specified
        IoT SiteWise Monitor portal or project
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.create_access_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#create_access_policy)
        """

    async def create_asset(
        self, **kwargs: Unpack[CreateAssetRequestRequestTypeDef]
    ) -> CreateAssetResponseTypeDef:
        """
        Creates an asset from an existing asset model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.create_asset)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#create_asset)
        """

    async def create_asset_model(
        self, **kwargs: Unpack[CreateAssetModelRequestRequestTypeDef]
    ) -> CreateAssetModelResponseTypeDef:
        """
        Creates an asset model from specified property and hierarchy definitions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.create_asset_model)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#create_asset_model)
        """

    async def create_asset_model_composite_model(
        self, **kwargs: Unpack[CreateAssetModelCompositeModelRequestRequestTypeDef]
    ) -> CreateAssetModelCompositeModelResponseTypeDef:
        """
        Creates a custom composite model from specified property and hierarchy
        definitions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.create_asset_model_composite_model)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#create_asset_model_composite_model)
        """

    async def create_bulk_import_job(
        self, **kwargs: Unpack[CreateBulkImportJobRequestRequestTypeDef]
    ) -> CreateBulkImportJobResponseTypeDef:
        """
        Defines a job to ingest data to IoT SiteWise from Amazon S3.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.create_bulk_import_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#create_bulk_import_job)
        """

    async def create_dashboard(
        self, **kwargs: Unpack[CreateDashboardRequestRequestTypeDef]
    ) -> CreateDashboardResponseTypeDef:
        """
        Creates a dashboard in an IoT SiteWise Monitor project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.create_dashboard)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#create_dashboard)
        """

    async def create_gateway(
        self, **kwargs: Unpack[CreateGatewayRequestRequestTypeDef]
    ) -> CreateGatewayResponseTypeDef:
        """
        Creates a gateway, which is a virtual or edge device that delivers industrial
        data streams from local servers to IoT
        SiteWise.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.create_gateway)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#create_gateway)
        """

    async def create_portal(
        self, **kwargs: Unpack[CreatePortalRequestRequestTypeDef]
    ) -> CreatePortalResponseTypeDef:
        """
        Creates a portal, which can contain projects and dashboards.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.create_portal)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#create_portal)
        """

    async def create_project(
        self, **kwargs: Unpack[CreateProjectRequestRequestTypeDef]
    ) -> CreateProjectResponseTypeDef:
        """
        Creates a project in the specified portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.create_project)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#create_project)
        """

    async def delete_access_policy(
        self, **kwargs: Unpack[DeleteAccessPolicyRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an access policy that grants the specified identity access to the
        specified IoT SiteWise Monitor
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.delete_access_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#delete_access_policy)
        """

    async def delete_asset(
        self, **kwargs: Unpack[DeleteAssetRequestRequestTypeDef]
    ) -> DeleteAssetResponseTypeDef:
        """
        Deletes an asset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.delete_asset)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#delete_asset)
        """

    async def delete_asset_model(
        self, **kwargs: Unpack[DeleteAssetModelRequestRequestTypeDef]
    ) -> DeleteAssetModelResponseTypeDef:
        """
        Deletes an asset model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.delete_asset_model)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#delete_asset_model)
        """

    async def delete_asset_model_composite_model(
        self, **kwargs: Unpack[DeleteAssetModelCompositeModelRequestRequestTypeDef]
    ) -> DeleteAssetModelCompositeModelResponseTypeDef:
        """
        Deletes a composite model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.delete_asset_model_composite_model)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#delete_asset_model_composite_model)
        """

    async def delete_dashboard(
        self, **kwargs: Unpack[DeleteDashboardRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a dashboard from IoT SiteWise Monitor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.delete_dashboard)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#delete_dashboard)
        """

    async def delete_gateway(
        self, **kwargs: Unpack[DeleteGatewayRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a gateway from IoT SiteWise.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.delete_gateway)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#delete_gateway)
        """

    async def delete_portal(
        self, **kwargs: Unpack[DeletePortalRequestRequestTypeDef]
    ) -> DeletePortalResponseTypeDef:
        """
        Deletes a portal from IoT SiteWise Monitor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.delete_portal)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#delete_portal)
        """

    async def delete_project(
        self, **kwargs: Unpack[DeleteProjectRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a project from IoT SiteWise Monitor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.delete_project)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#delete_project)
        """

    async def delete_time_series(
        self, **kwargs: Unpack[DeleteTimeSeriesRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a time series (data stream).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.delete_time_series)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#delete_time_series)
        """

    async def describe_access_policy(
        self, **kwargs: Unpack[DescribeAccessPolicyRequestRequestTypeDef]
    ) -> DescribeAccessPolicyResponseTypeDef:
        """
        Describes an access policy, which specifies an identity's access to an IoT
        SiteWise Monitor portal or
        project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.describe_access_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#describe_access_policy)
        """

    async def describe_action(
        self, **kwargs: Unpack[DescribeActionRequestRequestTypeDef]
    ) -> DescribeActionResponseTypeDef:
        """
        Retrieves information about an action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.describe_action)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#describe_action)
        """

    async def describe_asset(
        self, **kwargs: Unpack[DescribeAssetRequestRequestTypeDef]
    ) -> DescribeAssetResponseTypeDef:
        """
        Retrieves information about an asset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.describe_asset)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#describe_asset)
        """

    async def describe_asset_composite_model(
        self, **kwargs: Unpack[DescribeAssetCompositeModelRequestRequestTypeDef]
    ) -> DescribeAssetCompositeModelResponseTypeDef:
        """
        Retrieves information about an asset composite model (also known as an asset
        component).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.describe_asset_composite_model)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#describe_asset_composite_model)
        """

    async def describe_asset_model(
        self, **kwargs: Unpack[DescribeAssetModelRequestRequestTypeDef]
    ) -> DescribeAssetModelResponseTypeDef:
        """
        Retrieves information about an asset model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.describe_asset_model)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#describe_asset_model)
        """

    async def describe_asset_model_composite_model(
        self, **kwargs: Unpack[DescribeAssetModelCompositeModelRequestRequestTypeDef]
    ) -> DescribeAssetModelCompositeModelResponseTypeDef:
        """
        Retrieves information about an asset model composite model (also known as an
        asset model
        component).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.describe_asset_model_composite_model)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#describe_asset_model_composite_model)
        """

    async def describe_asset_property(
        self, **kwargs: Unpack[DescribeAssetPropertyRequestRequestTypeDef]
    ) -> DescribeAssetPropertyResponseTypeDef:
        """
        Retrieves information about an asset property.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.describe_asset_property)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#describe_asset_property)
        """

    async def describe_bulk_import_job(
        self, **kwargs: Unpack[DescribeBulkImportJobRequestRequestTypeDef]
    ) -> DescribeBulkImportJobResponseTypeDef:
        """
        Retrieves information about a bulk import job request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.describe_bulk_import_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#describe_bulk_import_job)
        """

    async def describe_dashboard(
        self, **kwargs: Unpack[DescribeDashboardRequestRequestTypeDef]
    ) -> DescribeDashboardResponseTypeDef:
        """
        Retrieves information about a dashboard.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.describe_dashboard)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#describe_dashboard)
        """

    async def describe_default_encryption_configuration(
        self,
    ) -> DescribeDefaultEncryptionConfigurationResponseTypeDef:
        """
        Retrieves information about the default encryption configuration for the Amazon
        Web Services account in the default or specified
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.describe_default_encryption_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#describe_default_encryption_configuration)
        """

    async def describe_gateway(
        self, **kwargs: Unpack[DescribeGatewayRequestRequestTypeDef]
    ) -> DescribeGatewayResponseTypeDef:
        """
        Retrieves information about a gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.describe_gateway)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#describe_gateway)
        """

    async def describe_gateway_capability_configuration(
        self, **kwargs: Unpack[DescribeGatewayCapabilityConfigurationRequestRequestTypeDef]
    ) -> DescribeGatewayCapabilityConfigurationResponseTypeDef:
        """
        Retrieves information about a gateway capability configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.describe_gateway_capability_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#describe_gateway_capability_configuration)
        """

    async def describe_logging_options(self) -> DescribeLoggingOptionsResponseTypeDef:
        """
        Retrieves the current IoT SiteWise logging options.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.describe_logging_options)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#describe_logging_options)
        """

    async def describe_portal(
        self, **kwargs: Unpack[DescribePortalRequestRequestTypeDef]
    ) -> DescribePortalResponseTypeDef:
        """
        Retrieves information about a portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.describe_portal)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#describe_portal)
        """

    async def describe_project(
        self, **kwargs: Unpack[DescribeProjectRequestRequestTypeDef]
    ) -> DescribeProjectResponseTypeDef:
        """
        Retrieves information about a project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.describe_project)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#describe_project)
        """

    async def describe_storage_configuration(self) -> DescribeStorageConfigurationResponseTypeDef:
        """
        Retrieves information about the storage configuration for IoT SiteWise.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.describe_storage_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#describe_storage_configuration)
        """

    async def describe_time_series(
        self, **kwargs: Unpack[DescribeTimeSeriesRequestRequestTypeDef]
    ) -> DescribeTimeSeriesResponseTypeDef:
        """
        Retrieves information about a time series (data stream).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.describe_time_series)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#describe_time_series)
        """

    async def disassociate_assets(
        self, **kwargs: Unpack[DisassociateAssetsRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Disassociates a child asset from the given parent asset through a hierarchy
        defined in the parent asset's
        model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.disassociate_assets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#disassociate_assets)
        """

    async def disassociate_time_series_from_asset_property(
        self, **kwargs: Unpack[DisassociateTimeSeriesFromAssetPropertyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Disassociates a time series (data stream) from an asset property.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.disassociate_time_series_from_asset_property)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#disassociate_time_series_from_asset_property)
        """

    async def execute_action(
        self, **kwargs: Unpack[ExecuteActionRequestRequestTypeDef]
    ) -> ExecuteActionResponseTypeDef:
        """
        Executes an action on a target resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.execute_action)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#execute_action)
        """

    async def execute_query(
        self, **kwargs: Unpack[ExecuteQueryRequestRequestTypeDef]
    ) -> ExecuteQueryResponseTypeDef:
        """
        Run SQL queries to retrieve metadata and time-series data from asset models,
        assets, measurements, metrics, transforms, and
        aggregates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.execute_query)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#execute_query)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#generate_presigned_url)
        """

    async def get_asset_property_aggregates(
        self, **kwargs: Unpack[GetAssetPropertyAggregatesRequestRequestTypeDef]
    ) -> GetAssetPropertyAggregatesResponseTypeDef:
        """
        Gets aggregated values for an asset property.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.get_asset_property_aggregates)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#get_asset_property_aggregates)
        """

    async def get_asset_property_value(
        self, **kwargs: Unpack[GetAssetPropertyValueRequestRequestTypeDef]
    ) -> GetAssetPropertyValueResponseTypeDef:
        """
        Gets an asset property's current value.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.get_asset_property_value)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#get_asset_property_value)
        """

    async def get_asset_property_value_history(
        self, **kwargs: Unpack[GetAssetPropertyValueHistoryRequestRequestTypeDef]
    ) -> GetAssetPropertyValueHistoryResponseTypeDef:
        """
        Gets the history of an asset property's values.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.get_asset_property_value_history)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#get_asset_property_value_history)
        """

    async def get_interpolated_asset_property_values(
        self, **kwargs: Unpack[GetInterpolatedAssetPropertyValuesRequestRequestTypeDef]
    ) -> GetInterpolatedAssetPropertyValuesResponseTypeDef:
        """
        Get interpolated values for an asset property for a specified time interval,
        during a period of
        time.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.get_interpolated_asset_property_values)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#get_interpolated_asset_property_values)
        """

    async def list_access_policies(
        self, **kwargs: Unpack[ListAccessPoliciesRequestRequestTypeDef]
    ) -> ListAccessPoliciesResponseTypeDef:
        """
        Retrieves a paginated list of access policies for an identity (an IAM Identity
        Center user, an IAM Identity Center group, or an IAM user) or an IoT SiteWise
        Monitor resource (a portal or
        project).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.list_access_policies)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#list_access_policies)
        """

    async def list_actions(
        self, **kwargs: Unpack[ListActionsRequestRequestTypeDef]
    ) -> ListActionsResponseTypeDef:
        """
        Retrieves a paginated list of actions for a specific target resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.list_actions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#list_actions)
        """

    async def list_asset_model_composite_models(
        self, **kwargs: Unpack[ListAssetModelCompositeModelsRequestRequestTypeDef]
    ) -> ListAssetModelCompositeModelsResponseTypeDef:
        """
        Retrieves a paginated list of composite models associated with the asset model
        See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/iotsitewise-2019-12-02/ListAssetModelCompositeModels).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.list_asset_model_composite_models)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#list_asset_model_composite_models)
        """

    async def list_asset_model_properties(
        self, **kwargs: Unpack[ListAssetModelPropertiesRequestRequestTypeDef]
    ) -> ListAssetModelPropertiesResponseTypeDef:
        """
        Retrieves a paginated list of properties associated with an asset model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.list_asset_model_properties)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#list_asset_model_properties)
        """

    async def list_asset_models(
        self, **kwargs: Unpack[ListAssetModelsRequestRequestTypeDef]
    ) -> ListAssetModelsResponseTypeDef:
        """
        Retrieves a paginated list of summaries of all asset models.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.list_asset_models)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#list_asset_models)
        """

    async def list_asset_properties(
        self, **kwargs: Unpack[ListAssetPropertiesRequestRequestTypeDef]
    ) -> ListAssetPropertiesResponseTypeDef:
        """
        Retrieves a paginated list of properties associated with an asset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.list_asset_properties)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#list_asset_properties)
        """

    async def list_asset_relationships(
        self, **kwargs: Unpack[ListAssetRelationshipsRequestRequestTypeDef]
    ) -> ListAssetRelationshipsResponseTypeDef:
        """
        Retrieves a paginated list of asset relationships for an asset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.list_asset_relationships)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#list_asset_relationships)
        """

    async def list_assets(
        self, **kwargs: Unpack[ListAssetsRequestRequestTypeDef]
    ) -> ListAssetsResponseTypeDef:
        """
        Retrieves a paginated list of asset summaries.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.list_assets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#list_assets)
        """

    async def list_associated_assets(
        self, **kwargs: Unpack[ListAssociatedAssetsRequestRequestTypeDef]
    ) -> ListAssociatedAssetsResponseTypeDef:
        """
        Retrieves a paginated list of associated assets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.list_associated_assets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#list_associated_assets)
        """

    async def list_bulk_import_jobs(
        self, **kwargs: Unpack[ListBulkImportJobsRequestRequestTypeDef]
    ) -> ListBulkImportJobsResponseTypeDef:
        """
        Retrieves a paginated list of bulk import job requests.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.list_bulk_import_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#list_bulk_import_jobs)
        """

    async def list_composition_relationships(
        self, **kwargs: Unpack[ListCompositionRelationshipsRequestRequestTypeDef]
    ) -> ListCompositionRelationshipsResponseTypeDef:
        """
        Retrieves a paginated list of composition relationships for an asset model of
        type
        `COMPONENT_MODEL`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.list_composition_relationships)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#list_composition_relationships)
        """

    async def list_dashboards(
        self, **kwargs: Unpack[ListDashboardsRequestRequestTypeDef]
    ) -> ListDashboardsResponseTypeDef:
        """
        Retrieves a paginated list of dashboards for an IoT SiteWise Monitor project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.list_dashboards)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#list_dashboards)
        """

    async def list_gateways(
        self, **kwargs: Unpack[ListGatewaysRequestRequestTypeDef]
    ) -> ListGatewaysResponseTypeDef:
        """
        Retrieves a paginated list of gateways.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.list_gateways)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#list_gateways)
        """

    async def list_portals(
        self, **kwargs: Unpack[ListPortalsRequestRequestTypeDef]
    ) -> ListPortalsResponseTypeDef:
        """
        Retrieves a paginated list of IoT SiteWise Monitor portals.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.list_portals)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#list_portals)
        """

    async def list_project_assets(
        self, **kwargs: Unpack[ListProjectAssetsRequestRequestTypeDef]
    ) -> ListProjectAssetsResponseTypeDef:
        """
        Retrieves a paginated list of assets associated with an IoT SiteWise Monitor
        project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.list_project_assets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#list_project_assets)
        """

    async def list_projects(
        self, **kwargs: Unpack[ListProjectsRequestRequestTypeDef]
    ) -> ListProjectsResponseTypeDef:
        """
        Retrieves a paginated list of projects for an IoT SiteWise Monitor portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.list_projects)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#list_projects)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Retrieves the list of tags for an IoT SiteWise resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#list_tags_for_resource)
        """

    async def list_time_series(
        self, **kwargs: Unpack[ListTimeSeriesRequestRequestTypeDef]
    ) -> ListTimeSeriesResponseTypeDef:
        """
        Retrieves a paginated list of time series (data streams).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.list_time_series)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#list_time_series)
        """

    async def put_default_encryption_configuration(
        self, **kwargs: Unpack[PutDefaultEncryptionConfigurationRequestRequestTypeDef]
    ) -> PutDefaultEncryptionConfigurationResponseTypeDef:
        """
        Sets the default encryption configuration for the Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.put_default_encryption_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#put_default_encryption_configuration)
        """

    async def put_logging_options(
        self, **kwargs: Unpack[PutLoggingOptionsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Sets logging options for IoT SiteWise.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.put_logging_options)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#put_logging_options)
        """

    async def put_storage_configuration(
        self, **kwargs: Unpack[PutStorageConfigurationRequestRequestTypeDef]
    ) -> PutStorageConfigurationResponseTypeDef:
        """
        Configures storage settings for IoT SiteWise.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.put_storage_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#put_storage_configuration)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Adds tags to an IoT SiteWise resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes a tag from an IoT SiteWise resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#untag_resource)
        """

    async def update_access_policy(
        self, **kwargs: Unpack[UpdateAccessPolicyRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates an existing access policy that specifies an identity's access to an IoT
        SiteWise Monitor portal or project
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.update_access_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#update_access_policy)
        """

    async def update_asset(
        self, **kwargs: Unpack[UpdateAssetRequestRequestTypeDef]
    ) -> UpdateAssetResponseTypeDef:
        """
        Updates an asset's name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.update_asset)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#update_asset)
        """

    async def update_asset_model(
        self, **kwargs: Unpack[UpdateAssetModelRequestRequestTypeDef]
    ) -> UpdateAssetModelResponseTypeDef:
        """
        Updates an asset model and all of the assets that were created from the model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.update_asset_model)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#update_asset_model)
        """

    async def update_asset_model_composite_model(
        self, **kwargs: Unpack[UpdateAssetModelCompositeModelRequestRequestTypeDef]
    ) -> UpdateAssetModelCompositeModelResponseTypeDef:
        """
        Updates a composite model and all of the assets that were created from the
        model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.update_asset_model_composite_model)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#update_asset_model_composite_model)
        """

    async def update_asset_property(
        self, **kwargs: Unpack[UpdateAssetPropertyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates an asset property's alias and notification state.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.update_asset_property)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#update_asset_property)
        """

    async def update_dashboard(
        self, **kwargs: Unpack[UpdateDashboardRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates an IoT SiteWise Monitor dashboard.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.update_dashboard)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#update_dashboard)
        """

    async def update_gateway(
        self, **kwargs: Unpack[UpdateGatewayRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates a gateway's name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.update_gateway)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#update_gateway)
        """

    async def update_gateway_capability_configuration(
        self, **kwargs: Unpack[UpdateGatewayCapabilityConfigurationRequestRequestTypeDef]
    ) -> UpdateGatewayCapabilityConfigurationResponseTypeDef:
        """
        Updates a gateway capability configuration or defines a new capability
        configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.update_gateway_capability_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#update_gateway_capability_configuration)
        """

    async def update_portal(
        self, **kwargs: Unpack[UpdatePortalRequestRequestTypeDef]
    ) -> UpdatePortalResponseTypeDef:
        """
        Updates an IoT SiteWise Monitor portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.update_portal)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#update_portal)
        """

    async def update_project(
        self, **kwargs: Unpack[UpdateProjectRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates an IoT SiteWise Monitor project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.update_project)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#update_project)
        """

    @overload
    def get_paginator(self, operation_name: Literal["execute_query"]) -> ExecuteQueryPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_asset_property_aggregates"]
    ) -> GetAssetPropertyAggregatesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_asset_property_value_history"]
    ) -> GetAssetPropertyValueHistoryPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_interpolated_asset_property_values"]
    ) -> GetInterpolatedAssetPropertyValuesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_access_policies"]
    ) -> ListAccessPoliciesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_actions"]) -> ListActionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_asset_model_composite_models"]
    ) -> ListAssetModelCompositeModelsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_asset_model_properties"]
    ) -> ListAssetModelPropertiesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_asset_models"]
    ) -> ListAssetModelsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_asset_properties"]
    ) -> ListAssetPropertiesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_asset_relationships"]
    ) -> ListAssetRelationshipsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_assets"]) -> ListAssetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_associated_assets"]
    ) -> ListAssociatedAssetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_bulk_import_jobs"]
    ) -> ListBulkImportJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_composition_relationships"]
    ) -> ListCompositionRelationshipsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_dashboards"]) -> ListDashboardsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_gateways"]) -> ListGatewaysPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_portals"]) -> ListPortalsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_project_assets"]
    ) -> ListProjectAssetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_projects"]) -> ListProjectsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_time_series"]) -> ListTimeSeriesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#get_paginator)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["asset_active"]) -> AssetActiveWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["asset_model_active"]) -> AssetModelActiveWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["asset_model_not_exists"]
    ) -> AssetModelNotExistsWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["asset_not_exists"]) -> AssetNotExistsWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["portal_active"]) -> PortalActiveWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["portal_not_exists"]) -> PortalNotExistsWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/#get_waiter)
        """

    async def __aenter__(self) -> "IoTSiteWiseClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise.html#IoTSiteWise.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/client/)
        """
