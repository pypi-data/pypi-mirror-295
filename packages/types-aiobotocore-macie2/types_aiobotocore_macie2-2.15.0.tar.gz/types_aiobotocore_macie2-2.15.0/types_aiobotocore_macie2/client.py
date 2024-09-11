"""
Type annotations for macie2 service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_macie2.client import Macie2Client

    session = get_session()
    async with session.create_client("macie2") as client:
        client: Macie2Client
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import (
    DescribeBucketsPaginator,
    GetUsageStatisticsPaginator,
    ListAllowListsPaginator,
    ListAutomatedDiscoveryAccountsPaginator,
    ListClassificationJobsPaginator,
    ListClassificationScopesPaginator,
    ListCustomDataIdentifiersPaginator,
    ListFindingsFiltersPaginator,
    ListFindingsPaginator,
    ListInvitationsPaginator,
    ListManagedDataIdentifiersPaginator,
    ListMembersPaginator,
    ListOrganizationAdminAccountsPaginator,
    ListResourceProfileArtifactsPaginator,
    ListResourceProfileDetectionsPaginator,
    ListSensitivityInspectionTemplatesPaginator,
    SearchResourcesPaginator,
)
from .type_defs import (
    AcceptInvitationRequestRequestTypeDef,
    BatchGetCustomDataIdentifiersRequestRequestTypeDef,
    BatchGetCustomDataIdentifiersResponseTypeDef,
    BatchUpdateAutomatedDiscoveryAccountsRequestRequestTypeDef,
    BatchUpdateAutomatedDiscoveryAccountsResponseTypeDef,
    CreateAllowListRequestRequestTypeDef,
    CreateAllowListResponseTypeDef,
    CreateClassificationJobRequestRequestTypeDef,
    CreateClassificationJobResponseTypeDef,
    CreateCustomDataIdentifierRequestRequestTypeDef,
    CreateCustomDataIdentifierResponseTypeDef,
    CreateFindingsFilterRequestRequestTypeDef,
    CreateFindingsFilterResponseTypeDef,
    CreateInvitationsRequestRequestTypeDef,
    CreateInvitationsResponseTypeDef,
    CreateMemberRequestRequestTypeDef,
    CreateMemberResponseTypeDef,
    CreateSampleFindingsRequestRequestTypeDef,
    DeclineInvitationsRequestRequestTypeDef,
    DeclineInvitationsResponseTypeDef,
    DeleteAllowListRequestRequestTypeDef,
    DeleteCustomDataIdentifierRequestRequestTypeDef,
    DeleteFindingsFilterRequestRequestTypeDef,
    DeleteInvitationsRequestRequestTypeDef,
    DeleteInvitationsResponseTypeDef,
    DeleteMemberRequestRequestTypeDef,
    DescribeBucketsRequestRequestTypeDef,
    DescribeBucketsResponseTypeDef,
    DescribeClassificationJobRequestRequestTypeDef,
    DescribeClassificationJobResponseTypeDef,
    DescribeOrganizationConfigurationResponseTypeDef,
    DisableOrganizationAdminAccountRequestRequestTypeDef,
    DisassociateMemberRequestRequestTypeDef,
    EnableMacieRequestRequestTypeDef,
    EnableOrganizationAdminAccountRequestRequestTypeDef,
    GetAdministratorAccountResponseTypeDef,
    GetAllowListRequestRequestTypeDef,
    GetAllowListResponseTypeDef,
    GetAutomatedDiscoveryConfigurationResponseTypeDef,
    GetBucketStatisticsRequestRequestTypeDef,
    GetBucketStatisticsResponseTypeDef,
    GetClassificationExportConfigurationResponseTypeDef,
    GetClassificationScopeRequestRequestTypeDef,
    GetClassificationScopeResponseTypeDef,
    GetCustomDataIdentifierRequestRequestTypeDef,
    GetCustomDataIdentifierResponseTypeDef,
    GetFindingsFilterRequestRequestTypeDef,
    GetFindingsFilterResponseTypeDef,
    GetFindingsPublicationConfigurationResponseTypeDef,
    GetFindingsRequestRequestTypeDef,
    GetFindingsResponseTypeDef,
    GetFindingStatisticsRequestRequestTypeDef,
    GetFindingStatisticsResponseTypeDef,
    GetInvitationsCountResponseTypeDef,
    GetMacieSessionResponseTypeDef,
    GetMasterAccountResponseTypeDef,
    GetMemberRequestRequestTypeDef,
    GetMemberResponseTypeDef,
    GetResourceProfileRequestRequestTypeDef,
    GetResourceProfileResponseTypeDef,
    GetRevealConfigurationResponseTypeDef,
    GetSensitiveDataOccurrencesAvailabilityRequestRequestTypeDef,
    GetSensitiveDataOccurrencesAvailabilityResponseTypeDef,
    GetSensitiveDataOccurrencesRequestRequestTypeDef,
    GetSensitiveDataOccurrencesResponseTypeDef,
    GetSensitivityInspectionTemplateRequestRequestTypeDef,
    GetSensitivityInspectionTemplateResponseTypeDef,
    GetUsageStatisticsRequestRequestTypeDef,
    GetUsageStatisticsResponseTypeDef,
    GetUsageTotalsRequestRequestTypeDef,
    GetUsageTotalsResponseTypeDef,
    ListAllowListsRequestRequestTypeDef,
    ListAllowListsResponseTypeDef,
    ListAutomatedDiscoveryAccountsRequestRequestTypeDef,
    ListAutomatedDiscoveryAccountsResponseTypeDef,
    ListClassificationJobsRequestRequestTypeDef,
    ListClassificationJobsResponseTypeDef,
    ListClassificationScopesRequestRequestTypeDef,
    ListClassificationScopesResponseTypeDef,
    ListCustomDataIdentifiersRequestRequestTypeDef,
    ListCustomDataIdentifiersResponseTypeDef,
    ListFindingsFiltersRequestRequestTypeDef,
    ListFindingsFiltersResponseTypeDef,
    ListFindingsRequestRequestTypeDef,
    ListFindingsResponseTypeDef,
    ListInvitationsRequestRequestTypeDef,
    ListInvitationsResponseTypeDef,
    ListManagedDataIdentifiersRequestRequestTypeDef,
    ListManagedDataIdentifiersResponseTypeDef,
    ListMembersRequestRequestTypeDef,
    ListMembersResponseTypeDef,
    ListOrganizationAdminAccountsRequestRequestTypeDef,
    ListOrganizationAdminAccountsResponseTypeDef,
    ListResourceProfileArtifactsRequestRequestTypeDef,
    ListResourceProfileArtifactsResponseTypeDef,
    ListResourceProfileDetectionsRequestRequestTypeDef,
    ListResourceProfileDetectionsResponseTypeDef,
    ListSensitivityInspectionTemplatesRequestRequestTypeDef,
    ListSensitivityInspectionTemplatesResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PutClassificationExportConfigurationRequestRequestTypeDef,
    PutClassificationExportConfigurationResponseTypeDef,
    PutFindingsPublicationConfigurationRequestRequestTypeDef,
    SearchResourcesRequestRequestTypeDef,
    SearchResourcesResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    TestCustomDataIdentifierRequestRequestTypeDef,
    TestCustomDataIdentifierResponseTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateAllowListRequestRequestTypeDef,
    UpdateAllowListResponseTypeDef,
    UpdateAutomatedDiscoveryConfigurationRequestRequestTypeDef,
    UpdateClassificationJobRequestRequestTypeDef,
    UpdateClassificationScopeRequestRequestTypeDef,
    UpdateFindingsFilterRequestRequestTypeDef,
    UpdateFindingsFilterResponseTypeDef,
    UpdateMacieSessionRequestRequestTypeDef,
    UpdateMemberSessionRequestRequestTypeDef,
    UpdateOrganizationConfigurationRequestRequestTypeDef,
    UpdateResourceProfileDetectionsRequestRequestTypeDef,
    UpdateResourceProfileRequestRequestTypeDef,
    UpdateRevealConfigurationRequestRequestTypeDef,
    UpdateRevealConfigurationResponseTypeDef,
    UpdateSensitivityInspectionTemplateRequestRequestTypeDef,
)
from .waiter import FindingRevealedWaiter

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("Macie2Client",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    UnprocessableEntityException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class Macie2Client(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        Macie2Client exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#exceptions)
        """

    async def accept_invitation(
        self, **kwargs: Unpack[AcceptInvitationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Accepts an Amazon Macie membership invitation that was received from a specific
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.accept_invitation)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#accept_invitation)
        """

    async def batch_get_custom_data_identifiers(
        self, **kwargs: Unpack[BatchGetCustomDataIdentifiersRequestRequestTypeDef]
    ) -> BatchGetCustomDataIdentifiersResponseTypeDef:
        """
        Retrieves information about one or more custom data identifiers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.batch_get_custom_data_identifiers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#batch_get_custom_data_identifiers)
        """

    async def batch_update_automated_discovery_accounts(
        self, **kwargs: Unpack[BatchUpdateAutomatedDiscoveryAccountsRequestRequestTypeDef]
    ) -> BatchUpdateAutomatedDiscoveryAccountsResponseTypeDef:
        """
        Changes the status of automated sensitive data discovery for one or more
        accounts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.batch_update_automated_discovery_accounts)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#batch_update_automated_discovery_accounts)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#close)
        """

    async def create_allow_list(
        self, **kwargs: Unpack[CreateAllowListRequestRequestTypeDef]
    ) -> CreateAllowListResponseTypeDef:
        """
        Creates and defines the settings for an allow list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.create_allow_list)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#create_allow_list)
        """

    async def create_classification_job(
        self, **kwargs: Unpack[CreateClassificationJobRequestRequestTypeDef]
    ) -> CreateClassificationJobResponseTypeDef:
        """
        Creates and defines the settings for a classification job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.create_classification_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#create_classification_job)
        """

    async def create_custom_data_identifier(
        self, **kwargs: Unpack[CreateCustomDataIdentifierRequestRequestTypeDef]
    ) -> CreateCustomDataIdentifierResponseTypeDef:
        """
        Creates and defines the criteria and other settings for a custom data
        identifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.create_custom_data_identifier)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#create_custom_data_identifier)
        """

    async def create_findings_filter(
        self, **kwargs: Unpack[CreateFindingsFilterRequestRequestTypeDef]
    ) -> CreateFindingsFilterResponseTypeDef:
        """
        Creates and defines the criteria and other settings for a findings filter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.create_findings_filter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#create_findings_filter)
        """

    async def create_invitations(
        self, **kwargs: Unpack[CreateInvitationsRequestRequestTypeDef]
    ) -> CreateInvitationsResponseTypeDef:
        """
        Sends an Amazon Macie membership invitation to one or more accounts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.create_invitations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#create_invitations)
        """

    async def create_member(
        self, **kwargs: Unpack[CreateMemberRequestRequestTypeDef]
    ) -> CreateMemberResponseTypeDef:
        """
        Associates an account with an Amazon Macie administrator account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.create_member)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#create_member)
        """

    async def create_sample_findings(
        self, **kwargs: Unpack[CreateSampleFindingsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates sample findings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.create_sample_findings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#create_sample_findings)
        """

    async def decline_invitations(
        self, **kwargs: Unpack[DeclineInvitationsRequestRequestTypeDef]
    ) -> DeclineInvitationsResponseTypeDef:
        """
        Declines Amazon Macie membership invitations that were received from specific
        accounts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.decline_invitations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#decline_invitations)
        """

    async def delete_allow_list(
        self, **kwargs: Unpack[DeleteAllowListRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an allow list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.delete_allow_list)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#delete_allow_list)
        """

    async def delete_custom_data_identifier(
        self, **kwargs: Unpack[DeleteCustomDataIdentifierRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Soft deletes a custom data identifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.delete_custom_data_identifier)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#delete_custom_data_identifier)
        """

    async def delete_findings_filter(
        self, **kwargs: Unpack[DeleteFindingsFilterRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a findings filter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.delete_findings_filter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#delete_findings_filter)
        """

    async def delete_invitations(
        self, **kwargs: Unpack[DeleteInvitationsRequestRequestTypeDef]
    ) -> DeleteInvitationsResponseTypeDef:
        """
        Deletes Amazon Macie membership invitations that were received from specific
        accounts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.delete_invitations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#delete_invitations)
        """

    async def delete_member(
        self, **kwargs: Unpack[DeleteMemberRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the association between an Amazon Macie administrator account and an
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.delete_member)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#delete_member)
        """

    async def describe_buckets(
        self, **kwargs: Unpack[DescribeBucketsRequestRequestTypeDef]
    ) -> DescribeBucketsResponseTypeDef:
        """
        Retrieves (queries) statistical data and other information about one or more S3
        buckets that Amazon Macie monitors and analyzes for an
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.describe_buckets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#describe_buckets)
        """

    async def describe_classification_job(
        self, **kwargs: Unpack[DescribeClassificationJobRequestRequestTypeDef]
    ) -> DescribeClassificationJobResponseTypeDef:
        """
        Retrieves the status and settings for a classification job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.describe_classification_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#describe_classification_job)
        """

    async def describe_organization_configuration(
        self,
    ) -> DescribeOrganizationConfigurationResponseTypeDef:
        """
        Retrieves the Amazon Macie configuration settings for an organization in
        Organizations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.describe_organization_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#describe_organization_configuration)
        """

    async def disable_macie(self) -> Dict[str, Any]:
        """
        Disables Amazon Macie and deletes all settings and resources for a Macie
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.disable_macie)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#disable_macie)
        """

    async def disable_organization_admin_account(
        self, **kwargs: Unpack[DisableOrganizationAdminAccountRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disables an account as the delegated Amazon Macie administrator account for an
        organization in
        Organizations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.disable_organization_admin_account)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#disable_organization_admin_account)
        """

    async def disassociate_from_administrator_account(self) -> Dict[str, Any]:
        """
        Disassociates a member account from its Amazon Macie administrator account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.disassociate_from_administrator_account)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#disassociate_from_administrator_account)
        """

    async def disassociate_from_master_account(self) -> Dict[str, Any]:
        """
        (Deprecated) Disassociates a member account from its Amazon Macie administrator
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.disassociate_from_master_account)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#disassociate_from_master_account)
        """

    async def disassociate_member(
        self, **kwargs: Unpack[DisassociateMemberRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates an Amazon Macie administrator account from a member account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.disassociate_member)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#disassociate_member)
        """

    async def enable_macie(
        self, **kwargs: Unpack[EnableMacieRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Enables Amazon Macie and specifies the configuration settings for a Macie
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.enable_macie)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#enable_macie)
        """

    async def enable_organization_admin_account(
        self, **kwargs: Unpack[EnableOrganizationAdminAccountRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Designates an account as the delegated Amazon Macie administrator account for
        an organization in
        Organizations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.enable_organization_admin_account)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#enable_organization_admin_account)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#generate_presigned_url)
        """

    async def get_administrator_account(self) -> GetAdministratorAccountResponseTypeDef:
        """
        Retrieves information about the Amazon Macie administrator account for an
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.get_administrator_account)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_administrator_account)
        """

    async def get_allow_list(
        self, **kwargs: Unpack[GetAllowListRequestRequestTypeDef]
    ) -> GetAllowListResponseTypeDef:
        """
        Retrieves the settings and status of an allow list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.get_allow_list)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_allow_list)
        """

    async def get_automated_discovery_configuration(
        self,
    ) -> GetAutomatedDiscoveryConfigurationResponseTypeDef:
        """
        Retrieves the configuration settings and status of automated sensitive data
        discovery for an organization or standalone
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.get_automated_discovery_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_automated_discovery_configuration)
        """

    async def get_bucket_statistics(
        self, **kwargs: Unpack[GetBucketStatisticsRequestRequestTypeDef]
    ) -> GetBucketStatisticsResponseTypeDef:
        """
        Retrieves (queries) aggregated statistical data about all the S3 buckets that
        Amazon Macie monitors and analyzes for an
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.get_bucket_statistics)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_bucket_statistics)
        """

    async def get_classification_export_configuration(
        self,
    ) -> GetClassificationExportConfigurationResponseTypeDef:
        """
        Retrieves the configuration settings for storing data classification results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.get_classification_export_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_classification_export_configuration)
        """

    async def get_classification_scope(
        self, **kwargs: Unpack[GetClassificationScopeRequestRequestTypeDef]
    ) -> GetClassificationScopeResponseTypeDef:
        """
        Retrieves the classification scope settings for an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.get_classification_scope)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_classification_scope)
        """

    async def get_custom_data_identifier(
        self, **kwargs: Unpack[GetCustomDataIdentifierRequestRequestTypeDef]
    ) -> GetCustomDataIdentifierResponseTypeDef:
        """
        Retrieves the criteria and other settings for a custom data identifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.get_custom_data_identifier)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_custom_data_identifier)
        """

    async def get_finding_statistics(
        self, **kwargs: Unpack[GetFindingStatisticsRequestRequestTypeDef]
    ) -> GetFindingStatisticsResponseTypeDef:
        """
        Retrieves (queries) aggregated statistical data about findings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.get_finding_statistics)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_finding_statistics)
        """

    async def get_findings(
        self, **kwargs: Unpack[GetFindingsRequestRequestTypeDef]
    ) -> GetFindingsResponseTypeDef:
        """
        Retrieves the details of one or more findings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.get_findings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_findings)
        """

    async def get_findings_filter(
        self, **kwargs: Unpack[GetFindingsFilterRequestRequestTypeDef]
    ) -> GetFindingsFilterResponseTypeDef:
        """
        Retrieves the criteria and other settings for a findings filter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.get_findings_filter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_findings_filter)
        """

    async def get_findings_publication_configuration(
        self,
    ) -> GetFindingsPublicationConfigurationResponseTypeDef:
        """
        Retrieves the configuration settings for publishing findings to Security Hub.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.get_findings_publication_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_findings_publication_configuration)
        """

    async def get_invitations_count(self) -> GetInvitationsCountResponseTypeDef:
        """
        Retrieves the count of Amazon Macie membership invitations that were received
        by an
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.get_invitations_count)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_invitations_count)
        """

    async def get_macie_session(self) -> GetMacieSessionResponseTypeDef:
        """
        Retrieves the status and configuration settings for an Amazon Macie account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.get_macie_session)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_macie_session)
        """

    async def get_master_account(self) -> GetMasterAccountResponseTypeDef:
        """
        (Deprecated) Retrieves information about the Amazon Macie administrator account
        for an
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.get_master_account)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_master_account)
        """

    async def get_member(
        self, **kwargs: Unpack[GetMemberRequestRequestTypeDef]
    ) -> GetMemberResponseTypeDef:
        """
        Retrieves information about an account that's associated with an Amazon Macie
        administrator
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.get_member)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_member)
        """

    async def get_resource_profile(
        self, **kwargs: Unpack[GetResourceProfileRequestRequestTypeDef]
    ) -> GetResourceProfileResponseTypeDef:
        """
        Retrieves (queries) sensitive data discovery statistics and the sensitivity
        score for an S3
        bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.get_resource_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_resource_profile)
        """

    async def get_reveal_configuration(self) -> GetRevealConfigurationResponseTypeDef:
        """
        Retrieves the status and configuration settings for retrieving occurrences of
        sensitive data reported by
        findings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.get_reveal_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_reveal_configuration)
        """

    async def get_sensitive_data_occurrences(
        self, **kwargs: Unpack[GetSensitiveDataOccurrencesRequestRequestTypeDef]
    ) -> GetSensitiveDataOccurrencesResponseTypeDef:
        """
        Retrieves occurrences of sensitive data reported by a finding.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.get_sensitive_data_occurrences)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_sensitive_data_occurrences)
        """

    async def get_sensitive_data_occurrences_availability(
        self, **kwargs: Unpack[GetSensitiveDataOccurrencesAvailabilityRequestRequestTypeDef]
    ) -> GetSensitiveDataOccurrencesAvailabilityResponseTypeDef:
        """
        Checks whether occurrences of sensitive data can be retrieved for a finding.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.get_sensitive_data_occurrences_availability)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_sensitive_data_occurrences_availability)
        """

    async def get_sensitivity_inspection_template(
        self, **kwargs: Unpack[GetSensitivityInspectionTemplateRequestRequestTypeDef]
    ) -> GetSensitivityInspectionTemplateResponseTypeDef:
        """
        Retrieves the settings for the sensitivity inspection template for an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.get_sensitivity_inspection_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_sensitivity_inspection_template)
        """

    async def get_usage_statistics(
        self, **kwargs: Unpack[GetUsageStatisticsRequestRequestTypeDef]
    ) -> GetUsageStatisticsResponseTypeDef:
        """
        Retrieves (queries) quotas and aggregated usage data for one or more accounts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.get_usage_statistics)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_usage_statistics)
        """

    async def get_usage_totals(
        self, **kwargs: Unpack[GetUsageTotalsRequestRequestTypeDef]
    ) -> GetUsageTotalsResponseTypeDef:
        """
        Retrieves (queries) aggregated usage data for an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.get_usage_totals)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_usage_totals)
        """

    async def list_allow_lists(
        self, **kwargs: Unpack[ListAllowListsRequestRequestTypeDef]
    ) -> ListAllowListsResponseTypeDef:
        """
        Retrieves a subset of information about all the allow lists for an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.list_allow_lists)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#list_allow_lists)
        """

    async def list_automated_discovery_accounts(
        self, **kwargs: Unpack[ListAutomatedDiscoveryAccountsRequestRequestTypeDef]
    ) -> ListAutomatedDiscoveryAccountsResponseTypeDef:
        """
        Retrieves the status of automated sensitive data discovery for one or more
        accounts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.list_automated_discovery_accounts)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#list_automated_discovery_accounts)
        """

    async def list_classification_jobs(
        self, **kwargs: Unpack[ListClassificationJobsRequestRequestTypeDef]
    ) -> ListClassificationJobsResponseTypeDef:
        """
        Retrieves a subset of information about one or more classification jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.list_classification_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#list_classification_jobs)
        """

    async def list_classification_scopes(
        self, **kwargs: Unpack[ListClassificationScopesRequestRequestTypeDef]
    ) -> ListClassificationScopesResponseTypeDef:
        """
        Retrieves a subset of information about the classification scope for an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.list_classification_scopes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#list_classification_scopes)
        """

    async def list_custom_data_identifiers(
        self, **kwargs: Unpack[ListCustomDataIdentifiersRequestRequestTypeDef]
    ) -> ListCustomDataIdentifiersResponseTypeDef:
        """
        Retrieves a subset of information about all the custom data identifiers for an
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.list_custom_data_identifiers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#list_custom_data_identifiers)
        """

    async def list_findings(
        self, **kwargs: Unpack[ListFindingsRequestRequestTypeDef]
    ) -> ListFindingsResponseTypeDef:
        """
        Retrieves a subset of information about one or more findings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.list_findings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#list_findings)
        """

    async def list_findings_filters(
        self, **kwargs: Unpack[ListFindingsFiltersRequestRequestTypeDef]
    ) -> ListFindingsFiltersResponseTypeDef:
        """
        Retrieves a subset of information about all the findings filters for an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.list_findings_filters)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#list_findings_filters)
        """

    async def list_invitations(
        self, **kwargs: Unpack[ListInvitationsRequestRequestTypeDef]
    ) -> ListInvitationsResponseTypeDef:
        """
        Retrieves information about Amazon Macie membership invitations that were
        received by an
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.list_invitations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#list_invitations)
        """

    async def list_managed_data_identifiers(
        self, **kwargs: Unpack[ListManagedDataIdentifiersRequestRequestTypeDef]
    ) -> ListManagedDataIdentifiersResponseTypeDef:
        """
        Retrieves information about all the managed data identifiers that Amazon Macie
        currently
        provides.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.list_managed_data_identifiers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#list_managed_data_identifiers)
        """

    async def list_members(
        self, **kwargs: Unpack[ListMembersRequestRequestTypeDef]
    ) -> ListMembersResponseTypeDef:
        """
        Retrieves information about the accounts that are associated with an Amazon
        Macie administrator
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.list_members)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#list_members)
        """

    async def list_organization_admin_accounts(
        self, **kwargs: Unpack[ListOrganizationAdminAccountsRequestRequestTypeDef]
    ) -> ListOrganizationAdminAccountsResponseTypeDef:
        """
        Retrieves information about the delegated Amazon Macie administrator account
        for an organization in
        Organizations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.list_organization_admin_accounts)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#list_organization_admin_accounts)
        """

    async def list_resource_profile_artifacts(
        self, **kwargs: Unpack[ListResourceProfileArtifactsRequestRequestTypeDef]
    ) -> ListResourceProfileArtifactsResponseTypeDef:
        """
        Retrieves information about objects that Amazon Macie selected from an S3
        bucket for automated sensitive data
        discovery.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.list_resource_profile_artifacts)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#list_resource_profile_artifacts)
        """

    async def list_resource_profile_detections(
        self, **kwargs: Unpack[ListResourceProfileDetectionsRequestRequestTypeDef]
    ) -> ListResourceProfileDetectionsResponseTypeDef:
        """
        Retrieves information about the types and amount of sensitive data that Amazon
        Macie found in an S3
        bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.list_resource_profile_detections)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#list_resource_profile_detections)
        """

    async def list_sensitivity_inspection_templates(
        self, **kwargs: Unpack[ListSensitivityInspectionTemplatesRequestRequestTypeDef]
    ) -> ListSensitivityInspectionTemplatesResponseTypeDef:
        """
        Retrieves a subset of information about the sensitivity inspection template for
        an
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.list_sensitivity_inspection_templates)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#list_sensitivity_inspection_templates)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Retrieves the tags (keys and values) that are associated with an Amazon Macie
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#list_tags_for_resource)
        """

    async def put_classification_export_configuration(
        self, **kwargs: Unpack[PutClassificationExportConfigurationRequestRequestTypeDef]
    ) -> PutClassificationExportConfigurationResponseTypeDef:
        """
        Adds or updates the configuration settings for storing data classification
        results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.put_classification_export_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#put_classification_export_configuration)
        """

    async def put_findings_publication_configuration(
        self, **kwargs: Unpack[PutFindingsPublicationConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the configuration settings for publishing findings to Security Hub.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.put_findings_publication_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#put_findings_publication_configuration)
        """

    async def search_resources(
        self, **kwargs: Unpack[SearchResourcesRequestRequestTypeDef]
    ) -> SearchResourcesResponseTypeDef:
        """
        Retrieves (queries) statistical data and other information about Amazon Web
        Services resources that Amazon Macie monitors and
        analyzes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.search_resources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#search_resources)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Adds or updates one or more tags (keys and values) that are associated with an
        Amazon Macie
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#tag_resource)
        """

    async def test_custom_data_identifier(
        self, **kwargs: Unpack[TestCustomDataIdentifierRequestRequestTypeDef]
    ) -> TestCustomDataIdentifierResponseTypeDef:
        """
        Tests criteria for a custom data identifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.test_custom_data_identifier)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#test_custom_data_identifier)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes one or more tags (keys and values) from an Amazon Macie resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#untag_resource)
        """

    async def update_allow_list(
        self, **kwargs: Unpack[UpdateAllowListRequestRequestTypeDef]
    ) -> UpdateAllowListResponseTypeDef:
        """
        Updates the settings for an allow list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.update_allow_list)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#update_allow_list)
        """

    async def update_automated_discovery_configuration(
        self, **kwargs: Unpack[UpdateAutomatedDiscoveryConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Changes the configuration settings and status of automated sensitive data
        discovery for an organization or standalone
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.update_automated_discovery_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#update_automated_discovery_configuration)
        """

    async def update_classification_job(
        self, **kwargs: Unpack[UpdateClassificationJobRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Changes the status of a classification job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.update_classification_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#update_classification_job)
        """

    async def update_classification_scope(
        self, **kwargs: Unpack[UpdateClassificationScopeRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the classification scope settings for an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.update_classification_scope)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#update_classification_scope)
        """

    async def update_findings_filter(
        self, **kwargs: Unpack[UpdateFindingsFilterRequestRequestTypeDef]
    ) -> UpdateFindingsFilterResponseTypeDef:
        """
        Updates the criteria and other settings for a findings filter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.update_findings_filter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#update_findings_filter)
        """

    async def update_macie_session(
        self, **kwargs: Unpack[UpdateMacieSessionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Suspends or re-enables Amazon Macie, or updates the configuration settings for
        a Macie
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.update_macie_session)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#update_macie_session)
        """

    async def update_member_session(
        self, **kwargs: Unpack[UpdateMemberSessionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Enables an Amazon Macie administrator to suspend or re-enable Macie for a
        member
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.update_member_session)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#update_member_session)
        """

    async def update_organization_configuration(
        self, **kwargs: Unpack[UpdateOrganizationConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the Amazon Macie configuration settings for an organization in
        Organizations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.update_organization_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#update_organization_configuration)
        """

    async def update_resource_profile(
        self, **kwargs: Unpack[UpdateResourceProfileRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the sensitivity score for an S3 bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.update_resource_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#update_resource_profile)
        """

    async def update_resource_profile_detections(
        self, **kwargs: Unpack[UpdateResourceProfileDetectionsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the sensitivity scoring settings for an S3 bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.update_resource_profile_detections)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#update_resource_profile_detections)
        """

    async def update_reveal_configuration(
        self, **kwargs: Unpack[UpdateRevealConfigurationRequestRequestTypeDef]
    ) -> UpdateRevealConfigurationResponseTypeDef:
        """
        Updates the status and configuration settings for retrieving occurrences of
        sensitive data reported by
        findings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.update_reveal_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#update_reveal_configuration)
        """

    async def update_sensitivity_inspection_template(
        self, **kwargs: Unpack[UpdateSensitivityInspectionTemplateRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the settings for the sensitivity inspection template for an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.update_sensitivity_inspection_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#update_sensitivity_inspection_template)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_buckets"]
    ) -> DescribeBucketsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_usage_statistics"]
    ) -> GetUsageStatisticsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_allow_lists"]) -> ListAllowListsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_automated_discovery_accounts"]
    ) -> ListAutomatedDiscoveryAccountsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_classification_jobs"]
    ) -> ListClassificationJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_classification_scopes"]
    ) -> ListClassificationScopesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_custom_data_identifiers"]
    ) -> ListCustomDataIdentifiersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_findings"]) -> ListFindingsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_findings_filters"]
    ) -> ListFindingsFiltersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_invitations"]
    ) -> ListInvitationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_managed_data_identifiers"]
    ) -> ListManagedDataIdentifiersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_members"]) -> ListMembersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_organization_admin_accounts"]
    ) -> ListOrganizationAdminAccountsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_resource_profile_artifacts"]
    ) -> ListResourceProfileArtifactsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_resource_profile_detections"]
    ) -> ListResourceProfileDetectionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_sensitivity_inspection_templates"]
    ) -> ListSensitivityInspectionTemplatesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["search_resources"]
    ) -> SearchResourcesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_paginator)
        """

    def get_waiter(self, waiter_name: Literal["finding_revealed"]) -> FindingRevealedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_waiter)
        """

    async def __aenter__(self) -> "Macie2Client":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/)
        """
