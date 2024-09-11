"""
Type annotations for securityhub service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_securityhub.client import SecurityHubClient

    session = get_session()
    async with session.create_client("securityhub") as client:
        client: SecurityHubClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import (
    DescribeActionTargetsPaginator,
    DescribeProductsPaginator,
    DescribeStandardsControlsPaginator,
    DescribeStandardsPaginator,
    GetEnabledStandardsPaginator,
    GetFindingHistoryPaginator,
    GetFindingsPaginator,
    GetInsightsPaginator,
    ListConfigurationPoliciesPaginator,
    ListConfigurationPolicyAssociationsPaginator,
    ListEnabledProductsForImportPaginator,
    ListFindingAggregatorsPaginator,
    ListInvitationsPaginator,
    ListMembersPaginator,
    ListOrganizationAdminAccountsPaginator,
    ListSecurityControlDefinitionsPaginator,
    ListStandardsControlAssociationsPaginator,
)
from .type_defs import (
    AcceptAdministratorInvitationRequestRequestTypeDef,
    AcceptInvitationRequestRequestTypeDef,
    BatchDeleteAutomationRulesRequestRequestTypeDef,
    BatchDeleteAutomationRulesResponseTypeDef,
    BatchDisableStandardsRequestRequestTypeDef,
    BatchDisableStandardsResponseTypeDef,
    BatchEnableStandardsRequestRequestTypeDef,
    BatchEnableStandardsResponseTypeDef,
    BatchGetAutomationRulesRequestRequestTypeDef,
    BatchGetAutomationRulesResponseTypeDef,
    BatchGetConfigurationPolicyAssociationsRequestRequestTypeDef,
    BatchGetConfigurationPolicyAssociationsResponseTypeDef,
    BatchGetSecurityControlsRequestRequestTypeDef,
    BatchGetSecurityControlsResponseTypeDef,
    BatchGetStandardsControlAssociationsRequestRequestTypeDef,
    BatchGetStandardsControlAssociationsResponseTypeDef,
    BatchImportFindingsRequestRequestTypeDef,
    BatchImportFindingsResponseTypeDef,
    BatchUpdateAutomationRulesRequestRequestTypeDef,
    BatchUpdateAutomationRulesResponseTypeDef,
    BatchUpdateFindingsRequestRequestTypeDef,
    BatchUpdateFindingsResponseTypeDef,
    BatchUpdateStandardsControlAssociationsRequestRequestTypeDef,
    BatchUpdateStandardsControlAssociationsResponseTypeDef,
    CreateActionTargetRequestRequestTypeDef,
    CreateActionTargetResponseTypeDef,
    CreateAutomationRuleRequestRequestTypeDef,
    CreateAutomationRuleResponseTypeDef,
    CreateConfigurationPolicyRequestRequestTypeDef,
    CreateConfigurationPolicyResponseTypeDef,
    CreateFindingAggregatorRequestRequestTypeDef,
    CreateFindingAggregatorResponseTypeDef,
    CreateInsightRequestRequestTypeDef,
    CreateInsightResponseTypeDef,
    CreateMembersRequestRequestTypeDef,
    CreateMembersResponseTypeDef,
    DeclineInvitationsRequestRequestTypeDef,
    DeclineInvitationsResponseTypeDef,
    DeleteActionTargetRequestRequestTypeDef,
    DeleteActionTargetResponseTypeDef,
    DeleteConfigurationPolicyRequestRequestTypeDef,
    DeleteFindingAggregatorRequestRequestTypeDef,
    DeleteInsightRequestRequestTypeDef,
    DeleteInsightResponseTypeDef,
    DeleteInvitationsRequestRequestTypeDef,
    DeleteInvitationsResponseTypeDef,
    DeleteMembersRequestRequestTypeDef,
    DeleteMembersResponseTypeDef,
    DescribeActionTargetsRequestRequestTypeDef,
    DescribeActionTargetsResponseTypeDef,
    DescribeHubRequestRequestTypeDef,
    DescribeHubResponseTypeDef,
    DescribeOrganizationConfigurationResponseTypeDef,
    DescribeProductsRequestRequestTypeDef,
    DescribeProductsResponseTypeDef,
    DescribeStandardsControlsRequestRequestTypeDef,
    DescribeStandardsControlsResponseTypeDef,
    DescribeStandardsRequestRequestTypeDef,
    DescribeStandardsResponseTypeDef,
    DisableImportFindingsForProductRequestRequestTypeDef,
    DisableOrganizationAdminAccountRequestRequestTypeDef,
    DisassociateMembersRequestRequestTypeDef,
    EnableImportFindingsForProductRequestRequestTypeDef,
    EnableImportFindingsForProductResponseTypeDef,
    EnableOrganizationAdminAccountRequestRequestTypeDef,
    EnableSecurityHubRequestRequestTypeDef,
    GetAdministratorAccountResponseTypeDef,
    GetConfigurationPolicyAssociationRequestRequestTypeDef,
    GetConfigurationPolicyAssociationResponseTypeDef,
    GetConfigurationPolicyRequestRequestTypeDef,
    GetConfigurationPolicyResponseTypeDef,
    GetEnabledStandardsRequestRequestTypeDef,
    GetEnabledStandardsResponseTypeDef,
    GetFindingAggregatorRequestRequestTypeDef,
    GetFindingAggregatorResponseTypeDef,
    GetFindingHistoryRequestRequestTypeDef,
    GetFindingHistoryResponseTypeDef,
    GetFindingsRequestRequestTypeDef,
    GetFindingsResponseTypeDef,
    GetInsightResultsRequestRequestTypeDef,
    GetInsightResultsResponseTypeDef,
    GetInsightsRequestRequestTypeDef,
    GetInsightsResponseTypeDef,
    GetInvitationsCountResponseTypeDef,
    GetMasterAccountResponseTypeDef,
    GetMembersRequestRequestTypeDef,
    GetMembersResponseTypeDef,
    GetSecurityControlDefinitionRequestRequestTypeDef,
    GetSecurityControlDefinitionResponseTypeDef,
    InviteMembersRequestRequestTypeDef,
    InviteMembersResponseTypeDef,
    ListAutomationRulesRequestRequestTypeDef,
    ListAutomationRulesResponseTypeDef,
    ListConfigurationPoliciesRequestRequestTypeDef,
    ListConfigurationPoliciesResponseTypeDef,
    ListConfigurationPolicyAssociationsRequestRequestTypeDef,
    ListConfigurationPolicyAssociationsResponseTypeDef,
    ListEnabledProductsForImportRequestRequestTypeDef,
    ListEnabledProductsForImportResponseTypeDef,
    ListFindingAggregatorsRequestRequestTypeDef,
    ListFindingAggregatorsResponseTypeDef,
    ListInvitationsRequestRequestTypeDef,
    ListInvitationsResponseTypeDef,
    ListMembersRequestRequestTypeDef,
    ListMembersResponseTypeDef,
    ListOrganizationAdminAccountsRequestRequestTypeDef,
    ListOrganizationAdminAccountsResponseTypeDef,
    ListSecurityControlDefinitionsRequestRequestTypeDef,
    ListSecurityControlDefinitionsResponseTypeDef,
    ListStandardsControlAssociationsRequestRequestTypeDef,
    ListStandardsControlAssociationsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    StartConfigurationPolicyAssociationRequestRequestTypeDef,
    StartConfigurationPolicyAssociationResponseTypeDef,
    StartConfigurationPolicyDisassociationRequestRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateActionTargetRequestRequestTypeDef,
    UpdateConfigurationPolicyRequestRequestTypeDef,
    UpdateConfigurationPolicyResponseTypeDef,
    UpdateFindingAggregatorRequestRequestTypeDef,
    UpdateFindingAggregatorResponseTypeDef,
    UpdateFindingsRequestRequestTypeDef,
    UpdateInsightRequestRequestTypeDef,
    UpdateOrganizationConfigurationRequestRequestTypeDef,
    UpdateSecurityControlRequestRequestTypeDef,
    UpdateSecurityHubConfigurationRequestRequestTypeDef,
    UpdateStandardsControlRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("SecurityHubClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InternalException: Type[BotocoreClientError]
    InvalidAccessException: Type[BotocoreClientError]
    InvalidInputException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ResourceConflictException: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]

class SecurityHubClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SecurityHubClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#exceptions)
        """

    async def accept_administrator_invitation(
        self, **kwargs: Unpack[AcceptAdministratorInvitationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Accepts the invitation to be a member account and be monitored by the Security
        Hub administrator account that the invitation was sent
        from.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.accept_administrator_invitation)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#accept_administrator_invitation)
        """

    async def accept_invitation(
        self, **kwargs: Unpack[AcceptInvitationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        This method is deprecated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.accept_invitation)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#accept_invitation)
        """

    async def batch_delete_automation_rules(
        self, **kwargs: Unpack[BatchDeleteAutomationRulesRequestRequestTypeDef]
    ) -> BatchDeleteAutomationRulesResponseTypeDef:
        """
        Deletes one or more automation rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.batch_delete_automation_rules)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#batch_delete_automation_rules)
        """

    async def batch_disable_standards(
        self, **kwargs: Unpack[BatchDisableStandardsRequestRequestTypeDef]
    ) -> BatchDisableStandardsResponseTypeDef:
        """
        Disables the standards specified by the provided `StandardsSubscriptionArns`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.batch_disable_standards)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#batch_disable_standards)
        """

    async def batch_enable_standards(
        self, **kwargs: Unpack[BatchEnableStandardsRequestRequestTypeDef]
    ) -> BatchEnableStandardsResponseTypeDef:
        """
        Enables the standards specified by the provided `StandardsArn`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.batch_enable_standards)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#batch_enable_standards)
        """

    async def batch_get_automation_rules(
        self, **kwargs: Unpack[BatchGetAutomationRulesRequestRequestTypeDef]
    ) -> BatchGetAutomationRulesResponseTypeDef:
        """
        Retrieves a list of details for automation rules based on rule Amazon Resource
        Names
        (ARNs).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.batch_get_automation_rules)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#batch_get_automation_rules)
        """

    async def batch_get_configuration_policy_associations(
        self, **kwargs: Unpack[BatchGetConfigurationPolicyAssociationsRequestRequestTypeDef]
    ) -> BatchGetConfigurationPolicyAssociationsResponseTypeDef:
        """
        Returns associations between an Security Hub configuration and a batch of
        target accounts, organizational units, or the
        root.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.batch_get_configuration_policy_associations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#batch_get_configuration_policy_associations)
        """

    async def batch_get_security_controls(
        self, **kwargs: Unpack[BatchGetSecurityControlsRequestRequestTypeDef]
    ) -> BatchGetSecurityControlsResponseTypeDef:
        """
        Provides details about a batch of security controls for the current Amazon Web
        Services account and Amazon Web Services
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.batch_get_security_controls)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#batch_get_security_controls)
        """

    async def batch_get_standards_control_associations(
        self, **kwargs: Unpack[BatchGetStandardsControlAssociationsRequestRequestTypeDef]
    ) -> BatchGetStandardsControlAssociationsResponseTypeDef:
        """
        For a batch of security controls and standards, identifies whether each control
        is currently enabled or disabled in a
        standard.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.batch_get_standards_control_associations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#batch_get_standards_control_associations)
        """

    async def batch_import_findings(
        self, **kwargs: Unpack[BatchImportFindingsRequestRequestTypeDef]
    ) -> BatchImportFindingsResponseTypeDef:
        """
        Imports security findings generated by a finding provider into Security Hub.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.batch_import_findings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#batch_import_findings)
        """

    async def batch_update_automation_rules(
        self, **kwargs: Unpack[BatchUpdateAutomationRulesRequestRequestTypeDef]
    ) -> BatchUpdateAutomationRulesResponseTypeDef:
        """
        Updates one or more automation rules based on rule Amazon Resource Names (ARNs)
        and input
        parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.batch_update_automation_rules)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#batch_update_automation_rules)
        """

    async def batch_update_findings(
        self, **kwargs: Unpack[BatchUpdateFindingsRequestRequestTypeDef]
    ) -> BatchUpdateFindingsResponseTypeDef:
        """
        Used by Security Hub customers to update information about their investigation
        into a
        finding.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.batch_update_findings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#batch_update_findings)
        """

    async def batch_update_standards_control_associations(
        self, **kwargs: Unpack[BatchUpdateStandardsControlAssociationsRequestRequestTypeDef]
    ) -> BatchUpdateStandardsControlAssociationsResponseTypeDef:
        """
        For a batch of security controls and standards, this operation updates the
        enablement status of a control in a
        standard.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.batch_update_standards_control_associations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#batch_update_standards_control_associations)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#close)
        """

    async def create_action_target(
        self, **kwargs: Unpack[CreateActionTargetRequestRequestTypeDef]
    ) -> CreateActionTargetResponseTypeDef:
        """
        Creates a custom action target in Security Hub.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.create_action_target)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#create_action_target)
        """

    async def create_automation_rule(
        self, **kwargs: Unpack[CreateAutomationRuleRequestRequestTypeDef]
    ) -> CreateAutomationRuleResponseTypeDef:
        """
        Creates an automation rule based on input parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.create_automation_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#create_automation_rule)
        """

    async def create_configuration_policy(
        self, **kwargs: Unpack[CreateConfigurationPolicyRequestRequestTypeDef]
    ) -> CreateConfigurationPolicyResponseTypeDef:
        """
        Creates a configuration policy with the defined configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.create_configuration_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#create_configuration_policy)
        """

    async def create_finding_aggregator(
        self, **kwargs: Unpack[CreateFindingAggregatorRequestRequestTypeDef]
    ) -> CreateFindingAggregatorResponseTypeDef:
        """
        Used to enable finding aggregation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.create_finding_aggregator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#create_finding_aggregator)
        """

    async def create_insight(
        self, **kwargs: Unpack[CreateInsightRequestRequestTypeDef]
    ) -> CreateInsightResponseTypeDef:
        """
        Creates a custom insight in Security Hub.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.create_insight)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#create_insight)
        """

    async def create_members(
        self, **kwargs: Unpack[CreateMembersRequestRequestTypeDef]
    ) -> CreateMembersResponseTypeDef:
        """
        Creates a member association in Security Hub between the specified accounts and
        the account used to make the request, which is the administrator
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.create_members)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#create_members)
        """

    async def decline_invitations(
        self, **kwargs: Unpack[DeclineInvitationsRequestRequestTypeDef]
    ) -> DeclineInvitationsResponseTypeDef:
        """
        Declines invitations to become a member account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.decline_invitations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#decline_invitations)
        """

    async def delete_action_target(
        self, **kwargs: Unpack[DeleteActionTargetRequestRequestTypeDef]
    ) -> DeleteActionTargetResponseTypeDef:
        """
        Deletes a custom action target from Security Hub.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.delete_action_target)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#delete_action_target)
        """

    async def delete_configuration_policy(
        self, **kwargs: Unpack[DeleteConfigurationPolicyRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a configuration policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.delete_configuration_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#delete_configuration_policy)
        """

    async def delete_finding_aggregator(
        self, **kwargs: Unpack[DeleteFindingAggregatorRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a finding aggregator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.delete_finding_aggregator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#delete_finding_aggregator)
        """

    async def delete_insight(
        self, **kwargs: Unpack[DeleteInsightRequestRequestTypeDef]
    ) -> DeleteInsightResponseTypeDef:
        """
        Deletes the insight specified by the `InsightArn`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.delete_insight)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#delete_insight)
        """

    async def delete_invitations(
        self, **kwargs: Unpack[DeleteInvitationsRequestRequestTypeDef]
    ) -> DeleteInvitationsResponseTypeDef:
        """
        Deletes invitations received by the Amazon Web Services account to become a
        member
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.delete_invitations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#delete_invitations)
        """

    async def delete_members(
        self, **kwargs: Unpack[DeleteMembersRequestRequestTypeDef]
    ) -> DeleteMembersResponseTypeDef:
        """
        Deletes the specified member accounts from Security Hub.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.delete_members)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#delete_members)
        """

    async def describe_action_targets(
        self, **kwargs: Unpack[DescribeActionTargetsRequestRequestTypeDef]
    ) -> DescribeActionTargetsResponseTypeDef:
        """
        Returns a list of the custom action targets in Security Hub in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.describe_action_targets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#describe_action_targets)
        """

    async def describe_hub(
        self, **kwargs: Unpack[DescribeHubRequestRequestTypeDef]
    ) -> DescribeHubResponseTypeDef:
        """
        Returns details about the Hub resource in your account, including the `HubArn`
        and the time when you enabled Security
        Hub.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.describe_hub)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#describe_hub)
        """

    async def describe_organization_configuration(
        self,
    ) -> DescribeOrganizationConfigurationResponseTypeDef:
        """
        Returns information about the way your organization is configured in Security
        Hub.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.describe_organization_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#describe_organization_configuration)
        """

    async def describe_products(
        self, **kwargs: Unpack[DescribeProductsRequestRequestTypeDef]
    ) -> DescribeProductsResponseTypeDef:
        """
        Returns information about product integrations in Security Hub.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.describe_products)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#describe_products)
        """

    async def describe_standards(
        self, **kwargs: Unpack[DescribeStandardsRequestRequestTypeDef]
    ) -> DescribeStandardsResponseTypeDef:
        """
        Returns a list of the available standards in Security Hub.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.describe_standards)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#describe_standards)
        """

    async def describe_standards_controls(
        self, **kwargs: Unpack[DescribeStandardsControlsRequestRequestTypeDef]
    ) -> DescribeStandardsControlsResponseTypeDef:
        """
        Returns a list of security standards controls.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.describe_standards_controls)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#describe_standards_controls)
        """

    async def disable_import_findings_for_product(
        self, **kwargs: Unpack[DisableImportFindingsForProductRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disables the integration of the specified product with Security Hub.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.disable_import_findings_for_product)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#disable_import_findings_for_product)
        """

    async def disable_organization_admin_account(
        self, **kwargs: Unpack[DisableOrganizationAdminAccountRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disables a Security Hub administrator account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.disable_organization_admin_account)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#disable_organization_admin_account)
        """

    async def disable_security_hub(self) -> Dict[str, Any]:
        """
        Disables Security Hub in your account only in the current Amazon Web Services
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.disable_security_hub)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#disable_security_hub)
        """

    async def disassociate_from_administrator_account(self) -> Dict[str, Any]:
        """
        Disassociates the current Security Hub member account from the associated
        administrator
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.disassociate_from_administrator_account)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#disassociate_from_administrator_account)
        """

    async def disassociate_from_master_account(self) -> Dict[str, Any]:
        """
        This method is deprecated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.disassociate_from_master_account)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#disassociate_from_master_account)
        """

    async def disassociate_members(
        self, **kwargs: Unpack[DisassociateMembersRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates the specified member accounts from the associated administrator
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.disassociate_members)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#disassociate_members)
        """

    async def enable_import_findings_for_product(
        self, **kwargs: Unpack[EnableImportFindingsForProductRequestRequestTypeDef]
    ) -> EnableImportFindingsForProductResponseTypeDef:
        """
        Enables the integration of a partner product with Security Hub.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.enable_import_findings_for_product)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#enable_import_findings_for_product)
        """

    async def enable_organization_admin_account(
        self, **kwargs: Unpack[EnableOrganizationAdminAccountRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Designates the Security Hub administrator account for an organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.enable_organization_admin_account)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#enable_organization_admin_account)
        """

    async def enable_security_hub(
        self, **kwargs: Unpack[EnableSecurityHubRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Enables Security Hub for your account in the current Region or the Region you
        specify in the
        request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.enable_security_hub)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#enable_security_hub)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#generate_presigned_url)
        """

    async def get_administrator_account(self) -> GetAdministratorAccountResponseTypeDef:
        """
        Provides the details for the Security Hub administrator account for the current
        member
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.get_administrator_account)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#get_administrator_account)
        """

    async def get_configuration_policy(
        self, **kwargs: Unpack[GetConfigurationPolicyRequestRequestTypeDef]
    ) -> GetConfigurationPolicyResponseTypeDef:
        """
        Provides information about a configuration policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.get_configuration_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#get_configuration_policy)
        """

    async def get_configuration_policy_association(
        self, **kwargs: Unpack[GetConfigurationPolicyAssociationRequestRequestTypeDef]
    ) -> GetConfigurationPolicyAssociationResponseTypeDef:
        """
        Returns the association between a configuration and a target account,
        organizational unit, or the
        root.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.get_configuration_policy_association)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#get_configuration_policy_association)
        """

    async def get_enabled_standards(
        self, **kwargs: Unpack[GetEnabledStandardsRequestRequestTypeDef]
    ) -> GetEnabledStandardsResponseTypeDef:
        """
        Returns a list of the standards that are currently enabled.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.get_enabled_standards)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#get_enabled_standards)
        """

    async def get_finding_aggregator(
        self, **kwargs: Unpack[GetFindingAggregatorRequestRequestTypeDef]
    ) -> GetFindingAggregatorResponseTypeDef:
        """
        Returns the current finding aggregation configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.get_finding_aggregator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#get_finding_aggregator)
        """

    async def get_finding_history(
        self, **kwargs: Unpack[GetFindingHistoryRequestRequestTypeDef]
    ) -> GetFindingHistoryResponseTypeDef:
        """
        Returns history for a Security Hub finding in the last 90 days.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.get_finding_history)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#get_finding_history)
        """

    async def get_findings(
        self, **kwargs: Unpack[GetFindingsRequestRequestTypeDef]
    ) -> GetFindingsResponseTypeDef:
        """
        Returns a list of findings that match the specified criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.get_findings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#get_findings)
        """

    async def get_insight_results(
        self, **kwargs: Unpack[GetInsightResultsRequestRequestTypeDef]
    ) -> GetInsightResultsResponseTypeDef:
        """
        Lists the results of the Security Hub insight specified by the insight ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.get_insight_results)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#get_insight_results)
        """

    async def get_insights(
        self, **kwargs: Unpack[GetInsightsRequestRequestTypeDef]
    ) -> GetInsightsResponseTypeDef:
        """
        Lists and describes insights for the specified insight ARNs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.get_insights)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#get_insights)
        """

    async def get_invitations_count(self) -> GetInvitationsCountResponseTypeDef:
        """
        Returns the count of all Security Hub membership invitations that were sent to
        the current member account, not including the currently accepted
        invitation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.get_invitations_count)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#get_invitations_count)
        """

    async def get_master_account(self) -> GetMasterAccountResponseTypeDef:
        """
        This method is deprecated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.get_master_account)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#get_master_account)
        """

    async def get_members(
        self, **kwargs: Unpack[GetMembersRequestRequestTypeDef]
    ) -> GetMembersResponseTypeDef:
        """
        Returns the details for the Security Hub member accounts for the specified
        account
        IDs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.get_members)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#get_members)
        """

    async def get_security_control_definition(
        self, **kwargs: Unpack[GetSecurityControlDefinitionRequestRequestTypeDef]
    ) -> GetSecurityControlDefinitionResponseTypeDef:
        """
        Retrieves the definition of a security control.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.get_security_control_definition)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#get_security_control_definition)
        """

    async def invite_members(
        self, **kwargs: Unpack[InviteMembersRequestRequestTypeDef]
    ) -> InviteMembersResponseTypeDef:
        """
        Invites other Amazon Web Services accounts to become member accounts for the
        Security Hub administrator account that the invitation is sent
        from.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.invite_members)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#invite_members)
        """

    async def list_automation_rules(
        self, **kwargs: Unpack[ListAutomationRulesRequestRequestTypeDef]
    ) -> ListAutomationRulesResponseTypeDef:
        """
        A list of automation rules and their metadata for the calling account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.list_automation_rules)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#list_automation_rules)
        """

    async def list_configuration_policies(
        self, **kwargs: Unpack[ListConfigurationPoliciesRequestRequestTypeDef]
    ) -> ListConfigurationPoliciesResponseTypeDef:
        """
        Lists the configuration policies that the Security Hub delegated administrator
        has created for your
        organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.list_configuration_policies)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#list_configuration_policies)
        """

    async def list_configuration_policy_associations(
        self, **kwargs: Unpack[ListConfigurationPolicyAssociationsRequestRequestTypeDef]
    ) -> ListConfigurationPolicyAssociationsResponseTypeDef:
        """
        Provides information about the associations for your configuration policies and
        self-managed
        behavior.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.list_configuration_policy_associations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#list_configuration_policy_associations)
        """

    async def list_enabled_products_for_import(
        self, **kwargs: Unpack[ListEnabledProductsForImportRequestRequestTypeDef]
    ) -> ListEnabledProductsForImportResponseTypeDef:
        """
        Lists all findings-generating solutions (products) that you are subscribed to
        receive findings from in Security
        Hub.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.list_enabled_products_for_import)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#list_enabled_products_for_import)
        """

    async def list_finding_aggregators(
        self, **kwargs: Unpack[ListFindingAggregatorsRequestRequestTypeDef]
    ) -> ListFindingAggregatorsResponseTypeDef:
        """
        If finding aggregation is enabled, then `ListFindingAggregators` returns the
        ARN of the finding
        aggregator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.list_finding_aggregators)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#list_finding_aggregators)
        """

    async def list_invitations(
        self, **kwargs: Unpack[ListInvitationsRequestRequestTypeDef]
    ) -> ListInvitationsResponseTypeDef:
        """
        Lists all Security Hub membership invitations that were sent to the current
        Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.list_invitations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#list_invitations)
        """

    async def list_members(
        self, **kwargs: Unpack[ListMembersRequestRequestTypeDef]
    ) -> ListMembersResponseTypeDef:
        """
        Lists details about all member accounts for the current Security Hub
        administrator
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.list_members)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#list_members)
        """

    async def list_organization_admin_accounts(
        self, **kwargs: Unpack[ListOrganizationAdminAccountsRequestRequestTypeDef]
    ) -> ListOrganizationAdminAccountsResponseTypeDef:
        """
        Lists the Security Hub administrator accounts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.list_organization_admin_accounts)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#list_organization_admin_accounts)
        """

    async def list_security_control_definitions(
        self, **kwargs: Unpack[ListSecurityControlDefinitionsRequestRequestTypeDef]
    ) -> ListSecurityControlDefinitionsResponseTypeDef:
        """
        Lists all of the security controls that apply to a specified standard.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.list_security_control_definitions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#list_security_control_definitions)
        """

    async def list_standards_control_associations(
        self, **kwargs: Unpack[ListStandardsControlAssociationsRequestRequestTypeDef]
    ) -> ListStandardsControlAssociationsResponseTypeDef:
        """
        Specifies whether a control is currently enabled or disabled in each enabled
        standard in the calling
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.list_standards_control_associations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#list_standards_control_associations)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of tags associated with a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#list_tags_for_resource)
        """

    async def start_configuration_policy_association(
        self, **kwargs: Unpack[StartConfigurationPolicyAssociationRequestRequestTypeDef]
    ) -> StartConfigurationPolicyAssociationResponseTypeDef:
        """
        Associates a target account, organizational unit, or the root with a specified
        configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.start_configuration_policy_association)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#start_configuration_policy_association)
        """

    async def start_configuration_policy_disassociation(
        self, **kwargs: Unpack[StartConfigurationPolicyDisassociationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates a target account, organizational unit, or the root from a
        specified
        configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.start_configuration_policy_disassociation)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#start_configuration_policy_disassociation)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Adds one or more tags to a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes one or more tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#untag_resource)
        """

    async def update_action_target(
        self, **kwargs: Unpack[UpdateActionTargetRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the name and description of a custom action target in Security Hub.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.update_action_target)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#update_action_target)
        """

    async def update_configuration_policy(
        self, **kwargs: Unpack[UpdateConfigurationPolicyRequestRequestTypeDef]
    ) -> UpdateConfigurationPolicyResponseTypeDef:
        """
        Updates a configuration policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.update_configuration_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#update_configuration_policy)
        """

    async def update_finding_aggregator(
        self, **kwargs: Unpack[UpdateFindingAggregatorRequestRequestTypeDef]
    ) -> UpdateFindingAggregatorResponseTypeDef:
        """
        Updates the finding aggregation configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.update_finding_aggregator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#update_finding_aggregator)
        """

    async def update_findings(
        self, **kwargs: Unpack[UpdateFindingsRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        `UpdateFindings` is a deprecated operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.update_findings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#update_findings)
        """

    async def update_insight(
        self, **kwargs: Unpack[UpdateInsightRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the Security Hub insight identified by the specified insight ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.update_insight)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#update_insight)
        """

    async def update_organization_configuration(
        self, **kwargs: Unpack[UpdateOrganizationConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the configuration of your organization in Security Hub.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.update_organization_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#update_organization_configuration)
        """

    async def update_security_control(
        self, **kwargs: Unpack[UpdateSecurityControlRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the properties of a security control.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.update_security_control)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#update_security_control)
        """

    async def update_security_hub_configuration(
        self, **kwargs: Unpack[UpdateSecurityHubConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates configuration options for Security Hub.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.update_security_hub_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#update_security_hub_configuration)
        """

    async def update_standards_control(
        self, **kwargs: Unpack[UpdateStandardsControlRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Used to control whether an individual security standard control is enabled or
        disabled.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.update_standards_control)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#update_standards_control)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_action_targets"]
    ) -> DescribeActionTargetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_products"]
    ) -> DescribeProductsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_standards"]
    ) -> DescribeStandardsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_standards_controls"]
    ) -> DescribeStandardsControlsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_enabled_standards"]
    ) -> GetEnabledStandardsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_finding_history"]
    ) -> GetFindingHistoryPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_findings"]) -> GetFindingsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_insights"]) -> GetInsightsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_configuration_policies"]
    ) -> ListConfigurationPoliciesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_configuration_policy_associations"]
    ) -> ListConfigurationPolicyAssociationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_enabled_products_for_import"]
    ) -> ListEnabledProductsForImportPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_finding_aggregators"]
    ) -> ListFindingAggregatorsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_invitations"]
    ) -> ListInvitationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_members"]) -> ListMembersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_organization_admin_accounts"]
    ) -> ListOrganizationAdminAccountsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_security_control_definitions"]
    ) -> ListSecurityControlDefinitionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_standards_control_associations"]
    ) -> ListStandardsControlAssociationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/#get_paginator)
        """

    async def __aenter__(self) -> "SecurityHubClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securityhub/client/)
        """
