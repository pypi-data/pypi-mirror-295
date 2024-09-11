"""
Type annotations for qconnect service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_qconnect.client import QConnectClient

    session = get_session()
    async with session.create_client("qconnect") as client:
        client: QConnectClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import (
    ListAssistantAssociationsPaginator,
    ListAssistantsPaginator,
    ListContentAssociationsPaginator,
    ListContentsPaginator,
    ListImportJobsPaginator,
    ListKnowledgeBasesPaginator,
    ListQuickResponsesPaginator,
    QueryAssistantPaginator,
    SearchContentPaginator,
    SearchQuickResponsesPaginator,
    SearchSessionsPaginator,
)
from .type_defs import (
    CreateAssistantAssociationRequestRequestTypeDef,
    CreateAssistantAssociationResponseTypeDef,
    CreateAssistantRequestRequestTypeDef,
    CreateAssistantResponseTypeDef,
    CreateContentAssociationRequestRequestTypeDef,
    CreateContentAssociationResponseTypeDef,
    CreateContentRequestRequestTypeDef,
    CreateContentResponseTypeDef,
    CreateKnowledgeBaseRequestRequestTypeDef,
    CreateKnowledgeBaseResponseTypeDef,
    CreateQuickResponseRequestRequestTypeDef,
    CreateQuickResponseResponseTypeDef,
    CreateSessionRequestRequestTypeDef,
    CreateSessionResponseTypeDef,
    DeleteAssistantAssociationRequestRequestTypeDef,
    DeleteAssistantRequestRequestTypeDef,
    DeleteContentAssociationRequestRequestTypeDef,
    DeleteContentRequestRequestTypeDef,
    DeleteImportJobRequestRequestTypeDef,
    DeleteKnowledgeBaseRequestRequestTypeDef,
    DeleteQuickResponseRequestRequestTypeDef,
    GetAssistantAssociationRequestRequestTypeDef,
    GetAssistantAssociationResponseTypeDef,
    GetAssistantRequestRequestTypeDef,
    GetAssistantResponseTypeDef,
    GetContentAssociationRequestRequestTypeDef,
    GetContentAssociationResponseTypeDef,
    GetContentRequestRequestTypeDef,
    GetContentResponseTypeDef,
    GetContentSummaryRequestRequestTypeDef,
    GetContentSummaryResponseTypeDef,
    GetImportJobRequestRequestTypeDef,
    GetImportJobResponseTypeDef,
    GetKnowledgeBaseRequestRequestTypeDef,
    GetKnowledgeBaseResponseTypeDef,
    GetQuickResponseRequestRequestTypeDef,
    GetQuickResponseResponseTypeDef,
    GetRecommendationsRequestRequestTypeDef,
    GetRecommendationsResponseTypeDef,
    GetSessionRequestRequestTypeDef,
    GetSessionResponseTypeDef,
    ListAssistantAssociationsRequestRequestTypeDef,
    ListAssistantAssociationsResponseTypeDef,
    ListAssistantsRequestRequestTypeDef,
    ListAssistantsResponseTypeDef,
    ListContentAssociationsRequestRequestTypeDef,
    ListContentAssociationsResponseTypeDef,
    ListContentsRequestRequestTypeDef,
    ListContentsResponseTypeDef,
    ListImportJobsRequestRequestTypeDef,
    ListImportJobsResponseTypeDef,
    ListKnowledgeBasesRequestRequestTypeDef,
    ListKnowledgeBasesResponseTypeDef,
    ListQuickResponsesRequestRequestTypeDef,
    ListQuickResponsesResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    NotifyRecommendationsReceivedRequestRequestTypeDef,
    NotifyRecommendationsReceivedResponseTypeDef,
    PutFeedbackRequestRequestTypeDef,
    PutFeedbackResponseTypeDef,
    QueryAssistantRequestRequestTypeDef,
    QueryAssistantResponseTypeDef,
    RemoveKnowledgeBaseTemplateUriRequestRequestTypeDef,
    SearchContentRequestRequestTypeDef,
    SearchContentResponseTypeDef,
    SearchQuickResponsesRequestRequestTypeDef,
    SearchQuickResponsesResponseTypeDef,
    SearchSessionsRequestRequestTypeDef,
    SearchSessionsResponseTypeDef,
    StartContentUploadRequestRequestTypeDef,
    StartContentUploadResponseTypeDef,
    StartImportJobRequestRequestTypeDef,
    StartImportJobResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateContentRequestRequestTypeDef,
    UpdateContentResponseTypeDef,
    UpdateKnowledgeBaseTemplateUriRequestRequestTypeDef,
    UpdateKnowledgeBaseTemplateUriResponseTypeDef,
    UpdateQuickResponseRequestRequestTypeDef,
    UpdateQuickResponseResponseTypeDef,
    UpdateSessionRequestRequestTypeDef,
    UpdateSessionResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("QConnectClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    PreconditionFailedException: Type[BotocoreClientError]
    RequestTimeoutException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class QConnectClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        QConnectClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#close)
        """

    async def create_assistant(
        self, **kwargs: Unpack[CreateAssistantRequestRequestTypeDef]
    ) -> CreateAssistantResponseTypeDef:
        """
        Creates an Amazon Q in Connect assistant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.create_assistant)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#create_assistant)
        """

    async def create_assistant_association(
        self, **kwargs: Unpack[CreateAssistantAssociationRequestRequestTypeDef]
    ) -> CreateAssistantAssociationResponseTypeDef:
        """
        Creates an association between an Amazon Q in Connect assistant and another
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.create_assistant_association)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#create_assistant_association)
        """

    async def create_content(
        self, **kwargs: Unpack[CreateContentRequestRequestTypeDef]
    ) -> CreateContentResponseTypeDef:
        """
        Creates Amazon Q in Connect content.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.create_content)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#create_content)
        """

    async def create_content_association(
        self, **kwargs: Unpack[CreateContentAssociationRequestRequestTypeDef]
    ) -> CreateContentAssociationResponseTypeDef:
        """
        Creates an association between a content resource in a knowledge base and
        [step-by-step
        guides](https://docs.aws.amazon.com/connect/latest/adminguide/step-by-step-guided-experiences.html).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.create_content_association)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#create_content_association)
        """

    async def create_knowledge_base(
        self, **kwargs: Unpack[CreateKnowledgeBaseRequestRequestTypeDef]
    ) -> CreateKnowledgeBaseResponseTypeDef:
        """
        Creates a knowledge base.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.create_knowledge_base)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#create_knowledge_base)
        """

    async def create_quick_response(
        self, **kwargs: Unpack[CreateQuickResponseRequestRequestTypeDef]
    ) -> CreateQuickResponseResponseTypeDef:
        """
        Creates an Amazon Q in Connect quick response.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.create_quick_response)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#create_quick_response)
        """

    async def create_session(
        self, **kwargs: Unpack[CreateSessionRequestRequestTypeDef]
    ) -> CreateSessionResponseTypeDef:
        """
        Creates a session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.create_session)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#create_session)
        """

    async def delete_assistant(
        self, **kwargs: Unpack[DeleteAssistantRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an assistant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.delete_assistant)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#delete_assistant)
        """

    async def delete_assistant_association(
        self, **kwargs: Unpack[DeleteAssistantAssociationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an assistant association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.delete_assistant_association)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#delete_assistant_association)
        """

    async def delete_content(
        self, **kwargs: Unpack[DeleteContentRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the content.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.delete_content)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#delete_content)
        """

    async def delete_content_association(
        self, **kwargs: Unpack[DeleteContentAssociationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the content association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.delete_content_association)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#delete_content_association)
        """

    async def delete_import_job(
        self, **kwargs: Unpack[DeleteImportJobRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the quick response import job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.delete_import_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#delete_import_job)
        """

    async def delete_knowledge_base(
        self, **kwargs: Unpack[DeleteKnowledgeBaseRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the knowledge base.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.delete_knowledge_base)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#delete_knowledge_base)
        """

    async def delete_quick_response(
        self, **kwargs: Unpack[DeleteQuickResponseRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a quick response.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.delete_quick_response)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#delete_quick_response)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#generate_presigned_url)
        """

    async def get_assistant(
        self, **kwargs: Unpack[GetAssistantRequestRequestTypeDef]
    ) -> GetAssistantResponseTypeDef:
        """
        Retrieves information about an assistant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.get_assistant)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#get_assistant)
        """

    async def get_assistant_association(
        self, **kwargs: Unpack[GetAssistantAssociationRequestRequestTypeDef]
    ) -> GetAssistantAssociationResponseTypeDef:
        """
        Retrieves information about an assistant association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.get_assistant_association)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#get_assistant_association)
        """

    async def get_content(
        self, **kwargs: Unpack[GetContentRequestRequestTypeDef]
    ) -> GetContentResponseTypeDef:
        """
        Retrieves content, including a pre-signed URL to download the content.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.get_content)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#get_content)
        """

    async def get_content_association(
        self, **kwargs: Unpack[GetContentAssociationRequestRequestTypeDef]
    ) -> GetContentAssociationResponseTypeDef:
        """
        Returns the content association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.get_content_association)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#get_content_association)
        """

    async def get_content_summary(
        self, **kwargs: Unpack[GetContentSummaryRequestRequestTypeDef]
    ) -> GetContentSummaryResponseTypeDef:
        """
        Retrieves summary information about the content.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.get_content_summary)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#get_content_summary)
        """

    async def get_import_job(
        self, **kwargs: Unpack[GetImportJobRequestRequestTypeDef]
    ) -> GetImportJobResponseTypeDef:
        """
        Retrieves the started import job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.get_import_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#get_import_job)
        """

    async def get_knowledge_base(
        self, **kwargs: Unpack[GetKnowledgeBaseRequestRequestTypeDef]
    ) -> GetKnowledgeBaseResponseTypeDef:
        """
        Retrieves information about the knowledge base.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.get_knowledge_base)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#get_knowledge_base)
        """

    async def get_quick_response(
        self, **kwargs: Unpack[GetQuickResponseRequestRequestTypeDef]
    ) -> GetQuickResponseResponseTypeDef:
        """
        Retrieves the quick response.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.get_quick_response)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#get_quick_response)
        """

    async def get_recommendations(
        self, **kwargs: Unpack[GetRecommendationsRequestRequestTypeDef]
    ) -> GetRecommendationsResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.get_recommendations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#get_recommendations)
        """

    async def get_session(
        self, **kwargs: Unpack[GetSessionRequestRequestTypeDef]
    ) -> GetSessionResponseTypeDef:
        """
        Retrieves information for a specified session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.get_session)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#get_session)
        """

    async def list_assistant_associations(
        self, **kwargs: Unpack[ListAssistantAssociationsRequestRequestTypeDef]
    ) -> ListAssistantAssociationsResponseTypeDef:
        """
        Lists information about assistant associations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.list_assistant_associations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#list_assistant_associations)
        """

    async def list_assistants(
        self, **kwargs: Unpack[ListAssistantsRequestRequestTypeDef]
    ) -> ListAssistantsResponseTypeDef:
        """
        Lists information about assistants.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.list_assistants)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#list_assistants)
        """

    async def list_content_associations(
        self, **kwargs: Unpack[ListContentAssociationsRequestRequestTypeDef]
    ) -> ListContentAssociationsResponseTypeDef:
        """
        Lists the content associations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.list_content_associations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#list_content_associations)
        """

    async def list_contents(
        self, **kwargs: Unpack[ListContentsRequestRequestTypeDef]
    ) -> ListContentsResponseTypeDef:
        """
        Lists the content.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.list_contents)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#list_contents)
        """

    async def list_import_jobs(
        self, **kwargs: Unpack[ListImportJobsRequestRequestTypeDef]
    ) -> ListImportJobsResponseTypeDef:
        """
        Lists information about import jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.list_import_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#list_import_jobs)
        """

    async def list_knowledge_bases(
        self, **kwargs: Unpack[ListKnowledgeBasesRequestRequestTypeDef]
    ) -> ListKnowledgeBasesResponseTypeDef:
        """
        Lists the knowledge bases.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.list_knowledge_bases)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#list_knowledge_bases)
        """

    async def list_quick_responses(
        self, **kwargs: Unpack[ListQuickResponsesRequestRequestTypeDef]
    ) -> ListQuickResponsesResponseTypeDef:
        """
        Lists information about quick response.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.list_quick_responses)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#list_quick_responses)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#list_tags_for_resource)
        """

    async def notify_recommendations_received(
        self, **kwargs: Unpack[NotifyRecommendationsReceivedRequestRequestTypeDef]
    ) -> NotifyRecommendationsReceivedResponseTypeDef:
        """
        Removes the specified recommendations from the specified assistant's queue of
        newly available
        recommendations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.notify_recommendations_received)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#notify_recommendations_received)
        """

    async def put_feedback(
        self, **kwargs: Unpack[PutFeedbackRequestRequestTypeDef]
    ) -> PutFeedbackResponseTypeDef:
        """
        Provides feedback against the specified assistant for the specified target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.put_feedback)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#put_feedback)
        """

    async def query_assistant(
        self, **kwargs: Unpack[QueryAssistantRequestRequestTypeDef]
    ) -> QueryAssistantResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.query_assistant)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#query_assistant)
        """

    async def remove_knowledge_base_template_uri(
        self, **kwargs: Unpack[RemoveKnowledgeBaseTemplateUriRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes a URI template from a knowledge base.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.remove_knowledge_base_template_uri)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#remove_knowledge_base_template_uri)
        """

    async def search_content(
        self, **kwargs: Unpack[SearchContentRequestRequestTypeDef]
    ) -> SearchContentResponseTypeDef:
        """
        Searches for content in a specified knowledge base.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.search_content)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#search_content)
        """

    async def search_quick_responses(
        self, **kwargs: Unpack[SearchQuickResponsesRequestRequestTypeDef]
    ) -> SearchQuickResponsesResponseTypeDef:
        """
        Searches existing Amazon Q in Connect quick responses in an Amazon Q in Connect
        knowledge
        base.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.search_quick_responses)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#search_quick_responses)
        """

    async def search_sessions(
        self, **kwargs: Unpack[SearchSessionsRequestRequestTypeDef]
    ) -> SearchSessionsResponseTypeDef:
        """
        Searches for sessions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.search_sessions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#search_sessions)
        """

    async def start_content_upload(
        self, **kwargs: Unpack[StartContentUploadRequestRequestTypeDef]
    ) -> StartContentUploadResponseTypeDef:
        """
        Get a URL to upload content to a knowledge base.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.start_content_upload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#start_content_upload)
        """

    async def start_import_job(
        self, **kwargs: Unpack[StartImportJobRequestRequestTypeDef]
    ) -> StartImportJobResponseTypeDef:
        """
        Start an asynchronous job to import Amazon Q in Connect resources from an
        uploaded source
        file.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.start_import_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#start_import_job)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Adds the specified tags to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes the specified tags from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#untag_resource)
        """

    async def update_content(
        self, **kwargs: Unpack[UpdateContentRequestRequestTypeDef]
    ) -> UpdateContentResponseTypeDef:
        """
        Updates information about the content.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.update_content)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#update_content)
        """

    async def update_knowledge_base_template_uri(
        self, **kwargs: Unpack[UpdateKnowledgeBaseTemplateUriRequestRequestTypeDef]
    ) -> UpdateKnowledgeBaseTemplateUriResponseTypeDef:
        """
        Updates the template URI of a knowledge base.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.update_knowledge_base_template_uri)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#update_knowledge_base_template_uri)
        """

    async def update_quick_response(
        self, **kwargs: Unpack[UpdateQuickResponseRequestRequestTypeDef]
    ) -> UpdateQuickResponseResponseTypeDef:
        """
        Updates an existing Amazon Q in Connect quick response.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.update_quick_response)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#update_quick_response)
        """

    async def update_session(
        self, **kwargs: Unpack[UpdateSessionRequestRequestTypeDef]
    ) -> UpdateSessionResponseTypeDef:
        """
        Updates a session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.update_session)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#update_session)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_assistant_associations"]
    ) -> ListAssistantAssociationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_assistants"]) -> ListAssistantsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_content_associations"]
    ) -> ListContentAssociationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_contents"]) -> ListContentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_import_jobs"]) -> ListImportJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_knowledge_bases"]
    ) -> ListKnowledgeBasesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_quick_responses"]
    ) -> ListQuickResponsesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["query_assistant"]) -> QueryAssistantPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["search_content"]) -> SearchContentPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["search_quick_responses"]
    ) -> SearchQuickResponsesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["search_sessions"]) -> SearchSessionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/#get_paginator)
        """

    async def __aenter__(self) -> "QConnectClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qconnect.html#QConnect.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qconnect/client/)
        """
