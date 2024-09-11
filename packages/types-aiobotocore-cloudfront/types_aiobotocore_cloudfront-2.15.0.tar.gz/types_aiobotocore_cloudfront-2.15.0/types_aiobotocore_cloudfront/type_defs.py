"""
Type annotations for cloudfront service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/type_defs/)

Usage::

    ```python
    from types_aiobotocore_cloudfront.type_defs import AliasICPRecordalTypeDef

    data: AliasICPRecordalTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Sequence, Union

from aiobotocore.response import StreamingBody

from .literals import (
    CachePolicyCookieBehaviorType,
    CachePolicyHeaderBehaviorType,
    CachePolicyQueryStringBehaviorType,
    CachePolicyTypeType,
    CertificateSourceType,
    ContinuousDeploymentPolicyTypeType,
    EventTypeType,
    FrameOptionsListType,
    FunctionRuntimeType,
    FunctionStageType,
    GeoRestrictionTypeType,
    HttpVersionType,
    ICPRecordalStatusType,
    ItemSelectionType,
    MethodType,
    MinimumProtocolVersionType,
    OriginAccessControlOriginTypesType,
    OriginAccessControlSigningBehaviorsType,
    OriginProtocolPolicyType,
    OriginRequestPolicyCookieBehaviorType,
    OriginRequestPolicyHeaderBehaviorType,
    OriginRequestPolicyQueryStringBehaviorType,
    OriginRequestPolicyTypeType,
    PriceClassType,
    RealtimeMetricsSubscriptionStatusType,
    ReferrerPolicyListType,
    ResponseHeadersPolicyAccessControlAllowMethodsValuesType,
    ResponseHeadersPolicyTypeType,
    SslProtocolType,
    SSLSupportMethodType,
    ViewerProtocolPolicyType,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 12):
    from typing import NotRequired
else:
    from typing_extensions import NotRequired
if sys.version_info >= (3, 12):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AliasICPRecordalTypeDef",
    "AliasesOutputTypeDef",
    "AliasesTypeDef",
    "CachedMethodsOutputTypeDef",
    "CachedMethodsTypeDef",
    "AssociateAliasRequestRequestTypeDef",
    "BlobTypeDef",
    "TrustedKeyGroupsOutputTypeDef",
    "TrustedSignersOutputTypeDef",
    "TrustedKeyGroupsTypeDef",
    "TrustedSignersTypeDef",
    "CookieNamesOutputTypeDef",
    "CookieNamesTypeDef",
    "HeadersOutputTypeDef",
    "HeadersTypeDef",
    "QueryStringNamesOutputTypeDef",
    "QueryStringNamesTypeDef",
    "CloudFrontOriginAccessIdentityConfigTypeDef",
    "CloudFrontOriginAccessIdentitySummaryTypeDef",
    "ConflictingAliasTypeDef",
    "ContentTypeProfileTypeDef",
    "StagingDistributionDnsNamesOutputTypeDef",
    "StagingDistributionDnsNamesTypeDef",
    "ContinuousDeploymentSingleHeaderConfigTypeDef",
    "SessionStickinessConfigTypeDef",
    "CopyDistributionRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "KeyGroupConfigTypeDef",
    "ImportSourceTypeDef",
    "KeyValueStoreTypeDef",
    "OriginAccessControlConfigTypeDef",
    "PublicKeyConfigTypeDef",
    "CustomErrorResponseTypeDef",
    "OriginCustomHeaderTypeDef",
    "OriginSslProtocolsOutputTypeDef",
    "OriginSslProtocolsTypeDef",
    "DeleteCachePolicyRequestRequestTypeDef",
    "DeleteCloudFrontOriginAccessIdentityRequestRequestTypeDef",
    "DeleteContinuousDeploymentPolicyRequestRequestTypeDef",
    "DeleteDistributionRequestRequestTypeDef",
    "DeleteFieldLevelEncryptionConfigRequestRequestTypeDef",
    "DeleteFieldLevelEncryptionProfileRequestRequestTypeDef",
    "DeleteFunctionRequestRequestTypeDef",
    "DeleteKeyGroupRequestRequestTypeDef",
    "DeleteKeyValueStoreRequestRequestTypeDef",
    "DeleteMonitoringSubscriptionRequestRequestTypeDef",
    "DeleteOriginAccessControlRequestRequestTypeDef",
    "DeleteOriginRequestPolicyRequestRequestTypeDef",
    "DeletePublicKeyRequestRequestTypeDef",
    "DeleteRealtimeLogConfigRequestRequestTypeDef",
    "DeleteResponseHeadersPolicyRequestRequestTypeDef",
    "DeleteStreamingDistributionRequestRequestTypeDef",
    "DescribeFunctionRequestRequestTypeDef",
    "DescribeKeyValueStoreRequestRequestTypeDef",
    "LoggingConfigTypeDef",
    "ViewerCertificateTypeDef",
    "DistributionIdListTypeDef",
    "FieldPatternsOutputTypeDef",
    "FieldPatternsTypeDef",
    "KinesisStreamConfigTypeDef",
    "QueryStringCacheKeysOutputTypeDef",
    "QueryStringCacheKeysTypeDef",
    "FunctionAssociationTypeDef",
    "FunctionMetadataTypeDef",
    "GeoRestrictionOutputTypeDef",
    "GeoRestrictionTypeDef",
    "GetCachePolicyConfigRequestRequestTypeDef",
    "GetCachePolicyRequestRequestTypeDef",
    "GetCloudFrontOriginAccessIdentityConfigRequestRequestTypeDef",
    "GetCloudFrontOriginAccessIdentityRequestRequestTypeDef",
    "GetContinuousDeploymentPolicyConfigRequestRequestTypeDef",
    "GetContinuousDeploymentPolicyRequestRequestTypeDef",
    "GetDistributionConfigRequestRequestTypeDef",
    "WaiterConfigTypeDef",
    "GetDistributionRequestRequestTypeDef",
    "GetFieldLevelEncryptionConfigRequestRequestTypeDef",
    "GetFieldLevelEncryptionProfileConfigRequestRequestTypeDef",
    "GetFieldLevelEncryptionProfileRequestRequestTypeDef",
    "GetFieldLevelEncryptionRequestRequestTypeDef",
    "GetFunctionRequestRequestTypeDef",
    "GetInvalidationRequestRequestTypeDef",
    "GetKeyGroupConfigRequestRequestTypeDef",
    "KeyGroupConfigOutputTypeDef",
    "GetKeyGroupRequestRequestTypeDef",
    "GetMonitoringSubscriptionRequestRequestTypeDef",
    "GetOriginAccessControlConfigRequestRequestTypeDef",
    "GetOriginAccessControlRequestRequestTypeDef",
    "GetOriginRequestPolicyConfigRequestRequestTypeDef",
    "GetOriginRequestPolicyRequestRequestTypeDef",
    "GetPublicKeyConfigRequestRequestTypeDef",
    "GetPublicKeyRequestRequestTypeDef",
    "GetRealtimeLogConfigRequestRequestTypeDef",
    "GetResponseHeadersPolicyConfigRequestRequestTypeDef",
    "GetResponseHeadersPolicyRequestRequestTypeDef",
    "GetStreamingDistributionConfigRequestRequestTypeDef",
    "GetStreamingDistributionRequestRequestTypeDef",
    "PathsOutputTypeDef",
    "PathsTypeDef",
    "InvalidationSummaryTypeDef",
    "KeyPairIdsTypeDef",
    "KeyValueStoreAssociationTypeDef",
    "LambdaFunctionAssociationTypeDef",
    "ListCachePoliciesRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "ListCloudFrontOriginAccessIdentitiesRequestRequestTypeDef",
    "ListConflictingAliasesRequestRequestTypeDef",
    "ListContinuousDeploymentPoliciesRequestRequestTypeDef",
    "ListDistributionsByCachePolicyIdRequestRequestTypeDef",
    "ListDistributionsByKeyGroupRequestRequestTypeDef",
    "ListDistributionsByOriginRequestPolicyIdRequestRequestTypeDef",
    "ListDistributionsByRealtimeLogConfigRequestRequestTypeDef",
    "ListDistributionsByResponseHeadersPolicyIdRequestRequestTypeDef",
    "ListDistributionsByWebACLIdRequestRequestTypeDef",
    "ListDistributionsRequestRequestTypeDef",
    "ListFieldLevelEncryptionConfigsRequestRequestTypeDef",
    "ListFieldLevelEncryptionProfilesRequestRequestTypeDef",
    "ListFunctionsRequestRequestTypeDef",
    "ListInvalidationsRequestRequestTypeDef",
    "ListKeyGroupsRequestRequestTypeDef",
    "ListKeyValueStoresRequestRequestTypeDef",
    "ListOriginAccessControlsRequestRequestTypeDef",
    "ListOriginRequestPoliciesRequestRequestTypeDef",
    "ListPublicKeysRequestRequestTypeDef",
    "ListRealtimeLogConfigsRequestRequestTypeDef",
    "ListResponseHeadersPoliciesRequestRequestTypeDef",
    "ListStreamingDistributionsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "RealtimeMetricsSubscriptionConfigTypeDef",
    "OriginAccessControlSummaryTypeDef",
    "StatusCodesOutputTypeDef",
    "StatusCodesTypeDef",
    "OriginGroupMemberTypeDef",
    "OriginShieldTypeDef",
    "S3OriginConfigTypeDef",
    "PublicKeySummaryTypeDef",
    "PublishFunctionRequestRequestTypeDef",
    "QueryArgProfileTypeDef",
    "ResponseHeadersPolicyAccessControlAllowHeadersOutputTypeDef",
    "ResponseHeadersPolicyAccessControlAllowHeadersTypeDef",
    "ResponseHeadersPolicyAccessControlAllowMethodsOutputTypeDef",
    "ResponseHeadersPolicyAccessControlAllowMethodsTypeDef",
    "ResponseHeadersPolicyAccessControlAllowOriginsOutputTypeDef",
    "ResponseHeadersPolicyAccessControlAllowOriginsTypeDef",
    "ResponseHeadersPolicyAccessControlExposeHeadersOutputTypeDef",
    "ResponseHeadersPolicyAccessControlExposeHeadersTypeDef",
    "ResponseHeadersPolicyServerTimingHeadersConfigTypeDef",
    "ResponseHeadersPolicyContentSecurityPolicyTypeDef",
    "ResponseHeadersPolicyContentTypeOptionsTypeDef",
    "ResponseHeadersPolicyCustomHeaderTypeDef",
    "ResponseHeadersPolicyFrameOptionsTypeDef",
    "ResponseHeadersPolicyReferrerPolicyTypeDef",
    "ResponseHeadersPolicyRemoveHeaderTypeDef",
    "ResponseHeadersPolicyStrictTransportSecurityTypeDef",
    "ResponseHeadersPolicyXSSProtectionTypeDef",
    "S3OriginTypeDef",
    "StreamingLoggingConfigTypeDef",
    "TagKeysTypeDef",
    "TagTypeDef",
    "UpdateDistributionWithStagingConfigRequestRequestTypeDef",
    "UpdateKeyValueStoreRequestRequestTypeDef",
    "AllowedMethodsOutputTypeDef",
    "AllowedMethodsTypeDef",
    "TestFunctionRequestRequestTypeDef",
    "CachePolicyCookiesConfigOutputTypeDef",
    "CookiePreferenceOutputTypeDef",
    "OriginRequestPolicyCookiesConfigOutputTypeDef",
    "CachePolicyCookiesConfigTypeDef",
    "CookiePreferenceTypeDef",
    "OriginRequestPolicyCookiesConfigTypeDef",
    "CachePolicyHeadersConfigOutputTypeDef",
    "OriginRequestPolicyHeadersConfigOutputTypeDef",
    "CachePolicyHeadersConfigTypeDef",
    "OriginRequestPolicyHeadersConfigTypeDef",
    "CachePolicyQueryStringsConfigOutputTypeDef",
    "OriginRequestPolicyQueryStringsConfigOutputTypeDef",
    "CachePolicyQueryStringsConfigTypeDef",
    "OriginRequestPolicyQueryStringsConfigTypeDef",
    "CloudFrontOriginAccessIdentityTypeDef",
    "CreateCloudFrontOriginAccessIdentityRequestRequestTypeDef",
    "UpdateCloudFrontOriginAccessIdentityRequestRequestTypeDef",
    "CloudFrontOriginAccessIdentityListTypeDef",
    "ConflictingAliasesListTypeDef",
    "ContentTypeProfilesOutputTypeDef",
    "ContentTypeProfilesTypeDef",
    "ContinuousDeploymentSingleWeightConfigTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetCloudFrontOriginAccessIdentityConfigResultTypeDef",
    "GetFunctionResultTypeDef",
    "CreateKeyGroupRequestRequestTypeDef",
    "UpdateKeyGroupRequestRequestTypeDef",
    "CreateKeyValueStoreRequestRequestTypeDef",
    "CreateKeyValueStoreResultTypeDef",
    "DescribeKeyValueStoreResultTypeDef",
    "KeyValueStoreListTypeDef",
    "UpdateKeyValueStoreResultTypeDef",
    "CreateOriginAccessControlRequestRequestTypeDef",
    "GetOriginAccessControlConfigResultTypeDef",
    "OriginAccessControlTypeDef",
    "UpdateOriginAccessControlRequestRequestTypeDef",
    "CreatePublicKeyRequestRequestTypeDef",
    "GetPublicKeyConfigResultTypeDef",
    "PublicKeyTypeDef",
    "UpdatePublicKeyRequestRequestTypeDef",
    "CustomErrorResponsesOutputTypeDef",
    "CustomErrorResponsesTypeDef",
    "CustomHeadersOutputTypeDef",
    "CustomHeadersTypeDef",
    "CustomOriginConfigOutputTypeDef",
    "CustomOriginConfigTypeDef",
    "ListDistributionsByCachePolicyIdResultTypeDef",
    "ListDistributionsByKeyGroupResultTypeDef",
    "ListDistributionsByOriginRequestPolicyIdResultTypeDef",
    "ListDistributionsByResponseHeadersPolicyIdResultTypeDef",
    "EncryptionEntityOutputTypeDef",
    "EncryptionEntityTypeDef",
    "EndPointTypeDef",
    "FunctionAssociationsOutputTypeDef",
    "FunctionAssociationsTypeDef",
    "RestrictionsOutputTypeDef",
    "RestrictionsTypeDef",
    "GetDistributionRequestDistributionDeployedWaitTypeDef",
    "GetInvalidationRequestInvalidationCompletedWaitTypeDef",
    "GetStreamingDistributionRequestStreamingDistributionDeployedWaitTypeDef",
    "GetKeyGroupConfigResultTypeDef",
    "KeyGroupTypeDef",
    "InvalidationBatchOutputTypeDef",
    "InvalidationBatchTypeDef",
    "InvalidationListTypeDef",
    "KGKeyPairIdsTypeDef",
    "SignerTypeDef",
    "KeyValueStoreAssociationsOutputTypeDef",
    "KeyValueStoreAssociationsTypeDef",
    "LambdaFunctionAssociationsOutputTypeDef",
    "LambdaFunctionAssociationsTypeDef",
    "ListCloudFrontOriginAccessIdentitiesRequestListCloudFrontOriginAccessIdentitiesPaginateTypeDef",
    "ListDistributionsRequestListDistributionsPaginateTypeDef",
    "ListInvalidationsRequestListInvalidationsPaginateTypeDef",
    "ListKeyValueStoresRequestListKeyValueStoresPaginateTypeDef",
    "ListStreamingDistributionsRequestListStreamingDistributionsPaginateTypeDef",
    "MonitoringSubscriptionTypeDef",
    "OriginAccessControlListTypeDef",
    "OriginGroupFailoverCriteriaOutputTypeDef",
    "OriginGroupFailoverCriteriaTypeDef",
    "OriginGroupMembersOutputTypeDef",
    "OriginGroupMembersTypeDef",
    "PublicKeyListTypeDef",
    "QueryArgProfilesOutputTypeDef",
    "QueryArgProfilesTypeDef",
    "ResponseHeadersPolicyCorsConfigOutputTypeDef",
    "ResponseHeadersPolicyCorsConfigTypeDef",
    "ResponseHeadersPolicyCustomHeadersConfigOutputTypeDef",
    "ResponseHeadersPolicyCustomHeadersConfigTypeDef",
    "ResponseHeadersPolicyRemoveHeadersConfigOutputTypeDef",
    "ResponseHeadersPolicyRemoveHeadersConfigTypeDef",
    "ResponseHeadersPolicySecurityHeadersConfigTypeDef",
    "StreamingDistributionSummaryTypeDef",
    "StreamingDistributionConfigOutputTypeDef",
    "StreamingDistributionConfigTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "TagsOutputTypeDef",
    "TagsTypeDef",
    "ForwardedValuesOutputTypeDef",
    "ForwardedValuesTypeDef",
    "ParametersInCacheKeyAndForwardedToOriginOutputTypeDef",
    "OriginRequestPolicyConfigOutputTypeDef",
    "ParametersInCacheKeyAndForwardedToOriginTypeDef",
    "OriginRequestPolicyConfigTypeDef",
    "CreateCloudFrontOriginAccessIdentityResultTypeDef",
    "GetCloudFrontOriginAccessIdentityResultTypeDef",
    "UpdateCloudFrontOriginAccessIdentityResultTypeDef",
    "ListCloudFrontOriginAccessIdentitiesResultTypeDef",
    "ListConflictingAliasesResultTypeDef",
    "ContentTypeProfileConfigOutputTypeDef",
    "ContentTypeProfileConfigTypeDef",
    "TrafficConfigTypeDef",
    "ListKeyValueStoresResultTypeDef",
    "CreateOriginAccessControlResultTypeDef",
    "GetOriginAccessControlResultTypeDef",
    "UpdateOriginAccessControlResultTypeDef",
    "CreatePublicKeyResultTypeDef",
    "GetPublicKeyResultTypeDef",
    "UpdatePublicKeyResultTypeDef",
    "OriginOutputTypeDef",
    "OriginTypeDef",
    "EncryptionEntitiesOutputTypeDef",
    "EncryptionEntitiesTypeDef",
    "CreateRealtimeLogConfigRequestRequestTypeDef",
    "RealtimeLogConfigTypeDef",
    "UpdateRealtimeLogConfigRequestRequestTypeDef",
    "CreateKeyGroupResultTypeDef",
    "GetKeyGroupResultTypeDef",
    "KeyGroupSummaryTypeDef",
    "UpdateKeyGroupResultTypeDef",
    "InvalidationTypeDef",
    "CreateInvalidationRequestRequestTypeDef",
    "ListInvalidationsResultTypeDef",
    "ActiveTrustedKeyGroupsTypeDef",
    "ActiveTrustedSignersTypeDef",
    "FunctionConfigOutputTypeDef",
    "FunctionConfigTypeDef",
    "CreateMonitoringSubscriptionRequestRequestTypeDef",
    "CreateMonitoringSubscriptionResultTypeDef",
    "GetMonitoringSubscriptionResultTypeDef",
    "ListOriginAccessControlsResultTypeDef",
    "OriginGroupOutputTypeDef",
    "OriginGroupTypeDef",
    "ListPublicKeysResultTypeDef",
    "QueryArgProfileConfigOutputTypeDef",
    "QueryArgProfileConfigTypeDef",
    "ResponseHeadersPolicyConfigOutputTypeDef",
    "ResponseHeadersPolicyConfigTypeDef",
    "StreamingDistributionListTypeDef",
    "GetStreamingDistributionConfigResultTypeDef",
    "CreateStreamingDistributionRequestRequestTypeDef",
    "UpdateStreamingDistributionRequestRequestTypeDef",
    "ListTagsForResourceResultTypeDef",
    "StreamingDistributionConfigWithTagsTypeDef",
    "TagResourceRequestRequestTypeDef",
    "CacheBehaviorOutputTypeDef",
    "DefaultCacheBehaviorOutputTypeDef",
    "CacheBehaviorTypeDef",
    "DefaultCacheBehaviorTypeDef",
    "CachePolicyConfigOutputTypeDef",
    "GetOriginRequestPolicyConfigResultTypeDef",
    "OriginRequestPolicyTypeDef",
    "CachePolicyConfigTypeDef",
    "CreateOriginRequestPolicyRequestRequestTypeDef",
    "UpdateOriginRequestPolicyRequestRequestTypeDef",
    "ContinuousDeploymentPolicyConfigOutputTypeDef",
    "ContinuousDeploymentPolicyConfigTypeDef",
    "OriginsOutputTypeDef",
    "OriginsTypeDef",
    "FieldLevelEncryptionProfileConfigOutputTypeDef",
    "FieldLevelEncryptionProfileSummaryTypeDef",
    "FieldLevelEncryptionProfileConfigTypeDef",
    "CreateRealtimeLogConfigResultTypeDef",
    "GetRealtimeLogConfigResultTypeDef",
    "RealtimeLogConfigsTypeDef",
    "UpdateRealtimeLogConfigResultTypeDef",
    "KeyGroupListTypeDef",
    "CreateInvalidationResultTypeDef",
    "GetInvalidationResultTypeDef",
    "StreamingDistributionTypeDef",
    "FunctionSummaryTypeDef",
    "CreateFunctionRequestRequestTypeDef",
    "UpdateFunctionRequestRequestTypeDef",
    "OriginGroupsOutputTypeDef",
    "OriginGroupsTypeDef",
    "FieldLevelEncryptionConfigOutputTypeDef",
    "FieldLevelEncryptionSummaryTypeDef",
    "FieldLevelEncryptionConfigTypeDef",
    "GetResponseHeadersPolicyConfigResultTypeDef",
    "ResponseHeadersPolicyTypeDef",
    "CreateResponseHeadersPolicyRequestRequestTypeDef",
    "UpdateResponseHeadersPolicyRequestRequestTypeDef",
    "ListStreamingDistributionsResultTypeDef",
    "CreateStreamingDistributionWithTagsRequestRequestTypeDef",
    "CacheBehaviorsOutputTypeDef",
    "CacheBehaviorsTypeDef",
    "CachePolicyTypeDef",
    "GetCachePolicyConfigResultTypeDef",
    "CreateOriginRequestPolicyResultTypeDef",
    "GetOriginRequestPolicyResultTypeDef",
    "OriginRequestPolicySummaryTypeDef",
    "UpdateOriginRequestPolicyResultTypeDef",
    "CreateCachePolicyRequestRequestTypeDef",
    "UpdateCachePolicyRequestRequestTypeDef",
    "ContinuousDeploymentPolicyTypeDef",
    "GetContinuousDeploymentPolicyConfigResultTypeDef",
    "CreateContinuousDeploymentPolicyRequestRequestTypeDef",
    "UpdateContinuousDeploymentPolicyRequestRequestTypeDef",
    "FieldLevelEncryptionProfileTypeDef",
    "GetFieldLevelEncryptionProfileConfigResultTypeDef",
    "FieldLevelEncryptionProfileListTypeDef",
    "CreateFieldLevelEncryptionProfileRequestRequestTypeDef",
    "UpdateFieldLevelEncryptionProfileRequestRequestTypeDef",
    "ListRealtimeLogConfigsResultTypeDef",
    "ListKeyGroupsResultTypeDef",
    "CreateStreamingDistributionResultTypeDef",
    "CreateStreamingDistributionWithTagsResultTypeDef",
    "GetStreamingDistributionResultTypeDef",
    "UpdateStreamingDistributionResultTypeDef",
    "CreateFunctionResultTypeDef",
    "DescribeFunctionResultTypeDef",
    "FunctionListTypeDef",
    "PublishFunctionResultTypeDef",
    "TestResultTypeDef",
    "UpdateFunctionResultTypeDef",
    "FieldLevelEncryptionTypeDef",
    "GetFieldLevelEncryptionConfigResultTypeDef",
    "FieldLevelEncryptionListTypeDef",
    "CreateFieldLevelEncryptionConfigRequestRequestTypeDef",
    "UpdateFieldLevelEncryptionConfigRequestRequestTypeDef",
    "CreateResponseHeadersPolicyResultTypeDef",
    "GetResponseHeadersPolicyResultTypeDef",
    "ResponseHeadersPolicySummaryTypeDef",
    "UpdateResponseHeadersPolicyResultTypeDef",
    "DistributionConfigOutputTypeDef",
    "DistributionSummaryTypeDef",
    "DistributionConfigTypeDef",
    "CachePolicySummaryTypeDef",
    "CreateCachePolicyResultTypeDef",
    "GetCachePolicyResultTypeDef",
    "UpdateCachePolicyResultTypeDef",
    "OriginRequestPolicyListTypeDef",
    "ContinuousDeploymentPolicySummaryTypeDef",
    "CreateContinuousDeploymentPolicyResultTypeDef",
    "GetContinuousDeploymentPolicyResultTypeDef",
    "UpdateContinuousDeploymentPolicyResultTypeDef",
    "CreateFieldLevelEncryptionProfileResultTypeDef",
    "GetFieldLevelEncryptionProfileResultTypeDef",
    "UpdateFieldLevelEncryptionProfileResultTypeDef",
    "ListFieldLevelEncryptionProfilesResultTypeDef",
    "ListFunctionsResultTypeDef",
    "TestFunctionResultTypeDef",
    "CreateFieldLevelEncryptionConfigResultTypeDef",
    "GetFieldLevelEncryptionResultTypeDef",
    "UpdateFieldLevelEncryptionConfigResultTypeDef",
    "ListFieldLevelEncryptionConfigsResultTypeDef",
    "ResponseHeadersPolicyListTypeDef",
    "DistributionTypeDef",
    "GetDistributionConfigResultTypeDef",
    "DistributionListTypeDef",
    "CreateDistributionRequestRequestTypeDef",
    "DistributionConfigWithTagsTypeDef",
    "UpdateDistributionRequestRequestTypeDef",
    "CachePolicyListTypeDef",
    "ListOriginRequestPoliciesResultTypeDef",
    "ContinuousDeploymentPolicyListTypeDef",
    "ListResponseHeadersPoliciesResultTypeDef",
    "CopyDistributionResultTypeDef",
    "CreateDistributionResultTypeDef",
    "CreateDistributionWithTagsResultTypeDef",
    "GetDistributionResultTypeDef",
    "UpdateDistributionResultTypeDef",
    "UpdateDistributionWithStagingConfigResultTypeDef",
    "ListDistributionsByRealtimeLogConfigResultTypeDef",
    "ListDistributionsByWebACLIdResultTypeDef",
    "ListDistributionsResultTypeDef",
    "CreateDistributionWithTagsRequestRequestTypeDef",
    "ListCachePoliciesResultTypeDef",
    "ListContinuousDeploymentPoliciesResultTypeDef",
)

AliasICPRecordalTypeDef = TypedDict(
    "AliasICPRecordalTypeDef",
    {
        "CNAME": NotRequired[str],
        "ICPRecordalStatus": NotRequired[ICPRecordalStatusType],
    },
)
AliasesOutputTypeDef = TypedDict(
    "AliasesOutputTypeDef",
    {
        "Quantity": int,
        "Items": NotRequired[List[str]],
    },
)
AliasesTypeDef = TypedDict(
    "AliasesTypeDef",
    {
        "Quantity": int,
        "Items": NotRequired[Sequence[str]],
    },
)
CachedMethodsOutputTypeDef = TypedDict(
    "CachedMethodsOutputTypeDef",
    {
        "Quantity": int,
        "Items": List[MethodType],
    },
)
CachedMethodsTypeDef = TypedDict(
    "CachedMethodsTypeDef",
    {
        "Quantity": int,
        "Items": Sequence[MethodType],
    },
)
AssociateAliasRequestRequestTypeDef = TypedDict(
    "AssociateAliasRequestRequestTypeDef",
    {
        "TargetDistributionId": str,
        "Alias": str,
    },
)
BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]
TrustedKeyGroupsOutputTypeDef = TypedDict(
    "TrustedKeyGroupsOutputTypeDef",
    {
        "Enabled": bool,
        "Quantity": int,
        "Items": NotRequired[List[str]],
    },
)
TrustedSignersOutputTypeDef = TypedDict(
    "TrustedSignersOutputTypeDef",
    {
        "Enabled": bool,
        "Quantity": int,
        "Items": NotRequired[List[str]],
    },
)
TrustedKeyGroupsTypeDef = TypedDict(
    "TrustedKeyGroupsTypeDef",
    {
        "Enabled": bool,
        "Quantity": int,
        "Items": NotRequired[Sequence[str]],
    },
)
TrustedSignersTypeDef = TypedDict(
    "TrustedSignersTypeDef",
    {
        "Enabled": bool,
        "Quantity": int,
        "Items": NotRequired[Sequence[str]],
    },
)
CookieNamesOutputTypeDef = TypedDict(
    "CookieNamesOutputTypeDef",
    {
        "Quantity": int,
        "Items": NotRequired[List[str]],
    },
)
CookieNamesTypeDef = TypedDict(
    "CookieNamesTypeDef",
    {
        "Quantity": int,
        "Items": NotRequired[Sequence[str]],
    },
)
HeadersOutputTypeDef = TypedDict(
    "HeadersOutputTypeDef",
    {
        "Quantity": int,
        "Items": NotRequired[List[str]],
    },
)
HeadersTypeDef = TypedDict(
    "HeadersTypeDef",
    {
        "Quantity": int,
        "Items": NotRequired[Sequence[str]],
    },
)
QueryStringNamesOutputTypeDef = TypedDict(
    "QueryStringNamesOutputTypeDef",
    {
        "Quantity": int,
        "Items": NotRequired[List[str]],
    },
)
QueryStringNamesTypeDef = TypedDict(
    "QueryStringNamesTypeDef",
    {
        "Quantity": int,
        "Items": NotRequired[Sequence[str]],
    },
)
CloudFrontOriginAccessIdentityConfigTypeDef = TypedDict(
    "CloudFrontOriginAccessIdentityConfigTypeDef",
    {
        "CallerReference": str,
        "Comment": str,
    },
)
CloudFrontOriginAccessIdentitySummaryTypeDef = TypedDict(
    "CloudFrontOriginAccessIdentitySummaryTypeDef",
    {
        "Id": str,
        "S3CanonicalUserId": str,
        "Comment": str,
    },
)
ConflictingAliasTypeDef = TypedDict(
    "ConflictingAliasTypeDef",
    {
        "Alias": NotRequired[str],
        "DistributionId": NotRequired[str],
        "AccountId": NotRequired[str],
    },
)
ContentTypeProfileTypeDef = TypedDict(
    "ContentTypeProfileTypeDef",
    {
        "Format": Literal["URLEncoded"],
        "ContentType": str,
        "ProfileId": NotRequired[str],
    },
)
StagingDistributionDnsNamesOutputTypeDef = TypedDict(
    "StagingDistributionDnsNamesOutputTypeDef",
    {
        "Quantity": int,
        "Items": NotRequired[List[str]],
    },
)
StagingDistributionDnsNamesTypeDef = TypedDict(
    "StagingDistributionDnsNamesTypeDef",
    {
        "Quantity": int,
        "Items": NotRequired[Sequence[str]],
    },
)
ContinuousDeploymentSingleHeaderConfigTypeDef = TypedDict(
    "ContinuousDeploymentSingleHeaderConfigTypeDef",
    {
        "Header": str,
        "Value": str,
    },
)
SessionStickinessConfigTypeDef = TypedDict(
    "SessionStickinessConfigTypeDef",
    {
        "IdleTTL": int,
        "MaximumTTL": int,
    },
)
CopyDistributionRequestRequestTypeDef = TypedDict(
    "CopyDistributionRequestRequestTypeDef",
    {
        "PrimaryDistributionId": str,
        "CallerReference": str,
        "Staging": NotRequired[bool],
        "IfMatch": NotRequired[str],
        "Enabled": NotRequired[bool],
    },
)
ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
        "HostId": NotRequired[str],
    },
)
KeyGroupConfigTypeDef = TypedDict(
    "KeyGroupConfigTypeDef",
    {
        "Name": str,
        "Items": Sequence[str],
        "Comment": NotRequired[str],
    },
)
ImportSourceTypeDef = TypedDict(
    "ImportSourceTypeDef",
    {
        "SourceType": Literal["S3"],
        "SourceARN": str,
    },
)
KeyValueStoreTypeDef = TypedDict(
    "KeyValueStoreTypeDef",
    {
        "Name": str,
        "Id": str,
        "Comment": str,
        "ARN": str,
        "LastModifiedTime": datetime,
        "Status": NotRequired[str],
    },
)
OriginAccessControlConfigTypeDef = TypedDict(
    "OriginAccessControlConfigTypeDef",
    {
        "Name": str,
        "SigningProtocol": Literal["sigv4"],
        "SigningBehavior": OriginAccessControlSigningBehaviorsType,
        "OriginAccessControlOriginType": OriginAccessControlOriginTypesType,
        "Description": NotRequired[str],
    },
)
PublicKeyConfigTypeDef = TypedDict(
    "PublicKeyConfigTypeDef",
    {
        "CallerReference": str,
        "Name": str,
        "EncodedKey": str,
        "Comment": NotRequired[str],
    },
)
CustomErrorResponseTypeDef = TypedDict(
    "CustomErrorResponseTypeDef",
    {
        "ErrorCode": int,
        "ResponsePagePath": NotRequired[str],
        "ResponseCode": NotRequired[str],
        "ErrorCachingMinTTL": NotRequired[int],
    },
)
OriginCustomHeaderTypeDef = TypedDict(
    "OriginCustomHeaderTypeDef",
    {
        "HeaderName": str,
        "HeaderValue": str,
    },
)
OriginSslProtocolsOutputTypeDef = TypedDict(
    "OriginSslProtocolsOutputTypeDef",
    {
        "Quantity": int,
        "Items": List[SslProtocolType],
    },
)
OriginSslProtocolsTypeDef = TypedDict(
    "OriginSslProtocolsTypeDef",
    {
        "Quantity": int,
        "Items": Sequence[SslProtocolType],
    },
)
DeleteCachePolicyRequestRequestTypeDef = TypedDict(
    "DeleteCachePolicyRequestRequestTypeDef",
    {
        "Id": str,
        "IfMatch": NotRequired[str],
    },
)
DeleteCloudFrontOriginAccessIdentityRequestRequestTypeDef = TypedDict(
    "DeleteCloudFrontOriginAccessIdentityRequestRequestTypeDef",
    {
        "Id": str,
        "IfMatch": NotRequired[str],
    },
)
DeleteContinuousDeploymentPolicyRequestRequestTypeDef = TypedDict(
    "DeleteContinuousDeploymentPolicyRequestRequestTypeDef",
    {
        "Id": str,
        "IfMatch": NotRequired[str],
    },
)
DeleteDistributionRequestRequestTypeDef = TypedDict(
    "DeleteDistributionRequestRequestTypeDef",
    {
        "Id": str,
        "IfMatch": NotRequired[str],
    },
)
DeleteFieldLevelEncryptionConfigRequestRequestTypeDef = TypedDict(
    "DeleteFieldLevelEncryptionConfigRequestRequestTypeDef",
    {
        "Id": str,
        "IfMatch": NotRequired[str],
    },
)
DeleteFieldLevelEncryptionProfileRequestRequestTypeDef = TypedDict(
    "DeleteFieldLevelEncryptionProfileRequestRequestTypeDef",
    {
        "Id": str,
        "IfMatch": NotRequired[str],
    },
)
DeleteFunctionRequestRequestTypeDef = TypedDict(
    "DeleteFunctionRequestRequestTypeDef",
    {
        "Name": str,
        "IfMatch": str,
    },
)
DeleteKeyGroupRequestRequestTypeDef = TypedDict(
    "DeleteKeyGroupRequestRequestTypeDef",
    {
        "Id": str,
        "IfMatch": NotRequired[str],
    },
)
DeleteKeyValueStoreRequestRequestTypeDef = TypedDict(
    "DeleteKeyValueStoreRequestRequestTypeDef",
    {
        "Name": str,
        "IfMatch": str,
    },
)
DeleteMonitoringSubscriptionRequestRequestTypeDef = TypedDict(
    "DeleteMonitoringSubscriptionRequestRequestTypeDef",
    {
        "DistributionId": str,
    },
)
DeleteOriginAccessControlRequestRequestTypeDef = TypedDict(
    "DeleteOriginAccessControlRequestRequestTypeDef",
    {
        "Id": str,
        "IfMatch": NotRequired[str],
    },
)
DeleteOriginRequestPolicyRequestRequestTypeDef = TypedDict(
    "DeleteOriginRequestPolicyRequestRequestTypeDef",
    {
        "Id": str,
        "IfMatch": NotRequired[str],
    },
)
DeletePublicKeyRequestRequestTypeDef = TypedDict(
    "DeletePublicKeyRequestRequestTypeDef",
    {
        "Id": str,
        "IfMatch": NotRequired[str],
    },
)
DeleteRealtimeLogConfigRequestRequestTypeDef = TypedDict(
    "DeleteRealtimeLogConfigRequestRequestTypeDef",
    {
        "Name": NotRequired[str],
        "ARN": NotRequired[str],
    },
)
DeleteResponseHeadersPolicyRequestRequestTypeDef = TypedDict(
    "DeleteResponseHeadersPolicyRequestRequestTypeDef",
    {
        "Id": str,
        "IfMatch": NotRequired[str],
    },
)
DeleteStreamingDistributionRequestRequestTypeDef = TypedDict(
    "DeleteStreamingDistributionRequestRequestTypeDef",
    {
        "Id": str,
        "IfMatch": NotRequired[str],
    },
)
DescribeFunctionRequestRequestTypeDef = TypedDict(
    "DescribeFunctionRequestRequestTypeDef",
    {
        "Name": str,
        "Stage": NotRequired[FunctionStageType],
    },
)
DescribeKeyValueStoreRequestRequestTypeDef = TypedDict(
    "DescribeKeyValueStoreRequestRequestTypeDef",
    {
        "Name": str,
    },
)
LoggingConfigTypeDef = TypedDict(
    "LoggingConfigTypeDef",
    {
        "Enabled": bool,
        "IncludeCookies": bool,
        "Bucket": str,
        "Prefix": str,
    },
)
ViewerCertificateTypeDef = TypedDict(
    "ViewerCertificateTypeDef",
    {
        "CloudFrontDefaultCertificate": NotRequired[bool],
        "IAMCertificateId": NotRequired[str],
        "ACMCertificateArn": NotRequired[str],
        "SSLSupportMethod": NotRequired[SSLSupportMethodType],
        "MinimumProtocolVersion": NotRequired[MinimumProtocolVersionType],
        "Certificate": NotRequired[str],
        "CertificateSource": NotRequired[CertificateSourceType],
    },
)
DistributionIdListTypeDef = TypedDict(
    "DistributionIdListTypeDef",
    {
        "Marker": str,
        "MaxItems": int,
        "IsTruncated": bool,
        "Quantity": int,
        "NextMarker": NotRequired[str],
        "Items": NotRequired[List[str]],
    },
)
FieldPatternsOutputTypeDef = TypedDict(
    "FieldPatternsOutputTypeDef",
    {
        "Quantity": int,
        "Items": NotRequired[List[str]],
    },
)
FieldPatternsTypeDef = TypedDict(
    "FieldPatternsTypeDef",
    {
        "Quantity": int,
        "Items": NotRequired[Sequence[str]],
    },
)
KinesisStreamConfigTypeDef = TypedDict(
    "KinesisStreamConfigTypeDef",
    {
        "RoleARN": str,
        "StreamARN": str,
    },
)
QueryStringCacheKeysOutputTypeDef = TypedDict(
    "QueryStringCacheKeysOutputTypeDef",
    {
        "Quantity": int,
        "Items": NotRequired[List[str]],
    },
)
QueryStringCacheKeysTypeDef = TypedDict(
    "QueryStringCacheKeysTypeDef",
    {
        "Quantity": int,
        "Items": NotRequired[Sequence[str]],
    },
)
FunctionAssociationTypeDef = TypedDict(
    "FunctionAssociationTypeDef",
    {
        "FunctionARN": str,
        "EventType": EventTypeType,
    },
)
FunctionMetadataTypeDef = TypedDict(
    "FunctionMetadataTypeDef",
    {
        "FunctionARN": str,
        "LastModifiedTime": datetime,
        "Stage": NotRequired[FunctionStageType],
        "CreatedTime": NotRequired[datetime],
    },
)
GeoRestrictionOutputTypeDef = TypedDict(
    "GeoRestrictionOutputTypeDef",
    {
        "RestrictionType": GeoRestrictionTypeType,
        "Quantity": int,
        "Items": NotRequired[List[str]],
    },
)
GeoRestrictionTypeDef = TypedDict(
    "GeoRestrictionTypeDef",
    {
        "RestrictionType": GeoRestrictionTypeType,
        "Quantity": int,
        "Items": NotRequired[Sequence[str]],
    },
)
GetCachePolicyConfigRequestRequestTypeDef = TypedDict(
    "GetCachePolicyConfigRequestRequestTypeDef",
    {
        "Id": str,
    },
)
GetCachePolicyRequestRequestTypeDef = TypedDict(
    "GetCachePolicyRequestRequestTypeDef",
    {
        "Id": str,
    },
)
GetCloudFrontOriginAccessIdentityConfigRequestRequestTypeDef = TypedDict(
    "GetCloudFrontOriginAccessIdentityConfigRequestRequestTypeDef",
    {
        "Id": str,
    },
)
GetCloudFrontOriginAccessIdentityRequestRequestTypeDef = TypedDict(
    "GetCloudFrontOriginAccessIdentityRequestRequestTypeDef",
    {
        "Id": str,
    },
)
GetContinuousDeploymentPolicyConfigRequestRequestTypeDef = TypedDict(
    "GetContinuousDeploymentPolicyConfigRequestRequestTypeDef",
    {
        "Id": str,
    },
)
GetContinuousDeploymentPolicyRequestRequestTypeDef = TypedDict(
    "GetContinuousDeploymentPolicyRequestRequestTypeDef",
    {
        "Id": str,
    },
)
GetDistributionConfigRequestRequestTypeDef = TypedDict(
    "GetDistributionConfigRequestRequestTypeDef",
    {
        "Id": str,
    },
)
WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef",
    {
        "Delay": NotRequired[int],
        "MaxAttempts": NotRequired[int],
    },
)
GetDistributionRequestRequestTypeDef = TypedDict(
    "GetDistributionRequestRequestTypeDef",
    {
        "Id": str,
    },
)
GetFieldLevelEncryptionConfigRequestRequestTypeDef = TypedDict(
    "GetFieldLevelEncryptionConfigRequestRequestTypeDef",
    {
        "Id": str,
    },
)
GetFieldLevelEncryptionProfileConfigRequestRequestTypeDef = TypedDict(
    "GetFieldLevelEncryptionProfileConfigRequestRequestTypeDef",
    {
        "Id": str,
    },
)
GetFieldLevelEncryptionProfileRequestRequestTypeDef = TypedDict(
    "GetFieldLevelEncryptionProfileRequestRequestTypeDef",
    {
        "Id": str,
    },
)
GetFieldLevelEncryptionRequestRequestTypeDef = TypedDict(
    "GetFieldLevelEncryptionRequestRequestTypeDef",
    {
        "Id": str,
    },
)
GetFunctionRequestRequestTypeDef = TypedDict(
    "GetFunctionRequestRequestTypeDef",
    {
        "Name": str,
        "Stage": NotRequired[FunctionStageType],
    },
)
GetInvalidationRequestRequestTypeDef = TypedDict(
    "GetInvalidationRequestRequestTypeDef",
    {
        "DistributionId": str,
        "Id": str,
    },
)
GetKeyGroupConfigRequestRequestTypeDef = TypedDict(
    "GetKeyGroupConfigRequestRequestTypeDef",
    {
        "Id": str,
    },
)
KeyGroupConfigOutputTypeDef = TypedDict(
    "KeyGroupConfigOutputTypeDef",
    {
        "Name": str,
        "Items": List[str],
        "Comment": NotRequired[str],
    },
)
GetKeyGroupRequestRequestTypeDef = TypedDict(
    "GetKeyGroupRequestRequestTypeDef",
    {
        "Id": str,
    },
)
GetMonitoringSubscriptionRequestRequestTypeDef = TypedDict(
    "GetMonitoringSubscriptionRequestRequestTypeDef",
    {
        "DistributionId": str,
    },
)
GetOriginAccessControlConfigRequestRequestTypeDef = TypedDict(
    "GetOriginAccessControlConfigRequestRequestTypeDef",
    {
        "Id": str,
    },
)
GetOriginAccessControlRequestRequestTypeDef = TypedDict(
    "GetOriginAccessControlRequestRequestTypeDef",
    {
        "Id": str,
    },
)
GetOriginRequestPolicyConfigRequestRequestTypeDef = TypedDict(
    "GetOriginRequestPolicyConfigRequestRequestTypeDef",
    {
        "Id": str,
    },
)
GetOriginRequestPolicyRequestRequestTypeDef = TypedDict(
    "GetOriginRequestPolicyRequestRequestTypeDef",
    {
        "Id": str,
    },
)
GetPublicKeyConfigRequestRequestTypeDef = TypedDict(
    "GetPublicKeyConfigRequestRequestTypeDef",
    {
        "Id": str,
    },
)
GetPublicKeyRequestRequestTypeDef = TypedDict(
    "GetPublicKeyRequestRequestTypeDef",
    {
        "Id": str,
    },
)
GetRealtimeLogConfigRequestRequestTypeDef = TypedDict(
    "GetRealtimeLogConfigRequestRequestTypeDef",
    {
        "Name": NotRequired[str],
        "ARN": NotRequired[str],
    },
)
GetResponseHeadersPolicyConfigRequestRequestTypeDef = TypedDict(
    "GetResponseHeadersPolicyConfigRequestRequestTypeDef",
    {
        "Id": str,
    },
)
GetResponseHeadersPolicyRequestRequestTypeDef = TypedDict(
    "GetResponseHeadersPolicyRequestRequestTypeDef",
    {
        "Id": str,
    },
)
GetStreamingDistributionConfigRequestRequestTypeDef = TypedDict(
    "GetStreamingDistributionConfigRequestRequestTypeDef",
    {
        "Id": str,
    },
)
GetStreamingDistributionRequestRequestTypeDef = TypedDict(
    "GetStreamingDistributionRequestRequestTypeDef",
    {
        "Id": str,
    },
)
PathsOutputTypeDef = TypedDict(
    "PathsOutputTypeDef",
    {
        "Quantity": int,
        "Items": NotRequired[List[str]],
    },
)
PathsTypeDef = TypedDict(
    "PathsTypeDef",
    {
        "Quantity": int,
        "Items": NotRequired[Sequence[str]],
    },
)
InvalidationSummaryTypeDef = TypedDict(
    "InvalidationSummaryTypeDef",
    {
        "Id": str,
        "CreateTime": datetime,
        "Status": str,
    },
)
KeyPairIdsTypeDef = TypedDict(
    "KeyPairIdsTypeDef",
    {
        "Quantity": int,
        "Items": NotRequired[List[str]],
    },
)
KeyValueStoreAssociationTypeDef = TypedDict(
    "KeyValueStoreAssociationTypeDef",
    {
        "KeyValueStoreARN": str,
    },
)
LambdaFunctionAssociationTypeDef = TypedDict(
    "LambdaFunctionAssociationTypeDef",
    {
        "LambdaFunctionARN": str,
        "EventType": EventTypeType,
        "IncludeBody": NotRequired[bool],
    },
)
ListCachePoliciesRequestRequestTypeDef = TypedDict(
    "ListCachePoliciesRequestRequestTypeDef",
    {
        "Type": NotRequired[CachePolicyTypeType],
        "Marker": NotRequired[str],
        "MaxItems": NotRequired[str],
    },
)
PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": NotRequired[int],
        "PageSize": NotRequired[int],
        "StartingToken": NotRequired[str],
    },
)
ListCloudFrontOriginAccessIdentitiesRequestRequestTypeDef = TypedDict(
    "ListCloudFrontOriginAccessIdentitiesRequestRequestTypeDef",
    {
        "Marker": NotRequired[str],
        "MaxItems": NotRequired[str],
    },
)
ListConflictingAliasesRequestRequestTypeDef = TypedDict(
    "ListConflictingAliasesRequestRequestTypeDef",
    {
        "DistributionId": str,
        "Alias": str,
        "Marker": NotRequired[str],
        "MaxItems": NotRequired[int],
    },
)
ListContinuousDeploymentPoliciesRequestRequestTypeDef = TypedDict(
    "ListContinuousDeploymentPoliciesRequestRequestTypeDef",
    {
        "Marker": NotRequired[str],
        "MaxItems": NotRequired[str],
    },
)
ListDistributionsByCachePolicyIdRequestRequestTypeDef = TypedDict(
    "ListDistributionsByCachePolicyIdRequestRequestTypeDef",
    {
        "CachePolicyId": str,
        "Marker": NotRequired[str],
        "MaxItems": NotRequired[str],
    },
)
ListDistributionsByKeyGroupRequestRequestTypeDef = TypedDict(
    "ListDistributionsByKeyGroupRequestRequestTypeDef",
    {
        "KeyGroupId": str,
        "Marker": NotRequired[str],
        "MaxItems": NotRequired[str],
    },
)
ListDistributionsByOriginRequestPolicyIdRequestRequestTypeDef = TypedDict(
    "ListDistributionsByOriginRequestPolicyIdRequestRequestTypeDef",
    {
        "OriginRequestPolicyId": str,
        "Marker": NotRequired[str],
        "MaxItems": NotRequired[str],
    },
)
ListDistributionsByRealtimeLogConfigRequestRequestTypeDef = TypedDict(
    "ListDistributionsByRealtimeLogConfigRequestRequestTypeDef",
    {
        "Marker": NotRequired[str],
        "MaxItems": NotRequired[str],
        "RealtimeLogConfigName": NotRequired[str],
        "RealtimeLogConfigArn": NotRequired[str],
    },
)
ListDistributionsByResponseHeadersPolicyIdRequestRequestTypeDef = TypedDict(
    "ListDistributionsByResponseHeadersPolicyIdRequestRequestTypeDef",
    {
        "ResponseHeadersPolicyId": str,
        "Marker": NotRequired[str],
        "MaxItems": NotRequired[str],
    },
)
ListDistributionsByWebACLIdRequestRequestTypeDef = TypedDict(
    "ListDistributionsByWebACLIdRequestRequestTypeDef",
    {
        "WebACLId": str,
        "Marker": NotRequired[str],
        "MaxItems": NotRequired[str],
    },
)
ListDistributionsRequestRequestTypeDef = TypedDict(
    "ListDistributionsRequestRequestTypeDef",
    {
        "Marker": NotRequired[str],
        "MaxItems": NotRequired[str],
    },
)
ListFieldLevelEncryptionConfigsRequestRequestTypeDef = TypedDict(
    "ListFieldLevelEncryptionConfigsRequestRequestTypeDef",
    {
        "Marker": NotRequired[str],
        "MaxItems": NotRequired[str],
    },
)
ListFieldLevelEncryptionProfilesRequestRequestTypeDef = TypedDict(
    "ListFieldLevelEncryptionProfilesRequestRequestTypeDef",
    {
        "Marker": NotRequired[str],
        "MaxItems": NotRequired[str],
    },
)
ListFunctionsRequestRequestTypeDef = TypedDict(
    "ListFunctionsRequestRequestTypeDef",
    {
        "Marker": NotRequired[str],
        "MaxItems": NotRequired[str],
        "Stage": NotRequired[FunctionStageType],
    },
)
ListInvalidationsRequestRequestTypeDef = TypedDict(
    "ListInvalidationsRequestRequestTypeDef",
    {
        "DistributionId": str,
        "Marker": NotRequired[str],
        "MaxItems": NotRequired[str],
    },
)
ListKeyGroupsRequestRequestTypeDef = TypedDict(
    "ListKeyGroupsRequestRequestTypeDef",
    {
        "Marker": NotRequired[str],
        "MaxItems": NotRequired[str],
    },
)
ListKeyValueStoresRequestRequestTypeDef = TypedDict(
    "ListKeyValueStoresRequestRequestTypeDef",
    {
        "Marker": NotRequired[str],
        "MaxItems": NotRequired[str],
        "Status": NotRequired[str],
    },
)
ListOriginAccessControlsRequestRequestTypeDef = TypedDict(
    "ListOriginAccessControlsRequestRequestTypeDef",
    {
        "Marker": NotRequired[str],
        "MaxItems": NotRequired[str],
    },
)
ListOriginRequestPoliciesRequestRequestTypeDef = TypedDict(
    "ListOriginRequestPoliciesRequestRequestTypeDef",
    {
        "Type": NotRequired[OriginRequestPolicyTypeType],
        "Marker": NotRequired[str],
        "MaxItems": NotRequired[str],
    },
)
ListPublicKeysRequestRequestTypeDef = TypedDict(
    "ListPublicKeysRequestRequestTypeDef",
    {
        "Marker": NotRequired[str],
        "MaxItems": NotRequired[str],
    },
)
ListRealtimeLogConfigsRequestRequestTypeDef = TypedDict(
    "ListRealtimeLogConfigsRequestRequestTypeDef",
    {
        "MaxItems": NotRequired[str],
        "Marker": NotRequired[str],
    },
)
ListResponseHeadersPoliciesRequestRequestTypeDef = TypedDict(
    "ListResponseHeadersPoliciesRequestRequestTypeDef",
    {
        "Type": NotRequired[ResponseHeadersPolicyTypeType],
        "Marker": NotRequired[str],
        "MaxItems": NotRequired[str],
    },
)
ListStreamingDistributionsRequestRequestTypeDef = TypedDict(
    "ListStreamingDistributionsRequestRequestTypeDef",
    {
        "Marker": NotRequired[str],
        "MaxItems": NotRequired[str],
    },
)
ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "Resource": str,
    },
)
RealtimeMetricsSubscriptionConfigTypeDef = TypedDict(
    "RealtimeMetricsSubscriptionConfigTypeDef",
    {
        "RealtimeMetricsSubscriptionStatus": RealtimeMetricsSubscriptionStatusType,
    },
)
OriginAccessControlSummaryTypeDef = TypedDict(
    "OriginAccessControlSummaryTypeDef",
    {
        "Id": str,
        "Description": str,
        "Name": str,
        "SigningProtocol": Literal["sigv4"],
        "SigningBehavior": OriginAccessControlSigningBehaviorsType,
        "OriginAccessControlOriginType": OriginAccessControlOriginTypesType,
    },
)
StatusCodesOutputTypeDef = TypedDict(
    "StatusCodesOutputTypeDef",
    {
        "Quantity": int,
        "Items": List[int],
    },
)
StatusCodesTypeDef = TypedDict(
    "StatusCodesTypeDef",
    {
        "Quantity": int,
        "Items": Sequence[int],
    },
)
OriginGroupMemberTypeDef = TypedDict(
    "OriginGroupMemberTypeDef",
    {
        "OriginId": str,
    },
)
OriginShieldTypeDef = TypedDict(
    "OriginShieldTypeDef",
    {
        "Enabled": bool,
        "OriginShieldRegion": NotRequired[str],
    },
)
S3OriginConfigTypeDef = TypedDict(
    "S3OriginConfigTypeDef",
    {
        "OriginAccessIdentity": str,
    },
)
PublicKeySummaryTypeDef = TypedDict(
    "PublicKeySummaryTypeDef",
    {
        "Id": str,
        "Name": str,
        "CreatedTime": datetime,
        "EncodedKey": str,
        "Comment": NotRequired[str],
    },
)
PublishFunctionRequestRequestTypeDef = TypedDict(
    "PublishFunctionRequestRequestTypeDef",
    {
        "Name": str,
        "IfMatch": str,
    },
)
QueryArgProfileTypeDef = TypedDict(
    "QueryArgProfileTypeDef",
    {
        "QueryArg": str,
        "ProfileId": str,
    },
)
ResponseHeadersPolicyAccessControlAllowHeadersOutputTypeDef = TypedDict(
    "ResponseHeadersPolicyAccessControlAllowHeadersOutputTypeDef",
    {
        "Quantity": int,
        "Items": List[str],
    },
)
ResponseHeadersPolicyAccessControlAllowHeadersTypeDef = TypedDict(
    "ResponseHeadersPolicyAccessControlAllowHeadersTypeDef",
    {
        "Quantity": int,
        "Items": Sequence[str],
    },
)
ResponseHeadersPolicyAccessControlAllowMethodsOutputTypeDef = TypedDict(
    "ResponseHeadersPolicyAccessControlAllowMethodsOutputTypeDef",
    {
        "Quantity": int,
        "Items": List[ResponseHeadersPolicyAccessControlAllowMethodsValuesType],
    },
)
ResponseHeadersPolicyAccessControlAllowMethodsTypeDef = TypedDict(
    "ResponseHeadersPolicyAccessControlAllowMethodsTypeDef",
    {
        "Quantity": int,
        "Items": Sequence[ResponseHeadersPolicyAccessControlAllowMethodsValuesType],
    },
)
ResponseHeadersPolicyAccessControlAllowOriginsOutputTypeDef = TypedDict(
    "ResponseHeadersPolicyAccessControlAllowOriginsOutputTypeDef",
    {
        "Quantity": int,
        "Items": List[str],
    },
)
ResponseHeadersPolicyAccessControlAllowOriginsTypeDef = TypedDict(
    "ResponseHeadersPolicyAccessControlAllowOriginsTypeDef",
    {
        "Quantity": int,
        "Items": Sequence[str],
    },
)
ResponseHeadersPolicyAccessControlExposeHeadersOutputTypeDef = TypedDict(
    "ResponseHeadersPolicyAccessControlExposeHeadersOutputTypeDef",
    {
        "Quantity": int,
        "Items": NotRequired[List[str]],
    },
)
ResponseHeadersPolicyAccessControlExposeHeadersTypeDef = TypedDict(
    "ResponseHeadersPolicyAccessControlExposeHeadersTypeDef",
    {
        "Quantity": int,
        "Items": NotRequired[Sequence[str]],
    },
)
ResponseHeadersPolicyServerTimingHeadersConfigTypeDef = TypedDict(
    "ResponseHeadersPolicyServerTimingHeadersConfigTypeDef",
    {
        "Enabled": bool,
        "SamplingRate": NotRequired[float],
    },
)
ResponseHeadersPolicyContentSecurityPolicyTypeDef = TypedDict(
    "ResponseHeadersPolicyContentSecurityPolicyTypeDef",
    {
        "Override": bool,
        "ContentSecurityPolicy": str,
    },
)
ResponseHeadersPolicyContentTypeOptionsTypeDef = TypedDict(
    "ResponseHeadersPolicyContentTypeOptionsTypeDef",
    {
        "Override": bool,
    },
)
ResponseHeadersPolicyCustomHeaderTypeDef = TypedDict(
    "ResponseHeadersPolicyCustomHeaderTypeDef",
    {
        "Header": str,
        "Value": str,
        "Override": bool,
    },
)
ResponseHeadersPolicyFrameOptionsTypeDef = TypedDict(
    "ResponseHeadersPolicyFrameOptionsTypeDef",
    {
        "Override": bool,
        "FrameOption": FrameOptionsListType,
    },
)
ResponseHeadersPolicyReferrerPolicyTypeDef = TypedDict(
    "ResponseHeadersPolicyReferrerPolicyTypeDef",
    {
        "Override": bool,
        "ReferrerPolicy": ReferrerPolicyListType,
    },
)
ResponseHeadersPolicyRemoveHeaderTypeDef = TypedDict(
    "ResponseHeadersPolicyRemoveHeaderTypeDef",
    {
        "Header": str,
    },
)
ResponseHeadersPolicyStrictTransportSecurityTypeDef = TypedDict(
    "ResponseHeadersPolicyStrictTransportSecurityTypeDef",
    {
        "Override": bool,
        "AccessControlMaxAgeSec": int,
        "IncludeSubdomains": NotRequired[bool],
        "Preload": NotRequired[bool],
    },
)
ResponseHeadersPolicyXSSProtectionTypeDef = TypedDict(
    "ResponseHeadersPolicyXSSProtectionTypeDef",
    {
        "Override": bool,
        "Protection": bool,
        "ModeBlock": NotRequired[bool],
        "ReportUri": NotRequired[str],
    },
)
S3OriginTypeDef = TypedDict(
    "S3OriginTypeDef",
    {
        "DomainName": str,
        "OriginAccessIdentity": str,
    },
)
StreamingLoggingConfigTypeDef = TypedDict(
    "StreamingLoggingConfigTypeDef",
    {
        "Enabled": bool,
        "Bucket": str,
        "Prefix": str,
    },
)
TagKeysTypeDef = TypedDict(
    "TagKeysTypeDef",
    {
        "Items": NotRequired[Sequence[str]],
    },
)
TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": NotRequired[str],
    },
)
UpdateDistributionWithStagingConfigRequestRequestTypeDef = TypedDict(
    "UpdateDistributionWithStagingConfigRequestRequestTypeDef",
    {
        "Id": str,
        "StagingDistributionId": NotRequired[str],
        "IfMatch": NotRequired[str],
    },
)
UpdateKeyValueStoreRequestRequestTypeDef = TypedDict(
    "UpdateKeyValueStoreRequestRequestTypeDef",
    {
        "Name": str,
        "Comment": str,
        "IfMatch": str,
    },
)
AllowedMethodsOutputTypeDef = TypedDict(
    "AllowedMethodsOutputTypeDef",
    {
        "Quantity": int,
        "Items": List[MethodType],
        "CachedMethods": NotRequired[CachedMethodsOutputTypeDef],
    },
)
AllowedMethodsTypeDef = TypedDict(
    "AllowedMethodsTypeDef",
    {
        "Quantity": int,
        "Items": Sequence[MethodType],
        "CachedMethods": NotRequired[CachedMethodsTypeDef],
    },
)
TestFunctionRequestRequestTypeDef = TypedDict(
    "TestFunctionRequestRequestTypeDef",
    {
        "Name": str,
        "IfMatch": str,
        "EventObject": BlobTypeDef,
        "Stage": NotRequired[FunctionStageType],
    },
)
CachePolicyCookiesConfigOutputTypeDef = TypedDict(
    "CachePolicyCookiesConfigOutputTypeDef",
    {
        "CookieBehavior": CachePolicyCookieBehaviorType,
        "Cookies": NotRequired[CookieNamesOutputTypeDef],
    },
)
CookiePreferenceOutputTypeDef = TypedDict(
    "CookiePreferenceOutputTypeDef",
    {
        "Forward": ItemSelectionType,
        "WhitelistedNames": NotRequired[CookieNamesOutputTypeDef],
    },
)
OriginRequestPolicyCookiesConfigOutputTypeDef = TypedDict(
    "OriginRequestPolicyCookiesConfigOutputTypeDef",
    {
        "CookieBehavior": OriginRequestPolicyCookieBehaviorType,
        "Cookies": NotRequired[CookieNamesOutputTypeDef],
    },
)
CachePolicyCookiesConfigTypeDef = TypedDict(
    "CachePolicyCookiesConfigTypeDef",
    {
        "CookieBehavior": CachePolicyCookieBehaviorType,
        "Cookies": NotRequired[CookieNamesTypeDef],
    },
)
CookiePreferenceTypeDef = TypedDict(
    "CookiePreferenceTypeDef",
    {
        "Forward": ItemSelectionType,
        "WhitelistedNames": NotRequired[CookieNamesTypeDef],
    },
)
OriginRequestPolicyCookiesConfigTypeDef = TypedDict(
    "OriginRequestPolicyCookiesConfigTypeDef",
    {
        "CookieBehavior": OriginRequestPolicyCookieBehaviorType,
        "Cookies": NotRequired[CookieNamesTypeDef],
    },
)
CachePolicyHeadersConfigOutputTypeDef = TypedDict(
    "CachePolicyHeadersConfigOutputTypeDef",
    {
        "HeaderBehavior": CachePolicyHeaderBehaviorType,
        "Headers": NotRequired[HeadersOutputTypeDef],
    },
)
OriginRequestPolicyHeadersConfigOutputTypeDef = TypedDict(
    "OriginRequestPolicyHeadersConfigOutputTypeDef",
    {
        "HeaderBehavior": OriginRequestPolicyHeaderBehaviorType,
        "Headers": NotRequired[HeadersOutputTypeDef],
    },
)
CachePolicyHeadersConfigTypeDef = TypedDict(
    "CachePolicyHeadersConfigTypeDef",
    {
        "HeaderBehavior": CachePolicyHeaderBehaviorType,
        "Headers": NotRequired[HeadersTypeDef],
    },
)
OriginRequestPolicyHeadersConfigTypeDef = TypedDict(
    "OriginRequestPolicyHeadersConfigTypeDef",
    {
        "HeaderBehavior": OriginRequestPolicyHeaderBehaviorType,
        "Headers": NotRequired[HeadersTypeDef],
    },
)
CachePolicyQueryStringsConfigOutputTypeDef = TypedDict(
    "CachePolicyQueryStringsConfigOutputTypeDef",
    {
        "QueryStringBehavior": CachePolicyQueryStringBehaviorType,
        "QueryStrings": NotRequired[QueryStringNamesOutputTypeDef],
    },
)
OriginRequestPolicyQueryStringsConfigOutputTypeDef = TypedDict(
    "OriginRequestPolicyQueryStringsConfigOutputTypeDef",
    {
        "QueryStringBehavior": OriginRequestPolicyQueryStringBehaviorType,
        "QueryStrings": NotRequired[QueryStringNamesOutputTypeDef],
    },
)
CachePolicyQueryStringsConfigTypeDef = TypedDict(
    "CachePolicyQueryStringsConfigTypeDef",
    {
        "QueryStringBehavior": CachePolicyQueryStringBehaviorType,
        "QueryStrings": NotRequired[QueryStringNamesTypeDef],
    },
)
OriginRequestPolicyQueryStringsConfigTypeDef = TypedDict(
    "OriginRequestPolicyQueryStringsConfigTypeDef",
    {
        "QueryStringBehavior": OriginRequestPolicyQueryStringBehaviorType,
        "QueryStrings": NotRequired[QueryStringNamesTypeDef],
    },
)
CloudFrontOriginAccessIdentityTypeDef = TypedDict(
    "CloudFrontOriginAccessIdentityTypeDef",
    {
        "Id": str,
        "S3CanonicalUserId": str,
        "CloudFrontOriginAccessIdentityConfig": NotRequired[
            CloudFrontOriginAccessIdentityConfigTypeDef
        ],
    },
)
CreateCloudFrontOriginAccessIdentityRequestRequestTypeDef = TypedDict(
    "CreateCloudFrontOriginAccessIdentityRequestRequestTypeDef",
    {
        "CloudFrontOriginAccessIdentityConfig": CloudFrontOriginAccessIdentityConfigTypeDef,
    },
)
UpdateCloudFrontOriginAccessIdentityRequestRequestTypeDef = TypedDict(
    "UpdateCloudFrontOriginAccessIdentityRequestRequestTypeDef",
    {
        "CloudFrontOriginAccessIdentityConfig": CloudFrontOriginAccessIdentityConfigTypeDef,
        "Id": str,
        "IfMatch": NotRequired[str],
    },
)
CloudFrontOriginAccessIdentityListTypeDef = TypedDict(
    "CloudFrontOriginAccessIdentityListTypeDef",
    {
        "Marker": str,
        "MaxItems": int,
        "IsTruncated": bool,
        "Quantity": int,
        "NextMarker": NotRequired[str],
        "Items": NotRequired[List[CloudFrontOriginAccessIdentitySummaryTypeDef]],
    },
)
ConflictingAliasesListTypeDef = TypedDict(
    "ConflictingAliasesListTypeDef",
    {
        "NextMarker": NotRequired[str],
        "MaxItems": NotRequired[int],
        "Quantity": NotRequired[int],
        "Items": NotRequired[List[ConflictingAliasTypeDef]],
    },
)
ContentTypeProfilesOutputTypeDef = TypedDict(
    "ContentTypeProfilesOutputTypeDef",
    {
        "Quantity": int,
        "Items": NotRequired[List[ContentTypeProfileTypeDef]],
    },
)
ContentTypeProfilesTypeDef = TypedDict(
    "ContentTypeProfilesTypeDef",
    {
        "Quantity": int,
        "Items": NotRequired[Sequence[ContentTypeProfileTypeDef]],
    },
)
ContinuousDeploymentSingleWeightConfigTypeDef = TypedDict(
    "ContinuousDeploymentSingleWeightConfigTypeDef",
    {
        "Weight": float,
        "SessionStickinessConfig": NotRequired[SessionStickinessConfigTypeDef],
    },
)
EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetCloudFrontOriginAccessIdentityConfigResultTypeDef = TypedDict(
    "GetCloudFrontOriginAccessIdentityConfigResultTypeDef",
    {
        "CloudFrontOriginAccessIdentityConfig": CloudFrontOriginAccessIdentityConfigTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetFunctionResultTypeDef = TypedDict(
    "GetFunctionResultTypeDef",
    {
        "FunctionCode": StreamingBody,
        "ETag": str,
        "ContentType": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateKeyGroupRequestRequestTypeDef = TypedDict(
    "CreateKeyGroupRequestRequestTypeDef",
    {
        "KeyGroupConfig": KeyGroupConfigTypeDef,
    },
)
UpdateKeyGroupRequestRequestTypeDef = TypedDict(
    "UpdateKeyGroupRequestRequestTypeDef",
    {
        "KeyGroupConfig": KeyGroupConfigTypeDef,
        "Id": str,
        "IfMatch": NotRequired[str],
    },
)
CreateKeyValueStoreRequestRequestTypeDef = TypedDict(
    "CreateKeyValueStoreRequestRequestTypeDef",
    {
        "Name": str,
        "Comment": NotRequired[str],
        "ImportSource": NotRequired[ImportSourceTypeDef],
    },
)
CreateKeyValueStoreResultTypeDef = TypedDict(
    "CreateKeyValueStoreResultTypeDef",
    {
        "KeyValueStore": KeyValueStoreTypeDef,
        "ETag": str,
        "Location": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DescribeKeyValueStoreResultTypeDef = TypedDict(
    "DescribeKeyValueStoreResultTypeDef",
    {
        "KeyValueStore": KeyValueStoreTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
KeyValueStoreListTypeDef = TypedDict(
    "KeyValueStoreListTypeDef",
    {
        "MaxItems": int,
        "Quantity": int,
        "NextMarker": NotRequired[str],
        "Items": NotRequired[List[KeyValueStoreTypeDef]],
    },
)
UpdateKeyValueStoreResultTypeDef = TypedDict(
    "UpdateKeyValueStoreResultTypeDef",
    {
        "KeyValueStore": KeyValueStoreTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateOriginAccessControlRequestRequestTypeDef = TypedDict(
    "CreateOriginAccessControlRequestRequestTypeDef",
    {
        "OriginAccessControlConfig": OriginAccessControlConfigTypeDef,
    },
)
GetOriginAccessControlConfigResultTypeDef = TypedDict(
    "GetOriginAccessControlConfigResultTypeDef",
    {
        "OriginAccessControlConfig": OriginAccessControlConfigTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
OriginAccessControlTypeDef = TypedDict(
    "OriginAccessControlTypeDef",
    {
        "Id": str,
        "OriginAccessControlConfig": NotRequired[OriginAccessControlConfigTypeDef],
    },
)
UpdateOriginAccessControlRequestRequestTypeDef = TypedDict(
    "UpdateOriginAccessControlRequestRequestTypeDef",
    {
        "OriginAccessControlConfig": OriginAccessControlConfigTypeDef,
        "Id": str,
        "IfMatch": NotRequired[str],
    },
)
CreatePublicKeyRequestRequestTypeDef = TypedDict(
    "CreatePublicKeyRequestRequestTypeDef",
    {
        "PublicKeyConfig": PublicKeyConfigTypeDef,
    },
)
GetPublicKeyConfigResultTypeDef = TypedDict(
    "GetPublicKeyConfigResultTypeDef",
    {
        "PublicKeyConfig": PublicKeyConfigTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
PublicKeyTypeDef = TypedDict(
    "PublicKeyTypeDef",
    {
        "Id": str,
        "CreatedTime": datetime,
        "PublicKeyConfig": PublicKeyConfigTypeDef,
    },
)
UpdatePublicKeyRequestRequestTypeDef = TypedDict(
    "UpdatePublicKeyRequestRequestTypeDef",
    {
        "PublicKeyConfig": PublicKeyConfigTypeDef,
        "Id": str,
        "IfMatch": NotRequired[str],
    },
)
CustomErrorResponsesOutputTypeDef = TypedDict(
    "CustomErrorResponsesOutputTypeDef",
    {
        "Quantity": int,
        "Items": NotRequired[List[CustomErrorResponseTypeDef]],
    },
)
CustomErrorResponsesTypeDef = TypedDict(
    "CustomErrorResponsesTypeDef",
    {
        "Quantity": int,
        "Items": NotRequired[Sequence[CustomErrorResponseTypeDef]],
    },
)
CustomHeadersOutputTypeDef = TypedDict(
    "CustomHeadersOutputTypeDef",
    {
        "Quantity": int,
        "Items": NotRequired[List[OriginCustomHeaderTypeDef]],
    },
)
CustomHeadersTypeDef = TypedDict(
    "CustomHeadersTypeDef",
    {
        "Quantity": int,
        "Items": NotRequired[Sequence[OriginCustomHeaderTypeDef]],
    },
)
CustomOriginConfigOutputTypeDef = TypedDict(
    "CustomOriginConfigOutputTypeDef",
    {
        "HTTPPort": int,
        "HTTPSPort": int,
        "OriginProtocolPolicy": OriginProtocolPolicyType,
        "OriginSslProtocols": NotRequired[OriginSslProtocolsOutputTypeDef],
        "OriginReadTimeout": NotRequired[int],
        "OriginKeepaliveTimeout": NotRequired[int],
    },
)
CustomOriginConfigTypeDef = TypedDict(
    "CustomOriginConfigTypeDef",
    {
        "HTTPPort": int,
        "HTTPSPort": int,
        "OriginProtocolPolicy": OriginProtocolPolicyType,
        "OriginSslProtocols": NotRequired[OriginSslProtocolsTypeDef],
        "OriginReadTimeout": NotRequired[int],
        "OriginKeepaliveTimeout": NotRequired[int],
    },
)
ListDistributionsByCachePolicyIdResultTypeDef = TypedDict(
    "ListDistributionsByCachePolicyIdResultTypeDef",
    {
        "DistributionIdList": DistributionIdListTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListDistributionsByKeyGroupResultTypeDef = TypedDict(
    "ListDistributionsByKeyGroupResultTypeDef",
    {
        "DistributionIdList": DistributionIdListTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListDistributionsByOriginRequestPolicyIdResultTypeDef = TypedDict(
    "ListDistributionsByOriginRequestPolicyIdResultTypeDef",
    {
        "DistributionIdList": DistributionIdListTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListDistributionsByResponseHeadersPolicyIdResultTypeDef = TypedDict(
    "ListDistributionsByResponseHeadersPolicyIdResultTypeDef",
    {
        "DistributionIdList": DistributionIdListTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
EncryptionEntityOutputTypeDef = TypedDict(
    "EncryptionEntityOutputTypeDef",
    {
        "PublicKeyId": str,
        "ProviderId": str,
        "FieldPatterns": FieldPatternsOutputTypeDef,
    },
)
EncryptionEntityTypeDef = TypedDict(
    "EncryptionEntityTypeDef",
    {
        "PublicKeyId": str,
        "ProviderId": str,
        "FieldPatterns": FieldPatternsTypeDef,
    },
)
EndPointTypeDef = TypedDict(
    "EndPointTypeDef",
    {
        "StreamType": str,
        "KinesisStreamConfig": NotRequired[KinesisStreamConfigTypeDef],
    },
)
FunctionAssociationsOutputTypeDef = TypedDict(
    "FunctionAssociationsOutputTypeDef",
    {
        "Quantity": int,
        "Items": NotRequired[List[FunctionAssociationTypeDef]],
    },
)
FunctionAssociationsTypeDef = TypedDict(
    "FunctionAssociationsTypeDef",
    {
        "Quantity": int,
        "Items": NotRequired[Sequence[FunctionAssociationTypeDef]],
    },
)
RestrictionsOutputTypeDef = TypedDict(
    "RestrictionsOutputTypeDef",
    {
        "GeoRestriction": GeoRestrictionOutputTypeDef,
    },
)
RestrictionsTypeDef = TypedDict(
    "RestrictionsTypeDef",
    {
        "GeoRestriction": GeoRestrictionTypeDef,
    },
)
GetDistributionRequestDistributionDeployedWaitTypeDef = TypedDict(
    "GetDistributionRequestDistributionDeployedWaitTypeDef",
    {
        "Id": str,
        "WaiterConfig": NotRequired[WaiterConfigTypeDef],
    },
)
GetInvalidationRequestInvalidationCompletedWaitTypeDef = TypedDict(
    "GetInvalidationRequestInvalidationCompletedWaitTypeDef",
    {
        "DistributionId": str,
        "Id": str,
        "WaiterConfig": NotRequired[WaiterConfigTypeDef],
    },
)
GetStreamingDistributionRequestStreamingDistributionDeployedWaitTypeDef = TypedDict(
    "GetStreamingDistributionRequestStreamingDistributionDeployedWaitTypeDef",
    {
        "Id": str,
        "WaiterConfig": NotRequired[WaiterConfigTypeDef],
    },
)
GetKeyGroupConfigResultTypeDef = TypedDict(
    "GetKeyGroupConfigResultTypeDef",
    {
        "KeyGroupConfig": KeyGroupConfigOutputTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
KeyGroupTypeDef = TypedDict(
    "KeyGroupTypeDef",
    {
        "Id": str,
        "LastModifiedTime": datetime,
        "KeyGroupConfig": KeyGroupConfigOutputTypeDef,
    },
)
InvalidationBatchOutputTypeDef = TypedDict(
    "InvalidationBatchOutputTypeDef",
    {
        "Paths": PathsOutputTypeDef,
        "CallerReference": str,
    },
)
InvalidationBatchTypeDef = TypedDict(
    "InvalidationBatchTypeDef",
    {
        "Paths": PathsTypeDef,
        "CallerReference": str,
    },
)
InvalidationListTypeDef = TypedDict(
    "InvalidationListTypeDef",
    {
        "Marker": str,
        "MaxItems": int,
        "IsTruncated": bool,
        "Quantity": int,
        "NextMarker": NotRequired[str],
        "Items": NotRequired[List[InvalidationSummaryTypeDef]],
    },
)
KGKeyPairIdsTypeDef = TypedDict(
    "KGKeyPairIdsTypeDef",
    {
        "KeyGroupId": NotRequired[str],
        "KeyPairIds": NotRequired[KeyPairIdsTypeDef],
    },
)
SignerTypeDef = TypedDict(
    "SignerTypeDef",
    {
        "AwsAccountNumber": NotRequired[str],
        "KeyPairIds": NotRequired[KeyPairIdsTypeDef],
    },
)
KeyValueStoreAssociationsOutputTypeDef = TypedDict(
    "KeyValueStoreAssociationsOutputTypeDef",
    {
        "Quantity": int,
        "Items": NotRequired[List[KeyValueStoreAssociationTypeDef]],
    },
)
KeyValueStoreAssociationsTypeDef = TypedDict(
    "KeyValueStoreAssociationsTypeDef",
    {
        "Quantity": int,
        "Items": NotRequired[Sequence[KeyValueStoreAssociationTypeDef]],
    },
)
LambdaFunctionAssociationsOutputTypeDef = TypedDict(
    "LambdaFunctionAssociationsOutputTypeDef",
    {
        "Quantity": int,
        "Items": NotRequired[List[LambdaFunctionAssociationTypeDef]],
    },
)
LambdaFunctionAssociationsTypeDef = TypedDict(
    "LambdaFunctionAssociationsTypeDef",
    {
        "Quantity": int,
        "Items": NotRequired[Sequence[LambdaFunctionAssociationTypeDef]],
    },
)
ListCloudFrontOriginAccessIdentitiesRequestListCloudFrontOriginAccessIdentitiesPaginateTypeDef = TypedDict(
    "ListCloudFrontOriginAccessIdentitiesRequestListCloudFrontOriginAccessIdentitiesPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListDistributionsRequestListDistributionsPaginateTypeDef = TypedDict(
    "ListDistributionsRequestListDistributionsPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListInvalidationsRequestListInvalidationsPaginateTypeDef = TypedDict(
    "ListInvalidationsRequestListInvalidationsPaginateTypeDef",
    {
        "DistributionId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListKeyValueStoresRequestListKeyValueStoresPaginateTypeDef = TypedDict(
    "ListKeyValueStoresRequestListKeyValueStoresPaginateTypeDef",
    {
        "Status": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListStreamingDistributionsRequestListStreamingDistributionsPaginateTypeDef = TypedDict(
    "ListStreamingDistributionsRequestListStreamingDistributionsPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
MonitoringSubscriptionTypeDef = TypedDict(
    "MonitoringSubscriptionTypeDef",
    {
        "RealtimeMetricsSubscriptionConfig": NotRequired[RealtimeMetricsSubscriptionConfigTypeDef],
    },
)
OriginAccessControlListTypeDef = TypedDict(
    "OriginAccessControlListTypeDef",
    {
        "Marker": str,
        "MaxItems": int,
        "IsTruncated": bool,
        "Quantity": int,
        "NextMarker": NotRequired[str],
        "Items": NotRequired[List[OriginAccessControlSummaryTypeDef]],
    },
)
OriginGroupFailoverCriteriaOutputTypeDef = TypedDict(
    "OriginGroupFailoverCriteriaOutputTypeDef",
    {
        "StatusCodes": StatusCodesOutputTypeDef,
    },
)
OriginGroupFailoverCriteriaTypeDef = TypedDict(
    "OriginGroupFailoverCriteriaTypeDef",
    {
        "StatusCodes": StatusCodesTypeDef,
    },
)
OriginGroupMembersOutputTypeDef = TypedDict(
    "OriginGroupMembersOutputTypeDef",
    {
        "Quantity": int,
        "Items": List[OriginGroupMemberTypeDef],
    },
)
OriginGroupMembersTypeDef = TypedDict(
    "OriginGroupMembersTypeDef",
    {
        "Quantity": int,
        "Items": Sequence[OriginGroupMemberTypeDef],
    },
)
PublicKeyListTypeDef = TypedDict(
    "PublicKeyListTypeDef",
    {
        "MaxItems": int,
        "Quantity": int,
        "NextMarker": NotRequired[str],
        "Items": NotRequired[List[PublicKeySummaryTypeDef]],
    },
)
QueryArgProfilesOutputTypeDef = TypedDict(
    "QueryArgProfilesOutputTypeDef",
    {
        "Quantity": int,
        "Items": NotRequired[List[QueryArgProfileTypeDef]],
    },
)
QueryArgProfilesTypeDef = TypedDict(
    "QueryArgProfilesTypeDef",
    {
        "Quantity": int,
        "Items": NotRequired[Sequence[QueryArgProfileTypeDef]],
    },
)
ResponseHeadersPolicyCorsConfigOutputTypeDef = TypedDict(
    "ResponseHeadersPolicyCorsConfigOutputTypeDef",
    {
        "AccessControlAllowOrigins": ResponseHeadersPolicyAccessControlAllowOriginsOutputTypeDef,
        "AccessControlAllowHeaders": ResponseHeadersPolicyAccessControlAllowHeadersOutputTypeDef,
        "AccessControlAllowMethods": ResponseHeadersPolicyAccessControlAllowMethodsOutputTypeDef,
        "AccessControlAllowCredentials": bool,
        "OriginOverride": bool,
        "AccessControlExposeHeaders": NotRequired[
            ResponseHeadersPolicyAccessControlExposeHeadersOutputTypeDef
        ],
        "AccessControlMaxAgeSec": NotRequired[int],
    },
)
ResponseHeadersPolicyCorsConfigTypeDef = TypedDict(
    "ResponseHeadersPolicyCorsConfigTypeDef",
    {
        "AccessControlAllowOrigins": ResponseHeadersPolicyAccessControlAllowOriginsTypeDef,
        "AccessControlAllowHeaders": ResponseHeadersPolicyAccessControlAllowHeadersTypeDef,
        "AccessControlAllowMethods": ResponseHeadersPolicyAccessControlAllowMethodsTypeDef,
        "AccessControlAllowCredentials": bool,
        "OriginOverride": bool,
        "AccessControlExposeHeaders": NotRequired[
            ResponseHeadersPolicyAccessControlExposeHeadersTypeDef
        ],
        "AccessControlMaxAgeSec": NotRequired[int],
    },
)
ResponseHeadersPolicyCustomHeadersConfigOutputTypeDef = TypedDict(
    "ResponseHeadersPolicyCustomHeadersConfigOutputTypeDef",
    {
        "Quantity": int,
        "Items": NotRequired[List[ResponseHeadersPolicyCustomHeaderTypeDef]],
    },
)
ResponseHeadersPolicyCustomHeadersConfigTypeDef = TypedDict(
    "ResponseHeadersPolicyCustomHeadersConfigTypeDef",
    {
        "Quantity": int,
        "Items": NotRequired[Sequence[ResponseHeadersPolicyCustomHeaderTypeDef]],
    },
)
ResponseHeadersPolicyRemoveHeadersConfigOutputTypeDef = TypedDict(
    "ResponseHeadersPolicyRemoveHeadersConfigOutputTypeDef",
    {
        "Quantity": int,
        "Items": NotRequired[List[ResponseHeadersPolicyRemoveHeaderTypeDef]],
    },
)
ResponseHeadersPolicyRemoveHeadersConfigTypeDef = TypedDict(
    "ResponseHeadersPolicyRemoveHeadersConfigTypeDef",
    {
        "Quantity": int,
        "Items": NotRequired[Sequence[ResponseHeadersPolicyRemoveHeaderTypeDef]],
    },
)
ResponseHeadersPolicySecurityHeadersConfigTypeDef = TypedDict(
    "ResponseHeadersPolicySecurityHeadersConfigTypeDef",
    {
        "XSSProtection": NotRequired[ResponseHeadersPolicyXSSProtectionTypeDef],
        "FrameOptions": NotRequired[ResponseHeadersPolicyFrameOptionsTypeDef],
        "ReferrerPolicy": NotRequired[ResponseHeadersPolicyReferrerPolicyTypeDef],
        "ContentSecurityPolicy": NotRequired[ResponseHeadersPolicyContentSecurityPolicyTypeDef],
        "ContentTypeOptions": NotRequired[ResponseHeadersPolicyContentTypeOptionsTypeDef],
        "StrictTransportSecurity": NotRequired[ResponseHeadersPolicyStrictTransportSecurityTypeDef],
    },
)
StreamingDistributionSummaryTypeDef = TypedDict(
    "StreamingDistributionSummaryTypeDef",
    {
        "Id": str,
        "ARN": str,
        "Status": str,
        "LastModifiedTime": datetime,
        "DomainName": str,
        "S3Origin": S3OriginTypeDef,
        "Aliases": AliasesOutputTypeDef,
        "TrustedSigners": TrustedSignersOutputTypeDef,
        "Comment": str,
        "PriceClass": PriceClassType,
        "Enabled": bool,
    },
)
StreamingDistributionConfigOutputTypeDef = TypedDict(
    "StreamingDistributionConfigOutputTypeDef",
    {
        "CallerReference": str,
        "S3Origin": S3OriginTypeDef,
        "Comment": str,
        "TrustedSigners": TrustedSignersOutputTypeDef,
        "Enabled": bool,
        "Aliases": NotRequired[AliasesOutputTypeDef],
        "Logging": NotRequired[StreamingLoggingConfigTypeDef],
        "PriceClass": NotRequired[PriceClassType],
    },
)
StreamingDistributionConfigTypeDef = TypedDict(
    "StreamingDistributionConfigTypeDef",
    {
        "CallerReference": str,
        "S3Origin": S3OriginTypeDef,
        "Comment": str,
        "TrustedSigners": TrustedSignersTypeDef,
        "Enabled": bool,
        "Aliases": NotRequired[AliasesTypeDef],
        "Logging": NotRequired[StreamingLoggingConfigTypeDef],
        "PriceClass": NotRequired[PriceClassType],
    },
)
UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "Resource": str,
        "TagKeys": TagKeysTypeDef,
    },
)
TagsOutputTypeDef = TypedDict(
    "TagsOutputTypeDef",
    {
        "Items": NotRequired[List[TagTypeDef]],
    },
)
TagsTypeDef = TypedDict(
    "TagsTypeDef",
    {
        "Items": NotRequired[Sequence[TagTypeDef]],
    },
)
ForwardedValuesOutputTypeDef = TypedDict(
    "ForwardedValuesOutputTypeDef",
    {
        "QueryString": bool,
        "Cookies": CookiePreferenceOutputTypeDef,
        "Headers": NotRequired[HeadersOutputTypeDef],
        "QueryStringCacheKeys": NotRequired[QueryStringCacheKeysOutputTypeDef],
    },
)
ForwardedValuesTypeDef = TypedDict(
    "ForwardedValuesTypeDef",
    {
        "QueryString": bool,
        "Cookies": CookiePreferenceTypeDef,
        "Headers": NotRequired[HeadersTypeDef],
        "QueryStringCacheKeys": NotRequired[QueryStringCacheKeysTypeDef],
    },
)
ParametersInCacheKeyAndForwardedToOriginOutputTypeDef = TypedDict(
    "ParametersInCacheKeyAndForwardedToOriginOutputTypeDef",
    {
        "EnableAcceptEncodingGzip": bool,
        "HeadersConfig": CachePolicyHeadersConfigOutputTypeDef,
        "CookiesConfig": CachePolicyCookiesConfigOutputTypeDef,
        "QueryStringsConfig": CachePolicyQueryStringsConfigOutputTypeDef,
        "EnableAcceptEncodingBrotli": NotRequired[bool],
    },
)
OriginRequestPolicyConfigOutputTypeDef = TypedDict(
    "OriginRequestPolicyConfigOutputTypeDef",
    {
        "Name": str,
        "HeadersConfig": OriginRequestPolicyHeadersConfigOutputTypeDef,
        "CookiesConfig": OriginRequestPolicyCookiesConfigOutputTypeDef,
        "QueryStringsConfig": OriginRequestPolicyQueryStringsConfigOutputTypeDef,
        "Comment": NotRequired[str],
    },
)
ParametersInCacheKeyAndForwardedToOriginTypeDef = TypedDict(
    "ParametersInCacheKeyAndForwardedToOriginTypeDef",
    {
        "EnableAcceptEncodingGzip": bool,
        "HeadersConfig": CachePolicyHeadersConfigTypeDef,
        "CookiesConfig": CachePolicyCookiesConfigTypeDef,
        "QueryStringsConfig": CachePolicyQueryStringsConfigTypeDef,
        "EnableAcceptEncodingBrotli": NotRequired[bool],
    },
)
OriginRequestPolicyConfigTypeDef = TypedDict(
    "OriginRequestPolicyConfigTypeDef",
    {
        "Name": str,
        "HeadersConfig": OriginRequestPolicyHeadersConfigTypeDef,
        "CookiesConfig": OriginRequestPolicyCookiesConfigTypeDef,
        "QueryStringsConfig": OriginRequestPolicyQueryStringsConfigTypeDef,
        "Comment": NotRequired[str],
    },
)
CreateCloudFrontOriginAccessIdentityResultTypeDef = TypedDict(
    "CreateCloudFrontOriginAccessIdentityResultTypeDef",
    {
        "CloudFrontOriginAccessIdentity": CloudFrontOriginAccessIdentityTypeDef,
        "Location": str,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetCloudFrontOriginAccessIdentityResultTypeDef = TypedDict(
    "GetCloudFrontOriginAccessIdentityResultTypeDef",
    {
        "CloudFrontOriginAccessIdentity": CloudFrontOriginAccessIdentityTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateCloudFrontOriginAccessIdentityResultTypeDef = TypedDict(
    "UpdateCloudFrontOriginAccessIdentityResultTypeDef",
    {
        "CloudFrontOriginAccessIdentity": CloudFrontOriginAccessIdentityTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListCloudFrontOriginAccessIdentitiesResultTypeDef = TypedDict(
    "ListCloudFrontOriginAccessIdentitiesResultTypeDef",
    {
        "CloudFrontOriginAccessIdentityList": CloudFrontOriginAccessIdentityListTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListConflictingAliasesResultTypeDef = TypedDict(
    "ListConflictingAliasesResultTypeDef",
    {
        "ConflictingAliasesList": ConflictingAliasesListTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ContentTypeProfileConfigOutputTypeDef = TypedDict(
    "ContentTypeProfileConfigOutputTypeDef",
    {
        "ForwardWhenContentTypeIsUnknown": bool,
        "ContentTypeProfiles": NotRequired[ContentTypeProfilesOutputTypeDef],
    },
)
ContentTypeProfileConfigTypeDef = TypedDict(
    "ContentTypeProfileConfigTypeDef",
    {
        "ForwardWhenContentTypeIsUnknown": bool,
        "ContentTypeProfiles": NotRequired[ContentTypeProfilesTypeDef],
    },
)
TrafficConfigTypeDef = TypedDict(
    "TrafficConfigTypeDef",
    {
        "Type": ContinuousDeploymentPolicyTypeType,
        "SingleWeightConfig": NotRequired[ContinuousDeploymentSingleWeightConfigTypeDef],
        "SingleHeaderConfig": NotRequired[ContinuousDeploymentSingleHeaderConfigTypeDef],
    },
)
ListKeyValueStoresResultTypeDef = TypedDict(
    "ListKeyValueStoresResultTypeDef",
    {
        "KeyValueStoreList": KeyValueStoreListTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateOriginAccessControlResultTypeDef = TypedDict(
    "CreateOriginAccessControlResultTypeDef",
    {
        "OriginAccessControl": OriginAccessControlTypeDef,
        "Location": str,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetOriginAccessControlResultTypeDef = TypedDict(
    "GetOriginAccessControlResultTypeDef",
    {
        "OriginAccessControl": OriginAccessControlTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateOriginAccessControlResultTypeDef = TypedDict(
    "UpdateOriginAccessControlResultTypeDef",
    {
        "OriginAccessControl": OriginAccessControlTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreatePublicKeyResultTypeDef = TypedDict(
    "CreatePublicKeyResultTypeDef",
    {
        "PublicKey": PublicKeyTypeDef,
        "Location": str,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetPublicKeyResultTypeDef = TypedDict(
    "GetPublicKeyResultTypeDef",
    {
        "PublicKey": PublicKeyTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdatePublicKeyResultTypeDef = TypedDict(
    "UpdatePublicKeyResultTypeDef",
    {
        "PublicKey": PublicKeyTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
OriginOutputTypeDef = TypedDict(
    "OriginOutputTypeDef",
    {
        "Id": str,
        "DomainName": str,
        "OriginPath": NotRequired[str],
        "CustomHeaders": NotRequired[CustomHeadersOutputTypeDef],
        "S3OriginConfig": NotRequired[S3OriginConfigTypeDef],
        "CustomOriginConfig": NotRequired[CustomOriginConfigOutputTypeDef],
        "ConnectionAttempts": NotRequired[int],
        "ConnectionTimeout": NotRequired[int],
        "OriginShield": NotRequired[OriginShieldTypeDef],
        "OriginAccessControlId": NotRequired[str],
    },
)
OriginTypeDef = TypedDict(
    "OriginTypeDef",
    {
        "Id": str,
        "DomainName": str,
        "OriginPath": NotRequired[str],
        "CustomHeaders": NotRequired[CustomHeadersTypeDef],
        "S3OriginConfig": NotRequired[S3OriginConfigTypeDef],
        "CustomOriginConfig": NotRequired[CustomOriginConfigTypeDef],
        "ConnectionAttempts": NotRequired[int],
        "ConnectionTimeout": NotRequired[int],
        "OriginShield": NotRequired[OriginShieldTypeDef],
        "OriginAccessControlId": NotRequired[str],
    },
)
EncryptionEntitiesOutputTypeDef = TypedDict(
    "EncryptionEntitiesOutputTypeDef",
    {
        "Quantity": int,
        "Items": NotRequired[List[EncryptionEntityOutputTypeDef]],
    },
)
EncryptionEntitiesTypeDef = TypedDict(
    "EncryptionEntitiesTypeDef",
    {
        "Quantity": int,
        "Items": NotRequired[Sequence[EncryptionEntityTypeDef]],
    },
)
CreateRealtimeLogConfigRequestRequestTypeDef = TypedDict(
    "CreateRealtimeLogConfigRequestRequestTypeDef",
    {
        "EndPoints": Sequence[EndPointTypeDef],
        "Fields": Sequence[str],
        "Name": str,
        "SamplingRate": int,
    },
)
RealtimeLogConfigTypeDef = TypedDict(
    "RealtimeLogConfigTypeDef",
    {
        "ARN": str,
        "Name": str,
        "SamplingRate": int,
        "EndPoints": List[EndPointTypeDef],
        "Fields": List[str],
    },
)
UpdateRealtimeLogConfigRequestRequestTypeDef = TypedDict(
    "UpdateRealtimeLogConfigRequestRequestTypeDef",
    {
        "EndPoints": NotRequired[Sequence[EndPointTypeDef]],
        "Fields": NotRequired[Sequence[str]],
        "Name": NotRequired[str],
        "ARN": NotRequired[str],
        "SamplingRate": NotRequired[int],
    },
)
CreateKeyGroupResultTypeDef = TypedDict(
    "CreateKeyGroupResultTypeDef",
    {
        "KeyGroup": KeyGroupTypeDef,
        "Location": str,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetKeyGroupResultTypeDef = TypedDict(
    "GetKeyGroupResultTypeDef",
    {
        "KeyGroup": KeyGroupTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
KeyGroupSummaryTypeDef = TypedDict(
    "KeyGroupSummaryTypeDef",
    {
        "KeyGroup": KeyGroupTypeDef,
    },
)
UpdateKeyGroupResultTypeDef = TypedDict(
    "UpdateKeyGroupResultTypeDef",
    {
        "KeyGroup": KeyGroupTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
InvalidationTypeDef = TypedDict(
    "InvalidationTypeDef",
    {
        "Id": str,
        "Status": str,
        "CreateTime": datetime,
        "InvalidationBatch": InvalidationBatchOutputTypeDef,
    },
)
CreateInvalidationRequestRequestTypeDef = TypedDict(
    "CreateInvalidationRequestRequestTypeDef",
    {
        "DistributionId": str,
        "InvalidationBatch": InvalidationBatchTypeDef,
    },
)
ListInvalidationsResultTypeDef = TypedDict(
    "ListInvalidationsResultTypeDef",
    {
        "InvalidationList": InvalidationListTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ActiveTrustedKeyGroupsTypeDef = TypedDict(
    "ActiveTrustedKeyGroupsTypeDef",
    {
        "Enabled": bool,
        "Quantity": int,
        "Items": NotRequired[List[KGKeyPairIdsTypeDef]],
    },
)
ActiveTrustedSignersTypeDef = TypedDict(
    "ActiveTrustedSignersTypeDef",
    {
        "Enabled": bool,
        "Quantity": int,
        "Items": NotRequired[List[SignerTypeDef]],
    },
)
FunctionConfigOutputTypeDef = TypedDict(
    "FunctionConfigOutputTypeDef",
    {
        "Comment": str,
        "Runtime": FunctionRuntimeType,
        "KeyValueStoreAssociations": NotRequired[KeyValueStoreAssociationsOutputTypeDef],
    },
)
FunctionConfigTypeDef = TypedDict(
    "FunctionConfigTypeDef",
    {
        "Comment": str,
        "Runtime": FunctionRuntimeType,
        "KeyValueStoreAssociations": NotRequired[KeyValueStoreAssociationsTypeDef],
    },
)
CreateMonitoringSubscriptionRequestRequestTypeDef = TypedDict(
    "CreateMonitoringSubscriptionRequestRequestTypeDef",
    {
        "DistributionId": str,
        "MonitoringSubscription": MonitoringSubscriptionTypeDef,
    },
)
CreateMonitoringSubscriptionResultTypeDef = TypedDict(
    "CreateMonitoringSubscriptionResultTypeDef",
    {
        "MonitoringSubscription": MonitoringSubscriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetMonitoringSubscriptionResultTypeDef = TypedDict(
    "GetMonitoringSubscriptionResultTypeDef",
    {
        "MonitoringSubscription": MonitoringSubscriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListOriginAccessControlsResultTypeDef = TypedDict(
    "ListOriginAccessControlsResultTypeDef",
    {
        "OriginAccessControlList": OriginAccessControlListTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
OriginGroupOutputTypeDef = TypedDict(
    "OriginGroupOutputTypeDef",
    {
        "Id": str,
        "FailoverCriteria": OriginGroupFailoverCriteriaOutputTypeDef,
        "Members": OriginGroupMembersOutputTypeDef,
    },
)
OriginGroupTypeDef = TypedDict(
    "OriginGroupTypeDef",
    {
        "Id": str,
        "FailoverCriteria": OriginGroupFailoverCriteriaTypeDef,
        "Members": OriginGroupMembersTypeDef,
    },
)
ListPublicKeysResultTypeDef = TypedDict(
    "ListPublicKeysResultTypeDef",
    {
        "PublicKeyList": PublicKeyListTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
QueryArgProfileConfigOutputTypeDef = TypedDict(
    "QueryArgProfileConfigOutputTypeDef",
    {
        "ForwardWhenQueryArgProfileIsUnknown": bool,
        "QueryArgProfiles": NotRequired[QueryArgProfilesOutputTypeDef],
    },
)
QueryArgProfileConfigTypeDef = TypedDict(
    "QueryArgProfileConfigTypeDef",
    {
        "ForwardWhenQueryArgProfileIsUnknown": bool,
        "QueryArgProfiles": NotRequired[QueryArgProfilesTypeDef],
    },
)
ResponseHeadersPolicyConfigOutputTypeDef = TypedDict(
    "ResponseHeadersPolicyConfigOutputTypeDef",
    {
        "Name": str,
        "Comment": NotRequired[str],
        "CorsConfig": NotRequired[ResponseHeadersPolicyCorsConfigOutputTypeDef],
        "SecurityHeadersConfig": NotRequired[ResponseHeadersPolicySecurityHeadersConfigTypeDef],
        "ServerTimingHeadersConfig": NotRequired[
            ResponseHeadersPolicyServerTimingHeadersConfigTypeDef
        ],
        "CustomHeadersConfig": NotRequired[ResponseHeadersPolicyCustomHeadersConfigOutputTypeDef],
        "RemoveHeadersConfig": NotRequired[ResponseHeadersPolicyRemoveHeadersConfigOutputTypeDef],
    },
)
ResponseHeadersPolicyConfigTypeDef = TypedDict(
    "ResponseHeadersPolicyConfigTypeDef",
    {
        "Name": str,
        "Comment": NotRequired[str],
        "CorsConfig": NotRequired[ResponseHeadersPolicyCorsConfigTypeDef],
        "SecurityHeadersConfig": NotRequired[ResponseHeadersPolicySecurityHeadersConfigTypeDef],
        "ServerTimingHeadersConfig": NotRequired[
            ResponseHeadersPolicyServerTimingHeadersConfigTypeDef
        ],
        "CustomHeadersConfig": NotRequired[ResponseHeadersPolicyCustomHeadersConfigTypeDef],
        "RemoveHeadersConfig": NotRequired[ResponseHeadersPolicyRemoveHeadersConfigTypeDef],
    },
)
StreamingDistributionListTypeDef = TypedDict(
    "StreamingDistributionListTypeDef",
    {
        "Marker": str,
        "MaxItems": int,
        "IsTruncated": bool,
        "Quantity": int,
        "NextMarker": NotRequired[str],
        "Items": NotRequired[List[StreamingDistributionSummaryTypeDef]],
    },
)
GetStreamingDistributionConfigResultTypeDef = TypedDict(
    "GetStreamingDistributionConfigResultTypeDef",
    {
        "StreamingDistributionConfig": StreamingDistributionConfigOutputTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateStreamingDistributionRequestRequestTypeDef = TypedDict(
    "CreateStreamingDistributionRequestRequestTypeDef",
    {
        "StreamingDistributionConfig": StreamingDistributionConfigTypeDef,
    },
)
UpdateStreamingDistributionRequestRequestTypeDef = TypedDict(
    "UpdateStreamingDistributionRequestRequestTypeDef",
    {
        "StreamingDistributionConfig": StreamingDistributionConfigTypeDef,
        "Id": str,
        "IfMatch": NotRequired[str],
    },
)
ListTagsForResourceResultTypeDef = TypedDict(
    "ListTagsForResourceResultTypeDef",
    {
        "Tags": TagsOutputTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
StreamingDistributionConfigWithTagsTypeDef = TypedDict(
    "StreamingDistributionConfigWithTagsTypeDef",
    {
        "StreamingDistributionConfig": StreamingDistributionConfigTypeDef,
        "Tags": TagsTypeDef,
    },
)
TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "Resource": str,
        "Tags": TagsTypeDef,
    },
)
CacheBehaviorOutputTypeDef = TypedDict(
    "CacheBehaviorOutputTypeDef",
    {
        "PathPattern": str,
        "TargetOriginId": str,
        "ViewerProtocolPolicy": ViewerProtocolPolicyType,
        "TrustedSigners": NotRequired[TrustedSignersOutputTypeDef],
        "TrustedKeyGroups": NotRequired[TrustedKeyGroupsOutputTypeDef],
        "AllowedMethods": NotRequired[AllowedMethodsOutputTypeDef],
        "SmoothStreaming": NotRequired[bool],
        "Compress": NotRequired[bool],
        "LambdaFunctionAssociations": NotRequired[LambdaFunctionAssociationsOutputTypeDef],
        "FunctionAssociations": NotRequired[FunctionAssociationsOutputTypeDef],
        "FieldLevelEncryptionId": NotRequired[str],
        "RealtimeLogConfigArn": NotRequired[str],
        "CachePolicyId": NotRequired[str],
        "OriginRequestPolicyId": NotRequired[str],
        "ResponseHeadersPolicyId": NotRequired[str],
        "ForwardedValues": NotRequired[ForwardedValuesOutputTypeDef],
        "MinTTL": NotRequired[int],
        "DefaultTTL": NotRequired[int],
        "MaxTTL": NotRequired[int],
    },
)
DefaultCacheBehaviorOutputTypeDef = TypedDict(
    "DefaultCacheBehaviorOutputTypeDef",
    {
        "TargetOriginId": str,
        "ViewerProtocolPolicy": ViewerProtocolPolicyType,
        "TrustedSigners": NotRequired[TrustedSignersOutputTypeDef],
        "TrustedKeyGroups": NotRequired[TrustedKeyGroupsOutputTypeDef],
        "AllowedMethods": NotRequired[AllowedMethodsOutputTypeDef],
        "SmoothStreaming": NotRequired[bool],
        "Compress": NotRequired[bool],
        "LambdaFunctionAssociations": NotRequired[LambdaFunctionAssociationsOutputTypeDef],
        "FunctionAssociations": NotRequired[FunctionAssociationsOutputTypeDef],
        "FieldLevelEncryptionId": NotRequired[str],
        "RealtimeLogConfigArn": NotRequired[str],
        "CachePolicyId": NotRequired[str],
        "OriginRequestPolicyId": NotRequired[str],
        "ResponseHeadersPolicyId": NotRequired[str],
        "ForwardedValues": NotRequired[ForwardedValuesOutputTypeDef],
        "MinTTL": NotRequired[int],
        "DefaultTTL": NotRequired[int],
        "MaxTTL": NotRequired[int],
    },
)
CacheBehaviorTypeDef = TypedDict(
    "CacheBehaviorTypeDef",
    {
        "PathPattern": str,
        "TargetOriginId": str,
        "ViewerProtocolPolicy": ViewerProtocolPolicyType,
        "TrustedSigners": NotRequired[TrustedSignersTypeDef],
        "TrustedKeyGroups": NotRequired[TrustedKeyGroupsTypeDef],
        "AllowedMethods": NotRequired[AllowedMethodsTypeDef],
        "SmoothStreaming": NotRequired[bool],
        "Compress": NotRequired[bool],
        "LambdaFunctionAssociations": NotRequired[LambdaFunctionAssociationsTypeDef],
        "FunctionAssociations": NotRequired[FunctionAssociationsTypeDef],
        "FieldLevelEncryptionId": NotRequired[str],
        "RealtimeLogConfigArn": NotRequired[str],
        "CachePolicyId": NotRequired[str],
        "OriginRequestPolicyId": NotRequired[str],
        "ResponseHeadersPolicyId": NotRequired[str],
        "ForwardedValues": NotRequired[ForwardedValuesTypeDef],
        "MinTTL": NotRequired[int],
        "DefaultTTL": NotRequired[int],
        "MaxTTL": NotRequired[int],
    },
)
DefaultCacheBehaviorTypeDef = TypedDict(
    "DefaultCacheBehaviorTypeDef",
    {
        "TargetOriginId": str,
        "ViewerProtocolPolicy": ViewerProtocolPolicyType,
        "TrustedSigners": NotRequired[TrustedSignersTypeDef],
        "TrustedKeyGroups": NotRequired[TrustedKeyGroupsTypeDef],
        "AllowedMethods": NotRequired[AllowedMethodsTypeDef],
        "SmoothStreaming": NotRequired[bool],
        "Compress": NotRequired[bool],
        "LambdaFunctionAssociations": NotRequired[LambdaFunctionAssociationsTypeDef],
        "FunctionAssociations": NotRequired[FunctionAssociationsTypeDef],
        "FieldLevelEncryptionId": NotRequired[str],
        "RealtimeLogConfigArn": NotRequired[str],
        "CachePolicyId": NotRequired[str],
        "OriginRequestPolicyId": NotRequired[str],
        "ResponseHeadersPolicyId": NotRequired[str],
        "ForwardedValues": NotRequired[ForwardedValuesTypeDef],
        "MinTTL": NotRequired[int],
        "DefaultTTL": NotRequired[int],
        "MaxTTL": NotRequired[int],
    },
)
CachePolicyConfigOutputTypeDef = TypedDict(
    "CachePolicyConfigOutputTypeDef",
    {
        "Name": str,
        "MinTTL": int,
        "Comment": NotRequired[str],
        "DefaultTTL": NotRequired[int],
        "MaxTTL": NotRequired[int],
        "ParametersInCacheKeyAndForwardedToOrigin": NotRequired[
            ParametersInCacheKeyAndForwardedToOriginOutputTypeDef
        ],
    },
)
GetOriginRequestPolicyConfigResultTypeDef = TypedDict(
    "GetOriginRequestPolicyConfigResultTypeDef",
    {
        "OriginRequestPolicyConfig": OriginRequestPolicyConfigOutputTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
OriginRequestPolicyTypeDef = TypedDict(
    "OriginRequestPolicyTypeDef",
    {
        "Id": str,
        "LastModifiedTime": datetime,
        "OriginRequestPolicyConfig": OriginRequestPolicyConfigOutputTypeDef,
    },
)
CachePolicyConfigTypeDef = TypedDict(
    "CachePolicyConfigTypeDef",
    {
        "Name": str,
        "MinTTL": int,
        "Comment": NotRequired[str],
        "DefaultTTL": NotRequired[int],
        "MaxTTL": NotRequired[int],
        "ParametersInCacheKeyAndForwardedToOrigin": NotRequired[
            ParametersInCacheKeyAndForwardedToOriginTypeDef
        ],
    },
)
CreateOriginRequestPolicyRequestRequestTypeDef = TypedDict(
    "CreateOriginRequestPolicyRequestRequestTypeDef",
    {
        "OriginRequestPolicyConfig": OriginRequestPolicyConfigTypeDef,
    },
)
UpdateOriginRequestPolicyRequestRequestTypeDef = TypedDict(
    "UpdateOriginRequestPolicyRequestRequestTypeDef",
    {
        "OriginRequestPolicyConfig": OriginRequestPolicyConfigTypeDef,
        "Id": str,
        "IfMatch": NotRequired[str],
    },
)
ContinuousDeploymentPolicyConfigOutputTypeDef = TypedDict(
    "ContinuousDeploymentPolicyConfigOutputTypeDef",
    {
        "StagingDistributionDnsNames": StagingDistributionDnsNamesOutputTypeDef,
        "Enabled": bool,
        "TrafficConfig": NotRequired[TrafficConfigTypeDef],
    },
)
ContinuousDeploymentPolicyConfigTypeDef = TypedDict(
    "ContinuousDeploymentPolicyConfigTypeDef",
    {
        "StagingDistributionDnsNames": StagingDistributionDnsNamesTypeDef,
        "Enabled": bool,
        "TrafficConfig": NotRequired[TrafficConfigTypeDef],
    },
)
OriginsOutputTypeDef = TypedDict(
    "OriginsOutputTypeDef",
    {
        "Quantity": int,
        "Items": List[OriginOutputTypeDef],
    },
)
OriginsTypeDef = TypedDict(
    "OriginsTypeDef",
    {
        "Quantity": int,
        "Items": Sequence[OriginTypeDef],
    },
)
FieldLevelEncryptionProfileConfigOutputTypeDef = TypedDict(
    "FieldLevelEncryptionProfileConfigOutputTypeDef",
    {
        "Name": str,
        "CallerReference": str,
        "EncryptionEntities": EncryptionEntitiesOutputTypeDef,
        "Comment": NotRequired[str],
    },
)
FieldLevelEncryptionProfileSummaryTypeDef = TypedDict(
    "FieldLevelEncryptionProfileSummaryTypeDef",
    {
        "Id": str,
        "LastModifiedTime": datetime,
        "Name": str,
        "EncryptionEntities": EncryptionEntitiesOutputTypeDef,
        "Comment": NotRequired[str],
    },
)
FieldLevelEncryptionProfileConfigTypeDef = TypedDict(
    "FieldLevelEncryptionProfileConfigTypeDef",
    {
        "Name": str,
        "CallerReference": str,
        "EncryptionEntities": EncryptionEntitiesTypeDef,
        "Comment": NotRequired[str],
    },
)
CreateRealtimeLogConfigResultTypeDef = TypedDict(
    "CreateRealtimeLogConfigResultTypeDef",
    {
        "RealtimeLogConfig": RealtimeLogConfigTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetRealtimeLogConfigResultTypeDef = TypedDict(
    "GetRealtimeLogConfigResultTypeDef",
    {
        "RealtimeLogConfig": RealtimeLogConfigTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
RealtimeLogConfigsTypeDef = TypedDict(
    "RealtimeLogConfigsTypeDef",
    {
        "MaxItems": int,
        "IsTruncated": bool,
        "Marker": str,
        "Items": NotRequired[List[RealtimeLogConfigTypeDef]],
        "NextMarker": NotRequired[str],
    },
)
UpdateRealtimeLogConfigResultTypeDef = TypedDict(
    "UpdateRealtimeLogConfigResultTypeDef",
    {
        "RealtimeLogConfig": RealtimeLogConfigTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
KeyGroupListTypeDef = TypedDict(
    "KeyGroupListTypeDef",
    {
        "MaxItems": int,
        "Quantity": int,
        "NextMarker": NotRequired[str],
        "Items": NotRequired[List[KeyGroupSummaryTypeDef]],
    },
)
CreateInvalidationResultTypeDef = TypedDict(
    "CreateInvalidationResultTypeDef",
    {
        "Location": str,
        "Invalidation": InvalidationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetInvalidationResultTypeDef = TypedDict(
    "GetInvalidationResultTypeDef",
    {
        "Invalidation": InvalidationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
StreamingDistributionTypeDef = TypedDict(
    "StreamingDistributionTypeDef",
    {
        "Id": str,
        "ARN": str,
        "Status": str,
        "DomainName": str,
        "ActiveTrustedSigners": ActiveTrustedSignersTypeDef,
        "StreamingDistributionConfig": StreamingDistributionConfigOutputTypeDef,
        "LastModifiedTime": NotRequired[datetime],
    },
)
FunctionSummaryTypeDef = TypedDict(
    "FunctionSummaryTypeDef",
    {
        "Name": str,
        "FunctionConfig": FunctionConfigOutputTypeDef,
        "FunctionMetadata": FunctionMetadataTypeDef,
        "Status": NotRequired[str],
    },
)
CreateFunctionRequestRequestTypeDef = TypedDict(
    "CreateFunctionRequestRequestTypeDef",
    {
        "Name": str,
        "FunctionConfig": FunctionConfigTypeDef,
        "FunctionCode": BlobTypeDef,
    },
)
UpdateFunctionRequestRequestTypeDef = TypedDict(
    "UpdateFunctionRequestRequestTypeDef",
    {
        "Name": str,
        "IfMatch": str,
        "FunctionConfig": FunctionConfigTypeDef,
        "FunctionCode": BlobTypeDef,
    },
)
OriginGroupsOutputTypeDef = TypedDict(
    "OriginGroupsOutputTypeDef",
    {
        "Quantity": int,
        "Items": NotRequired[List[OriginGroupOutputTypeDef]],
    },
)
OriginGroupsTypeDef = TypedDict(
    "OriginGroupsTypeDef",
    {
        "Quantity": int,
        "Items": NotRequired[Sequence[OriginGroupTypeDef]],
    },
)
FieldLevelEncryptionConfigOutputTypeDef = TypedDict(
    "FieldLevelEncryptionConfigOutputTypeDef",
    {
        "CallerReference": str,
        "Comment": NotRequired[str],
        "QueryArgProfileConfig": NotRequired[QueryArgProfileConfigOutputTypeDef],
        "ContentTypeProfileConfig": NotRequired[ContentTypeProfileConfigOutputTypeDef],
    },
)
FieldLevelEncryptionSummaryTypeDef = TypedDict(
    "FieldLevelEncryptionSummaryTypeDef",
    {
        "Id": str,
        "LastModifiedTime": datetime,
        "Comment": NotRequired[str],
        "QueryArgProfileConfig": NotRequired[QueryArgProfileConfigOutputTypeDef],
        "ContentTypeProfileConfig": NotRequired[ContentTypeProfileConfigOutputTypeDef],
    },
)
FieldLevelEncryptionConfigTypeDef = TypedDict(
    "FieldLevelEncryptionConfigTypeDef",
    {
        "CallerReference": str,
        "Comment": NotRequired[str],
        "QueryArgProfileConfig": NotRequired[QueryArgProfileConfigTypeDef],
        "ContentTypeProfileConfig": NotRequired[ContentTypeProfileConfigTypeDef],
    },
)
GetResponseHeadersPolicyConfigResultTypeDef = TypedDict(
    "GetResponseHeadersPolicyConfigResultTypeDef",
    {
        "ResponseHeadersPolicyConfig": ResponseHeadersPolicyConfigOutputTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ResponseHeadersPolicyTypeDef = TypedDict(
    "ResponseHeadersPolicyTypeDef",
    {
        "Id": str,
        "LastModifiedTime": datetime,
        "ResponseHeadersPolicyConfig": ResponseHeadersPolicyConfigOutputTypeDef,
    },
)
CreateResponseHeadersPolicyRequestRequestTypeDef = TypedDict(
    "CreateResponseHeadersPolicyRequestRequestTypeDef",
    {
        "ResponseHeadersPolicyConfig": ResponseHeadersPolicyConfigTypeDef,
    },
)
UpdateResponseHeadersPolicyRequestRequestTypeDef = TypedDict(
    "UpdateResponseHeadersPolicyRequestRequestTypeDef",
    {
        "ResponseHeadersPolicyConfig": ResponseHeadersPolicyConfigTypeDef,
        "Id": str,
        "IfMatch": NotRequired[str],
    },
)
ListStreamingDistributionsResultTypeDef = TypedDict(
    "ListStreamingDistributionsResultTypeDef",
    {
        "StreamingDistributionList": StreamingDistributionListTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateStreamingDistributionWithTagsRequestRequestTypeDef = TypedDict(
    "CreateStreamingDistributionWithTagsRequestRequestTypeDef",
    {
        "StreamingDistributionConfigWithTags": StreamingDistributionConfigWithTagsTypeDef,
    },
)
CacheBehaviorsOutputTypeDef = TypedDict(
    "CacheBehaviorsOutputTypeDef",
    {
        "Quantity": int,
        "Items": NotRequired[List[CacheBehaviorOutputTypeDef]],
    },
)
CacheBehaviorsTypeDef = TypedDict(
    "CacheBehaviorsTypeDef",
    {
        "Quantity": int,
        "Items": NotRequired[Sequence[CacheBehaviorTypeDef]],
    },
)
CachePolicyTypeDef = TypedDict(
    "CachePolicyTypeDef",
    {
        "Id": str,
        "LastModifiedTime": datetime,
        "CachePolicyConfig": CachePolicyConfigOutputTypeDef,
    },
)
GetCachePolicyConfigResultTypeDef = TypedDict(
    "GetCachePolicyConfigResultTypeDef",
    {
        "CachePolicyConfig": CachePolicyConfigOutputTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateOriginRequestPolicyResultTypeDef = TypedDict(
    "CreateOriginRequestPolicyResultTypeDef",
    {
        "OriginRequestPolicy": OriginRequestPolicyTypeDef,
        "Location": str,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetOriginRequestPolicyResultTypeDef = TypedDict(
    "GetOriginRequestPolicyResultTypeDef",
    {
        "OriginRequestPolicy": OriginRequestPolicyTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
OriginRequestPolicySummaryTypeDef = TypedDict(
    "OriginRequestPolicySummaryTypeDef",
    {
        "Type": OriginRequestPolicyTypeType,
        "OriginRequestPolicy": OriginRequestPolicyTypeDef,
    },
)
UpdateOriginRequestPolicyResultTypeDef = TypedDict(
    "UpdateOriginRequestPolicyResultTypeDef",
    {
        "OriginRequestPolicy": OriginRequestPolicyTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateCachePolicyRequestRequestTypeDef = TypedDict(
    "CreateCachePolicyRequestRequestTypeDef",
    {
        "CachePolicyConfig": CachePolicyConfigTypeDef,
    },
)
UpdateCachePolicyRequestRequestTypeDef = TypedDict(
    "UpdateCachePolicyRequestRequestTypeDef",
    {
        "CachePolicyConfig": CachePolicyConfigTypeDef,
        "Id": str,
        "IfMatch": NotRequired[str],
    },
)
ContinuousDeploymentPolicyTypeDef = TypedDict(
    "ContinuousDeploymentPolicyTypeDef",
    {
        "Id": str,
        "LastModifiedTime": datetime,
        "ContinuousDeploymentPolicyConfig": ContinuousDeploymentPolicyConfigOutputTypeDef,
    },
)
GetContinuousDeploymentPolicyConfigResultTypeDef = TypedDict(
    "GetContinuousDeploymentPolicyConfigResultTypeDef",
    {
        "ContinuousDeploymentPolicyConfig": ContinuousDeploymentPolicyConfigOutputTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateContinuousDeploymentPolicyRequestRequestTypeDef = TypedDict(
    "CreateContinuousDeploymentPolicyRequestRequestTypeDef",
    {
        "ContinuousDeploymentPolicyConfig": ContinuousDeploymentPolicyConfigTypeDef,
    },
)
UpdateContinuousDeploymentPolicyRequestRequestTypeDef = TypedDict(
    "UpdateContinuousDeploymentPolicyRequestRequestTypeDef",
    {
        "ContinuousDeploymentPolicyConfig": ContinuousDeploymentPolicyConfigTypeDef,
        "Id": str,
        "IfMatch": NotRequired[str],
    },
)
FieldLevelEncryptionProfileTypeDef = TypedDict(
    "FieldLevelEncryptionProfileTypeDef",
    {
        "Id": str,
        "LastModifiedTime": datetime,
        "FieldLevelEncryptionProfileConfig": FieldLevelEncryptionProfileConfigOutputTypeDef,
    },
)
GetFieldLevelEncryptionProfileConfigResultTypeDef = TypedDict(
    "GetFieldLevelEncryptionProfileConfigResultTypeDef",
    {
        "FieldLevelEncryptionProfileConfig": FieldLevelEncryptionProfileConfigOutputTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
FieldLevelEncryptionProfileListTypeDef = TypedDict(
    "FieldLevelEncryptionProfileListTypeDef",
    {
        "MaxItems": int,
        "Quantity": int,
        "NextMarker": NotRequired[str],
        "Items": NotRequired[List[FieldLevelEncryptionProfileSummaryTypeDef]],
    },
)
CreateFieldLevelEncryptionProfileRequestRequestTypeDef = TypedDict(
    "CreateFieldLevelEncryptionProfileRequestRequestTypeDef",
    {
        "FieldLevelEncryptionProfileConfig": FieldLevelEncryptionProfileConfigTypeDef,
    },
)
UpdateFieldLevelEncryptionProfileRequestRequestTypeDef = TypedDict(
    "UpdateFieldLevelEncryptionProfileRequestRequestTypeDef",
    {
        "FieldLevelEncryptionProfileConfig": FieldLevelEncryptionProfileConfigTypeDef,
        "Id": str,
        "IfMatch": NotRequired[str],
    },
)
ListRealtimeLogConfigsResultTypeDef = TypedDict(
    "ListRealtimeLogConfigsResultTypeDef",
    {
        "RealtimeLogConfigs": RealtimeLogConfigsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListKeyGroupsResultTypeDef = TypedDict(
    "ListKeyGroupsResultTypeDef",
    {
        "KeyGroupList": KeyGroupListTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateStreamingDistributionResultTypeDef = TypedDict(
    "CreateStreamingDistributionResultTypeDef",
    {
        "StreamingDistribution": StreamingDistributionTypeDef,
        "Location": str,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateStreamingDistributionWithTagsResultTypeDef = TypedDict(
    "CreateStreamingDistributionWithTagsResultTypeDef",
    {
        "StreamingDistribution": StreamingDistributionTypeDef,
        "Location": str,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetStreamingDistributionResultTypeDef = TypedDict(
    "GetStreamingDistributionResultTypeDef",
    {
        "StreamingDistribution": StreamingDistributionTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateStreamingDistributionResultTypeDef = TypedDict(
    "UpdateStreamingDistributionResultTypeDef",
    {
        "StreamingDistribution": StreamingDistributionTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateFunctionResultTypeDef = TypedDict(
    "CreateFunctionResultTypeDef",
    {
        "FunctionSummary": FunctionSummaryTypeDef,
        "Location": str,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DescribeFunctionResultTypeDef = TypedDict(
    "DescribeFunctionResultTypeDef",
    {
        "FunctionSummary": FunctionSummaryTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
FunctionListTypeDef = TypedDict(
    "FunctionListTypeDef",
    {
        "MaxItems": int,
        "Quantity": int,
        "NextMarker": NotRequired[str],
        "Items": NotRequired[List[FunctionSummaryTypeDef]],
    },
)
PublishFunctionResultTypeDef = TypedDict(
    "PublishFunctionResultTypeDef",
    {
        "FunctionSummary": FunctionSummaryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
TestResultTypeDef = TypedDict(
    "TestResultTypeDef",
    {
        "FunctionSummary": NotRequired[FunctionSummaryTypeDef],
        "ComputeUtilization": NotRequired[str],
        "FunctionExecutionLogs": NotRequired[List[str]],
        "FunctionErrorMessage": NotRequired[str],
        "FunctionOutput": NotRequired[str],
    },
)
UpdateFunctionResultTypeDef = TypedDict(
    "UpdateFunctionResultTypeDef",
    {
        "FunctionSummary": FunctionSummaryTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
FieldLevelEncryptionTypeDef = TypedDict(
    "FieldLevelEncryptionTypeDef",
    {
        "Id": str,
        "LastModifiedTime": datetime,
        "FieldLevelEncryptionConfig": FieldLevelEncryptionConfigOutputTypeDef,
    },
)
GetFieldLevelEncryptionConfigResultTypeDef = TypedDict(
    "GetFieldLevelEncryptionConfigResultTypeDef",
    {
        "FieldLevelEncryptionConfig": FieldLevelEncryptionConfigOutputTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
FieldLevelEncryptionListTypeDef = TypedDict(
    "FieldLevelEncryptionListTypeDef",
    {
        "MaxItems": int,
        "Quantity": int,
        "NextMarker": NotRequired[str],
        "Items": NotRequired[List[FieldLevelEncryptionSummaryTypeDef]],
    },
)
CreateFieldLevelEncryptionConfigRequestRequestTypeDef = TypedDict(
    "CreateFieldLevelEncryptionConfigRequestRequestTypeDef",
    {
        "FieldLevelEncryptionConfig": FieldLevelEncryptionConfigTypeDef,
    },
)
UpdateFieldLevelEncryptionConfigRequestRequestTypeDef = TypedDict(
    "UpdateFieldLevelEncryptionConfigRequestRequestTypeDef",
    {
        "FieldLevelEncryptionConfig": FieldLevelEncryptionConfigTypeDef,
        "Id": str,
        "IfMatch": NotRequired[str],
    },
)
CreateResponseHeadersPolicyResultTypeDef = TypedDict(
    "CreateResponseHeadersPolicyResultTypeDef",
    {
        "ResponseHeadersPolicy": ResponseHeadersPolicyTypeDef,
        "Location": str,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetResponseHeadersPolicyResultTypeDef = TypedDict(
    "GetResponseHeadersPolicyResultTypeDef",
    {
        "ResponseHeadersPolicy": ResponseHeadersPolicyTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ResponseHeadersPolicySummaryTypeDef = TypedDict(
    "ResponseHeadersPolicySummaryTypeDef",
    {
        "Type": ResponseHeadersPolicyTypeType,
        "ResponseHeadersPolicy": ResponseHeadersPolicyTypeDef,
    },
)
UpdateResponseHeadersPolicyResultTypeDef = TypedDict(
    "UpdateResponseHeadersPolicyResultTypeDef",
    {
        "ResponseHeadersPolicy": ResponseHeadersPolicyTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DistributionConfigOutputTypeDef = TypedDict(
    "DistributionConfigOutputTypeDef",
    {
        "CallerReference": str,
        "Origins": OriginsOutputTypeDef,
        "DefaultCacheBehavior": DefaultCacheBehaviorOutputTypeDef,
        "Comment": str,
        "Enabled": bool,
        "Aliases": NotRequired[AliasesOutputTypeDef],
        "DefaultRootObject": NotRequired[str],
        "OriginGroups": NotRequired[OriginGroupsOutputTypeDef],
        "CacheBehaviors": NotRequired[CacheBehaviorsOutputTypeDef],
        "CustomErrorResponses": NotRequired[CustomErrorResponsesOutputTypeDef],
        "Logging": NotRequired[LoggingConfigTypeDef],
        "PriceClass": NotRequired[PriceClassType],
        "ViewerCertificate": NotRequired[ViewerCertificateTypeDef],
        "Restrictions": NotRequired[RestrictionsOutputTypeDef],
        "WebACLId": NotRequired[str],
        "HttpVersion": NotRequired[HttpVersionType],
        "IsIPV6Enabled": NotRequired[bool],
        "ContinuousDeploymentPolicyId": NotRequired[str],
        "Staging": NotRequired[bool],
    },
)
DistributionSummaryTypeDef = TypedDict(
    "DistributionSummaryTypeDef",
    {
        "Id": str,
        "ARN": str,
        "Status": str,
        "LastModifiedTime": datetime,
        "DomainName": str,
        "Aliases": AliasesOutputTypeDef,
        "Origins": OriginsOutputTypeDef,
        "DefaultCacheBehavior": DefaultCacheBehaviorOutputTypeDef,
        "CacheBehaviors": CacheBehaviorsOutputTypeDef,
        "CustomErrorResponses": CustomErrorResponsesOutputTypeDef,
        "Comment": str,
        "PriceClass": PriceClassType,
        "Enabled": bool,
        "ViewerCertificate": ViewerCertificateTypeDef,
        "Restrictions": RestrictionsOutputTypeDef,
        "WebACLId": str,
        "HttpVersion": HttpVersionType,
        "IsIPV6Enabled": bool,
        "Staging": bool,
        "OriginGroups": NotRequired[OriginGroupsOutputTypeDef],
        "AliasICPRecordals": NotRequired[List[AliasICPRecordalTypeDef]],
    },
)
DistributionConfigTypeDef = TypedDict(
    "DistributionConfigTypeDef",
    {
        "CallerReference": str,
        "Origins": OriginsTypeDef,
        "DefaultCacheBehavior": DefaultCacheBehaviorTypeDef,
        "Comment": str,
        "Enabled": bool,
        "Aliases": NotRequired[AliasesTypeDef],
        "DefaultRootObject": NotRequired[str],
        "OriginGroups": NotRequired[OriginGroupsTypeDef],
        "CacheBehaviors": NotRequired[CacheBehaviorsTypeDef],
        "CustomErrorResponses": NotRequired[CustomErrorResponsesTypeDef],
        "Logging": NotRequired[LoggingConfigTypeDef],
        "PriceClass": NotRequired[PriceClassType],
        "ViewerCertificate": NotRequired[ViewerCertificateTypeDef],
        "Restrictions": NotRequired[RestrictionsTypeDef],
        "WebACLId": NotRequired[str],
        "HttpVersion": NotRequired[HttpVersionType],
        "IsIPV6Enabled": NotRequired[bool],
        "ContinuousDeploymentPolicyId": NotRequired[str],
        "Staging": NotRequired[bool],
    },
)
CachePolicySummaryTypeDef = TypedDict(
    "CachePolicySummaryTypeDef",
    {
        "Type": CachePolicyTypeType,
        "CachePolicy": CachePolicyTypeDef,
    },
)
CreateCachePolicyResultTypeDef = TypedDict(
    "CreateCachePolicyResultTypeDef",
    {
        "CachePolicy": CachePolicyTypeDef,
        "Location": str,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetCachePolicyResultTypeDef = TypedDict(
    "GetCachePolicyResultTypeDef",
    {
        "CachePolicy": CachePolicyTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateCachePolicyResultTypeDef = TypedDict(
    "UpdateCachePolicyResultTypeDef",
    {
        "CachePolicy": CachePolicyTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
OriginRequestPolicyListTypeDef = TypedDict(
    "OriginRequestPolicyListTypeDef",
    {
        "MaxItems": int,
        "Quantity": int,
        "NextMarker": NotRequired[str],
        "Items": NotRequired[List[OriginRequestPolicySummaryTypeDef]],
    },
)
ContinuousDeploymentPolicySummaryTypeDef = TypedDict(
    "ContinuousDeploymentPolicySummaryTypeDef",
    {
        "ContinuousDeploymentPolicy": ContinuousDeploymentPolicyTypeDef,
    },
)
CreateContinuousDeploymentPolicyResultTypeDef = TypedDict(
    "CreateContinuousDeploymentPolicyResultTypeDef",
    {
        "ContinuousDeploymentPolicy": ContinuousDeploymentPolicyTypeDef,
        "Location": str,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetContinuousDeploymentPolicyResultTypeDef = TypedDict(
    "GetContinuousDeploymentPolicyResultTypeDef",
    {
        "ContinuousDeploymentPolicy": ContinuousDeploymentPolicyTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateContinuousDeploymentPolicyResultTypeDef = TypedDict(
    "UpdateContinuousDeploymentPolicyResultTypeDef",
    {
        "ContinuousDeploymentPolicy": ContinuousDeploymentPolicyTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateFieldLevelEncryptionProfileResultTypeDef = TypedDict(
    "CreateFieldLevelEncryptionProfileResultTypeDef",
    {
        "FieldLevelEncryptionProfile": FieldLevelEncryptionProfileTypeDef,
        "Location": str,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetFieldLevelEncryptionProfileResultTypeDef = TypedDict(
    "GetFieldLevelEncryptionProfileResultTypeDef",
    {
        "FieldLevelEncryptionProfile": FieldLevelEncryptionProfileTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateFieldLevelEncryptionProfileResultTypeDef = TypedDict(
    "UpdateFieldLevelEncryptionProfileResultTypeDef",
    {
        "FieldLevelEncryptionProfile": FieldLevelEncryptionProfileTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListFieldLevelEncryptionProfilesResultTypeDef = TypedDict(
    "ListFieldLevelEncryptionProfilesResultTypeDef",
    {
        "FieldLevelEncryptionProfileList": FieldLevelEncryptionProfileListTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListFunctionsResultTypeDef = TypedDict(
    "ListFunctionsResultTypeDef",
    {
        "FunctionList": FunctionListTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
TestFunctionResultTypeDef = TypedDict(
    "TestFunctionResultTypeDef",
    {
        "TestResult": TestResultTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateFieldLevelEncryptionConfigResultTypeDef = TypedDict(
    "CreateFieldLevelEncryptionConfigResultTypeDef",
    {
        "FieldLevelEncryption": FieldLevelEncryptionTypeDef,
        "Location": str,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetFieldLevelEncryptionResultTypeDef = TypedDict(
    "GetFieldLevelEncryptionResultTypeDef",
    {
        "FieldLevelEncryption": FieldLevelEncryptionTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateFieldLevelEncryptionConfigResultTypeDef = TypedDict(
    "UpdateFieldLevelEncryptionConfigResultTypeDef",
    {
        "FieldLevelEncryption": FieldLevelEncryptionTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListFieldLevelEncryptionConfigsResultTypeDef = TypedDict(
    "ListFieldLevelEncryptionConfigsResultTypeDef",
    {
        "FieldLevelEncryptionList": FieldLevelEncryptionListTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ResponseHeadersPolicyListTypeDef = TypedDict(
    "ResponseHeadersPolicyListTypeDef",
    {
        "MaxItems": int,
        "Quantity": int,
        "NextMarker": NotRequired[str],
        "Items": NotRequired[List[ResponseHeadersPolicySummaryTypeDef]],
    },
)
DistributionTypeDef = TypedDict(
    "DistributionTypeDef",
    {
        "Id": str,
        "ARN": str,
        "Status": str,
        "LastModifiedTime": datetime,
        "InProgressInvalidationBatches": int,
        "DomainName": str,
        "DistributionConfig": DistributionConfigOutputTypeDef,
        "ActiveTrustedSigners": NotRequired[ActiveTrustedSignersTypeDef],
        "ActiveTrustedKeyGroups": NotRequired[ActiveTrustedKeyGroupsTypeDef],
        "AliasICPRecordals": NotRequired[List[AliasICPRecordalTypeDef]],
    },
)
GetDistributionConfigResultTypeDef = TypedDict(
    "GetDistributionConfigResultTypeDef",
    {
        "DistributionConfig": DistributionConfigOutputTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DistributionListTypeDef = TypedDict(
    "DistributionListTypeDef",
    {
        "Marker": str,
        "MaxItems": int,
        "IsTruncated": bool,
        "Quantity": int,
        "NextMarker": NotRequired[str],
        "Items": NotRequired[List[DistributionSummaryTypeDef]],
    },
)
CreateDistributionRequestRequestTypeDef = TypedDict(
    "CreateDistributionRequestRequestTypeDef",
    {
        "DistributionConfig": DistributionConfigTypeDef,
    },
)
DistributionConfigWithTagsTypeDef = TypedDict(
    "DistributionConfigWithTagsTypeDef",
    {
        "DistributionConfig": DistributionConfigTypeDef,
        "Tags": TagsTypeDef,
    },
)
UpdateDistributionRequestRequestTypeDef = TypedDict(
    "UpdateDistributionRequestRequestTypeDef",
    {
        "DistributionConfig": DistributionConfigTypeDef,
        "Id": str,
        "IfMatch": NotRequired[str],
    },
)
CachePolicyListTypeDef = TypedDict(
    "CachePolicyListTypeDef",
    {
        "MaxItems": int,
        "Quantity": int,
        "NextMarker": NotRequired[str],
        "Items": NotRequired[List[CachePolicySummaryTypeDef]],
    },
)
ListOriginRequestPoliciesResultTypeDef = TypedDict(
    "ListOriginRequestPoliciesResultTypeDef",
    {
        "OriginRequestPolicyList": OriginRequestPolicyListTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ContinuousDeploymentPolicyListTypeDef = TypedDict(
    "ContinuousDeploymentPolicyListTypeDef",
    {
        "MaxItems": int,
        "Quantity": int,
        "NextMarker": NotRequired[str],
        "Items": NotRequired[List[ContinuousDeploymentPolicySummaryTypeDef]],
    },
)
ListResponseHeadersPoliciesResultTypeDef = TypedDict(
    "ListResponseHeadersPoliciesResultTypeDef",
    {
        "ResponseHeadersPolicyList": ResponseHeadersPolicyListTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CopyDistributionResultTypeDef = TypedDict(
    "CopyDistributionResultTypeDef",
    {
        "Distribution": DistributionTypeDef,
        "Location": str,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateDistributionResultTypeDef = TypedDict(
    "CreateDistributionResultTypeDef",
    {
        "Distribution": DistributionTypeDef,
        "Location": str,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateDistributionWithTagsResultTypeDef = TypedDict(
    "CreateDistributionWithTagsResultTypeDef",
    {
        "Distribution": DistributionTypeDef,
        "Location": str,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetDistributionResultTypeDef = TypedDict(
    "GetDistributionResultTypeDef",
    {
        "Distribution": DistributionTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateDistributionResultTypeDef = TypedDict(
    "UpdateDistributionResultTypeDef",
    {
        "Distribution": DistributionTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateDistributionWithStagingConfigResultTypeDef = TypedDict(
    "UpdateDistributionWithStagingConfigResultTypeDef",
    {
        "Distribution": DistributionTypeDef,
        "ETag": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListDistributionsByRealtimeLogConfigResultTypeDef = TypedDict(
    "ListDistributionsByRealtimeLogConfigResultTypeDef",
    {
        "DistributionList": DistributionListTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListDistributionsByWebACLIdResultTypeDef = TypedDict(
    "ListDistributionsByWebACLIdResultTypeDef",
    {
        "DistributionList": DistributionListTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListDistributionsResultTypeDef = TypedDict(
    "ListDistributionsResultTypeDef",
    {
        "DistributionList": DistributionListTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateDistributionWithTagsRequestRequestTypeDef = TypedDict(
    "CreateDistributionWithTagsRequestRequestTypeDef",
    {
        "DistributionConfigWithTags": DistributionConfigWithTagsTypeDef,
    },
)
ListCachePoliciesResultTypeDef = TypedDict(
    "ListCachePoliciesResultTypeDef",
    {
        "CachePolicyList": CachePolicyListTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListContinuousDeploymentPoliciesResultTypeDef = TypedDict(
    "ListContinuousDeploymentPoliciesResultTypeDef",
    {
        "ContinuousDeploymentPolicyList": ContinuousDeploymentPolicyListTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
