"""
Type annotations for waf-regional service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_waf_regional.client import WAFRegionalClient

    session = get_session()
    async with session.create_client("waf-regional") as client:
        client: WAFRegionalClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .type_defs import (
    AssociateWebACLRequestRequestTypeDef,
    CreateByteMatchSetRequestRequestTypeDef,
    CreateByteMatchSetResponseTypeDef,
    CreateGeoMatchSetRequestRequestTypeDef,
    CreateGeoMatchSetResponseTypeDef,
    CreateIPSetRequestRequestTypeDef,
    CreateIPSetResponseTypeDef,
    CreateRateBasedRuleRequestRequestTypeDef,
    CreateRateBasedRuleResponseTypeDef,
    CreateRegexMatchSetRequestRequestTypeDef,
    CreateRegexMatchSetResponseTypeDef,
    CreateRegexPatternSetRequestRequestTypeDef,
    CreateRegexPatternSetResponseTypeDef,
    CreateRuleGroupRequestRequestTypeDef,
    CreateRuleGroupResponseTypeDef,
    CreateRuleRequestRequestTypeDef,
    CreateRuleResponseTypeDef,
    CreateSizeConstraintSetRequestRequestTypeDef,
    CreateSizeConstraintSetResponseTypeDef,
    CreateSqlInjectionMatchSetRequestRequestTypeDef,
    CreateSqlInjectionMatchSetResponseTypeDef,
    CreateWebACLMigrationStackRequestRequestTypeDef,
    CreateWebACLMigrationStackResponseTypeDef,
    CreateWebACLRequestRequestTypeDef,
    CreateWebACLResponseTypeDef,
    CreateXssMatchSetRequestRequestTypeDef,
    CreateXssMatchSetResponseTypeDef,
    DeleteByteMatchSetRequestRequestTypeDef,
    DeleteByteMatchSetResponseTypeDef,
    DeleteGeoMatchSetRequestRequestTypeDef,
    DeleteGeoMatchSetResponseTypeDef,
    DeleteIPSetRequestRequestTypeDef,
    DeleteIPSetResponseTypeDef,
    DeleteLoggingConfigurationRequestRequestTypeDef,
    DeletePermissionPolicyRequestRequestTypeDef,
    DeleteRateBasedRuleRequestRequestTypeDef,
    DeleteRateBasedRuleResponseTypeDef,
    DeleteRegexMatchSetRequestRequestTypeDef,
    DeleteRegexMatchSetResponseTypeDef,
    DeleteRegexPatternSetRequestRequestTypeDef,
    DeleteRegexPatternSetResponseTypeDef,
    DeleteRuleGroupRequestRequestTypeDef,
    DeleteRuleGroupResponseTypeDef,
    DeleteRuleRequestRequestTypeDef,
    DeleteRuleResponseTypeDef,
    DeleteSizeConstraintSetRequestRequestTypeDef,
    DeleteSizeConstraintSetResponseTypeDef,
    DeleteSqlInjectionMatchSetRequestRequestTypeDef,
    DeleteSqlInjectionMatchSetResponseTypeDef,
    DeleteWebACLRequestRequestTypeDef,
    DeleteWebACLResponseTypeDef,
    DeleteXssMatchSetRequestRequestTypeDef,
    DeleteXssMatchSetResponseTypeDef,
    DisassociateWebACLRequestRequestTypeDef,
    GetByteMatchSetRequestRequestTypeDef,
    GetByteMatchSetResponseTypeDef,
    GetChangeTokenResponseTypeDef,
    GetChangeTokenStatusRequestRequestTypeDef,
    GetChangeTokenStatusResponseTypeDef,
    GetGeoMatchSetRequestRequestTypeDef,
    GetGeoMatchSetResponseTypeDef,
    GetIPSetRequestRequestTypeDef,
    GetIPSetResponseTypeDef,
    GetLoggingConfigurationRequestRequestTypeDef,
    GetLoggingConfigurationResponseTypeDef,
    GetPermissionPolicyRequestRequestTypeDef,
    GetPermissionPolicyResponseTypeDef,
    GetRateBasedRuleManagedKeysRequestRequestTypeDef,
    GetRateBasedRuleManagedKeysResponseTypeDef,
    GetRateBasedRuleRequestRequestTypeDef,
    GetRateBasedRuleResponseTypeDef,
    GetRegexMatchSetRequestRequestTypeDef,
    GetRegexMatchSetResponseTypeDef,
    GetRegexPatternSetRequestRequestTypeDef,
    GetRegexPatternSetResponseTypeDef,
    GetRuleGroupRequestRequestTypeDef,
    GetRuleGroupResponseTypeDef,
    GetRuleRequestRequestTypeDef,
    GetRuleResponseTypeDef,
    GetSampledRequestsRequestRequestTypeDef,
    GetSampledRequestsResponseTypeDef,
    GetSizeConstraintSetRequestRequestTypeDef,
    GetSizeConstraintSetResponseTypeDef,
    GetSqlInjectionMatchSetRequestRequestTypeDef,
    GetSqlInjectionMatchSetResponseTypeDef,
    GetWebACLForResourceRequestRequestTypeDef,
    GetWebACLForResourceResponseTypeDef,
    GetWebACLRequestRequestTypeDef,
    GetWebACLResponseTypeDef,
    GetXssMatchSetRequestRequestTypeDef,
    GetXssMatchSetResponseTypeDef,
    ListActivatedRulesInRuleGroupRequestRequestTypeDef,
    ListActivatedRulesInRuleGroupResponseTypeDef,
    ListByteMatchSetsRequestRequestTypeDef,
    ListByteMatchSetsResponseTypeDef,
    ListGeoMatchSetsRequestRequestTypeDef,
    ListGeoMatchSetsResponseTypeDef,
    ListIPSetsRequestRequestTypeDef,
    ListIPSetsResponseTypeDef,
    ListLoggingConfigurationsRequestRequestTypeDef,
    ListLoggingConfigurationsResponseTypeDef,
    ListRateBasedRulesRequestRequestTypeDef,
    ListRateBasedRulesResponseTypeDef,
    ListRegexMatchSetsRequestRequestTypeDef,
    ListRegexMatchSetsResponseTypeDef,
    ListRegexPatternSetsRequestRequestTypeDef,
    ListRegexPatternSetsResponseTypeDef,
    ListResourcesForWebACLRequestRequestTypeDef,
    ListResourcesForWebACLResponseTypeDef,
    ListRuleGroupsRequestRequestTypeDef,
    ListRuleGroupsResponseTypeDef,
    ListRulesRequestRequestTypeDef,
    ListRulesResponseTypeDef,
    ListSizeConstraintSetsRequestRequestTypeDef,
    ListSizeConstraintSetsResponseTypeDef,
    ListSqlInjectionMatchSetsRequestRequestTypeDef,
    ListSqlInjectionMatchSetsResponseTypeDef,
    ListSubscribedRuleGroupsRequestRequestTypeDef,
    ListSubscribedRuleGroupsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListWebACLsRequestRequestTypeDef,
    ListWebACLsResponseTypeDef,
    ListXssMatchSetsRequestRequestTypeDef,
    ListXssMatchSetsResponseTypeDef,
    PutLoggingConfigurationRequestRequestTypeDef,
    PutLoggingConfigurationResponseTypeDef,
    PutPermissionPolicyRequestRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateByteMatchSetRequestRequestTypeDef,
    UpdateByteMatchSetResponseTypeDef,
    UpdateGeoMatchSetRequestRequestTypeDef,
    UpdateGeoMatchSetResponseTypeDef,
    UpdateIPSetRequestRequestTypeDef,
    UpdateIPSetResponseTypeDef,
    UpdateRateBasedRuleRequestRequestTypeDef,
    UpdateRateBasedRuleResponseTypeDef,
    UpdateRegexMatchSetRequestRequestTypeDef,
    UpdateRegexMatchSetResponseTypeDef,
    UpdateRegexPatternSetRequestRequestTypeDef,
    UpdateRegexPatternSetResponseTypeDef,
    UpdateRuleGroupRequestRequestTypeDef,
    UpdateRuleGroupResponseTypeDef,
    UpdateRuleRequestRequestTypeDef,
    UpdateRuleResponseTypeDef,
    UpdateSizeConstraintSetRequestRequestTypeDef,
    UpdateSizeConstraintSetResponseTypeDef,
    UpdateSqlInjectionMatchSetRequestRequestTypeDef,
    UpdateSqlInjectionMatchSetResponseTypeDef,
    UpdateWebACLRequestRequestTypeDef,
    UpdateWebACLResponseTypeDef,
    UpdateXssMatchSetRequestRequestTypeDef,
    UpdateXssMatchSetResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("WAFRegionalClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    WAFBadRequestException: Type[BotocoreClientError]
    WAFDisallowedNameException: Type[BotocoreClientError]
    WAFEntityMigrationException: Type[BotocoreClientError]
    WAFInternalErrorException: Type[BotocoreClientError]
    WAFInvalidAccountException: Type[BotocoreClientError]
    WAFInvalidOperationException: Type[BotocoreClientError]
    WAFInvalidParameterException: Type[BotocoreClientError]
    WAFInvalidPermissionPolicyException: Type[BotocoreClientError]
    WAFInvalidRegexPatternException: Type[BotocoreClientError]
    WAFLimitsExceededException: Type[BotocoreClientError]
    WAFNonEmptyEntityException: Type[BotocoreClientError]
    WAFNonexistentContainerException: Type[BotocoreClientError]
    WAFNonexistentItemException: Type[BotocoreClientError]
    WAFReferencedItemException: Type[BotocoreClientError]
    WAFServiceLinkedRoleErrorException: Type[BotocoreClientError]
    WAFStaleDataException: Type[BotocoreClientError]
    WAFSubscriptionNotFoundException: Type[BotocoreClientError]
    WAFTagOperationException: Type[BotocoreClientError]
    WAFTagOperationInternalErrorException: Type[BotocoreClientError]
    WAFUnavailableEntityException: Type[BotocoreClientError]


class WAFRegionalClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        WAFRegionalClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#exceptions)
        """

    async def associate_web_acl(
        self, **kwargs: Unpack[AssociateWebACLRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.associate_web_acl)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#associate_web_acl)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#close)
        """

    async def create_byte_match_set(
        self, **kwargs: Unpack[CreateByteMatchSetRequestRequestTypeDef]
    ) -> CreateByteMatchSetResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.create_byte_match_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#create_byte_match_set)
        """

    async def create_geo_match_set(
        self, **kwargs: Unpack[CreateGeoMatchSetRequestRequestTypeDef]
    ) -> CreateGeoMatchSetResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.create_geo_match_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#create_geo_match_set)
        """

    async def create_ip_set(
        self, **kwargs: Unpack[CreateIPSetRequestRequestTypeDef]
    ) -> CreateIPSetResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.create_ip_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#create_ip_set)
        """

    async def create_rate_based_rule(
        self, **kwargs: Unpack[CreateRateBasedRuleRequestRequestTypeDef]
    ) -> CreateRateBasedRuleResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.create_rate_based_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#create_rate_based_rule)
        """

    async def create_regex_match_set(
        self, **kwargs: Unpack[CreateRegexMatchSetRequestRequestTypeDef]
    ) -> CreateRegexMatchSetResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.create_regex_match_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#create_regex_match_set)
        """

    async def create_regex_pattern_set(
        self, **kwargs: Unpack[CreateRegexPatternSetRequestRequestTypeDef]
    ) -> CreateRegexPatternSetResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.create_regex_pattern_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#create_regex_pattern_set)
        """

    async def create_rule(
        self, **kwargs: Unpack[CreateRuleRequestRequestTypeDef]
    ) -> CreateRuleResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.create_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#create_rule)
        """

    async def create_rule_group(
        self, **kwargs: Unpack[CreateRuleGroupRequestRequestTypeDef]
    ) -> CreateRuleGroupResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.create_rule_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#create_rule_group)
        """

    async def create_size_constraint_set(
        self, **kwargs: Unpack[CreateSizeConstraintSetRequestRequestTypeDef]
    ) -> CreateSizeConstraintSetResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.create_size_constraint_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#create_size_constraint_set)
        """

    async def create_sql_injection_match_set(
        self, **kwargs: Unpack[CreateSqlInjectionMatchSetRequestRequestTypeDef]
    ) -> CreateSqlInjectionMatchSetResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.create_sql_injection_match_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#create_sql_injection_match_set)
        """

    async def create_web_acl(
        self, **kwargs: Unpack[CreateWebACLRequestRequestTypeDef]
    ) -> CreateWebACLResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.create_web_acl)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#create_web_acl)
        """

    async def create_web_acl_migration_stack(
        self, **kwargs: Unpack[CreateWebACLMigrationStackRequestRequestTypeDef]
    ) -> CreateWebACLMigrationStackResponseTypeDef:
        """
        Creates an AWS CloudFormation WAFV2 template for the specified web ACL in the
        specified Amazon S3
        bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.create_web_acl_migration_stack)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#create_web_acl_migration_stack)
        """

    async def create_xss_match_set(
        self, **kwargs: Unpack[CreateXssMatchSetRequestRequestTypeDef]
    ) -> CreateXssMatchSetResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.create_xss_match_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#create_xss_match_set)
        """

    async def delete_byte_match_set(
        self, **kwargs: Unpack[DeleteByteMatchSetRequestRequestTypeDef]
    ) -> DeleteByteMatchSetResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.delete_byte_match_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#delete_byte_match_set)
        """

    async def delete_geo_match_set(
        self, **kwargs: Unpack[DeleteGeoMatchSetRequestRequestTypeDef]
    ) -> DeleteGeoMatchSetResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.delete_geo_match_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#delete_geo_match_set)
        """

    async def delete_ip_set(
        self, **kwargs: Unpack[DeleteIPSetRequestRequestTypeDef]
    ) -> DeleteIPSetResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.delete_ip_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#delete_ip_set)
        """

    async def delete_logging_configuration(
        self, **kwargs: Unpack[DeleteLoggingConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.delete_logging_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#delete_logging_configuration)
        """

    async def delete_permission_policy(
        self, **kwargs: Unpack[DeletePermissionPolicyRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.delete_permission_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#delete_permission_policy)
        """

    async def delete_rate_based_rule(
        self, **kwargs: Unpack[DeleteRateBasedRuleRequestRequestTypeDef]
    ) -> DeleteRateBasedRuleResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.delete_rate_based_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#delete_rate_based_rule)
        """

    async def delete_regex_match_set(
        self, **kwargs: Unpack[DeleteRegexMatchSetRequestRequestTypeDef]
    ) -> DeleteRegexMatchSetResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.delete_regex_match_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#delete_regex_match_set)
        """

    async def delete_regex_pattern_set(
        self, **kwargs: Unpack[DeleteRegexPatternSetRequestRequestTypeDef]
    ) -> DeleteRegexPatternSetResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.delete_regex_pattern_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#delete_regex_pattern_set)
        """

    async def delete_rule(
        self, **kwargs: Unpack[DeleteRuleRequestRequestTypeDef]
    ) -> DeleteRuleResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.delete_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#delete_rule)
        """

    async def delete_rule_group(
        self, **kwargs: Unpack[DeleteRuleGroupRequestRequestTypeDef]
    ) -> DeleteRuleGroupResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.delete_rule_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#delete_rule_group)
        """

    async def delete_size_constraint_set(
        self, **kwargs: Unpack[DeleteSizeConstraintSetRequestRequestTypeDef]
    ) -> DeleteSizeConstraintSetResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.delete_size_constraint_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#delete_size_constraint_set)
        """

    async def delete_sql_injection_match_set(
        self, **kwargs: Unpack[DeleteSqlInjectionMatchSetRequestRequestTypeDef]
    ) -> DeleteSqlInjectionMatchSetResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.delete_sql_injection_match_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#delete_sql_injection_match_set)
        """

    async def delete_web_acl(
        self, **kwargs: Unpack[DeleteWebACLRequestRequestTypeDef]
    ) -> DeleteWebACLResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.delete_web_acl)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#delete_web_acl)
        """

    async def delete_xss_match_set(
        self, **kwargs: Unpack[DeleteXssMatchSetRequestRequestTypeDef]
    ) -> DeleteXssMatchSetResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.delete_xss_match_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#delete_xss_match_set)
        """

    async def disassociate_web_acl(
        self, **kwargs: Unpack[DisassociateWebACLRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.disassociate_web_acl)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#disassociate_web_acl)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#generate_presigned_url)
        """

    async def get_byte_match_set(
        self, **kwargs: Unpack[GetByteMatchSetRequestRequestTypeDef]
    ) -> GetByteMatchSetResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.get_byte_match_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#get_byte_match_set)
        """

    async def get_change_token(self) -> GetChangeTokenResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.get_change_token)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#get_change_token)
        """

    async def get_change_token_status(
        self, **kwargs: Unpack[GetChangeTokenStatusRequestRequestTypeDef]
    ) -> GetChangeTokenStatusResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.get_change_token_status)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#get_change_token_status)
        """

    async def get_geo_match_set(
        self, **kwargs: Unpack[GetGeoMatchSetRequestRequestTypeDef]
    ) -> GetGeoMatchSetResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.get_geo_match_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#get_geo_match_set)
        """

    async def get_ip_set(
        self, **kwargs: Unpack[GetIPSetRequestRequestTypeDef]
    ) -> GetIPSetResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.get_ip_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#get_ip_set)
        """

    async def get_logging_configuration(
        self, **kwargs: Unpack[GetLoggingConfigurationRequestRequestTypeDef]
    ) -> GetLoggingConfigurationResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.get_logging_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#get_logging_configuration)
        """

    async def get_permission_policy(
        self, **kwargs: Unpack[GetPermissionPolicyRequestRequestTypeDef]
    ) -> GetPermissionPolicyResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.get_permission_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#get_permission_policy)
        """

    async def get_rate_based_rule(
        self, **kwargs: Unpack[GetRateBasedRuleRequestRequestTypeDef]
    ) -> GetRateBasedRuleResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.get_rate_based_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#get_rate_based_rule)
        """

    async def get_rate_based_rule_managed_keys(
        self, **kwargs: Unpack[GetRateBasedRuleManagedKeysRequestRequestTypeDef]
    ) -> GetRateBasedRuleManagedKeysResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.get_rate_based_rule_managed_keys)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#get_rate_based_rule_managed_keys)
        """

    async def get_regex_match_set(
        self, **kwargs: Unpack[GetRegexMatchSetRequestRequestTypeDef]
    ) -> GetRegexMatchSetResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.get_regex_match_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#get_regex_match_set)
        """

    async def get_regex_pattern_set(
        self, **kwargs: Unpack[GetRegexPatternSetRequestRequestTypeDef]
    ) -> GetRegexPatternSetResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.get_regex_pattern_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#get_regex_pattern_set)
        """

    async def get_rule(
        self, **kwargs: Unpack[GetRuleRequestRequestTypeDef]
    ) -> GetRuleResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.get_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#get_rule)
        """

    async def get_rule_group(
        self, **kwargs: Unpack[GetRuleGroupRequestRequestTypeDef]
    ) -> GetRuleGroupResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.get_rule_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#get_rule_group)
        """

    async def get_sampled_requests(
        self, **kwargs: Unpack[GetSampledRequestsRequestRequestTypeDef]
    ) -> GetSampledRequestsResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.get_sampled_requests)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#get_sampled_requests)
        """

    async def get_size_constraint_set(
        self, **kwargs: Unpack[GetSizeConstraintSetRequestRequestTypeDef]
    ) -> GetSizeConstraintSetResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.get_size_constraint_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#get_size_constraint_set)
        """

    async def get_sql_injection_match_set(
        self, **kwargs: Unpack[GetSqlInjectionMatchSetRequestRequestTypeDef]
    ) -> GetSqlInjectionMatchSetResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.get_sql_injection_match_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#get_sql_injection_match_set)
        """

    async def get_web_acl(
        self, **kwargs: Unpack[GetWebACLRequestRequestTypeDef]
    ) -> GetWebACLResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.get_web_acl)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#get_web_acl)
        """

    async def get_web_acl_for_resource(
        self, **kwargs: Unpack[GetWebACLForResourceRequestRequestTypeDef]
    ) -> GetWebACLForResourceResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.get_web_acl_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#get_web_acl_for_resource)
        """

    async def get_xss_match_set(
        self, **kwargs: Unpack[GetXssMatchSetRequestRequestTypeDef]
    ) -> GetXssMatchSetResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.get_xss_match_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#get_xss_match_set)
        """

    async def list_activated_rules_in_rule_group(
        self, **kwargs: Unpack[ListActivatedRulesInRuleGroupRequestRequestTypeDef]
    ) -> ListActivatedRulesInRuleGroupResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.list_activated_rules_in_rule_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#list_activated_rules_in_rule_group)
        """

    async def list_byte_match_sets(
        self, **kwargs: Unpack[ListByteMatchSetsRequestRequestTypeDef]
    ) -> ListByteMatchSetsResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.list_byte_match_sets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#list_byte_match_sets)
        """

    async def list_geo_match_sets(
        self, **kwargs: Unpack[ListGeoMatchSetsRequestRequestTypeDef]
    ) -> ListGeoMatchSetsResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.list_geo_match_sets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#list_geo_match_sets)
        """

    async def list_ip_sets(
        self, **kwargs: Unpack[ListIPSetsRequestRequestTypeDef]
    ) -> ListIPSetsResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.list_ip_sets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#list_ip_sets)
        """

    async def list_logging_configurations(
        self, **kwargs: Unpack[ListLoggingConfigurationsRequestRequestTypeDef]
    ) -> ListLoggingConfigurationsResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.list_logging_configurations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#list_logging_configurations)
        """

    async def list_rate_based_rules(
        self, **kwargs: Unpack[ListRateBasedRulesRequestRequestTypeDef]
    ) -> ListRateBasedRulesResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.list_rate_based_rules)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#list_rate_based_rules)
        """

    async def list_regex_match_sets(
        self, **kwargs: Unpack[ListRegexMatchSetsRequestRequestTypeDef]
    ) -> ListRegexMatchSetsResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.list_regex_match_sets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#list_regex_match_sets)
        """

    async def list_regex_pattern_sets(
        self, **kwargs: Unpack[ListRegexPatternSetsRequestRequestTypeDef]
    ) -> ListRegexPatternSetsResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.list_regex_pattern_sets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#list_regex_pattern_sets)
        """

    async def list_resources_for_web_acl(
        self, **kwargs: Unpack[ListResourcesForWebACLRequestRequestTypeDef]
    ) -> ListResourcesForWebACLResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.list_resources_for_web_acl)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#list_resources_for_web_acl)
        """

    async def list_rule_groups(
        self, **kwargs: Unpack[ListRuleGroupsRequestRequestTypeDef]
    ) -> ListRuleGroupsResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.list_rule_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#list_rule_groups)
        """

    async def list_rules(
        self, **kwargs: Unpack[ListRulesRequestRequestTypeDef]
    ) -> ListRulesResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.list_rules)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#list_rules)
        """

    async def list_size_constraint_sets(
        self, **kwargs: Unpack[ListSizeConstraintSetsRequestRequestTypeDef]
    ) -> ListSizeConstraintSetsResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.list_size_constraint_sets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#list_size_constraint_sets)
        """

    async def list_sql_injection_match_sets(
        self, **kwargs: Unpack[ListSqlInjectionMatchSetsRequestRequestTypeDef]
    ) -> ListSqlInjectionMatchSetsResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.list_sql_injection_match_sets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#list_sql_injection_match_sets)
        """

    async def list_subscribed_rule_groups(
        self, **kwargs: Unpack[ListSubscribedRuleGroupsRequestRequestTypeDef]
    ) -> ListSubscribedRuleGroupsResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.list_subscribed_rule_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#list_subscribed_rule_groups)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#list_tags_for_resource)
        """

    async def list_web_acls(
        self, **kwargs: Unpack[ListWebACLsRequestRequestTypeDef]
    ) -> ListWebACLsResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.list_web_acls)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#list_web_acls)
        """

    async def list_xss_match_sets(
        self, **kwargs: Unpack[ListXssMatchSetsRequestRequestTypeDef]
    ) -> ListXssMatchSetsResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.list_xss_match_sets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#list_xss_match_sets)
        """

    async def put_logging_configuration(
        self, **kwargs: Unpack[PutLoggingConfigurationRequestRequestTypeDef]
    ) -> PutLoggingConfigurationResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.put_logging_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#put_logging_configuration)
        """

    async def put_permission_policy(
        self, **kwargs: Unpack[PutPermissionPolicyRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.put_permission_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#put_permission_policy)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#untag_resource)
        """

    async def update_byte_match_set(
        self, **kwargs: Unpack[UpdateByteMatchSetRequestRequestTypeDef]
    ) -> UpdateByteMatchSetResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.update_byte_match_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#update_byte_match_set)
        """

    async def update_geo_match_set(
        self, **kwargs: Unpack[UpdateGeoMatchSetRequestRequestTypeDef]
    ) -> UpdateGeoMatchSetResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.update_geo_match_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#update_geo_match_set)
        """

    async def update_ip_set(
        self, **kwargs: Unpack[UpdateIPSetRequestRequestTypeDef]
    ) -> UpdateIPSetResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.update_ip_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#update_ip_set)
        """

    async def update_rate_based_rule(
        self, **kwargs: Unpack[UpdateRateBasedRuleRequestRequestTypeDef]
    ) -> UpdateRateBasedRuleResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.update_rate_based_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#update_rate_based_rule)
        """

    async def update_regex_match_set(
        self, **kwargs: Unpack[UpdateRegexMatchSetRequestRequestTypeDef]
    ) -> UpdateRegexMatchSetResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.update_regex_match_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#update_regex_match_set)
        """

    async def update_regex_pattern_set(
        self, **kwargs: Unpack[UpdateRegexPatternSetRequestRequestTypeDef]
    ) -> UpdateRegexPatternSetResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.update_regex_pattern_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#update_regex_pattern_set)
        """

    async def update_rule(
        self, **kwargs: Unpack[UpdateRuleRequestRequestTypeDef]
    ) -> UpdateRuleResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.update_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#update_rule)
        """

    async def update_rule_group(
        self, **kwargs: Unpack[UpdateRuleGroupRequestRequestTypeDef]
    ) -> UpdateRuleGroupResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.update_rule_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#update_rule_group)
        """

    async def update_size_constraint_set(
        self, **kwargs: Unpack[UpdateSizeConstraintSetRequestRequestTypeDef]
    ) -> UpdateSizeConstraintSetResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.update_size_constraint_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#update_size_constraint_set)
        """

    async def update_sql_injection_match_set(
        self, **kwargs: Unpack[UpdateSqlInjectionMatchSetRequestRequestTypeDef]
    ) -> UpdateSqlInjectionMatchSetResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.update_sql_injection_match_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#update_sql_injection_match_set)
        """

    async def update_web_acl(
        self, **kwargs: Unpack[UpdateWebACLRequestRequestTypeDef]
    ) -> UpdateWebACLResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.update_web_acl)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#update_web_acl)
        """

    async def update_xss_match_set(
        self, **kwargs: Unpack[UpdateXssMatchSetRequestRequestTypeDef]
    ) -> UpdateXssMatchSetResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client.update_xss_match_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/#update_xss_match_set)
        """

    async def __aenter__(self) -> "WAFRegionalClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf-regional.html#WAFRegional.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf_regional/client/)
        """
