"""
Type annotations for fms service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_fms.client import FMSClient

    session = get_session()
    async with session.create_client("fms") as client:
        client: FMSClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import (
    ListAdminAccountsForOrganizationPaginator,
    ListAdminsManagingAccountPaginator,
    ListAppsListsPaginator,
    ListComplianceStatusPaginator,
    ListMemberAccountsPaginator,
    ListPoliciesPaginator,
    ListProtocolsListsPaginator,
    ListThirdPartyFirewallFirewallPoliciesPaginator,
)
from .type_defs import (
    AssociateAdminAccountRequestRequestTypeDef,
    AssociateThirdPartyFirewallRequestRequestTypeDef,
    AssociateThirdPartyFirewallResponseTypeDef,
    BatchAssociateResourceRequestRequestTypeDef,
    BatchAssociateResourceResponseTypeDef,
    BatchDisassociateResourceRequestRequestTypeDef,
    BatchDisassociateResourceResponseTypeDef,
    DeleteAppsListRequestRequestTypeDef,
    DeletePolicyRequestRequestTypeDef,
    DeleteProtocolsListRequestRequestTypeDef,
    DeleteResourceSetRequestRequestTypeDef,
    DisassociateThirdPartyFirewallRequestRequestTypeDef,
    DisassociateThirdPartyFirewallResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    GetAdminAccountResponseTypeDef,
    GetAdminScopeRequestRequestTypeDef,
    GetAdminScopeResponseTypeDef,
    GetAppsListRequestRequestTypeDef,
    GetAppsListResponseTypeDef,
    GetComplianceDetailRequestRequestTypeDef,
    GetComplianceDetailResponseTypeDef,
    GetNotificationChannelResponseTypeDef,
    GetPolicyRequestRequestTypeDef,
    GetPolicyResponseTypeDef,
    GetProtectionStatusRequestRequestTypeDef,
    GetProtectionStatusResponseTypeDef,
    GetProtocolsListRequestRequestTypeDef,
    GetProtocolsListResponseTypeDef,
    GetResourceSetRequestRequestTypeDef,
    GetResourceSetResponseTypeDef,
    GetThirdPartyFirewallAssociationStatusRequestRequestTypeDef,
    GetThirdPartyFirewallAssociationStatusResponseTypeDef,
    GetViolationDetailsRequestRequestTypeDef,
    GetViolationDetailsResponseTypeDef,
    ListAdminAccountsForOrganizationRequestRequestTypeDef,
    ListAdminAccountsForOrganizationResponseTypeDef,
    ListAdminsManagingAccountRequestRequestTypeDef,
    ListAdminsManagingAccountResponseTypeDef,
    ListAppsListsRequestRequestTypeDef,
    ListAppsListsResponseTypeDef,
    ListComplianceStatusRequestRequestTypeDef,
    ListComplianceStatusResponseTypeDef,
    ListDiscoveredResourcesRequestRequestTypeDef,
    ListDiscoveredResourcesResponseTypeDef,
    ListMemberAccountsRequestRequestTypeDef,
    ListMemberAccountsResponseTypeDef,
    ListPoliciesRequestRequestTypeDef,
    ListPoliciesResponseTypeDef,
    ListProtocolsListsRequestRequestTypeDef,
    ListProtocolsListsResponseTypeDef,
    ListResourceSetResourcesRequestRequestTypeDef,
    ListResourceSetResourcesResponseTypeDef,
    ListResourceSetsRequestRequestTypeDef,
    ListResourceSetsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListThirdPartyFirewallFirewallPoliciesRequestRequestTypeDef,
    ListThirdPartyFirewallFirewallPoliciesResponseTypeDef,
    PutAdminAccountRequestRequestTypeDef,
    PutAppsListRequestRequestTypeDef,
    PutAppsListResponseTypeDef,
    PutNotificationChannelRequestRequestTypeDef,
    PutPolicyRequestRequestTypeDef,
    PutPolicyResponseTypeDef,
    PutProtocolsListRequestRequestTypeDef,
    PutProtocolsListResponseTypeDef,
    PutResourceSetRequestRequestTypeDef,
    PutResourceSetResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("FMSClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    InternalErrorException: Type[BotocoreClientError]
    InvalidInputException: Type[BotocoreClientError]
    InvalidOperationException: Type[BotocoreClientError]
    InvalidTypeException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]


class FMSClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        FMSClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/#exceptions)
        """

    async def associate_admin_account(
        self, **kwargs: Unpack[AssociateAdminAccountRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Sets a Firewall Manager default administrator account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.associate_admin_account)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/#associate_admin_account)
        """

    async def associate_third_party_firewall(
        self, **kwargs: Unpack[AssociateThirdPartyFirewallRequestRequestTypeDef]
    ) -> AssociateThirdPartyFirewallResponseTypeDef:
        """
        Sets the Firewall Manager policy administrator as a tenant administrator of a
        third-party firewall
        service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.associate_third_party_firewall)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/#associate_third_party_firewall)
        """

    async def batch_associate_resource(
        self, **kwargs: Unpack[BatchAssociateResourceRequestRequestTypeDef]
    ) -> BatchAssociateResourceResponseTypeDef:
        """
        Associate resources to a Firewall Manager resource set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.batch_associate_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/#batch_associate_resource)
        """

    async def batch_disassociate_resource(
        self, **kwargs: Unpack[BatchDisassociateResourceRequestRequestTypeDef]
    ) -> BatchDisassociateResourceResponseTypeDef:
        """
        Disassociates resources from a Firewall Manager resource set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.batch_disassociate_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/#batch_disassociate_resource)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/#close)
        """

    async def delete_apps_list(
        self, **kwargs: Unpack[DeleteAppsListRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Permanently deletes an Firewall Manager applications list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.delete_apps_list)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/#delete_apps_list)
        """

    async def delete_notification_channel(self) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an Firewall Manager association with the IAM role and the Amazon Simple
        Notification Service (SNS) topic that is used to record Firewall Manager SNS
        logs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.delete_notification_channel)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/#delete_notification_channel)
        """

    async def delete_policy(
        self, **kwargs: Unpack[DeletePolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Permanently deletes an Firewall Manager policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.delete_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/#delete_policy)
        """

    async def delete_protocols_list(
        self, **kwargs: Unpack[DeleteProtocolsListRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Permanently deletes an Firewall Manager protocols list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.delete_protocols_list)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/#delete_protocols_list)
        """

    async def delete_resource_set(
        self, **kwargs: Unpack[DeleteResourceSetRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified  ResourceSet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.delete_resource_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/#delete_resource_set)
        """

    async def disassociate_admin_account(self) -> EmptyResponseMetadataTypeDef:
        """
        Disassociates an Firewall Manager administrator account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.disassociate_admin_account)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/#disassociate_admin_account)
        """

    async def disassociate_third_party_firewall(
        self, **kwargs: Unpack[DisassociateThirdPartyFirewallRequestRequestTypeDef]
    ) -> DisassociateThirdPartyFirewallResponseTypeDef:
        """
        Disassociates a Firewall Manager policy administrator from a third-party
        firewall
        tenant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.disassociate_third_party_firewall)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/#disassociate_third_party_firewall)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/#generate_presigned_url)
        """

    async def get_admin_account(self) -> GetAdminAccountResponseTypeDef:
        """
        Returns the Organizations account that is associated with Firewall Manager as
        the Firewall Manager default
        administrator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.get_admin_account)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/#get_admin_account)
        """

    async def get_admin_scope(
        self, **kwargs: Unpack[GetAdminScopeRequestRequestTypeDef]
    ) -> GetAdminScopeResponseTypeDef:
        """
        Returns information about the specified account's administrative scope.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.get_admin_scope)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/#get_admin_scope)
        """

    async def get_apps_list(
        self, **kwargs: Unpack[GetAppsListRequestRequestTypeDef]
    ) -> GetAppsListResponseTypeDef:
        """
        Returns information about the specified Firewall Manager applications list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.get_apps_list)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/#get_apps_list)
        """

    async def get_compliance_detail(
        self, **kwargs: Unpack[GetComplianceDetailRequestRequestTypeDef]
    ) -> GetComplianceDetailResponseTypeDef:
        """
        Returns detailed compliance information about the specified member account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.get_compliance_detail)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/#get_compliance_detail)
        """

    async def get_notification_channel(self) -> GetNotificationChannelResponseTypeDef:
        """
        Information about the Amazon Simple Notification Service (SNS) topic that is
        used to record Firewall Manager SNS
        logs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.get_notification_channel)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/#get_notification_channel)
        """

    async def get_policy(
        self, **kwargs: Unpack[GetPolicyRequestRequestTypeDef]
    ) -> GetPolicyResponseTypeDef:
        """
        Returns information about the specified Firewall Manager policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.get_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/#get_policy)
        """

    async def get_protection_status(
        self, **kwargs: Unpack[GetProtectionStatusRequestRequestTypeDef]
    ) -> GetProtectionStatusResponseTypeDef:
        """
        If you created a Shield Advanced policy, returns policy-level attack summary
        information in the event of a potential DDoS
        attack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.get_protection_status)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/#get_protection_status)
        """

    async def get_protocols_list(
        self, **kwargs: Unpack[GetProtocolsListRequestRequestTypeDef]
    ) -> GetProtocolsListResponseTypeDef:
        """
        Returns information about the specified Firewall Manager protocols list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.get_protocols_list)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/#get_protocols_list)
        """

    async def get_resource_set(
        self, **kwargs: Unpack[GetResourceSetRequestRequestTypeDef]
    ) -> GetResourceSetResponseTypeDef:
        """
        Gets information about a specific resource set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.get_resource_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/#get_resource_set)
        """

    async def get_third_party_firewall_association_status(
        self, **kwargs: Unpack[GetThirdPartyFirewallAssociationStatusRequestRequestTypeDef]
    ) -> GetThirdPartyFirewallAssociationStatusResponseTypeDef:
        """
        The onboarding status of a Firewall Manager admin account to third-party
        firewall vendor
        tenant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.get_third_party_firewall_association_status)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/#get_third_party_firewall_association_status)
        """

    async def get_violation_details(
        self, **kwargs: Unpack[GetViolationDetailsRequestRequestTypeDef]
    ) -> GetViolationDetailsResponseTypeDef:
        """
        Retrieves violations for a resource based on the specified Firewall Manager
        policy and Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.get_violation_details)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/#get_violation_details)
        """

    async def list_admin_accounts_for_organization(
        self, **kwargs: Unpack[ListAdminAccountsForOrganizationRequestRequestTypeDef]
    ) -> ListAdminAccountsForOrganizationResponseTypeDef:
        """
        Returns a `AdminAccounts` object that lists the Firewall Manager administrators
        within the organization that are onboarded to Firewall Manager by
        AssociateAdminAccount.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.list_admin_accounts_for_organization)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/#list_admin_accounts_for_organization)
        """

    async def list_admins_managing_account(
        self, **kwargs: Unpack[ListAdminsManagingAccountRequestRequestTypeDef]
    ) -> ListAdminsManagingAccountResponseTypeDef:
        """
        Lists the accounts that are managing the specified Organizations member account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.list_admins_managing_account)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/#list_admins_managing_account)
        """

    async def list_apps_lists(
        self, **kwargs: Unpack[ListAppsListsRequestRequestTypeDef]
    ) -> ListAppsListsResponseTypeDef:
        """
        Returns an array of `AppsListDataSummary` objects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.list_apps_lists)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/#list_apps_lists)
        """

    async def list_compliance_status(
        self, **kwargs: Unpack[ListComplianceStatusRequestRequestTypeDef]
    ) -> ListComplianceStatusResponseTypeDef:
        """
        Returns an array of `PolicyComplianceStatus` objects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.list_compliance_status)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/#list_compliance_status)
        """

    async def list_discovered_resources(
        self, **kwargs: Unpack[ListDiscoveredResourcesRequestRequestTypeDef]
    ) -> ListDiscoveredResourcesResponseTypeDef:
        """
        Returns an array of resources in the organization's accounts that are available
        to be associated with a resource
        set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.list_discovered_resources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/#list_discovered_resources)
        """

    async def list_member_accounts(
        self, **kwargs: Unpack[ListMemberAccountsRequestRequestTypeDef]
    ) -> ListMemberAccountsResponseTypeDef:
        """
        Returns a `MemberAccounts` object that lists the member accounts in the
        administrator's Amazon Web Services
        organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.list_member_accounts)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/#list_member_accounts)
        """

    async def list_policies(
        self, **kwargs: Unpack[ListPoliciesRequestRequestTypeDef]
    ) -> ListPoliciesResponseTypeDef:
        """
        Returns an array of `PolicySummary` objects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.list_policies)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/#list_policies)
        """

    async def list_protocols_lists(
        self, **kwargs: Unpack[ListProtocolsListsRequestRequestTypeDef]
    ) -> ListProtocolsListsResponseTypeDef:
        """
        Returns an array of `ProtocolsListDataSummary` objects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.list_protocols_lists)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/#list_protocols_lists)
        """

    async def list_resource_set_resources(
        self, **kwargs: Unpack[ListResourceSetResourcesRequestRequestTypeDef]
    ) -> ListResourceSetResourcesResponseTypeDef:
        """
        Returns an array of resources that are currently associated to a resource set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.list_resource_set_resources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/#list_resource_set_resources)
        """

    async def list_resource_sets(
        self, **kwargs: Unpack[ListResourceSetsRequestRequestTypeDef]
    ) -> ListResourceSetsResponseTypeDef:
        """
        Returns an array of `ResourceSetSummary` objects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.list_resource_sets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/#list_resource_sets)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Retrieves the list of tags for the specified Amazon Web Services resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/#list_tags_for_resource)
        """

    async def list_third_party_firewall_firewall_policies(
        self, **kwargs: Unpack[ListThirdPartyFirewallFirewallPoliciesRequestRequestTypeDef]
    ) -> ListThirdPartyFirewallFirewallPoliciesResponseTypeDef:
        """
        Retrieves a list of all of the third-party firewall policies that are
        associated with the third-party firewall administrator's
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.list_third_party_firewall_firewall_policies)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/#list_third_party_firewall_firewall_policies)
        """

    async def put_admin_account(
        self, **kwargs: Unpack[PutAdminAccountRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates or updates an Firewall Manager administrator account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.put_admin_account)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/#put_admin_account)
        """

    async def put_apps_list(
        self, **kwargs: Unpack[PutAppsListRequestRequestTypeDef]
    ) -> PutAppsListResponseTypeDef:
        """
        Creates an Firewall Manager applications list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.put_apps_list)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/#put_apps_list)
        """

    async def put_notification_channel(
        self, **kwargs: Unpack[PutNotificationChannelRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Designates the IAM role and Amazon Simple Notification Service (SNS) topic that
        Firewall Manager uses to record SNS
        logs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.put_notification_channel)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/#put_notification_channel)
        """

    async def put_policy(
        self, **kwargs: Unpack[PutPolicyRequestRequestTypeDef]
    ) -> PutPolicyResponseTypeDef:
        """
        Creates an Firewall Manager policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.put_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/#put_policy)
        """

    async def put_protocols_list(
        self, **kwargs: Unpack[PutProtocolsListRequestRequestTypeDef]
    ) -> PutProtocolsListResponseTypeDef:
        """
        Creates an Firewall Manager protocols list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.put_protocols_list)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/#put_protocols_list)
        """

    async def put_resource_set(
        self, **kwargs: Unpack[PutResourceSetRequestRequestTypeDef]
    ) -> PutResourceSetResponseTypeDef:
        """
        Creates the resource set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.put_resource_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/#put_resource_set)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Adds one or more tags to an Amazon Web Services resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes one or more tags from an Amazon Web Services resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/#untag_resource)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_admin_accounts_for_organization"]
    ) -> ListAdminAccountsForOrganizationPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_admins_managing_account"]
    ) -> ListAdminsManagingAccountPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_apps_lists"]) -> ListAppsListsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_compliance_status"]
    ) -> ListComplianceStatusPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_member_accounts"]
    ) -> ListMemberAccountsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_policies"]) -> ListPoliciesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_protocols_lists"]
    ) -> ListProtocolsListsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_third_party_firewall_firewall_policies"]
    ) -> ListThirdPartyFirewallFirewallPoliciesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/#get_paginator)
        """

    async def __aenter__(self) -> "FMSClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fms.html#FMS.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fms/client/)
        """
