"""
Type annotations for qconnect service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/type_defs/)

Usage::

    ```python
    from types_aiobotocore_qconnect.type_defs import AmazonConnectGuideAssociationDataTypeDef

    data: AmazonConnectGuideAssociationDataTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    AssistantCapabilityTypeType,
    AssistantStatusType,
    ContentStatusType,
    ImportJobStatusType,
    KnowledgeBaseStatusType,
    KnowledgeBaseTypeType,
    OrderType,
    PriorityType,
    QueryResultTypeType,
    QuickResponseFilterOperatorType,
    QuickResponseQueryOperatorType,
    QuickResponseStatusType,
    RecommendationSourceTypeType,
    RecommendationTriggerTypeType,
    RecommendationTypeType,
    RelevanceLevelType,
    RelevanceType,
    TargetTypeType,
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
    "AmazonConnectGuideAssociationDataTypeDef",
    "AppIntegrationsConfigurationOutputTypeDef",
    "AppIntegrationsConfigurationTypeDef",
    "AssistantAssociationInputDataTypeDef",
    "KnowledgeBaseAssociationDataTypeDef",
    "AssistantCapabilityConfigurationTypeDef",
    "AssistantIntegrationConfigurationTypeDef",
    "ServerSideEncryptionConfigurationTypeDef",
    "ConnectConfigurationTypeDef",
    "RankingDataTypeDef",
    "ContentDataTypeDef",
    "GenerativeContentFeedbackDataTypeDef",
    "ContentReferenceTypeDef",
    "ContentSummaryTypeDef",
    "ResponseMetadataTypeDef",
    "CreateContentRequestRequestTypeDef",
    "RenderingConfigurationTypeDef",
    "GroupingConfigurationTypeDef",
    "QuickResponseDataProviderTypeDef",
    "GenerativeReferenceTypeDef",
    "DeleteAssistantAssociationRequestRequestTypeDef",
    "DeleteAssistantRequestRequestTypeDef",
    "DeleteContentAssociationRequestRequestTypeDef",
    "DeleteContentRequestRequestTypeDef",
    "DeleteImportJobRequestRequestTypeDef",
    "DeleteKnowledgeBaseRequestRequestTypeDef",
    "DeleteQuickResponseRequestRequestTypeDef",
    "HighlightTypeDef",
    "FilterTypeDef",
    "GetAssistantAssociationRequestRequestTypeDef",
    "GetAssistantRequestRequestTypeDef",
    "GetContentAssociationRequestRequestTypeDef",
    "GetContentRequestRequestTypeDef",
    "GetContentSummaryRequestRequestTypeDef",
    "GetImportJobRequestRequestTypeDef",
    "GetKnowledgeBaseRequestRequestTypeDef",
    "GetQuickResponseRequestRequestTypeDef",
    "GetRecommendationsRequestRequestTypeDef",
    "GetSessionRequestRequestTypeDef",
    "GroupingConfigurationOutputTypeDef",
    "PaginatorConfigTypeDef",
    "ListAssistantAssociationsRequestRequestTypeDef",
    "ListAssistantsRequestRequestTypeDef",
    "ListContentAssociationsRequestRequestTypeDef",
    "ListContentsRequestRequestTypeDef",
    "ListImportJobsRequestRequestTypeDef",
    "ListKnowledgeBasesRequestRequestTypeDef",
    "ListQuickResponsesRequestRequestTypeDef",
    "QuickResponseSummaryTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "NotifyRecommendationsReceivedErrorTypeDef",
    "NotifyRecommendationsReceivedRequestRequestTypeDef",
    "TagConditionTypeDef",
    "QueryConditionItemTypeDef",
    "QueryRecommendationTriggerDataTypeDef",
    "QuickResponseContentProviderTypeDef",
    "QuickResponseFilterFieldTypeDef",
    "QuickResponseOrderFieldTypeDef",
    "QuickResponseQueryFieldTypeDef",
    "RemoveKnowledgeBaseTemplateUriRequestRequestTypeDef",
    "SessionSummaryTypeDef",
    "SessionIntegrationConfigurationTypeDef",
    "StartContentUploadRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateContentRequestRequestTypeDef",
    "UpdateKnowledgeBaseTemplateUriRequestRequestTypeDef",
    "ContentAssociationContentsTypeDef",
    "SourceConfigurationOutputTypeDef",
    "SourceConfigurationTypeDef",
    "CreateAssistantAssociationRequestRequestTypeDef",
    "AssistantAssociationOutputDataTypeDef",
    "AssistantDataTypeDef",
    "AssistantSummaryTypeDef",
    "CreateAssistantRequestRequestTypeDef",
    "ConfigurationTypeDef",
    "GenerativeDataDetailsTypeDef",
    "ContentFeedbackDataTypeDef",
    "CreateContentResponseTypeDef",
    "GetContentResponseTypeDef",
    "GetContentSummaryResponseTypeDef",
    "ListContentsResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "SearchContentResponseTypeDef",
    "StartContentUploadResponseTypeDef",
    "UpdateContentResponseTypeDef",
    "CreateQuickResponseRequestRequestTypeDef",
    "UpdateQuickResponseRequestRequestTypeDef",
    "DataReferenceTypeDef",
    "DocumentTextTypeDef",
    "SearchExpressionTypeDef",
    "ListAssistantAssociationsRequestListAssistantAssociationsPaginateTypeDef",
    "ListAssistantsRequestListAssistantsPaginateTypeDef",
    "ListContentAssociationsRequestListContentAssociationsPaginateTypeDef",
    "ListContentsRequestListContentsPaginateTypeDef",
    "ListImportJobsRequestListImportJobsPaginateTypeDef",
    "ListKnowledgeBasesRequestListKnowledgeBasesPaginateTypeDef",
    "ListQuickResponsesRequestListQuickResponsesPaginateTypeDef",
    "ListQuickResponsesResponseTypeDef",
    "NotifyRecommendationsReceivedResponseTypeDef",
    "OrConditionOutputTypeDef",
    "OrConditionTypeDef",
    "QueryConditionTypeDef",
    "RecommendationTriggerDataTypeDef",
    "QuickResponseContentsTypeDef",
    "QuickResponseSearchExpressionTypeDef",
    "SearchSessionsResponseTypeDef",
    "ContentAssociationDataTypeDef",
    "ContentAssociationSummaryTypeDef",
    "CreateContentAssociationRequestRequestTypeDef",
    "KnowledgeBaseDataTypeDef",
    "KnowledgeBaseSummaryTypeDef",
    "CreateKnowledgeBaseRequestRequestTypeDef",
    "AssistantAssociationDataTypeDef",
    "AssistantAssociationSummaryTypeDef",
    "CreateAssistantResponseTypeDef",
    "GetAssistantResponseTypeDef",
    "ListAssistantsResponseTypeDef",
    "ExternalSourceConfigurationTypeDef",
    "PutFeedbackRequestRequestTypeDef",
    "PutFeedbackResponseTypeDef",
    "DataSummaryTypeDef",
    "DocumentTypeDef",
    "TextDataTypeDef",
    "SearchContentRequestRequestTypeDef",
    "SearchContentRequestSearchContentPaginateTypeDef",
    "SearchSessionsRequestRequestTypeDef",
    "SearchSessionsRequestSearchSessionsPaginateTypeDef",
    "TagFilterOutputTypeDef",
    "TagFilterTypeDef",
    "QueryAssistantRequestQueryAssistantPaginateTypeDef",
    "QueryAssistantRequestRequestTypeDef",
    "RecommendationTriggerTypeDef",
    "QuickResponseDataTypeDef",
    "QuickResponseSearchResultDataTypeDef",
    "SearchQuickResponsesRequestRequestTypeDef",
    "SearchQuickResponsesRequestSearchQuickResponsesPaginateTypeDef",
    "CreateContentAssociationResponseTypeDef",
    "GetContentAssociationResponseTypeDef",
    "ListContentAssociationsResponseTypeDef",
    "CreateKnowledgeBaseResponseTypeDef",
    "GetKnowledgeBaseResponseTypeDef",
    "UpdateKnowledgeBaseTemplateUriResponseTypeDef",
    "ListKnowledgeBasesResponseTypeDef",
    "CreateAssistantAssociationResponseTypeDef",
    "GetAssistantAssociationResponseTypeDef",
    "ListAssistantAssociationsResponseTypeDef",
    "ImportJobDataTypeDef",
    "ImportJobSummaryTypeDef",
    "StartImportJobRequestRequestTypeDef",
    "RecommendationDataTypeDef",
    "ResultDataTypeDef",
    "ContentDataDetailsTypeDef",
    "SourceContentDataDetailsTypeDef",
    "SessionDataTypeDef",
    "CreateSessionRequestRequestTypeDef",
    "UpdateSessionRequestRequestTypeDef",
    "CreateQuickResponseResponseTypeDef",
    "GetQuickResponseResponseTypeDef",
    "UpdateQuickResponseResponseTypeDef",
    "SearchQuickResponsesResponseTypeDef",
    "GetImportJobResponseTypeDef",
    "StartImportJobResponseTypeDef",
    "ListImportJobsResponseTypeDef",
    "GetRecommendationsResponseTypeDef",
    "QueryAssistantResponseTypeDef",
    "DataDetailsTypeDef",
    "CreateSessionResponseTypeDef",
    "GetSessionResponseTypeDef",
    "UpdateSessionResponseTypeDef",
)

AmazonConnectGuideAssociationDataTypeDef = TypedDict(
    "AmazonConnectGuideAssociationDataTypeDef",
    {
        "flowId": NotRequired[str],
    },
)
AppIntegrationsConfigurationOutputTypeDef = TypedDict(
    "AppIntegrationsConfigurationOutputTypeDef",
    {
        "appIntegrationArn": str,
        "objectFields": NotRequired[List[str]],
    },
)
AppIntegrationsConfigurationTypeDef = TypedDict(
    "AppIntegrationsConfigurationTypeDef",
    {
        "appIntegrationArn": str,
        "objectFields": NotRequired[Sequence[str]],
    },
)
AssistantAssociationInputDataTypeDef = TypedDict(
    "AssistantAssociationInputDataTypeDef",
    {
        "knowledgeBaseId": NotRequired[str],
    },
)
KnowledgeBaseAssociationDataTypeDef = TypedDict(
    "KnowledgeBaseAssociationDataTypeDef",
    {
        "knowledgeBaseArn": NotRequired[str],
        "knowledgeBaseId": NotRequired[str],
    },
)
AssistantCapabilityConfigurationTypeDef = TypedDict(
    "AssistantCapabilityConfigurationTypeDef",
    {
        "type": NotRequired[AssistantCapabilityTypeType],
    },
)
AssistantIntegrationConfigurationTypeDef = TypedDict(
    "AssistantIntegrationConfigurationTypeDef",
    {
        "topicIntegrationArn": NotRequired[str],
    },
)
ServerSideEncryptionConfigurationTypeDef = TypedDict(
    "ServerSideEncryptionConfigurationTypeDef",
    {
        "kmsKeyId": NotRequired[str],
    },
)
ConnectConfigurationTypeDef = TypedDict(
    "ConnectConfigurationTypeDef",
    {
        "instanceId": NotRequired[str],
    },
)
RankingDataTypeDef = TypedDict(
    "RankingDataTypeDef",
    {
        "relevanceLevel": NotRequired[RelevanceLevelType],
        "relevanceScore": NotRequired[float],
    },
)
ContentDataTypeDef = TypedDict(
    "ContentDataTypeDef",
    {
        "contentArn": str,
        "contentId": str,
        "contentType": str,
        "knowledgeBaseArn": str,
        "knowledgeBaseId": str,
        "metadata": Dict[str, str],
        "name": str,
        "revisionId": str,
        "status": ContentStatusType,
        "title": str,
        "url": str,
        "urlExpiry": datetime,
        "linkOutUri": NotRequired[str],
        "tags": NotRequired[Dict[str, str]],
    },
)
GenerativeContentFeedbackDataTypeDef = TypedDict(
    "GenerativeContentFeedbackDataTypeDef",
    {
        "relevance": RelevanceType,
    },
)
ContentReferenceTypeDef = TypedDict(
    "ContentReferenceTypeDef",
    {
        "contentArn": NotRequired[str],
        "contentId": NotRequired[str],
        "knowledgeBaseArn": NotRequired[str],
        "knowledgeBaseId": NotRequired[str],
    },
)
ContentSummaryTypeDef = TypedDict(
    "ContentSummaryTypeDef",
    {
        "contentArn": str,
        "contentId": str,
        "contentType": str,
        "knowledgeBaseArn": str,
        "knowledgeBaseId": str,
        "metadata": Dict[str, str],
        "name": str,
        "revisionId": str,
        "status": ContentStatusType,
        "title": str,
        "tags": NotRequired[Dict[str, str]],
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
CreateContentRequestRequestTypeDef = TypedDict(
    "CreateContentRequestRequestTypeDef",
    {
        "knowledgeBaseId": str,
        "name": str,
        "uploadId": str,
        "clientToken": NotRequired[str],
        "metadata": NotRequired[Mapping[str, str]],
        "overrideLinkOutUri": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
        "title": NotRequired[str],
    },
)
RenderingConfigurationTypeDef = TypedDict(
    "RenderingConfigurationTypeDef",
    {
        "templateUri": NotRequired[str],
    },
)
GroupingConfigurationTypeDef = TypedDict(
    "GroupingConfigurationTypeDef",
    {
        "criteria": NotRequired[str],
        "values": NotRequired[Sequence[str]],
    },
)
QuickResponseDataProviderTypeDef = TypedDict(
    "QuickResponseDataProviderTypeDef",
    {
        "content": NotRequired[str],
    },
)
GenerativeReferenceTypeDef = TypedDict(
    "GenerativeReferenceTypeDef",
    {
        "generationId": NotRequired[str],
        "modelId": NotRequired[str],
    },
)
DeleteAssistantAssociationRequestRequestTypeDef = TypedDict(
    "DeleteAssistantAssociationRequestRequestTypeDef",
    {
        "assistantAssociationId": str,
        "assistantId": str,
    },
)
DeleteAssistantRequestRequestTypeDef = TypedDict(
    "DeleteAssistantRequestRequestTypeDef",
    {
        "assistantId": str,
    },
)
DeleteContentAssociationRequestRequestTypeDef = TypedDict(
    "DeleteContentAssociationRequestRequestTypeDef",
    {
        "contentAssociationId": str,
        "contentId": str,
        "knowledgeBaseId": str,
    },
)
DeleteContentRequestRequestTypeDef = TypedDict(
    "DeleteContentRequestRequestTypeDef",
    {
        "contentId": str,
        "knowledgeBaseId": str,
    },
)
DeleteImportJobRequestRequestTypeDef = TypedDict(
    "DeleteImportJobRequestRequestTypeDef",
    {
        "importJobId": str,
        "knowledgeBaseId": str,
    },
)
DeleteKnowledgeBaseRequestRequestTypeDef = TypedDict(
    "DeleteKnowledgeBaseRequestRequestTypeDef",
    {
        "knowledgeBaseId": str,
    },
)
DeleteQuickResponseRequestRequestTypeDef = TypedDict(
    "DeleteQuickResponseRequestRequestTypeDef",
    {
        "knowledgeBaseId": str,
        "quickResponseId": str,
    },
)
HighlightTypeDef = TypedDict(
    "HighlightTypeDef",
    {
        "beginOffsetInclusive": NotRequired[int],
        "endOffsetExclusive": NotRequired[int],
    },
)
FilterTypeDef = TypedDict(
    "FilterTypeDef",
    {
        "field": Literal["NAME"],
        "operator": Literal["EQUALS"],
        "value": str,
    },
)
GetAssistantAssociationRequestRequestTypeDef = TypedDict(
    "GetAssistantAssociationRequestRequestTypeDef",
    {
        "assistantAssociationId": str,
        "assistantId": str,
    },
)
GetAssistantRequestRequestTypeDef = TypedDict(
    "GetAssistantRequestRequestTypeDef",
    {
        "assistantId": str,
    },
)
GetContentAssociationRequestRequestTypeDef = TypedDict(
    "GetContentAssociationRequestRequestTypeDef",
    {
        "contentAssociationId": str,
        "contentId": str,
        "knowledgeBaseId": str,
    },
)
GetContentRequestRequestTypeDef = TypedDict(
    "GetContentRequestRequestTypeDef",
    {
        "contentId": str,
        "knowledgeBaseId": str,
    },
)
GetContentSummaryRequestRequestTypeDef = TypedDict(
    "GetContentSummaryRequestRequestTypeDef",
    {
        "contentId": str,
        "knowledgeBaseId": str,
    },
)
GetImportJobRequestRequestTypeDef = TypedDict(
    "GetImportJobRequestRequestTypeDef",
    {
        "importJobId": str,
        "knowledgeBaseId": str,
    },
)
GetKnowledgeBaseRequestRequestTypeDef = TypedDict(
    "GetKnowledgeBaseRequestRequestTypeDef",
    {
        "knowledgeBaseId": str,
    },
)
GetQuickResponseRequestRequestTypeDef = TypedDict(
    "GetQuickResponseRequestRequestTypeDef",
    {
        "knowledgeBaseId": str,
        "quickResponseId": str,
    },
)
GetRecommendationsRequestRequestTypeDef = TypedDict(
    "GetRecommendationsRequestRequestTypeDef",
    {
        "assistantId": str,
        "sessionId": str,
        "maxResults": NotRequired[int],
        "waitTimeSeconds": NotRequired[int],
    },
)
GetSessionRequestRequestTypeDef = TypedDict(
    "GetSessionRequestRequestTypeDef",
    {
        "assistantId": str,
        "sessionId": str,
    },
)
GroupingConfigurationOutputTypeDef = TypedDict(
    "GroupingConfigurationOutputTypeDef",
    {
        "criteria": NotRequired[str],
        "values": NotRequired[List[str]],
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
ListAssistantAssociationsRequestRequestTypeDef = TypedDict(
    "ListAssistantAssociationsRequestRequestTypeDef",
    {
        "assistantId": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
ListAssistantsRequestRequestTypeDef = TypedDict(
    "ListAssistantsRequestRequestTypeDef",
    {
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
ListContentAssociationsRequestRequestTypeDef = TypedDict(
    "ListContentAssociationsRequestRequestTypeDef",
    {
        "contentId": str,
        "knowledgeBaseId": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
ListContentsRequestRequestTypeDef = TypedDict(
    "ListContentsRequestRequestTypeDef",
    {
        "knowledgeBaseId": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
ListImportJobsRequestRequestTypeDef = TypedDict(
    "ListImportJobsRequestRequestTypeDef",
    {
        "knowledgeBaseId": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
ListKnowledgeBasesRequestRequestTypeDef = TypedDict(
    "ListKnowledgeBasesRequestRequestTypeDef",
    {
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
ListQuickResponsesRequestRequestTypeDef = TypedDict(
    "ListQuickResponsesRequestRequestTypeDef",
    {
        "knowledgeBaseId": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
QuickResponseSummaryTypeDef = TypedDict(
    "QuickResponseSummaryTypeDef",
    {
        "contentType": str,
        "createdTime": datetime,
        "knowledgeBaseArn": str,
        "knowledgeBaseId": str,
        "lastModifiedTime": datetime,
        "name": str,
        "quickResponseArn": str,
        "quickResponseId": str,
        "status": QuickResponseStatusType,
        "channels": NotRequired[List[str]],
        "description": NotRequired[str],
        "isActive": NotRequired[bool],
        "lastModifiedBy": NotRequired[str],
        "tags": NotRequired[Dict[str, str]],
    },
)
ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)
NotifyRecommendationsReceivedErrorTypeDef = TypedDict(
    "NotifyRecommendationsReceivedErrorTypeDef",
    {
        "message": NotRequired[str],
        "recommendationId": NotRequired[str],
    },
)
NotifyRecommendationsReceivedRequestRequestTypeDef = TypedDict(
    "NotifyRecommendationsReceivedRequestRequestTypeDef",
    {
        "assistantId": str,
        "recommendationIds": Sequence[str],
        "sessionId": str,
    },
)
TagConditionTypeDef = TypedDict(
    "TagConditionTypeDef",
    {
        "key": str,
        "value": NotRequired[str],
    },
)
QueryConditionItemTypeDef = TypedDict(
    "QueryConditionItemTypeDef",
    {
        "comparator": Literal["EQUALS"],
        "field": Literal["RESULT_TYPE"],
        "value": str,
    },
)
QueryRecommendationTriggerDataTypeDef = TypedDict(
    "QueryRecommendationTriggerDataTypeDef",
    {
        "text": NotRequired[str],
    },
)
QuickResponseContentProviderTypeDef = TypedDict(
    "QuickResponseContentProviderTypeDef",
    {
        "content": NotRequired[str],
    },
)
QuickResponseFilterFieldTypeDef = TypedDict(
    "QuickResponseFilterFieldTypeDef",
    {
        "name": str,
        "operator": QuickResponseFilterOperatorType,
        "includeNoExistence": NotRequired[bool],
        "values": NotRequired[Sequence[str]],
    },
)
QuickResponseOrderFieldTypeDef = TypedDict(
    "QuickResponseOrderFieldTypeDef",
    {
        "name": str,
        "order": NotRequired[OrderType],
    },
)
QuickResponseQueryFieldTypeDef = TypedDict(
    "QuickResponseQueryFieldTypeDef",
    {
        "name": str,
        "operator": QuickResponseQueryOperatorType,
        "values": Sequence[str],
        "allowFuzziness": NotRequired[bool],
        "priority": NotRequired[PriorityType],
    },
)
RemoveKnowledgeBaseTemplateUriRequestRequestTypeDef = TypedDict(
    "RemoveKnowledgeBaseTemplateUriRequestRequestTypeDef",
    {
        "knowledgeBaseId": str,
    },
)
SessionSummaryTypeDef = TypedDict(
    "SessionSummaryTypeDef",
    {
        "assistantArn": str,
        "assistantId": str,
        "sessionArn": str,
        "sessionId": str,
    },
)
SessionIntegrationConfigurationTypeDef = TypedDict(
    "SessionIntegrationConfigurationTypeDef",
    {
        "topicIntegrationArn": NotRequired[str],
    },
)
StartContentUploadRequestRequestTypeDef = TypedDict(
    "StartContentUploadRequestRequestTypeDef",
    {
        "contentType": str,
        "knowledgeBaseId": str,
        "presignedUrlTimeToLive": NotRequired[int],
    },
)
TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Mapping[str, str],
    },
)
UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)
UpdateContentRequestRequestTypeDef = TypedDict(
    "UpdateContentRequestRequestTypeDef",
    {
        "contentId": str,
        "knowledgeBaseId": str,
        "metadata": NotRequired[Mapping[str, str]],
        "overrideLinkOutUri": NotRequired[str],
        "removeOverrideLinkOutUri": NotRequired[bool],
        "revisionId": NotRequired[str],
        "title": NotRequired[str],
        "uploadId": NotRequired[str],
    },
)
UpdateKnowledgeBaseTemplateUriRequestRequestTypeDef = TypedDict(
    "UpdateKnowledgeBaseTemplateUriRequestRequestTypeDef",
    {
        "knowledgeBaseId": str,
        "templateUri": str,
    },
)
ContentAssociationContentsTypeDef = TypedDict(
    "ContentAssociationContentsTypeDef",
    {
        "amazonConnectGuideAssociation": NotRequired[AmazonConnectGuideAssociationDataTypeDef],
    },
)
SourceConfigurationOutputTypeDef = TypedDict(
    "SourceConfigurationOutputTypeDef",
    {
        "appIntegrations": NotRequired[AppIntegrationsConfigurationOutputTypeDef],
    },
)
SourceConfigurationTypeDef = TypedDict(
    "SourceConfigurationTypeDef",
    {
        "appIntegrations": NotRequired[AppIntegrationsConfigurationTypeDef],
    },
)
CreateAssistantAssociationRequestRequestTypeDef = TypedDict(
    "CreateAssistantAssociationRequestRequestTypeDef",
    {
        "assistantId": str,
        "association": AssistantAssociationInputDataTypeDef,
        "associationType": Literal["KNOWLEDGE_BASE"],
        "clientToken": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
    },
)
AssistantAssociationOutputDataTypeDef = TypedDict(
    "AssistantAssociationOutputDataTypeDef",
    {
        "knowledgeBaseAssociation": NotRequired[KnowledgeBaseAssociationDataTypeDef],
    },
)
AssistantDataTypeDef = TypedDict(
    "AssistantDataTypeDef",
    {
        "assistantArn": str,
        "assistantId": str,
        "name": str,
        "status": AssistantStatusType,
        "type": Literal["AGENT"],
        "capabilityConfiguration": NotRequired[AssistantCapabilityConfigurationTypeDef],
        "description": NotRequired[str],
        "integrationConfiguration": NotRequired[AssistantIntegrationConfigurationTypeDef],
        "serverSideEncryptionConfiguration": NotRequired[ServerSideEncryptionConfigurationTypeDef],
        "tags": NotRequired[Dict[str, str]],
    },
)
AssistantSummaryTypeDef = TypedDict(
    "AssistantSummaryTypeDef",
    {
        "assistantArn": str,
        "assistantId": str,
        "name": str,
        "status": AssistantStatusType,
        "type": Literal["AGENT"],
        "capabilityConfiguration": NotRequired[AssistantCapabilityConfigurationTypeDef],
        "description": NotRequired[str],
        "integrationConfiguration": NotRequired[AssistantIntegrationConfigurationTypeDef],
        "serverSideEncryptionConfiguration": NotRequired[ServerSideEncryptionConfigurationTypeDef],
        "tags": NotRequired[Dict[str, str]],
    },
)
CreateAssistantRequestRequestTypeDef = TypedDict(
    "CreateAssistantRequestRequestTypeDef",
    {
        "name": str,
        "type": Literal["AGENT"],
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
        "serverSideEncryptionConfiguration": NotRequired[ServerSideEncryptionConfigurationTypeDef],
        "tags": NotRequired[Mapping[str, str]],
    },
)
ConfigurationTypeDef = TypedDict(
    "ConfigurationTypeDef",
    {
        "connectConfiguration": NotRequired[ConnectConfigurationTypeDef],
    },
)
GenerativeDataDetailsTypeDef = TypedDict(
    "GenerativeDataDetailsTypeDef",
    {
        "completion": str,
        "rankingData": RankingDataTypeDef,
        "references": List["DataSummaryTypeDef"],
    },
)
ContentFeedbackDataTypeDef = TypedDict(
    "ContentFeedbackDataTypeDef",
    {
        "generativeContentFeedbackData": NotRequired[GenerativeContentFeedbackDataTypeDef],
    },
)
CreateContentResponseTypeDef = TypedDict(
    "CreateContentResponseTypeDef",
    {
        "content": ContentDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetContentResponseTypeDef = TypedDict(
    "GetContentResponseTypeDef",
    {
        "content": ContentDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetContentSummaryResponseTypeDef = TypedDict(
    "GetContentSummaryResponseTypeDef",
    {
        "contentSummary": ContentSummaryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListContentsResponseTypeDef = TypedDict(
    "ListContentsResponseTypeDef",
    {
        "contentSummaries": List[ContentSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
SearchContentResponseTypeDef = TypedDict(
    "SearchContentResponseTypeDef",
    {
        "contentSummaries": List[ContentSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
StartContentUploadResponseTypeDef = TypedDict(
    "StartContentUploadResponseTypeDef",
    {
        "headersToInclude": Dict[str, str],
        "uploadId": str,
        "url": str,
        "urlExpiry": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateContentResponseTypeDef = TypedDict(
    "UpdateContentResponseTypeDef",
    {
        "content": ContentDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateQuickResponseRequestRequestTypeDef = TypedDict(
    "CreateQuickResponseRequestRequestTypeDef",
    {
        "content": QuickResponseDataProviderTypeDef,
        "knowledgeBaseId": str,
        "name": str,
        "channels": NotRequired[Sequence[str]],
        "clientToken": NotRequired[str],
        "contentType": NotRequired[str],
        "description": NotRequired[str],
        "groupingConfiguration": NotRequired[GroupingConfigurationTypeDef],
        "isActive": NotRequired[bool],
        "language": NotRequired[str],
        "shortcutKey": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
    },
)
UpdateQuickResponseRequestRequestTypeDef = TypedDict(
    "UpdateQuickResponseRequestRequestTypeDef",
    {
        "knowledgeBaseId": str,
        "quickResponseId": str,
        "channels": NotRequired[Sequence[str]],
        "content": NotRequired[QuickResponseDataProviderTypeDef],
        "contentType": NotRequired[str],
        "description": NotRequired[str],
        "groupingConfiguration": NotRequired[GroupingConfigurationTypeDef],
        "isActive": NotRequired[bool],
        "language": NotRequired[str],
        "name": NotRequired[str],
        "removeDescription": NotRequired[bool],
        "removeGroupingConfiguration": NotRequired[bool],
        "removeShortcutKey": NotRequired[bool],
        "shortcutKey": NotRequired[str],
    },
)
DataReferenceTypeDef = TypedDict(
    "DataReferenceTypeDef",
    {
        "contentReference": NotRequired[ContentReferenceTypeDef],
        "generativeReference": NotRequired[GenerativeReferenceTypeDef],
    },
)
DocumentTextTypeDef = TypedDict(
    "DocumentTextTypeDef",
    {
        "highlights": NotRequired[List[HighlightTypeDef]],
        "text": NotRequired[str],
    },
)
SearchExpressionTypeDef = TypedDict(
    "SearchExpressionTypeDef",
    {
        "filters": Sequence[FilterTypeDef],
    },
)
ListAssistantAssociationsRequestListAssistantAssociationsPaginateTypeDef = TypedDict(
    "ListAssistantAssociationsRequestListAssistantAssociationsPaginateTypeDef",
    {
        "assistantId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListAssistantsRequestListAssistantsPaginateTypeDef = TypedDict(
    "ListAssistantsRequestListAssistantsPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListContentAssociationsRequestListContentAssociationsPaginateTypeDef = TypedDict(
    "ListContentAssociationsRequestListContentAssociationsPaginateTypeDef",
    {
        "contentId": str,
        "knowledgeBaseId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListContentsRequestListContentsPaginateTypeDef = TypedDict(
    "ListContentsRequestListContentsPaginateTypeDef",
    {
        "knowledgeBaseId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListImportJobsRequestListImportJobsPaginateTypeDef = TypedDict(
    "ListImportJobsRequestListImportJobsPaginateTypeDef",
    {
        "knowledgeBaseId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListKnowledgeBasesRequestListKnowledgeBasesPaginateTypeDef = TypedDict(
    "ListKnowledgeBasesRequestListKnowledgeBasesPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListQuickResponsesRequestListQuickResponsesPaginateTypeDef = TypedDict(
    "ListQuickResponsesRequestListQuickResponsesPaginateTypeDef",
    {
        "knowledgeBaseId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListQuickResponsesResponseTypeDef = TypedDict(
    "ListQuickResponsesResponseTypeDef",
    {
        "nextToken": str,
        "quickResponseSummaries": List[QuickResponseSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
NotifyRecommendationsReceivedResponseTypeDef = TypedDict(
    "NotifyRecommendationsReceivedResponseTypeDef",
    {
        "errors": List[NotifyRecommendationsReceivedErrorTypeDef],
        "recommendationIds": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
OrConditionOutputTypeDef = TypedDict(
    "OrConditionOutputTypeDef",
    {
        "andConditions": NotRequired[List[TagConditionTypeDef]],
        "tagCondition": NotRequired[TagConditionTypeDef],
    },
)
OrConditionTypeDef = TypedDict(
    "OrConditionTypeDef",
    {
        "andConditions": NotRequired[Sequence[TagConditionTypeDef]],
        "tagCondition": NotRequired[TagConditionTypeDef],
    },
)
QueryConditionTypeDef = TypedDict(
    "QueryConditionTypeDef",
    {
        "single": NotRequired[QueryConditionItemTypeDef],
    },
)
RecommendationTriggerDataTypeDef = TypedDict(
    "RecommendationTriggerDataTypeDef",
    {
        "query": NotRequired[QueryRecommendationTriggerDataTypeDef],
    },
)
QuickResponseContentsTypeDef = TypedDict(
    "QuickResponseContentsTypeDef",
    {
        "markdown": NotRequired[QuickResponseContentProviderTypeDef],
        "plainText": NotRequired[QuickResponseContentProviderTypeDef],
    },
)
QuickResponseSearchExpressionTypeDef = TypedDict(
    "QuickResponseSearchExpressionTypeDef",
    {
        "filters": NotRequired[Sequence[QuickResponseFilterFieldTypeDef]],
        "orderOnField": NotRequired[QuickResponseOrderFieldTypeDef],
        "queries": NotRequired[Sequence[QuickResponseQueryFieldTypeDef]],
    },
)
SearchSessionsResponseTypeDef = TypedDict(
    "SearchSessionsResponseTypeDef",
    {
        "nextToken": str,
        "sessionSummaries": List[SessionSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ContentAssociationDataTypeDef = TypedDict(
    "ContentAssociationDataTypeDef",
    {
        "associationData": ContentAssociationContentsTypeDef,
        "associationType": Literal["AMAZON_CONNECT_GUIDE"],
        "contentArn": str,
        "contentAssociationArn": str,
        "contentAssociationId": str,
        "contentId": str,
        "knowledgeBaseArn": str,
        "knowledgeBaseId": str,
        "tags": NotRequired[Dict[str, str]],
    },
)
ContentAssociationSummaryTypeDef = TypedDict(
    "ContentAssociationSummaryTypeDef",
    {
        "associationData": ContentAssociationContentsTypeDef,
        "associationType": Literal["AMAZON_CONNECT_GUIDE"],
        "contentArn": str,
        "contentAssociationArn": str,
        "contentAssociationId": str,
        "contentId": str,
        "knowledgeBaseArn": str,
        "knowledgeBaseId": str,
        "tags": NotRequired[Dict[str, str]],
    },
)
CreateContentAssociationRequestRequestTypeDef = TypedDict(
    "CreateContentAssociationRequestRequestTypeDef",
    {
        "association": ContentAssociationContentsTypeDef,
        "associationType": Literal["AMAZON_CONNECT_GUIDE"],
        "contentId": str,
        "knowledgeBaseId": str,
        "clientToken": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
    },
)
KnowledgeBaseDataTypeDef = TypedDict(
    "KnowledgeBaseDataTypeDef",
    {
        "knowledgeBaseArn": str,
        "knowledgeBaseId": str,
        "knowledgeBaseType": KnowledgeBaseTypeType,
        "name": str,
        "status": KnowledgeBaseStatusType,
        "description": NotRequired[str],
        "lastContentModificationTime": NotRequired[datetime],
        "renderingConfiguration": NotRequired[RenderingConfigurationTypeDef],
        "serverSideEncryptionConfiguration": NotRequired[ServerSideEncryptionConfigurationTypeDef],
        "sourceConfiguration": NotRequired[SourceConfigurationOutputTypeDef],
        "tags": NotRequired[Dict[str, str]],
    },
)
KnowledgeBaseSummaryTypeDef = TypedDict(
    "KnowledgeBaseSummaryTypeDef",
    {
        "knowledgeBaseArn": str,
        "knowledgeBaseId": str,
        "knowledgeBaseType": KnowledgeBaseTypeType,
        "name": str,
        "status": KnowledgeBaseStatusType,
        "description": NotRequired[str],
        "renderingConfiguration": NotRequired[RenderingConfigurationTypeDef],
        "serverSideEncryptionConfiguration": NotRequired[ServerSideEncryptionConfigurationTypeDef],
        "sourceConfiguration": NotRequired[SourceConfigurationOutputTypeDef],
        "tags": NotRequired[Dict[str, str]],
    },
)
CreateKnowledgeBaseRequestRequestTypeDef = TypedDict(
    "CreateKnowledgeBaseRequestRequestTypeDef",
    {
        "knowledgeBaseType": KnowledgeBaseTypeType,
        "name": str,
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
        "renderingConfiguration": NotRequired[RenderingConfigurationTypeDef],
        "serverSideEncryptionConfiguration": NotRequired[ServerSideEncryptionConfigurationTypeDef],
        "sourceConfiguration": NotRequired[SourceConfigurationTypeDef],
        "tags": NotRequired[Mapping[str, str]],
    },
)
AssistantAssociationDataTypeDef = TypedDict(
    "AssistantAssociationDataTypeDef",
    {
        "assistantArn": str,
        "assistantAssociationArn": str,
        "assistantAssociationId": str,
        "assistantId": str,
        "associationData": AssistantAssociationOutputDataTypeDef,
        "associationType": Literal["KNOWLEDGE_BASE"],
        "tags": NotRequired[Dict[str, str]],
    },
)
AssistantAssociationSummaryTypeDef = TypedDict(
    "AssistantAssociationSummaryTypeDef",
    {
        "assistantArn": str,
        "assistantAssociationArn": str,
        "assistantAssociationId": str,
        "assistantId": str,
        "associationData": AssistantAssociationOutputDataTypeDef,
        "associationType": Literal["KNOWLEDGE_BASE"],
        "tags": NotRequired[Dict[str, str]],
    },
)
CreateAssistantResponseTypeDef = TypedDict(
    "CreateAssistantResponseTypeDef",
    {
        "assistant": AssistantDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetAssistantResponseTypeDef = TypedDict(
    "GetAssistantResponseTypeDef",
    {
        "assistant": AssistantDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListAssistantsResponseTypeDef = TypedDict(
    "ListAssistantsResponseTypeDef",
    {
        "assistantSummaries": List[AssistantSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ExternalSourceConfigurationTypeDef = TypedDict(
    "ExternalSourceConfigurationTypeDef",
    {
        "configuration": ConfigurationTypeDef,
        "source": Literal["AMAZON_CONNECT"],
    },
)
PutFeedbackRequestRequestTypeDef = TypedDict(
    "PutFeedbackRequestRequestTypeDef",
    {
        "assistantId": str,
        "contentFeedback": ContentFeedbackDataTypeDef,
        "targetId": str,
        "targetType": TargetTypeType,
    },
)
PutFeedbackResponseTypeDef = TypedDict(
    "PutFeedbackResponseTypeDef",
    {
        "assistantArn": str,
        "assistantId": str,
        "contentFeedback": ContentFeedbackDataTypeDef,
        "targetId": str,
        "targetType": TargetTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DataSummaryTypeDef = TypedDict(
    "DataSummaryTypeDef",
    {
        "details": "DataDetailsTypeDef",
        "reference": DataReferenceTypeDef,
    },
)
DocumentTypeDef = TypedDict(
    "DocumentTypeDef",
    {
        "contentReference": ContentReferenceTypeDef,
        "excerpt": NotRequired[DocumentTextTypeDef],
        "title": NotRequired[DocumentTextTypeDef],
    },
)
TextDataTypeDef = TypedDict(
    "TextDataTypeDef",
    {
        "excerpt": NotRequired[DocumentTextTypeDef],
        "title": NotRequired[DocumentTextTypeDef],
    },
)
SearchContentRequestRequestTypeDef = TypedDict(
    "SearchContentRequestRequestTypeDef",
    {
        "knowledgeBaseId": str,
        "searchExpression": SearchExpressionTypeDef,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
SearchContentRequestSearchContentPaginateTypeDef = TypedDict(
    "SearchContentRequestSearchContentPaginateTypeDef",
    {
        "knowledgeBaseId": str,
        "searchExpression": SearchExpressionTypeDef,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
SearchSessionsRequestRequestTypeDef = TypedDict(
    "SearchSessionsRequestRequestTypeDef",
    {
        "assistantId": str,
        "searchExpression": SearchExpressionTypeDef,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
SearchSessionsRequestSearchSessionsPaginateTypeDef = TypedDict(
    "SearchSessionsRequestSearchSessionsPaginateTypeDef",
    {
        "assistantId": str,
        "searchExpression": SearchExpressionTypeDef,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
TagFilterOutputTypeDef = TypedDict(
    "TagFilterOutputTypeDef",
    {
        "andConditions": NotRequired[List[TagConditionTypeDef]],
        "orConditions": NotRequired[List[OrConditionOutputTypeDef]],
        "tagCondition": NotRequired[TagConditionTypeDef],
    },
)
TagFilterTypeDef = TypedDict(
    "TagFilterTypeDef",
    {
        "andConditions": NotRequired[Sequence[TagConditionTypeDef]],
        "orConditions": NotRequired[Sequence[OrConditionTypeDef]],
        "tagCondition": NotRequired[TagConditionTypeDef],
    },
)
QueryAssistantRequestQueryAssistantPaginateTypeDef = TypedDict(
    "QueryAssistantRequestQueryAssistantPaginateTypeDef",
    {
        "assistantId": str,
        "queryText": str,
        "queryCondition": NotRequired[Sequence[QueryConditionTypeDef]],
        "sessionId": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
QueryAssistantRequestRequestTypeDef = TypedDict(
    "QueryAssistantRequestRequestTypeDef",
    {
        "assistantId": str,
        "queryText": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
        "queryCondition": NotRequired[Sequence[QueryConditionTypeDef]],
        "sessionId": NotRequired[str],
    },
)
RecommendationTriggerTypeDef = TypedDict(
    "RecommendationTriggerTypeDef",
    {
        "data": RecommendationTriggerDataTypeDef,
        "id": str,
        "recommendationIds": List[str],
        "source": RecommendationSourceTypeType,
        "type": RecommendationTriggerTypeType,
    },
)
QuickResponseDataTypeDef = TypedDict(
    "QuickResponseDataTypeDef",
    {
        "contentType": str,
        "createdTime": datetime,
        "knowledgeBaseArn": str,
        "knowledgeBaseId": str,
        "lastModifiedTime": datetime,
        "name": str,
        "quickResponseArn": str,
        "quickResponseId": str,
        "status": QuickResponseStatusType,
        "channels": NotRequired[List[str]],
        "contents": NotRequired[QuickResponseContentsTypeDef],
        "description": NotRequired[str],
        "groupingConfiguration": NotRequired[GroupingConfigurationOutputTypeDef],
        "isActive": NotRequired[bool],
        "language": NotRequired[str],
        "lastModifiedBy": NotRequired[str],
        "shortcutKey": NotRequired[str],
        "tags": NotRequired[Dict[str, str]],
    },
)
QuickResponseSearchResultDataTypeDef = TypedDict(
    "QuickResponseSearchResultDataTypeDef",
    {
        "contentType": str,
        "contents": QuickResponseContentsTypeDef,
        "createdTime": datetime,
        "isActive": bool,
        "knowledgeBaseArn": str,
        "knowledgeBaseId": str,
        "lastModifiedTime": datetime,
        "name": str,
        "quickResponseArn": str,
        "quickResponseId": str,
        "status": QuickResponseStatusType,
        "attributesInterpolated": NotRequired[List[str]],
        "attributesNotInterpolated": NotRequired[List[str]],
        "channels": NotRequired[List[str]],
        "description": NotRequired[str],
        "groupingConfiguration": NotRequired[GroupingConfigurationOutputTypeDef],
        "language": NotRequired[str],
        "lastModifiedBy": NotRequired[str],
        "shortcutKey": NotRequired[str],
        "tags": NotRequired[Dict[str, str]],
    },
)
SearchQuickResponsesRequestRequestTypeDef = TypedDict(
    "SearchQuickResponsesRequestRequestTypeDef",
    {
        "knowledgeBaseId": str,
        "searchExpression": QuickResponseSearchExpressionTypeDef,
        "attributes": NotRequired[Mapping[str, str]],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
SearchQuickResponsesRequestSearchQuickResponsesPaginateTypeDef = TypedDict(
    "SearchQuickResponsesRequestSearchQuickResponsesPaginateTypeDef",
    {
        "knowledgeBaseId": str,
        "searchExpression": QuickResponseSearchExpressionTypeDef,
        "attributes": NotRequired[Mapping[str, str]],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
CreateContentAssociationResponseTypeDef = TypedDict(
    "CreateContentAssociationResponseTypeDef",
    {
        "contentAssociation": ContentAssociationDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetContentAssociationResponseTypeDef = TypedDict(
    "GetContentAssociationResponseTypeDef",
    {
        "contentAssociation": ContentAssociationDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListContentAssociationsResponseTypeDef = TypedDict(
    "ListContentAssociationsResponseTypeDef",
    {
        "contentAssociationSummaries": List[ContentAssociationSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateKnowledgeBaseResponseTypeDef = TypedDict(
    "CreateKnowledgeBaseResponseTypeDef",
    {
        "knowledgeBase": KnowledgeBaseDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetKnowledgeBaseResponseTypeDef = TypedDict(
    "GetKnowledgeBaseResponseTypeDef",
    {
        "knowledgeBase": KnowledgeBaseDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateKnowledgeBaseTemplateUriResponseTypeDef = TypedDict(
    "UpdateKnowledgeBaseTemplateUriResponseTypeDef",
    {
        "knowledgeBase": KnowledgeBaseDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListKnowledgeBasesResponseTypeDef = TypedDict(
    "ListKnowledgeBasesResponseTypeDef",
    {
        "knowledgeBaseSummaries": List[KnowledgeBaseSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateAssistantAssociationResponseTypeDef = TypedDict(
    "CreateAssistantAssociationResponseTypeDef",
    {
        "assistantAssociation": AssistantAssociationDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetAssistantAssociationResponseTypeDef = TypedDict(
    "GetAssistantAssociationResponseTypeDef",
    {
        "assistantAssociation": AssistantAssociationDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListAssistantAssociationsResponseTypeDef = TypedDict(
    "ListAssistantAssociationsResponseTypeDef",
    {
        "assistantAssociationSummaries": List[AssistantAssociationSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ImportJobDataTypeDef = TypedDict(
    "ImportJobDataTypeDef",
    {
        "createdTime": datetime,
        "importJobId": str,
        "importJobType": Literal["QUICK_RESPONSES"],
        "knowledgeBaseArn": str,
        "knowledgeBaseId": str,
        "lastModifiedTime": datetime,
        "status": ImportJobStatusType,
        "uploadId": str,
        "url": str,
        "urlExpiry": datetime,
        "externalSourceConfiguration": NotRequired[ExternalSourceConfigurationTypeDef],
        "failedRecordReport": NotRequired[str],
        "metadata": NotRequired[Dict[str, str]],
    },
)
ImportJobSummaryTypeDef = TypedDict(
    "ImportJobSummaryTypeDef",
    {
        "createdTime": datetime,
        "importJobId": str,
        "importJobType": Literal["QUICK_RESPONSES"],
        "knowledgeBaseArn": str,
        "knowledgeBaseId": str,
        "lastModifiedTime": datetime,
        "status": ImportJobStatusType,
        "uploadId": str,
        "externalSourceConfiguration": NotRequired[ExternalSourceConfigurationTypeDef],
        "metadata": NotRequired[Dict[str, str]],
    },
)
StartImportJobRequestRequestTypeDef = TypedDict(
    "StartImportJobRequestRequestTypeDef",
    {
        "importJobType": Literal["QUICK_RESPONSES"],
        "knowledgeBaseId": str,
        "uploadId": str,
        "clientToken": NotRequired[str],
        "externalSourceConfiguration": NotRequired[ExternalSourceConfigurationTypeDef],
        "metadata": NotRequired[Mapping[str, str]],
    },
)
RecommendationDataTypeDef = TypedDict(
    "RecommendationDataTypeDef",
    {
        "recommendationId": str,
        "data": NotRequired["DataSummaryTypeDef"],
        "document": NotRequired[DocumentTypeDef],
        "relevanceLevel": NotRequired[RelevanceLevelType],
        "relevanceScore": NotRequired[float],
        "type": NotRequired[RecommendationTypeType],
    },
)
ResultDataTypeDef = TypedDict(
    "ResultDataTypeDef",
    {
        "resultId": str,
        "data": NotRequired["DataSummaryTypeDef"],
        "document": NotRequired[DocumentTypeDef],
        "relevanceScore": NotRequired[float],
        "type": NotRequired[QueryResultTypeType],
    },
)
ContentDataDetailsTypeDef = TypedDict(
    "ContentDataDetailsTypeDef",
    {
        "rankingData": RankingDataTypeDef,
        "textData": TextDataTypeDef,
    },
)
SourceContentDataDetailsTypeDef = TypedDict(
    "SourceContentDataDetailsTypeDef",
    {
        "id": str,
        "rankingData": RankingDataTypeDef,
        "textData": TextDataTypeDef,
        "type": Literal["KNOWLEDGE_CONTENT"],
    },
)
SessionDataTypeDef = TypedDict(
    "SessionDataTypeDef",
    {
        "name": str,
        "sessionArn": str,
        "sessionId": str,
        "description": NotRequired[str],
        "integrationConfiguration": NotRequired[SessionIntegrationConfigurationTypeDef],
        "tagFilter": NotRequired[TagFilterOutputTypeDef],
        "tags": NotRequired[Dict[str, str]],
    },
)
CreateSessionRequestRequestTypeDef = TypedDict(
    "CreateSessionRequestRequestTypeDef",
    {
        "assistantId": str,
        "name": str,
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
        "tagFilter": NotRequired[TagFilterTypeDef],
        "tags": NotRequired[Mapping[str, str]],
    },
)
UpdateSessionRequestRequestTypeDef = TypedDict(
    "UpdateSessionRequestRequestTypeDef",
    {
        "assistantId": str,
        "sessionId": str,
        "description": NotRequired[str],
        "tagFilter": NotRequired[TagFilterTypeDef],
    },
)
CreateQuickResponseResponseTypeDef = TypedDict(
    "CreateQuickResponseResponseTypeDef",
    {
        "quickResponse": QuickResponseDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetQuickResponseResponseTypeDef = TypedDict(
    "GetQuickResponseResponseTypeDef",
    {
        "quickResponse": QuickResponseDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateQuickResponseResponseTypeDef = TypedDict(
    "UpdateQuickResponseResponseTypeDef",
    {
        "quickResponse": QuickResponseDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
SearchQuickResponsesResponseTypeDef = TypedDict(
    "SearchQuickResponsesResponseTypeDef",
    {
        "nextToken": str,
        "results": List[QuickResponseSearchResultDataTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetImportJobResponseTypeDef = TypedDict(
    "GetImportJobResponseTypeDef",
    {
        "importJob": ImportJobDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
StartImportJobResponseTypeDef = TypedDict(
    "StartImportJobResponseTypeDef",
    {
        "importJob": ImportJobDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListImportJobsResponseTypeDef = TypedDict(
    "ListImportJobsResponseTypeDef",
    {
        "importJobSummaries": List[ImportJobSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetRecommendationsResponseTypeDef = TypedDict(
    "GetRecommendationsResponseTypeDef",
    {
        "recommendations": List[RecommendationDataTypeDef],
        "triggers": List[RecommendationTriggerTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
QueryAssistantResponseTypeDef = TypedDict(
    "QueryAssistantResponseTypeDef",
    {
        "nextToken": str,
        "results": List[ResultDataTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DataDetailsTypeDef = TypedDict(
    "DataDetailsTypeDef",
    {
        "contentData": NotRequired[ContentDataDetailsTypeDef],
        "generativeData": NotRequired["GenerativeDataDetailsTypeDef"],
        "sourceContentData": NotRequired[SourceContentDataDetailsTypeDef],
    },
)
CreateSessionResponseTypeDef = TypedDict(
    "CreateSessionResponseTypeDef",
    {
        "session": SessionDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetSessionResponseTypeDef = TypedDict(
    "GetSessionResponseTypeDef",
    {
        "session": SessionDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateSessionResponseTypeDef = TypedDict(
    "UpdateSessionResponseTypeDef",
    {
        "session": SessionDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
