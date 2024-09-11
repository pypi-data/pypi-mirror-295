"""
Type annotations for bedrock-agent-runtime service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent_runtime/type_defs/)

Usage::

    ```python
    from types_aiobotocore_bedrock_agent_runtime.type_defs import AccessDeniedExceptionTypeDef

    data: AccessDeniedExceptionTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from aiobotocore.eventstream import AioEventStream
from aiobotocore.response import StreamingBody

from .literals import (
    ActionInvocationTypeType,
    ConfirmationStateType,
    CreationModeType,
    ExecutionTypeType,
    ExternalSourceTypeType,
    FileSourceTypeType,
    FileUseCaseType,
    GuadrailActionType,
    GuardrailActionType,
    GuardrailContentFilterConfidenceType,
    GuardrailContentFilterTypeType,
    GuardrailPiiEntityTypeType,
    GuardrailSensitiveInformationPolicyActionType,
    InvocationTypeType,
    NodeTypeType,
    PromptTypeType,
    ResponseStateType,
    RetrievalResultLocationTypeType,
    RetrieveAndGenerateTypeType,
    SearchTypeType,
    SourceType,
    TypeType,
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
    "AccessDeniedExceptionTypeDef",
    "ParameterTypeDef",
    "ActionGroupInvocationOutputTypeDef",
    "ApiParameterTypeDef",
    "ContentBodyTypeDef",
    "BadGatewayExceptionTypeDef",
    "BlobTypeDef",
    "CodeInterpreterInvocationInputTypeDef",
    "CodeInterpreterInvocationOutputTypeDef",
    "ConflictExceptionTypeDef",
    "DeleteAgentMemoryRequestRequestTypeDef",
    "DependencyFailedExceptionTypeDef",
    "S3ObjectDocTypeDef",
    "GuardrailConfigurationTypeDef",
    "PromptTemplateTypeDef",
    "FailureTraceTypeDef",
    "OutputFileTypeDef",
    "S3ObjectFileTypeDef",
    "FilterAttributeTypeDef",
    "FinalResponseTypeDef",
    "FlowCompletionEventTypeDef",
    "FlowInputContentTypeDef",
    "FlowOutputContentTypeDef",
    "InternalServerExceptionTypeDef",
    "ResourceNotFoundExceptionTypeDef",
    "ServiceQuotaExceededExceptionTypeDef",
    "ThrottlingExceptionTypeDef",
    "ValidationExceptionTypeDef",
    "FunctionParameterTypeDef",
    "PaginatorConfigTypeDef",
    "GetAgentMemoryRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "GuardrailContentFilterTypeDef",
    "GuardrailCustomWordTypeDef",
    "GuardrailManagedWordTypeDef",
    "GuardrailPiiEntityFilterTypeDef",
    "GuardrailRegexFilterTypeDef",
    "GuardrailTopicTypeDef",
    "TextInferenceConfigTypeDef",
    "InferenceConfigurationTypeDef",
    "KnowledgeBaseLookupInputTypeDef",
    "KnowledgeBaseQueryTypeDef",
    "KnowledgeBaseVectorSearchConfigurationTypeDef",
    "RetrievalResultContentTypeDef",
    "MemorySessionSummaryTypeDef",
    "UsageTypeDef",
    "RepromptResponseTypeDef",
    "QueryTransformationConfigurationTypeDef",
    "RawResponseTypeDef",
    "RationaleTypeDef",
    "PostProcessingParsedResponseTypeDef",
    "PreProcessingParsedResponseTypeDef",
    "RetrievalResultConfluenceLocationTypeDef",
    "RetrievalResultS3LocationTypeDef",
    "RetrievalResultSalesforceLocationTypeDef",
    "RetrievalResultSharePointLocationTypeDef",
    "RetrievalResultWebLocationTypeDef",
    "RetrieveAndGenerateInputTypeDef",
    "RetrieveAndGenerateOutputTypeDef",
    "RetrieveAndGenerateSessionConfigurationTypeDef",
    "SpanTypeDef",
    "PropertyParametersTypeDef",
    "RequestBodyTypeDef",
    "ApiResultTypeDef",
    "FunctionResultTypeDef",
    "ByteContentDocTypeDef",
    "ByteContentFileTypeDef",
    "FilePartTypeDef",
    "RetrievalFilterTypeDef",
    "FlowInputTypeDef",
    "FlowOutputEventTypeDef",
    "FunctionInvocationInputTypeDef",
    "GetAgentMemoryRequestGetAgentMemoryPaginateTypeDef",
    "GuardrailContentPolicyAssessmentTypeDef",
    "GuardrailWordPolicyAssessmentTypeDef",
    "GuardrailSensitiveInformationPolicyAssessmentTypeDef",
    "GuardrailTopicPolicyAssessmentTypeDef",
    "InferenceConfigTypeDef",
    "ModelInvocationInputTypeDef",
    "KnowledgeBaseRetrievalConfigurationTypeDef",
    "MemoryTypeDef",
    "MetadataTypeDef",
    "OrchestrationConfigurationTypeDef",
    "PostProcessingModelInvocationOutputTypeDef",
    "PreProcessingModelInvocationOutputTypeDef",
    "RetrievalResultLocationTypeDef",
    "TextResponsePartTypeDef",
    "ApiRequestBodyTypeDef",
    "ActionGroupInvocationInputTypeDef",
    "InvocationResultMemberTypeDef",
    "ExternalSourceTypeDef",
    "FileSourceTypeDef",
    "InvokeFlowRequestRequestTypeDef",
    "FlowResponseStreamTypeDef",
    "GuardrailAssessmentTypeDef",
    "ExternalSourcesGenerationConfigurationTypeDef",
    "GenerationConfigurationTypeDef",
    "KnowledgeBaseConfigurationTypeDef",
    "RetrieveRequestRequestTypeDef",
    "RetrieveRequestRetrievePaginateTypeDef",
    "GetAgentMemoryResponseTypeDef",
    "OrchestrationModelInvocationOutputTypeDef",
    "PostProcessingTraceTypeDef",
    "PreProcessingTraceTypeDef",
    "KnowledgeBaseRetrievalResultTypeDef",
    "RetrievedReferenceTypeDef",
    "GeneratedResponsePartTypeDef",
    "ApiInvocationInputTypeDef",
    "InvocationInputTypeDef",
    "InputFileTypeDef",
    "InvokeFlowResponseTypeDef",
    "GuardrailTraceTypeDef",
    "ExternalSourcesRetrieveAndGenerateConfigurationTypeDef",
    "KnowledgeBaseRetrieveAndGenerateConfigurationTypeDef",
    "RetrieveResponseTypeDef",
    "KnowledgeBaseLookupOutputTypeDef",
    "CitationTypeDef",
    "InvocationInputMemberTypeDef",
    "SessionStateTypeDef",
    "RetrieveAndGenerateConfigurationTypeDef",
    "ObservationTypeDef",
    "AttributionTypeDef",
    "RetrieveAndGenerateResponseTypeDef",
    "ReturnControlPayloadTypeDef",
    "InvokeAgentRequestRequestTypeDef",
    "RetrieveAndGenerateRequestRequestTypeDef",
    "OrchestrationTraceTypeDef",
    "PayloadPartTypeDef",
    "TraceTypeDef",
    "TracePartTypeDef",
    "ResponseStreamTypeDef",
    "InvokeAgentResponseTypeDef",
)

AccessDeniedExceptionTypeDef = TypedDict(
    "AccessDeniedExceptionTypeDef",
    {
        "message": NotRequired[str],
    },
)
ParameterTypeDef = TypedDict(
    "ParameterTypeDef",
    {
        "name": NotRequired[str],
        "type": NotRequired[str],
        "value": NotRequired[str],
    },
)
ActionGroupInvocationOutputTypeDef = TypedDict(
    "ActionGroupInvocationOutputTypeDef",
    {
        "text": NotRequired[str],
    },
)
ApiParameterTypeDef = TypedDict(
    "ApiParameterTypeDef",
    {
        "name": NotRequired[str],
        "type": NotRequired[str],
        "value": NotRequired[str],
    },
)
ContentBodyTypeDef = TypedDict(
    "ContentBodyTypeDef",
    {
        "body": NotRequired[str],
    },
)
BadGatewayExceptionTypeDef = TypedDict(
    "BadGatewayExceptionTypeDef",
    {
        "message": NotRequired[str],
        "resourceName": NotRequired[str],
    },
)
BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]
CodeInterpreterInvocationInputTypeDef = TypedDict(
    "CodeInterpreterInvocationInputTypeDef",
    {
        "code": NotRequired[str],
        "files": NotRequired[List[str]],
    },
)
CodeInterpreterInvocationOutputTypeDef = TypedDict(
    "CodeInterpreterInvocationOutputTypeDef",
    {
        "executionError": NotRequired[str],
        "executionOutput": NotRequired[str],
        "executionTimeout": NotRequired[bool],
        "files": NotRequired[List[str]],
    },
)
ConflictExceptionTypeDef = TypedDict(
    "ConflictExceptionTypeDef",
    {
        "message": NotRequired[str],
    },
)
DeleteAgentMemoryRequestRequestTypeDef = TypedDict(
    "DeleteAgentMemoryRequestRequestTypeDef",
    {
        "agentAliasId": str,
        "agentId": str,
        "memoryId": NotRequired[str],
    },
)
DependencyFailedExceptionTypeDef = TypedDict(
    "DependencyFailedExceptionTypeDef",
    {
        "message": NotRequired[str],
        "resourceName": NotRequired[str],
    },
)
S3ObjectDocTypeDef = TypedDict(
    "S3ObjectDocTypeDef",
    {
        "uri": str,
    },
)
GuardrailConfigurationTypeDef = TypedDict(
    "GuardrailConfigurationTypeDef",
    {
        "guardrailId": str,
        "guardrailVersion": str,
    },
)
PromptTemplateTypeDef = TypedDict(
    "PromptTemplateTypeDef",
    {
        "textPromptTemplate": NotRequired[str],
    },
)
FailureTraceTypeDef = TypedDict(
    "FailureTraceTypeDef",
    {
        "failureReason": NotRequired[str],
        "traceId": NotRequired[str],
    },
)
OutputFileTypeDef = TypedDict(
    "OutputFileTypeDef",
    {
        "bytes": NotRequired[bytes],
        "name": NotRequired[str],
        "type": NotRequired[str],
    },
)
S3ObjectFileTypeDef = TypedDict(
    "S3ObjectFileTypeDef",
    {
        "uri": str,
    },
)
FilterAttributeTypeDef = TypedDict(
    "FilterAttributeTypeDef",
    {
        "key": str,
        "value": Mapping[str, Any],
    },
)
FinalResponseTypeDef = TypedDict(
    "FinalResponseTypeDef",
    {
        "text": NotRequired[str],
    },
)
FlowCompletionEventTypeDef = TypedDict(
    "FlowCompletionEventTypeDef",
    {
        "completionReason": Literal["SUCCESS"],
    },
)
FlowInputContentTypeDef = TypedDict(
    "FlowInputContentTypeDef",
    {
        "document": NotRequired[Mapping[str, Any]],
    },
)
FlowOutputContentTypeDef = TypedDict(
    "FlowOutputContentTypeDef",
    {
        "document": NotRequired[Dict[str, Any]],
    },
)
InternalServerExceptionTypeDef = TypedDict(
    "InternalServerExceptionTypeDef",
    {
        "message": NotRequired[str],
    },
)
ResourceNotFoundExceptionTypeDef = TypedDict(
    "ResourceNotFoundExceptionTypeDef",
    {
        "message": NotRequired[str],
    },
)
ServiceQuotaExceededExceptionTypeDef = TypedDict(
    "ServiceQuotaExceededExceptionTypeDef",
    {
        "message": NotRequired[str],
    },
)
ThrottlingExceptionTypeDef = TypedDict(
    "ThrottlingExceptionTypeDef",
    {
        "message": NotRequired[str],
    },
)
ValidationExceptionTypeDef = TypedDict(
    "ValidationExceptionTypeDef",
    {
        "message": NotRequired[str],
    },
)
FunctionParameterTypeDef = TypedDict(
    "FunctionParameterTypeDef",
    {
        "name": NotRequired[str],
        "type": NotRequired[str],
        "value": NotRequired[str],
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
GetAgentMemoryRequestRequestTypeDef = TypedDict(
    "GetAgentMemoryRequestRequestTypeDef",
    {
        "agentAliasId": str,
        "agentId": str,
        "memoryId": str,
        "memoryType": Literal["SESSION_SUMMARY"],
        "maxItems": NotRequired[int],
        "nextToken": NotRequired[str],
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
GuardrailContentFilterTypeDef = TypedDict(
    "GuardrailContentFilterTypeDef",
    {
        "action": NotRequired[Literal["BLOCKED"]],
        "confidence": NotRequired[GuardrailContentFilterConfidenceType],
        "type": NotRequired[GuardrailContentFilterTypeType],
    },
)
GuardrailCustomWordTypeDef = TypedDict(
    "GuardrailCustomWordTypeDef",
    {
        "action": NotRequired[Literal["BLOCKED"]],
        "match": NotRequired[str],
    },
)
GuardrailManagedWordTypeDef = TypedDict(
    "GuardrailManagedWordTypeDef",
    {
        "action": NotRequired[Literal["BLOCKED"]],
        "match": NotRequired[str],
        "type": NotRequired[Literal["PROFANITY"]],
    },
)
GuardrailPiiEntityFilterTypeDef = TypedDict(
    "GuardrailPiiEntityFilterTypeDef",
    {
        "action": NotRequired[GuardrailSensitiveInformationPolicyActionType],
        "match": NotRequired[str],
        "type": NotRequired[GuardrailPiiEntityTypeType],
    },
)
GuardrailRegexFilterTypeDef = TypedDict(
    "GuardrailRegexFilterTypeDef",
    {
        "action": NotRequired[GuardrailSensitiveInformationPolicyActionType],
        "match": NotRequired[str],
        "name": NotRequired[str],
        "regex": NotRequired[str],
    },
)
GuardrailTopicTypeDef = TypedDict(
    "GuardrailTopicTypeDef",
    {
        "action": NotRequired[Literal["BLOCKED"]],
        "name": NotRequired[str],
        "type": NotRequired[Literal["DENY"]],
    },
)
TextInferenceConfigTypeDef = TypedDict(
    "TextInferenceConfigTypeDef",
    {
        "maxTokens": NotRequired[int],
        "stopSequences": NotRequired[Sequence[str]],
        "temperature": NotRequired[float],
        "topP": NotRequired[float],
    },
)
InferenceConfigurationTypeDef = TypedDict(
    "InferenceConfigurationTypeDef",
    {
        "maximumLength": NotRequired[int],
        "stopSequences": NotRequired[List[str]],
        "temperature": NotRequired[float],
        "topK": NotRequired[int],
        "topP": NotRequired[float],
    },
)
KnowledgeBaseLookupInputTypeDef = TypedDict(
    "KnowledgeBaseLookupInputTypeDef",
    {
        "knowledgeBaseId": NotRequired[str],
        "text": NotRequired[str],
    },
)
KnowledgeBaseQueryTypeDef = TypedDict(
    "KnowledgeBaseQueryTypeDef",
    {
        "text": str,
    },
)
KnowledgeBaseVectorSearchConfigurationTypeDef = TypedDict(
    "KnowledgeBaseVectorSearchConfigurationTypeDef",
    {
        "filter": NotRequired["RetrievalFilterTypeDef"],
        "numberOfResults": NotRequired[int],
        "overrideSearchType": NotRequired[SearchTypeType],
    },
)
RetrievalResultContentTypeDef = TypedDict(
    "RetrievalResultContentTypeDef",
    {
        "text": str,
    },
)
MemorySessionSummaryTypeDef = TypedDict(
    "MemorySessionSummaryTypeDef",
    {
        "memoryId": NotRequired[str],
        "sessionExpiryTime": NotRequired[datetime],
        "sessionId": NotRequired[str],
        "sessionStartTime": NotRequired[datetime],
        "summaryText": NotRequired[str],
    },
)
UsageTypeDef = TypedDict(
    "UsageTypeDef",
    {
        "inputTokens": NotRequired[int],
        "outputTokens": NotRequired[int],
    },
)
RepromptResponseTypeDef = TypedDict(
    "RepromptResponseTypeDef",
    {
        "source": NotRequired[SourceType],
        "text": NotRequired[str],
    },
)
QueryTransformationConfigurationTypeDef = TypedDict(
    "QueryTransformationConfigurationTypeDef",
    {
        "type": Literal["QUERY_DECOMPOSITION"],
    },
)
RawResponseTypeDef = TypedDict(
    "RawResponseTypeDef",
    {
        "content": NotRequired[str],
    },
)
RationaleTypeDef = TypedDict(
    "RationaleTypeDef",
    {
        "text": NotRequired[str],
        "traceId": NotRequired[str],
    },
)
PostProcessingParsedResponseTypeDef = TypedDict(
    "PostProcessingParsedResponseTypeDef",
    {
        "text": NotRequired[str],
    },
)
PreProcessingParsedResponseTypeDef = TypedDict(
    "PreProcessingParsedResponseTypeDef",
    {
        "isValid": NotRequired[bool],
        "rationale": NotRequired[str],
    },
)
RetrievalResultConfluenceLocationTypeDef = TypedDict(
    "RetrievalResultConfluenceLocationTypeDef",
    {
        "url": NotRequired[str],
    },
)
RetrievalResultS3LocationTypeDef = TypedDict(
    "RetrievalResultS3LocationTypeDef",
    {
        "uri": NotRequired[str],
    },
)
RetrievalResultSalesforceLocationTypeDef = TypedDict(
    "RetrievalResultSalesforceLocationTypeDef",
    {
        "url": NotRequired[str],
    },
)
RetrievalResultSharePointLocationTypeDef = TypedDict(
    "RetrievalResultSharePointLocationTypeDef",
    {
        "url": NotRequired[str],
    },
)
RetrievalResultWebLocationTypeDef = TypedDict(
    "RetrievalResultWebLocationTypeDef",
    {
        "url": NotRequired[str],
    },
)
RetrieveAndGenerateInputTypeDef = TypedDict(
    "RetrieveAndGenerateInputTypeDef",
    {
        "text": str,
    },
)
RetrieveAndGenerateOutputTypeDef = TypedDict(
    "RetrieveAndGenerateOutputTypeDef",
    {
        "text": str,
    },
)
RetrieveAndGenerateSessionConfigurationTypeDef = TypedDict(
    "RetrieveAndGenerateSessionConfigurationTypeDef",
    {
        "kmsKeyArn": str,
    },
)
SpanTypeDef = TypedDict(
    "SpanTypeDef",
    {
        "end": NotRequired[int],
        "start": NotRequired[int],
    },
)
PropertyParametersTypeDef = TypedDict(
    "PropertyParametersTypeDef",
    {
        "properties": NotRequired[List[ParameterTypeDef]],
    },
)
RequestBodyTypeDef = TypedDict(
    "RequestBodyTypeDef",
    {
        "content": NotRequired[Dict[str, List[ParameterTypeDef]]],
    },
)
ApiResultTypeDef = TypedDict(
    "ApiResultTypeDef",
    {
        "actionGroup": str,
        "apiPath": NotRequired[str],
        "confirmationState": NotRequired[ConfirmationStateType],
        "httpMethod": NotRequired[str],
        "httpStatusCode": NotRequired[int],
        "responseBody": NotRequired[Mapping[str, ContentBodyTypeDef]],
        "responseState": NotRequired[ResponseStateType],
    },
)
FunctionResultTypeDef = TypedDict(
    "FunctionResultTypeDef",
    {
        "actionGroup": str,
        "confirmationState": NotRequired[ConfirmationStateType],
        "function": NotRequired[str],
        "responseBody": NotRequired[Mapping[str, ContentBodyTypeDef]],
        "responseState": NotRequired[ResponseStateType],
    },
)
ByteContentDocTypeDef = TypedDict(
    "ByteContentDocTypeDef",
    {
        "contentType": str,
        "data": BlobTypeDef,
        "identifier": str,
    },
)
ByteContentFileTypeDef = TypedDict(
    "ByteContentFileTypeDef",
    {
        "data": BlobTypeDef,
        "mediaType": str,
    },
)
FilePartTypeDef = TypedDict(
    "FilePartTypeDef",
    {
        "files": NotRequired[List[OutputFileTypeDef]],
    },
)
RetrievalFilterTypeDef = TypedDict(
    "RetrievalFilterTypeDef",
    {
        "andAll": NotRequired[Sequence[Dict[str, Any]]],
        "equals": NotRequired[FilterAttributeTypeDef],
        "greaterThan": NotRequired[FilterAttributeTypeDef],
        "greaterThanOrEquals": NotRequired[FilterAttributeTypeDef],
        "in": NotRequired[FilterAttributeTypeDef],
        "lessThan": NotRequired[FilterAttributeTypeDef],
        "lessThanOrEquals": NotRequired[FilterAttributeTypeDef],
        "listContains": NotRequired[FilterAttributeTypeDef],
        "notEquals": NotRequired[FilterAttributeTypeDef],
        "notIn": NotRequired[FilterAttributeTypeDef],
        "orAll": NotRequired[Sequence[Dict[str, Any]]],
        "startsWith": NotRequired[FilterAttributeTypeDef],
        "stringContains": NotRequired[FilterAttributeTypeDef],
    },
)
FlowInputTypeDef = TypedDict(
    "FlowInputTypeDef",
    {
        "content": FlowInputContentTypeDef,
        "nodeName": str,
        "nodeOutputName": str,
    },
)
FlowOutputEventTypeDef = TypedDict(
    "FlowOutputEventTypeDef",
    {
        "content": FlowOutputContentTypeDef,
        "nodeName": str,
        "nodeType": NodeTypeType,
    },
)
FunctionInvocationInputTypeDef = TypedDict(
    "FunctionInvocationInputTypeDef",
    {
        "actionGroup": str,
        "actionInvocationType": NotRequired[ActionInvocationTypeType],
        "function": NotRequired[str],
        "parameters": NotRequired[List[FunctionParameterTypeDef]],
    },
)
GetAgentMemoryRequestGetAgentMemoryPaginateTypeDef = TypedDict(
    "GetAgentMemoryRequestGetAgentMemoryPaginateTypeDef",
    {
        "agentAliasId": str,
        "agentId": str,
        "memoryId": str,
        "memoryType": Literal["SESSION_SUMMARY"],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
GuardrailContentPolicyAssessmentTypeDef = TypedDict(
    "GuardrailContentPolicyAssessmentTypeDef",
    {
        "filters": NotRequired[List[GuardrailContentFilterTypeDef]],
    },
)
GuardrailWordPolicyAssessmentTypeDef = TypedDict(
    "GuardrailWordPolicyAssessmentTypeDef",
    {
        "customWords": NotRequired[List[GuardrailCustomWordTypeDef]],
        "managedWordLists": NotRequired[List[GuardrailManagedWordTypeDef]],
    },
)
GuardrailSensitiveInformationPolicyAssessmentTypeDef = TypedDict(
    "GuardrailSensitiveInformationPolicyAssessmentTypeDef",
    {
        "piiEntities": NotRequired[List[GuardrailPiiEntityFilterTypeDef]],
        "regexes": NotRequired[List[GuardrailRegexFilterTypeDef]],
    },
)
GuardrailTopicPolicyAssessmentTypeDef = TypedDict(
    "GuardrailTopicPolicyAssessmentTypeDef",
    {
        "topics": NotRequired[List[GuardrailTopicTypeDef]],
    },
)
InferenceConfigTypeDef = TypedDict(
    "InferenceConfigTypeDef",
    {
        "textInferenceConfig": NotRequired[TextInferenceConfigTypeDef],
    },
)
ModelInvocationInputTypeDef = TypedDict(
    "ModelInvocationInputTypeDef",
    {
        "inferenceConfiguration": NotRequired[InferenceConfigurationTypeDef],
        "overrideLambda": NotRequired[str],
        "parserMode": NotRequired[CreationModeType],
        "promptCreationMode": NotRequired[CreationModeType],
        "text": NotRequired[str],
        "traceId": NotRequired[str],
        "type": NotRequired[PromptTypeType],
    },
)
KnowledgeBaseRetrievalConfigurationTypeDef = TypedDict(
    "KnowledgeBaseRetrievalConfigurationTypeDef",
    {
        "vectorSearchConfiguration": KnowledgeBaseVectorSearchConfigurationTypeDef,
    },
)
MemoryTypeDef = TypedDict(
    "MemoryTypeDef",
    {
        "sessionSummary": NotRequired[MemorySessionSummaryTypeDef],
    },
)
MetadataTypeDef = TypedDict(
    "MetadataTypeDef",
    {
        "usage": NotRequired[UsageTypeDef],
    },
)
OrchestrationConfigurationTypeDef = TypedDict(
    "OrchestrationConfigurationTypeDef",
    {
        "queryTransformationConfiguration": QueryTransformationConfigurationTypeDef,
    },
)
PostProcessingModelInvocationOutputTypeDef = TypedDict(
    "PostProcessingModelInvocationOutputTypeDef",
    {
        "parsedResponse": NotRequired[PostProcessingParsedResponseTypeDef],
        "traceId": NotRequired[str],
    },
)
PreProcessingModelInvocationOutputTypeDef = TypedDict(
    "PreProcessingModelInvocationOutputTypeDef",
    {
        "parsedResponse": NotRequired[PreProcessingParsedResponseTypeDef],
        "traceId": NotRequired[str],
    },
)
RetrievalResultLocationTypeDef = TypedDict(
    "RetrievalResultLocationTypeDef",
    {
        "type": RetrievalResultLocationTypeType,
        "confluenceLocation": NotRequired[RetrievalResultConfluenceLocationTypeDef],
        "s3Location": NotRequired[RetrievalResultS3LocationTypeDef],
        "salesforceLocation": NotRequired[RetrievalResultSalesforceLocationTypeDef],
        "sharePointLocation": NotRequired[RetrievalResultSharePointLocationTypeDef],
        "webLocation": NotRequired[RetrievalResultWebLocationTypeDef],
    },
)
TextResponsePartTypeDef = TypedDict(
    "TextResponsePartTypeDef",
    {
        "span": NotRequired[SpanTypeDef],
        "text": NotRequired[str],
    },
)
ApiRequestBodyTypeDef = TypedDict(
    "ApiRequestBodyTypeDef",
    {
        "content": NotRequired[Dict[str, PropertyParametersTypeDef]],
    },
)
ActionGroupInvocationInputTypeDef = TypedDict(
    "ActionGroupInvocationInputTypeDef",
    {
        "actionGroupName": NotRequired[str],
        "apiPath": NotRequired[str],
        "executionType": NotRequired[ExecutionTypeType],
        "function": NotRequired[str],
        "invocationId": NotRequired[str],
        "parameters": NotRequired[List[ParameterTypeDef]],
        "requestBody": NotRequired[RequestBodyTypeDef],
        "verb": NotRequired[str],
    },
)
InvocationResultMemberTypeDef = TypedDict(
    "InvocationResultMemberTypeDef",
    {
        "apiResult": NotRequired[ApiResultTypeDef],
        "functionResult": NotRequired[FunctionResultTypeDef],
    },
)
ExternalSourceTypeDef = TypedDict(
    "ExternalSourceTypeDef",
    {
        "sourceType": ExternalSourceTypeType,
        "byteContent": NotRequired[ByteContentDocTypeDef],
        "s3Location": NotRequired[S3ObjectDocTypeDef],
    },
)
FileSourceTypeDef = TypedDict(
    "FileSourceTypeDef",
    {
        "sourceType": FileSourceTypeType,
        "byteContent": NotRequired[ByteContentFileTypeDef],
        "s3Location": NotRequired[S3ObjectFileTypeDef],
    },
)
InvokeFlowRequestRequestTypeDef = TypedDict(
    "InvokeFlowRequestRequestTypeDef",
    {
        "flowAliasIdentifier": str,
        "flowIdentifier": str,
        "inputs": Sequence[FlowInputTypeDef],
    },
)
FlowResponseStreamTypeDef = TypedDict(
    "FlowResponseStreamTypeDef",
    {
        "accessDeniedException": NotRequired[AccessDeniedExceptionTypeDef],
        "badGatewayException": NotRequired[BadGatewayExceptionTypeDef],
        "conflictException": NotRequired[ConflictExceptionTypeDef],
        "dependencyFailedException": NotRequired[DependencyFailedExceptionTypeDef],
        "flowCompletionEvent": NotRequired[FlowCompletionEventTypeDef],
        "flowOutputEvent": NotRequired[FlowOutputEventTypeDef],
        "internalServerException": NotRequired[InternalServerExceptionTypeDef],
        "resourceNotFoundException": NotRequired[ResourceNotFoundExceptionTypeDef],
        "serviceQuotaExceededException": NotRequired[ServiceQuotaExceededExceptionTypeDef],
        "throttlingException": NotRequired[ThrottlingExceptionTypeDef],
        "validationException": NotRequired[ValidationExceptionTypeDef],
    },
)
GuardrailAssessmentTypeDef = TypedDict(
    "GuardrailAssessmentTypeDef",
    {
        "contentPolicy": NotRequired[GuardrailContentPolicyAssessmentTypeDef],
        "sensitiveInformationPolicy": NotRequired[
            GuardrailSensitiveInformationPolicyAssessmentTypeDef
        ],
        "topicPolicy": NotRequired[GuardrailTopicPolicyAssessmentTypeDef],
        "wordPolicy": NotRequired[GuardrailWordPolicyAssessmentTypeDef],
    },
)
ExternalSourcesGenerationConfigurationTypeDef = TypedDict(
    "ExternalSourcesGenerationConfigurationTypeDef",
    {
        "additionalModelRequestFields": NotRequired[Mapping[str, Mapping[str, Any]]],
        "guardrailConfiguration": NotRequired[GuardrailConfigurationTypeDef],
        "inferenceConfig": NotRequired[InferenceConfigTypeDef],
        "promptTemplate": NotRequired[PromptTemplateTypeDef],
    },
)
GenerationConfigurationTypeDef = TypedDict(
    "GenerationConfigurationTypeDef",
    {
        "additionalModelRequestFields": NotRequired[Mapping[str, Mapping[str, Any]]],
        "guardrailConfiguration": NotRequired[GuardrailConfigurationTypeDef],
        "inferenceConfig": NotRequired[InferenceConfigTypeDef],
        "promptTemplate": NotRequired[PromptTemplateTypeDef],
    },
)
KnowledgeBaseConfigurationTypeDef = TypedDict(
    "KnowledgeBaseConfigurationTypeDef",
    {
        "knowledgeBaseId": str,
        "retrievalConfiguration": KnowledgeBaseRetrievalConfigurationTypeDef,
    },
)
RetrieveRequestRequestTypeDef = TypedDict(
    "RetrieveRequestRequestTypeDef",
    {
        "knowledgeBaseId": str,
        "retrievalQuery": KnowledgeBaseQueryTypeDef,
        "nextToken": NotRequired[str],
        "retrievalConfiguration": NotRequired[KnowledgeBaseRetrievalConfigurationTypeDef],
    },
)
RetrieveRequestRetrievePaginateTypeDef = TypedDict(
    "RetrieveRequestRetrievePaginateTypeDef",
    {
        "knowledgeBaseId": str,
        "retrievalQuery": KnowledgeBaseQueryTypeDef,
        "retrievalConfiguration": NotRequired[KnowledgeBaseRetrievalConfigurationTypeDef],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
GetAgentMemoryResponseTypeDef = TypedDict(
    "GetAgentMemoryResponseTypeDef",
    {
        "memoryContents": List[MemoryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
OrchestrationModelInvocationOutputTypeDef = TypedDict(
    "OrchestrationModelInvocationOutputTypeDef",
    {
        "metadata": NotRequired[MetadataTypeDef],
        "rawResponse": NotRequired[RawResponseTypeDef],
        "traceId": NotRequired[str],
    },
)
PostProcessingTraceTypeDef = TypedDict(
    "PostProcessingTraceTypeDef",
    {
        "modelInvocationInput": NotRequired[ModelInvocationInputTypeDef],
        "modelInvocationOutput": NotRequired[PostProcessingModelInvocationOutputTypeDef],
    },
)
PreProcessingTraceTypeDef = TypedDict(
    "PreProcessingTraceTypeDef",
    {
        "modelInvocationInput": NotRequired[ModelInvocationInputTypeDef],
        "modelInvocationOutput": NotRequired[PreProcessingModelInvocationOutputTypeDef],
    },
)
KnowledgeBaseRetrievalResultTypeDef = TypedDict(
    "KnowledgeBaseRetrievalResultTypeDef",
    {
        "content": RetrievalResultContentTypeDef,
        "location": NotRequired[RetrievalResultLocationTypeDef],
        "metadata": NotRequired[Dict[str, Dict[str, Any]]],
        "score": NotRequired[float],
    },
)
RetrievedReferenceTypeDef = TypedDict(
    "RetrievedReferenceTypeDef",
    {
        "content": NotRequired[RetrievalResultContentTypeDef],
        "location": NotRequired[RetrievalResultLocationTypeDef],
        "metadata": NotRequired[Dict[str, Dict[str, Any]]],
    },
)
GeneratedResponsePartTypeDef = TypedDict(
    "GeneratedResponsePartTypeDef",
    {
        "textResponsePart": NotRequired[TextResponsePartTypeDef],
    },
)
ApiInvocationInputTypeDef = TypedDict(
    "ApiInvocationInputTypeDef",
    {
        "actionGroup": str,
        "actionInvocationType": NotRequired[ActionInvocationTypeType],
        "apiPath": NotRequired[str],
        "httpMethod": NotRequired[str],
        "parameters": NotRequired[List[ApiParameterTypeDef]],
        "requestBody": NotRequired[ApiRequestBodyTypeDef],
    },
)
InvocationInputTypeDef = TypedDict(
    "InvocationInputTypeDef",
    {
        "actionGroupInvocationInput": NotRequired[ActionGroupInvocationInputTypeDef],
        "codeInterpreterInvocationInput": NotRequired[CodeInterpreterInvocationInputTypeDef],
        "invocationType": NotRequired[InvocationTypeType],
        "knowledgeBaseLookupInput": NotRequired[KnowledgeBaseLookupInputTypeDef],
        "traceId": NotRequired[str],
    },
)
InputFileTypeDef = TypedDict(
    "InputFileTypeDef",
    {
        "name": str,
        "source": FileSourceTypeDef,
        "useCase": FileUseCaseType,
    },
)
InvokeFlowResponseTypeDef = TypedDict(
    "InvokeFlowResponseTypeDef",
    {
        "responseStream": "AioEventStream[FlowResponseStreamTypeDef]",
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GuardrailTraceTypeDef = TypedDict(
    "GuardrailTraceTypeDef",
    {
        "action": NotRequired[GuardrailActionType],
        "inputAssessments": NotRequired[List[GuardrailAssessmentTypeDef]],
        "outputAssessments": NotRequired[List[GuardrailAssessmentTypeDef]],
        "traceId": NotRequired[str],
    },
)
ExternalSourcesRetrieveAndGenerateConfigurationTypeDef = TypedDict(
    "ExternalSourcesRetrieveAndGenerateConfigurationTypeDef",
    {
        "modelArn": str,
        "sources": Sequence[ExternalSourceTypeDef],
        "generationConfiguration": NotRequired[ExternalSourcesGenerationConfigurationTypeDef],
    },
)
KnowledgeBaseRetrieveAndGenerateConfigurationTypeDef = TypedDict(
    "KnowledgeBaseRetrieveAndGenerateConfigurationTypeDef",
    {
        "knowledgeBaseId": str,
        "modelArn": str,
        "generationConfiguration": NotRequired[GenerationConfigurationTypeDef],
        "orchestrationConfiguration": NotRequired[OrchestrationConfigurationTypeDef],
        "retrievalConfiguration": NotRequired[KnowledgeBaseRetrievalConfigurationTypeDef],
    },
)
RetrieveResponseTypeDef = TypedDict(
    "RetrieveResponseTypeDef",
    {
        "nextToken": str,
        "retrievalResults": List[KnowledgeBaseRetrievalResultTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
KnowledgeBaseLookupOutputTypeDef = TypedDict(
    "KnowledgeBaseLookupOutputTypeDef",
    {
        "retrievedReferences": NotRequired[List[RetrievedReferenceTypeDef]],
    },
)
CitationTypeDef = TypedDict(
    "CitationTypeDef",
    {
        "generatedResponsePart": NotRequired[GeneratedResponsePartTypeDef],
        "retrievedReferences": NotRequired[List[RetrievedReferenceTypeDef]],
    },
)
InvocationInputMemberTypeDef = TypedDict(
    "InvocationInputMemberTypeDef",
    {
        "apiInvocationInput": NotRequired[ApiInvocationInputTypeDef],
        "functionInvocationInput": NotRequired[FunctionInvocationInputTypeDef],
    },
)
SessionStateTypeDef = TypedDict(
    "SessionStateTypeDef",
    {
        "files": NotRequired[Sequence[InputFileTypeDef]],
        "invocationId": NotRequired[str],
        "knowledgeBaseConfigurations": NotRequired[Sequence[KnowledgeBaseConfigurationTypeDef]],
        "promptSessionAttributes": NotRequired[Mapping[str, str]],
        "returnControlInvocationResults": NotRequired[Sequence[InvocationResultMemberTypeDef]],
        "sessionAttributes": NotRequired[Mapping[str, str]],
    },
)
RetrieveAndGenerateConfigurationTypeDef = TypedDict(
    "RetrieveAndGenerateConfigurationTypeDef",
    {
        "type": RetrieveAndGenerateTypeType,
        "externalSourcesConfiguration": NotRequired[
            ExternalSourcesRetrieveAndGenerateConfigurationTypeDef
        ],
        "knowledgeBaseConfiguration": NotRequired[
            KnowledgeBaseRetrieveAndGenerateConfigurationTypeDef
        ],
    },
)
ObservationTypeDef = TypedDict(
    "ObservationTypeDef",
    {
        "actionGroupInvocationOutput": NotRequired[ActionGroupInvocationOutputTypeDef],
        "codeInterpreterInvocationOutput": NotRequired[CodeInterpreterInvocationOutputTypeDef],
        "finalResponse": NotRequired[FinalResponseTypeDef],
        "knowledgeBaseLookupOutput": NotRequired[KnowledgeBaseLookupOutputTypeDef],
        "repromptResponse": NotRequired[RepromptResponseTypeDef],
        "traceId": NotRequired[str],
        "type": NotRequired[TypeType],
    },
)
AttributionTypeDef = TypedDict(
    "AttributionTypeDef",
    {
        "citations": NotRequired[List[CitationTypeDef]],
    },
)
RetrieveAndGenerateResponseTypeDef = TypedDict(
    "RetrieveAndGenerateResponseTypeDef",
    {
        "citations": List[CitationTypeDef],
        "guardrailAction": GuadrailActionType,
        "output": RetrieveAndGenerateOutputTypeDef,
        "sessionId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ReturnControlPayloadTypeDef = TypedDict(
    "ReturnControlPayloadTypeDef",
    {
        "invocationId": NotRequired[str],
        "invocationInputs": NotRequired[List[InvocationInputMemberTypeDef]],
    },
)
InvokeAgentRequestRequestTypeDef = TypedDict(
    "InvokeAgentRequestRequestTypeDef",
    {
        "agentAliasId": str,
        "agentId": str,
        "sessionId": str,
        "enableTrace": NotRequired[bool],
        "endSession": NotRequired[bool],
        "inputText": NotRequired[str],
        "memoryId": NotRequired[str],
        "sessionState": NotRequired[SessionStateTypeDef],
    },
)
RetrieveAndGenerateRequestRequestTypeDef = TypedDict(
    "RetrieveAndGenerateRequestRequestTypeDef",
    {
        "input": RetrieveAndGenerateInputTypeDef,
        "retrieveAndGenerateConfiguration": NotRequired[RetrieveAndGenerateConfigurationTypeDef],
        "sessionConfiguration": NotRequired[RetrieveAndGenerateSessionConfigurationTypeDef],
        "sessionId": NotRequired[str],
    },
)
OrchestrationTraceTypeDef = TypedDict(
    "OrchestrationTraceTypeDef",
    {
        "invocationInput": NotRequired[InvocationInputTypeDef],
        "modelInvocationInput": NotRequired[ModelInvocationInputTypeDef],
        "modelInvocationOutput": NotRequired[OrchestrationModelInvocationOutputTypeDef],
        "observation": NotRequired[ObservationTypeDef],
        "rationale": NotRequired[RationaleTypeDef],
    },
)
PayloadPartTypeDef = TypedDict(
    "PayloadPartTypeDef",
    {
        "attribution": NotRequired[AttributionTypeDef],
        "bytes": NotRequired[bytes],
    },
)
TraceTypeDef = TypedDict(
    "TraceTypeDef",
    {
        "failureTrace": NotRequired[FailureTraceTypeDef],
        "guardrailTrace": NotRequired[GuardrailTraceTypeDef],
        "orchestrationTrace": NotRequired[OrchestrationTraceTypeDef],
        "postProcessingTrace": NotRequired[PostProcessingTraceTypeDef],
        "preProcessingTrace": NotRequired[PreProcessingTraceTypeDef],
    },
)
TracePartTypeDef = TypedDict(
    "TracePartTypeDef",
    {
        "agentAliasId": NotRequired[str],
        "agentId": NotRequired[str],
        "agentVersion": NotRequired[str],
        "sessionId": NotRequired[str],
        "trace": NotRequired[TraceTypeDef],
    },
)
ResponseStreamTypeDef = TypedDict(
    "ResponseStreamTypeDef",
    {
        "accessDeniedException": NotRequired[AccessDeniedExceptionTypeDef],
        "badGatewayException": NotRequired[BadGatewayExceptionTypeDef],
        "chunk": NotRequired[PayloadPartTypeDef],
        "conflictException": NotRequired[ConflictExceptionTypeDef],
        "dependencyFailedException": NotRequired[DependencyFailedExceptionTypeDef],
        "files": NotRequired[FilePartTypeDef],
        "internalServerException": NotRequired[InternalServerExceptionTypeDef],
        "resourceNotFoundException": NotRequired[ResourceNotFoundExceptionTypeDef],
        "returnControl": NotRequired[ReturnControlPayloadTypeDef],
        "serviceQuotaExceededException": NotRequired[ServiceQuotaExceededExceptionTypeDef],
        "throttlingException": NotRequired[ThrottlingExceptionTypeDef],
        "trace": NotRequired[TracePartTypeDef],
        "validationException": NotRequired[ValidationExceptionTypeDef],
    },
)
InvokeAgentResponseTypeDef = TypedDict(
    "InvokeAgentResponseTypeDef",
    {
        "completion": "AioEventStream[ResponseStreamTypeDef]",
        "contentType": str,
        "memoryId": str,
        "sessionId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
