"""
Type annotations for bedrock-agent service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent/type_defs/)

Usage::

    ```python
    from mypy_boto3_bedrock_agent.type_defs import S3IdentifierTypeDef

    data: S3IdentifierTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence, Union

from .literals import (
    ActionGroupSignatureType,
    ActionGroupStateType,
    AgentAliasStatusType,
    AgentStatusType,
    ChunkingStrategyType,
    ConfluenceAuthTypeType,
    CreationModeType,
    DataDeletionPolicyType,
    DataSourceStatusType,
    DataSourceTypeType,
    FlowConnectionTypeType,
    FlowNodeIODataTypeType,
    FlowNodeTypeType,
    FlowStatusType,
    FlowValidationSeverityType,
    IngestionJobSortByAttributeType,
    IngestionJobStatusType,
    KnowledgeBaseStateType,
    KnowledgeBaseStatusType,
    KnowledgeBaseStorageTypeType,
    PromptStateType,
    PromptTypeType,
    RequireConfirmationType,
    SortOrderType,
    TypeType,
    WebScopeTypeType,
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
    "S3IdentifierTypeDef",
    "ActionGroupExecutorTypeDef",
    "ActionGroupSummaryTypeDef",
    "AgentAliasRoutingConfigurationListItemTypeDef",
    "AgentFlowNodeConfigurationTypeDef",
    "AgentKnowledgeBaseSummaryTypeDef",
    "AgentKnowledgeBaseTypeDef",
    "GuardrailConfigurationTypeDef",
    "MemoryConfigurationOutputTypeDef",
    "AssociateAgentKnowledgeBaseRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "BedrockEmbeddingModelConfigurationTypeDef",
    "ParsingPromptTypeDef",
    "FixedSizeChunkingConfigurationTypeDef",
    "SemanticChunkingConfigurationTypeDef",
    "FlowConditionTypeDef",
    "ConfluenceSourceConfigurationTypeDef",
    "MemoryConfigurationTypeDef",
    "ServerSideEncryptionConfigurationTypeDef",
    "FlowAliasRoutingConfigurationListItemTypeDef",
    "CreateFlowVersionRequestRequestTypeDef",
    "CreatePromptVersionRequestRequestTypeDef",
    "S3DataSourceConfigurationOutputTypeDef",
    "S3DataSourceConfigurationTypeDef",
    "DataSourceSummaryTypeDef",
    "DeleteAgentActionGroupRequestRequestTypeDef",
    "DeleteAgentAliasRequestRequestTypeDef",
    "DeleteAgentRequestRequestTypeDef",
    "DeleteAgentVersionRequestRequestTypeDef",
    "DeleteDataSourceRequestRequestTypeDef",
    "DeleteFlowAliasRequestRequestTypeDef",
    "DeleteFlowRequestRequestTypeDef",
    "DeleteFlowVersionRequestRequestTypeDef",
    "DeleteKnowledgeBaseRequestRequestTypeDef",
    "DeletePromptRequestRequestTypeDef",
    "DisassociateAgentKnowledgeBaseRequestRequestTypeDef",
    "FlowConditionalConnectionConfigurationTypeDef",
    "FlowDataConnectionConfigurationTypeDef",
    "KnowledgeBaseFlowNodeConfigurationTypeDef",
    "LambdaFunctionFlowNodeConfigurationTypeDef",
    "LexFlowNodeConfigurationTypeDef",
    "FlowNodeInputTypeDef",
    "FlowNodeOutputTypeDef",
    "FlowSummaryTypeDef",
    "FlowValidationTypeDef",
    "FlowVersionSummaryTypeDef",
    "ParameterDetailTypeDef",
    "GetAgentActionGroupRequestRequestTypeDef",
    "GetAgentAliasRequestRequestTypeDef",
    "GetAgentKnowledgeBaseRequestRequestTypeDef",
    "GetAgentRequestRequestTypeDef",
    "GetAgentVersionRequestRequestTypeDef",
    "GetDataSourceRequestRequestTypeDef",
    "GetFlowAliasRequestRequestTypeDef",
    "GetFlowRequestRequestTypeDef",
    "GetFlowVersionRequestRequestTypeDef",
    "GetIngestionJobRequestRequestTypeDef",
    "GetKnowledgeBaseRequestRequestTypeDef",
    "GetPromptRequestRequestTypeDef",
    "HierarchicalChunkingLevelConfigurationTypeDef",
    "InferenceConfigurationOutputTypeDef",
    "InferenceConfigurationTypeDef",
    "IngestionJobFilterTypeDef",
    "IngestionJobSortByTypeDef",
    "IngestionJobStatisticsTypeDef",
    "S3LocationTypeDef",
    "KnowledgeBaseSummaryTypeDef",
    "PaginatorConfigTypeDef",
    "ListAgentActionGroupsRequestRequestTypeDef",
    "ListAgentAliasesRequestRequestTypeDef",
    "ListAgentKnowledgeBasesRequestRequestTypeDef",
    "ListAgentVersionsRequestRequestTypeDef",
    "ListAgentsRequestRequestTypeDef",
    "ListDataSourcesRequestRequestTypeDef",
    "ListFlowAliasesRequestRequestTypeDef",
    "ListFlowVersionsRequestRequestTypeDef",
    "ListFlowsRequestRequestTypeDef",
    "ListKnowledgeBasesRequestRequestTypeDef",
    "ListPromptsRequestRequestTypeDef",
    "PromptSummaryTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "MongoDbAtlasFieldMappingTypeDef",
    "OpenSearchServerlessFieldMappingTypeDef",
    "PatternObjectFilterOutputTypeDef",
    "PatternObjectFilterTypeDef",
    "PineconeFieldMappingTypeDef",
    "PrepareAgentRequestRequestTypeDef",
    "PrepareFlowRequestRequestTypeDef",
    "PromptFlowNodeResourceConfigurationTypeDef",
    "PromptModelInferenceConfigurationOutputTypeDef",
    "PromptModelInferenceConfigurationTypeDef",
    "PromptInputVariableTypeDef",
    "PromptMetadataEntryTypeDef",
    "RdsFieldMappingTypeDef",
    "RedisEnterpriseCloudFieldMappingTypeDef",
    "RetrievalFlowNodeS3ConfigurationTypeDef",
    "SalesforceSourceConfigurationTypeDef",
    "SeedUrlTypeDef",
    "SharePointSourceConfigurationOutputTypeDef",
    "SharePointSourceConfigurationTypeDef",
    "StartIngestionJobRequestRequestTypeDef",
    "StorageFlowNodeS3ConfigurationTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TransformationLambdaConfigurationTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAgentKnowledgeBaseRequestRequestTypeDef",
    "WebCrawlerLimitsTypeDef",
    "APISchemaTypeDef",
    "AgentAliasHistoryEventTypeDef",
    "AgentAliasSummaryTypeDef",
    "CreateAgentAliasRequestRequestTypeDef",
    "UpdateAgentAliasRequestRequestTypeDef",
    "AgentSummaryTypeDef",
    "AgentVersionSummaryTypeDef",
    "AssociateAgentKnowledgeBaseResponseTypeDef",
    "DeleteAgentAliasResponseTypeDef",
    "DeleteAgentResponseTypeDef",
    "DeleteAgentVersionResponseTypeDef",
    "DeleteDataSourceResponseTypeDef",
    "DeleteFlowAliasResponseTypeDef",
    "DeleteFlowResponseTypeDef",
    "DeleteFlowVersionResponseTypeDef",
    "DeleteKnowledgeBaseResponseTypeDef",
    "DeletePromptResponseTypeDef",
    "GetAgentKnowledgeBaseResponseTypeDef",
    "ListAgentActionGroupsResponseTypeDef",
    "ListAgentKnowledgeBasesResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PrepareAgentResponseTypeDef",
    "PrepareFlowResponseTypeDef",
    "UpdateAgentKnowledgeBaseResponseTypeDef",
    "EmbeddingModelConfigurationTypeDef",
    "BedrockFoundationModelConfigurationTypeDef",
    "ConditionFlowNodeConfigurationOutputTypeDef",
    "ConditionFlowNodeConfigurationTypeDef",
    "CreateFlowAliasRequestRequestTypeDef",
    "CreateFlowAliasResponseTypeDef",
    "FlowAliasSummaryTypeDef",
    "GetFlowAliasResponseTypeDef",
    "UpdateFlowAliasRequestRequestTypeDef",
    "UpdateFlowAliasResponseTypeDef",
    "ListDataSourcesResponseTypeDef",
    "FlowConnectionConfigurationTypeDef",
    "ListFlowsResponseTypeDef",
    "ListFlowVersionsResponseTypeDef",
    "FunctionOutputTypeDef",
    "FunctionTypeDef",
    "HierarchicalChunkingConfigurationOutputTypeDef",
    "HierarchicalChunkingConfigurationTypeDef",
    "PromptConfigurationOutputTypeDef",
    "PromptConfigurationTypeDef",
    "ListIngestionJobsRequestRequestTypeDef",
    "IngestionJobSummaryTypeDef",
    "IngestionJobTypeDef",
    "IntermediateStorageTypeDef",
    "ListKnowledgeBasesResponseTypeDef",
    "ListAgentActionGroupsRequestListAgentActionGroupsPaginateTypeDef",
    "ListAgentAliasesRequestListAgentAliasesPaginateTypeDef",
    "ListAgentKnowledgeBasesRequestListAgentKnowledgeBasesPaginateTypeDef",
    "ListAgentVersionsRequestListAgentVersionsPaginateTypeDef",
    "ListAgentsRequestListAgentsPaginateTypeDef",
    "ListDataSourcesRequestListDataSourcesPaginateTypeDef",
    "ListFlowAliasesRequestListFlowAliasesPaginateTypeDef",
    "ListFlowVersionsRequestListFlowVersionsPaginateTypeDef",
    "ListFlowsRequestListFlowsPaginateTypeDef",
    "ListIngestionJobsRequestListIngestionJobsPaginateTypeDef",
    "ListKnowledgeBasesRequestListKnowledgeBasesPaginateTypeDef",
    "ListPromptsRequestListPromptsPaginateTypeDef",
    "ListPromptsResponseTypeDef",
    "MongoDbAtlasConfigurationTypeDef",
    "OpenSearchServerlessConfigurationTypeDef",
    "PatternObjectFilterConfigurationOutputTypeDef",
    "PatternObjectFilterConfigurationTypeDef",
    "PineconeConfigurationTypeDef",
    "PromptInferenceConfigurationOutputTypeDef",
    "PromptInferenceConfigurationTypeDef",
    "TextPromptTemplateConfigurationOutputTypeDef",
    "TextPromptTemplateConfigurationTypeDef",
    "RdsConfigurationTypeDef",
    "RedisEnterpriseCloudConfigurationTypeDef",
    "RetrievalFlowNodeServiceConfigurationTypeDef",
    "UrlConfigurationOutputTypeDef",
    "UrlConfigurationTypeDef",
    "StorageFlowNodeServiceConfigurationTypeDef",
    "TransformationFunctionTypeDef",
    "WebCrawlerConfigurationOutputTypeDef",
    "WebCrawlerConfigurationTypeDef",
    "AgentAliasTypeDef",
    "ListAgentAliasesResponseTypeDef",
    "ListAgentsResponseTypeDef",
    "ListAgentVersionsResponseTypeDef",
    "VectorKnowledgeBaseConfigurationTypeDef",
    "ParsingConfigurationTypeDef",
    "ListFlowAliasesResponseTypeDef",
    "FlowConnectionTypeDef",
    "FunctionSchemaOutputTypeDef",
    "FunctionSchemaTypeDef",
    "ChunkingConfigurationOutputTypeDef",
    "ChunkingConfigurationTypeDef",
    "PromptOverrideConfigurationOutputTypeDef",
    "PromptOverrideConfigurationTypeDef",
    "ListIngestionJobsResponseTypeDef",
    "GetIngestionJobResponseTypeDef",
    "StartIngestionJobResponseTypeDef",
    "CrawlFilterConfigurationOutputTypeDef",
    "CrawlFilterConfigurationTypeDef",
    "PromptTemplateConfigurationOutputTypeDef",
    "PromptTemplateConfigurationTypeDef",
    "StorageConfigurationTypeDef",
    "RetrievalFlowNodeConfigurationTypeDef",
    "WebSourceConfigurationOutputTypeDef",
    "WebSourceConfigurationTypeDef",
    "StorageFlowNodeConfigurationTypeDef",
    "TransformationTypeDef",
    "CreateAgentAliasResponseTypeDef",
    "GetAgentAliasResponseTypeDef",
    "UpdateAgentAliasResponseTypeDef",
    "KnowledgeBaseConfigurationTypeDef",
    "AgentActionGroupTypeDef",
    "CreateAgentActionGroupRequestRequestTypeDef",
    "UpdateAgentActionGroupRequestRequestTypeDef",
    "AgentTypeDef",
    "AgentVersionTypeDef",
    "CreateAgentRequestRequestTypeDef",
    "UpdateAgentRequestRequestTypeDef",
    "ConfluenceCrawlerConfigurationOutputTypeDef",
    "SalesforceCrawlerConfigurationOutputTypeDef",
    "SharePointCrawlerConfigurationOutputTypeDef",
    "ConfluenceCrawlerConfigurationTypeDef",
    "SalesforceCrawlerConfigurationTypeDef",
    "SharePointCrawlerConfigurationTypeDef",
    "PromptFlowNodeInlineConfigurationOutputTypeDef",
    "PromptVariantOutputTypeDef",
    "PromptFlowNodeInlineConfigurationTypeDef",
    "PromptVariantTypeDef",
    "WebDataSourceConfigurationOutputTypeDef",
    "WebDataSourceConfigurationTypeDef",
    "CustomTransformationConfigurationOutputTypeDef",
    "CustomTransformationConfigurationTypeDef",
    "CreateKnowledgeBaseRequestRequestTypeDef",
    "KnowledgeBaseTypeDef",
    "UpdateKnowledgeBaseRequestRequestTypeDef",
    "CreateAgentActionGroupResponseTypeDef",
    "GetAgentActionGroupResponseTypeDef",
    "UpdateAgentActionGroupResponseTypeDef",
    "CreateAgentResponseTypeDef",
    "GetAgentResponseTypeDef",
    "UpdateAgentResponseTypeDef",
    "GetAgentVersionResponseTypeDef",
    "ConfluenceDataSourceConfigurationOutputTypeDef",
    "SalesforceDataSourceConfigurationOutputTypeDef",
    "SharePointDataSourceConfigurationOutputTypeDef",
    "ConfluenceDataSourceConfigurationTypeDef",
    "SalesforceDataSourceConfigurationTypeDef",
    "SharePointDataSourceConfigurationTypeDef",
    "PromptFlowNodeSourceConfigurationOutputTypeDef",
    "CreatePromptResponseTypeDef",
    "CreatePromptVersionResponseTypeDef",
    "GetPromptResponseTypeDef",
    "UpdatePromptResponseTypeDef",
    "PromptFlowNodeSourceConfigurationTypeDef",
    "PromptVariantUnionTypeDef",
    "VectorIngestionConfigurationOutputTypeDef",
    "VectorIngestionConfigurationTypeDef",
    "CreateKnowledgeBaseResponseTypeDef",
    "GetKnowledgeBaseResponseTypeDef",
    "UpdateKnowledgeBaseResponseTypeDef",
    "DataSourceConfigurationOutputTypeDef",
    "DataSourceConfigurationTypeDef",
    "PromptFlowNodeConfigurationOutputTypeDef",
    "PromptFlowNodeConfigurationTypeDef",
    "CreatePromptRequestRequestTypeDef",
    "UpdatePromptRequestRequestTypeDef",
    "DataSourceTypeDef",
    "CreateDataSourceRequestRequestTypeDef",
    "UpdateDataSourceRequestRequestTypeDef",
    "FlowNodeConfigurationOutputTypeDef",
    "FlowNodeConfigurationTypeDef",
    "CreateDataSourceResponseTypeDef",
    "GetDataSourceResponseTypeDef",
    "UpdateDataSourceResponseTypeDef",
    "FlowNodeExtraOutputTypeDef",
    "FlowNodeTypeDef",
    "FlowDefinitionOutputTypeDef",
    "FlowDefinitionTypeDef",
    "CreateFlowResponseTypeDef",
    "CreateFlowVersionResponseTypeDef",
    "GetFlowResponseTypeDef",
    "GetFlowVersionResponseTypeDef",
    "UpdateFlowResponseTypeDef",
    "CreateFlowRequestRequestTypeDef",
    "UpdateFlowRequestRequestTypeDef",
)

S3IdentifierTypeDef = TypedDict(
    "S3IdentifierTypeDef",
    {
        "s3BucketName": NotRequired[str],
        "s3ObjectKey": NotRequired[str],
    },
)
ActionGroupExecutorTypeDef = TypedDict(
    "ActionGroupExecutorTypeDef",
    {
        "customControl": NotRequired[Literal["RETURN_CONTROL"]],
        "lambda": NotRequired[str],
    },
)
ActionGroupSummaryTypeDef = TypedDict(
    "ActionGroupSummaryTypeDef",
    {
        "actionGroupId": str,
        "actionGroupName": str,
        "actionGroupState": ActionGroupStateType,
        "updatedAt": datetime,
        "description": NotRequired[str],
    },
)
AgentAliasRoutingConfigurationListItemTypeDef = TypedDict(
    "AgentAliasRoutingConfigurationListItemTypeDef",
    {
        "agentVersion": NotRequired[str],
        "provisionedThroughput": NotRequired[str],
    },
)
AgentFlowNodeConfigurationTypeDef = TypedDict(
    "AgentFlowNodeConfigurationTypeDef",
    {
        "agentAliasArn": str,
    },
)
AgentKnowledgeBaseSummaryTypeDef = TypedDict(
    "AgentKnowledgeBaseSummaryTypeDef",
    {
        "knowledgeBaseId": str,
        "knowledgeBaseState": KnowledgeBaseStateType,
        "updatedAt": datetime,
        "description": NotRequired[str],
    },
)
AgentKnowledgeBaseTypeDef = TypedDict(
    "AgentKnowledgeBaseTypeDef",
    {
        "agentId": str,
        "agentVersion": str,
        "createdAt": datetime,
        "description": str,
        "knowledgeBaseId": str,
        "knowledgeBaseState": KnowledgeBaseStateType,
        "updatedAt": datetime,
    },
)
GuardrailConfigurationTypeDef = TypedDict(
    "GuardrailConfigurationTypeDef",
    {
        "guardrailIdentifier": NotRequired[str],
        "guardrailVersion": NotRequired[str],
    },
)
MemoryConfigurationOutputTypeDef = TypedDict(
    "MemoryConfigurationOutputTypeDef",
    {
        "enabledMemoryTypes": List[Literal["SESSION_SUMMARY"]],
        "storageDays": NotRequired[int],
    },
)
AssociateAgentKnowledgeBaseRequestRequestTypeDef = TypedDict(
    "AssociateAgentKnowledgeBaseRequestRequestTypeDef",
    {
        "agentId": str,
        "agentVersion": str,
        "description": str,
        "knowledgeBaseId": str,
        "knowledgeBaseState": NotRequired[KnowledgeBaseStateType],
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
BedrockEmbeddingModelConfigurationTypeDef = TypedDict(
    "BedrockEmbeddingModelConfigurationTypeDef",
    {
        "dimensions": NotRequired[int],
    },
)
ParsingPromptTypeDef = TypedDict(
    "ParsingPromptTypeDef",
    {
        "parsingPromptText": str,
    },
)
FixedSizeChunkingConfigurationTypeDef = TypedDict(
    "FixedSizeChunkingConfigurationTypeDef",
    {
        "maxTokens": int,
        "overlapPercentage": int,
    },
)
SemanticChunkingConfigurationTypeDef = TypedDict(
    "SemanticChunkingConfigurationTypeDef",
    {
        "breakpointPercentileThreshold": int,
        "bufferSize": int,
        "maxTokens": int,
    },
)
FlowConditionTypeDef = TypedDict(
    "FlowConditionTypeDef",
    {
        "name": str,
        "expression": NotRequired[str],
    },
)
ConfluenceSourceConfigurationTypeDef = TypedDict(
    "ConfluenceSourceConfigurationTypeDef",
    {
        "authType": ConfluenceAuthTypeType,
        "credentialsSecretArn": str,
        "hostType": Literal["SAAS"],
        "hostUrl": str,
    },
)
MemoryConfigurationTypeDef = TypedDict(
    "MemoryConfigurationTypeDef",
    {
        "enabledMemoryTypes": Sequence[Literal["SESSION_SUMMARY"]],
        "storageDays": NotRequired[int],
    },
)
ServerSideEncryptionConfigurationTypeDef = TypedDict(
    "ServerSideEncryptionConfigurationTypeDef",
    {
        "kmsKeyArn": NotRequired[str],
    },
)
FlowAliasRoutingConfigurationListItemTypeDef = TypedDict(
    "FlowAliasRoutingConfigurationListItemTypeDef",
    {
        "flowVersion": NotRequired[str],
    },
)
CreateFlowVersionRequestRequestTypeDef = TypedDict(
    "CreateFlowVersionRequestRequestTypeDef",
    {
        "flowIdentifier": str,
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
    },
)
CreatePromptVersionRequestRequestTypeDef = TypedDict(
    "CreatePromptVersionRequestRequestTypeDef",
    {
        "promptIdentifier": str,
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
    },
)
S3DataSourceConfigurationOutputTypeDef = TypedDict(
    "S3DataSourceConfigurationOutputTypeDef",
    {
        "bucketArn": str,
        "bucketOwnerAccountId": NotRequired[str],
        "inclusionPrefixes": NotRequired[List[str]],
    },
)
S3DataSourceConfigurationTypeDef = TypedDict(
    "S3DataSourceConfigurationTypeDef",
    {
        "bucketArn": str,
        "bucketOwnerAccountId": NotRequired[str],
        "inclusionPrefixes": NotRequired[Sequence[str]],
    },
)
DataSourceSummaryTypeDef = TypedDict(
    "DataSourceSummaryTypeDef",
    {
        "dataSourceId": str,
        "knowledgeBaseId": str,
        "name": str,
        "status": DataSourceStatusType,
        "updatedAt": datetime,
        "description": NotRequired[str],
    },
)
DeleteAgentActionGroupRequestRequestTypeDef = TypedDict(
    "DeleteAgentActionGroupRequestRequestTypeDef",
    {
        "actionGroupId": str,
        "agentId": str,
        "agentVersion": str,
        "skipResourceInUseCheck": NotRequired[bool],
    },
)
DeleteAgentAliasRequestRequestTypeDef = TypedDict(
    "DeleteAgentAliasRequestRequestTypeDef",
    {
        "agentAliasId": str,
        "agentId": str,
    },
)
DeleteAgentRequestRequestTypeDef = TypedDict(
    "DeleteAgentRequestRequestTypeDef",
    {
        "agentId": str,
        "skipResourceInUseCheck": NotRequired[bool],
    },
)
DeleteAgentVersionRequestRequestTypeDef = TypedDict(
    "DeleteAgentVersionRequestRequestTypeDef",
    {
        "agentId": str,
        "agentVersion": str,
        "skipResourceInUseCheck": NotRequired[bool],
    },
)
DeleteDataSourceRequestRequestTypeDef = TypedDict(
    "DeleteDataSourceRequestRequestTypeDef",
    {
        "dataSourceId": str,
        "knowledgeBaseId": str,
    },
)
DeleteFlowAliasRequestRequestTypeDef = TypedDict(
    "DeleteFlowAliasRequestRequestTypeDef",
    {
        "aliasIdentifier": str,
        "flowIdentifier": str,
    },
)
DeleteFlowRequestRequestTypeDef = TypedDict(
    "DeleteFlowRequestRequestTypeDef",
    {
        "flowIdentifier": str,
        "skipResourceInUseCheck": NotRequired[bool],
    },
)
DeleteFlowVersionRequestRequestTypeDef = TypedDict(
    "DeleteFlowVersionRequestRequestTypeDef",
    {
        "flowIdentifier": str,
        "flowVersion": str,
        "skipResourceInUseCheck": NotRequired[bool],
    },
)
DeleteKnowledgeBaseRequestRequestTypeDef = TypedDict(
    "DeleteKnowledgeBaseRequestRequestTypeDef",
    {
        "knowledgeBaseId": str,
    },
)
DeletePromptRequestRequestTypeDef = TypedDict(
    "DeletePromptRequestRequestTypeDef",
    {
        "promptIdentifier": str,
        "promptVersion": NotRequired[str],
    },
)
DisassociateAgentKnowledgeBaseRequestRequestTypeDef = TypedDict(
    "DisassociateAgentKnowledgeBaseRequestRequestTypeDef",
    {
        "agentId": str,
        "agentVersion": str,
        "knowledgeBaseId": str,
    },
)
FlowConditionalConnectionConfigurationTypeDef = TypedDict(
    "FlowConditionalConnectionConfigurationTypeDef",
    {
        "condition": str,
    },
)
FlowDataConnectionConfigurationTypeDef = TypedDict(
    "FlowDataConnectionConfigurationTypeDef",
    {
        "sourceOutput": str,
        "targetInput": str,
    },
)
KnowledgeBaseFlowNodeConfigurationTypeDef = TypedDict(
    "KnowledgeBaseFlowNodeConfigurationTypeDef",
    {
        "knowledgeBaseId": str,
        "modelId": NotRequired[str],
    },
)
LambdaFunctionFlowNodeConfigurationTypeDef = TypedDict(
    "LambdaFunctionFlowNodeConfigurationTypeDef",
    {
        "lambdaArn": str,
    },
)
LexFlowNodeConfigurationTypeDef = TypedDict(
    "LexFlowNodeConfigurationTypeDef",
    {
        "botAliasArn": str,
        "localeId": str,
    },
)
FlowNodeInputTypeDef = TypedDict(
    "FlowNodeInputTypeDef",
    {
        "expression": str,
        "name": str,
        "type": FlowNodeIODataTypeType,
    },
)
FlowNodeOutputTypeDef = TypedDict(
    "FlowNodeOutputTypeDef",
    {
        "name": str,
        "type": FlowNodeIODataTypeType,
    },
)
FlowSummaryTypeDef = TypedDict(
    "FlowSummaryTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "id": str,
        "name": str,
        "status": FlowStatusType,
        "updatedAt": datetime,
        "version": str,
        "description": NotRequired[str],
    },
)
FlowValidationTypeDef = TypedDict(
    "FlowValidationTypeDef",
    {
        "message": str,
        "severity": FlowValidationSeverityType,
    },
)
FlowVersionSummaryTypeDef = TypedDict(
    "FlowVersionSummaryTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "id": str,
        "status": FlowStatusType,
        "version": str,
    },
)
ParameterDetailTypeDef = TypedDict(
    "ParameterDetailTypeDef",
    {
        "type": TypeType,
        "description": NotRequired[str],
        "required": NotRequired[bool],
    },
)
GetAgentActionGroupRequestRequestTypeDef = TypedDict(
    "GetAgentActionGroupRequestRequestTypeDef",
    {
        "actionGroupId": str,
        "agentId": str,
        "agentVersion": str,
    },
)
GetAgentAliasRequestRequestTypeDef = TypedDict(
    "GetAgentAliasRequestRequestTypeDef",
    {
        "agentAliasId": str,
        "agentId": str,
    },
)
GetAgentKnowledgeBaseRequestRequestTypeDef = TypedDict(
    "GetAgentKnowledgeBaseRequestRequestTypeDef",
    {
        "agentId": str,
        "agentVersion": str,
        "knowledgeBaseId": str,
    },
)
GetAgentRequestRequestTypeDef = TypedDict(
    "GetAgentRequestRequestTypeDef",
    {
        "agentId": str,
    },
)
GetAgentVersionRequestRequestTypeDef = TypedDict(
    "GetAgentVersionRequestRequestTypeDef",
    {
        "agentId": str,
        "agentVersion": str,
    },
)
GetDataSourceRequestRequestTypeDef = TypedDict(
    "GetDataSourceRequestRequestTypeDef",
    {
        "dataSourceId": str,
        "knowledgeBaseId": str,
    },
)
GetFlowAliasRequestRequestTypeDef = TypedDict(
    "GetFlowAliasRequestRequestTypeDef",
    {
        "aliasIdentifier": str,
        "flowIdentifier": str,
    },
)
GetFlowRequestRequestTypeDef = TypedDict(
    "GetFlowRequestRequestTypeDef",
    {
        "flowIdentifier": str,
    },
)
GetFlowVersionRequestRequestTypeDef = TypedDict(
    "GetFlowVersionRequestRequestTypeDef",
    {
        "flowIdentifier": str,
        "flowVersion": str,
    },
)
GetIngestionJobRequestRequestTypeDef = TypedDict(
    "GetIngestionJobRequestRequestTypeDef",
    {
        "dataSourceId": str,
        "ingestionJobId": str,
        "knowledgeBaseId": str,
    },
)
GetKnowledgeBaseRequestRequestTypeDef = TypedDict(
    "GetKnowledgeBaseRequestRequestTypeDef",
    {
        "knowledgeBaseId": str,
    },
)
GetPromptRequestRequestTypeDef = TypedDict(
    "GetPromptRequestRequestTypeDef",
    {
        "promptIdentifier": str,
        "promptVersion": NotRequired[str],
    },
)
HierarchicalChunkingLevelConfigurationTypeDef = TypedDict(
    "HierarchicalChunkingLevelConfigurationTypeDef",
    {
        "maxTokens": int,
    },
)
InferenceConfigurationOutputTypeDef = TypedDict(
    "InferenceConfigurationOutputTypeDef",
    {
        "maximumLength": NotRequired[int],
        "stopSequences": NotRequired[List[str]],
        "temperature": NotRequired[float],
        "topK": NotRequired[int],
        "topP": NotRequired[float],
    },
)
InferenceConfigurationTypeDef = TypedDict(
    "InferenceConfigurationTypeDef",
    {
        "maximumLength": NotRequired[int],
        "stopSequences": NotRequired[Sequence[str]],
        "temperature": NotRequired[float],
        "topK": NotRequired[int],
        "topP": NotRequired[float],
    },
)
IngestionJobFilterTypeDef = TypedDict(
    "IngestionJobFilterTypeDef",
    {
        "attribute": Literal["STATUS"],
        "operator": Literal["EQ"],
        "values": Sequence[str],
    },
)
IngestionJobSortByTypeDef = TypedDict(
    "IngestionJobSortByTypeDef",
    {
        "attribute": IngestionJobSortByAttributeType,
        "order": SortOrderType,
    },
)
IngestionJobStatisticsTypeDef = TypedDict(
    "IngestionJobStatisticsTypeDef",
    {
        "numberOfDocumentsDeleted": NotRequired[int],
        "numberOfDocumentsFailed": NotRequired[int],
        "numberOfDocumentsScanned": NotRequired[int],
        "numberOfMetadataDocumentsModified": NotRequired[int],
        "numberOfMetadataDocumentsScanned": NotRequired[int],
        "numberOfModifiedDocumentsIndexed": NotRequired[int],
        "numberOfNewDocumentsIndexed": NotRequired[int],
    },
)
S3LocationTypeDef = TypedDict(
    "S3LocationTypeDef",
    {
        "uri": str,
    },
)
KnowledgeBaseSummaryTypeDef = TypedDict(
    "KnowledgeBaseSummaryTypeDef",
    {
        "knowledgeBaseId": str,
        "name": str,
        "status": KnowledgeBaseStatusType,
        "updatedAt": datetime,
        "description": NotRequired[str],
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
ListAgentActionGroupsRequestRequestTypeDef = TypedDict(
    "ListAgentActionGroupsRequestRequestTypeDef",
    {
        "agentId": str,
        "agentVersion": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
ListAgentAliasesRequestRequestTypeDef = TypedDict(
    "ListAgentAliasesRequestRequestTypeDef",
    {
        "agentId": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
ListAgentKnowledgeBasesRequestRequestTypeDef = TypedDict(
    "ListAgentKnowledgeBasesRequestRequestTypeDef",
    {
        "agentId": str,
        "agentVersion": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
ListAgentVersionsRequestRequestTypeDef = TypedDict(
    "ListAgentVersionsRequestRequestTypeDef",
    {
        "agentId": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
ListAgentsRequestRequestTypeDef = TypedDict(
    "ListAgentsRequestRequestTypeDef",
    {
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
ListDataSourcesRequestRequestTypeDef = TypedDict(
    "ListDataSourcesRequestRequestTypeDef",
    {
        "knowledgeBaseId": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
ListFlowAliasesRequestRequestTypeDef = TypedDict(
    "ListFlowAliasesRequestRequestTypeDef",
    {
        "flowIdentifier": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
ListFlowVersionsRequestRequestTypeDef = TypedDict(
    "ListFlowVersionsRequestRequestTypeDef",
    {
        "flowIdentifier": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
ListFlowsRequestRequestTypeDef = TypedDict(
    "ListFlowsRequestRequestTypeDef",
    {
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
ListPromptsRequestRequestTypeDef = TypedDict(
    "ListPromptsRequestRequestTypeDef",
    {
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
        "promptIdentifier": NotRequired[str],
    },
)
PromptSummaryTypeDef = TypedDict(
    "PromptSummaryTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "id": str,
        "name": str,
        "updatedAt": datetime,
        "version": str,
        "description": NotRequired[str],
    },
)
ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)
MongoDbAtlasFieldMappingTypeDef = TypedDict(
    "MongoDbAtlasFieldMappingTypeDef",
    {
        "metadataField": str,
        "textField": str,
        "vectorField": str,
    },
)
OpenSearchServerlessFieldMappingTypeDef = TypedDict(
    "OpenSearchServerlessFieldMappingTypeDef",
    {
        "metadataField": str,
        "textField": str,
        "vectorField": str,
    },
)
PatternObjectFilterOutputTypeDef = TypedDict(
    "PatternObjectFilterOutputTypeDef",
    {
        "objectType": str,
        "exclusionFilters": NotRequired[List[str]],
        "inclusionFilters": NotRequired[List[str]],
    },
)
PatternObjectFilterTypeDef = TypedDict(
    "PatternObjectFilterTypeDef",
    {
        "objectType": str,
        "exclusionFilters": NotRequired[Sequence[str]],
        "inclusionFilters": NotRequired[Sequence[str]],
    },
)
PineconeFieldMappingTypeDef = TypedDict(
    "PineconeFieldMappingTypeDef",
    {
        "metadataField": str,
        "textField": str,
    },
)
PrepareAgentRequestRequestTypeDef = TypedDict(
    "PrepareAgentRequestRequestTypeDef",
    {
        "agentId": str,
    },
)
PrepareFlowRequestRequestTypeDef = TypedDict(
    "PrepareFlowRequestRequestTypeDef",
    {
        "flowIdentifier": str,
    },
)
PromptFlowNodeResourceConfigurationTypeDef = TypedDict(
    "PromptFlowNodeResourceConfigurationTypeDef",
    {
        "promptArn": str,
    },
)
PromptModelInferenceConfigurationOutputTypeDef = TypedDict(
    "PromptModelInferenceConfigurationOutputTypeDef",
    {
        "maxTokens": NotRequired[int],
        "stopSequences": NotRequired[List[str]],
        "temperature": NotRequired[float],
        "topK": NotRequired[int],
        "topP": NotRequired[float],
    },
)
PromptModelInferenceConfigurationTypeDef = TypedDict(
    "PromptModelInferenceConfigurationTypeDef",
    {
        "maxTokens": NotRequired[int],
        "stopSequences": NotRequired[Sequence[str]],
        "temperature": NotRequired[float],
        "topK": NotRequired[int],
        "topP": NotRequired[float],
    },
)
PromptInputVariableTypeDef = TypedDict(
    "PromptInputVariableTypeDef",
    {
        "name": NotRequired[str],
    },
)
PromptMetadataEntryTypeDef = TypedDict(
    "PromptMetadataEntryTypeDef",
    {
        "key": str,
        "value": str,
    },
)
RdsFieldMappingTypeDef = TypedDict(
    "RdsFieldMappingTypeDef",
    {
        "metadataField": str,
        "primaryKeyField": str,
        "textField": str,
        "vectorField": str,
    },
)
RedisEnterpriseCloudFieldMappingTypeDef = TypedDict(
    "RedisEnterpriseCloudFieldMappingTypeDef",
    {
        "metadataField": str,
        "textField": str,
        "vectorField": str,
    },
)
RetrievalFlowNodeS3ConfigurationTypeDef = TypedDict(
    "RetrievalFlowNodeS3ConfigurationTypeDef",
    {
        "bucketName": str,
    },
)
SalesforceSourceConfigurationTypeDef = TypedDict(
    "SalesforceSourceConfigurationTypeDef",
    {
        "authType": Literal["OAUTH2_CLIENT_CREDENTIALS"],
        "credentialsSecretArn": str,
        "hostUrl": str,
    },
)
SeedUrlTypeDef = TypedDict(
    "SeedUrlTypeDef",
    {
        "url": NotRequired[str],
    },
)
SharePointSourceConfigurationOutputTypeDef = TypedDict(
    "SharePointSourceConfigurationOutputTypeDef",
    {
        "authType": Literal["OAUTH2_CLIENT_CREDENTIALS"],
        "credentialsSecretArn": str,
        "domain": str,
        "hostType": Literal["ONLINE"],
        "siteUrls": List[str],
        "tenantId": NotRequired[str],
    },
)
SharePointSourceConfigurationTypeDef = TypedDict(
    "SharePointSourceConfigurationTypeDef",
    {
        "authType": Literal["OAUTH2_CLIENT_CREDENTIALS"],
        "credentialsSecretArn": str,
        "domain": str,
        "hostType": Literal["ONLINE"],
        "siteUrls": Sequence[str],
        "tenantId": NotRequired[str],
    },
)
StartIngestionJobRequestRequestTypeDef = TypedDict(
    "StartIngestionJobRequestRequestTypeDef",
    {
        "dataSourceId": str,
        "knowledgeBaseId": str,
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
    },
)
StorageFlowNodeS3ConfigurationTypeDef = TypedDict(
    "StorageFlowNodeS3ConfigurationTypeDef",
    {
        "bucketName": str,
    },
)
TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Mapping[str, str],
    },
)
TransformationLambdaConfigurationTypeDef = TypedDict(
    "TransformationLambdaConfigurationTypeDef",
    {
        "lambdaArn": str,
    },
)
UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)
UpdateAgentKnowledgeBaseRequestRequestTypeDef = TypedDict(
    "UpdateAgentKnowledgeBaseRequestRequestTypeDef",
    {
        "agentId": str,
        "agentVersion": str,
        "knowledgeBaseId": str,
        "description": NotRequired[str],
        "knowledgeBaseState": NotRequired[KnowledgeBaseStateType],
    },
)
WebCrawlerLimitsTypeDef = TypedDict(
    "WebCrawlerLimitsTypeDef",
    {
        "rateLimit": NotRequired[int],
    },
)
APISchemaTypeDef = TypedDict(
    "APISchemaTypeDef",
    {
        "payload": NotRequired[str],
        "s3": NotRequired[S3IdentifierTypeDef],
    },
)
AgentAliasHistoryEventTypeDef = TypedDict(
    "AgentAliasHistoryEventTypeDef",
    {
        "endDate": NotRequired[datetime],
        "routingConfiguration": NotRequired[List[AgentAliasRoutingConfigurationListItemTypeDef]],
        "startDate": NotRequired[datetime],
    },
)
AgentAliasSummaryTypeDef = TypedDict(
    "AgentAliasSummaryTypeDef",
    {
        "agentAliasId": str,
        "agentAliasName": str,
        "agentAliasStatus": AgentAliasStatusType,
        "createdAt": datetime,
        "updatedAt": datetime,
        "description": NotRequired[str],
        "routingConfiguration": NotRequired[List[AgentAliasRoutingConfigurationListItemTypeDef]],
    },
)
CreateAgentAliasRequestRequestTypeDef = TypedDict(
    "CreateAgentAliasRequestRequestTypeDef",
    {
        "agentAliasName": str,
        "agentId": str,
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
        "routingConfiguration": NotRequired[
            Sequence[AgentAliasRoutingConfigurationListItemTypeDef]
        ],
        "tags": NotRequired[Mapping[str, str]],
    },
)
UpdateAgentAliasRequestRequestTypeDef = TypedDict(
    "UpdateAgentAliasRequestRequestTypeDef",
    {
        "agentAliasId": str,
        "agentAliasName": str,
        "agentId": str,
        "description": NotRequired[str],
        "routingConfiguration": NotRequired[
            Sequence[AgentAliasRoutingConfigurationListItemTypeDef]
        ],
    },
)
AgentSummaryTypeDef = TypedDict(
    "AgentSummaryTypeDef",
    {
        "agentId": str,
        "agentName": str,
        "agentStatus": AgentStatusType,
        "updatedAt": datetime,
        "description": NotRequired[str],
        "guardrailConfiguration": NotRequired[GuardrailConfigurationTypeDef],
        "latestAgentVersion": NotRequired[str],
    },
)
AgentVersionSummaryTypeDef = TypedDict(
    "AgentVersionSummaryTypeDef",
    {
        "agentName": str,
        "agentStatus": AgentStatusType,
        "agentVersion": str,
        "createdAt": datetime,
        "updatedAt": datetime,
        "description": NotRequired[str],
        "guardrailConfiguration": NotRequired[GuardrailConfigurationTypeDef],
    },
)
AssociateAgentKnowledgeBaseResponseTypeDef = TypedDict(
    "AssociateAgentKnowledgeBaseResponseTypeDef",
    {
        "agentKnowledgeBase": AgentKnowledgeBaseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteAgentAliasResponseTypeDef = TypedDict(
    "DeleteAgentAliasResponseTypeDef",
    {
        "agentAliasId": str,
        "agentAliasStatus": AgentAliasStatusType,
        "agentId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteAgentResponseTypeDef = TypedDict(
    "DeleteAgentResponseTypeDef",
    {
        "agentId": str,
        "agentStatus": AgentStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteAgentVersionResponseTypeDef = TypedDict(
    "DeleteAgentVersionResponseTypeDef",
    {
        "agentId": str,
        "agentStatus": AgentStatusType,
        "agentVersion": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteDataSourceResponseTypeDef = TypedDict(
    "DeleteDataSourceResponseTypeDef",
    {
        "dataSourceId": str,
        "knowledgeBaseId": str,
        "status": DataSourceStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteFlowAliasResponseTypeDef = TypedDict(
    "DeleteFlowAliasResponseTypeDef",
    {
        "flowId": str,
        "id": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteFlowResponseTypeDef = TypedDict(
    "DeleteFlowResponseTypeDef",
    {
        "id": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteFlowVersionResponseTypeDef = TypedDict(
    "DeleteFlowVersionResponseTypeDef",
    {
        "id": str,
        "version": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteKnowledgeBaseResponseTypeDef = TypedDict(
    "DeleteKnowledgeBaseResponseTypeDef",
    {
        "knowledgeBaseId": str,
        "status": KnowledgeBaseStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeletePromptResponseTypeDef = TypedDict(
    "DeletePromptResponseTypeDef",
    {
        "id": str,
        "version": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetAgentKnowledgeBaseResponseTypeDef = TypedDict(
    "GetAgentKnowledgeBaseResponseTypeDef",
    {
        "agentKnowledgeBase": AgentKnowledgeBaseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListAgentActionGroupsResponseTypeDef = TypedDict(
    "ListAgentActionGroupsResponseTypeDef",
    {
        "actionGroupSummaries": List[ActionGroupSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListAgentKnowledgeBasesResponseTypeDef = TypedDict(
    "ListAgentKnowledgeBasesResponseTypeDef",
    {
        "agentKnowledgeBaseSummaries": List[AgentKnowledgeBaseSummaryTypeDef],
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
PrepareAgentResponseTypeDef = TypedDict(
    "PrepareAgentResponseTypeDef",
    {
        "agentId": str,
        "agentStatus": AgentStatusType,
        "agentVersion": str,
        "preparedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
PrepareFlowResponseTypeDef = TypedDict(
    "PrepareFlowResponseTypeDef",
    {
        "id": str,
        "status": FlowStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateAgentKnowledgeBaseResponseTypeDef = TypedDict(
    "UpdateAgentKnowledgeBaseResponseTypeDef",
    {
        "agentKnowledgeBase": AgentKnowledgeBaseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
EmbeddingModelConfigurationTypeDef = TypedDict(
    "EmbeddingModelConfigurationTypeDef",
    {
        "bedrockEmbeddingModelConfiguration": NotRequired[
            BedrockEmbeddingModelConfigurationTypeDef
        ],
    },
)
BedrockFoundationModelConfigurationTypeDef = TypedDict(
    "BedrockFoundationModelConfigurationTypeDef",
    {
        "modelArn": str,
        "parsingPrompt": NotRequired[ParsingPromptTypeDef],
    },
)
ConditionFlowNodeConfigurationOutputTypeDef = TypedDict(
    "ConditionFlowNodeConfigurationOutputTypeDef",
    {
        "conditions": List[FlowConditionTypeDef],
    },
)
ConditionFlowNodeConfigurationTypeDef = TypedDict(
    "ConditionFlowNodeConfigurationTypeDef",
    {
        "conditions": Sequence[FlowConditionTypeDef],
    },
)
CreateFlowAliasRequestRequestTypeDef = TypedDict(
    "CreateFlowAliasRequestRequestTypeDef",
    {
        "flowIdentifier": str,
        "name": str,
        "routingConfiguration": Sequence[FlowAliasRoutingConfigurationListItemTypeDef],
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
    },
)
CreateFlowAliasResponseTypeDef = TypedDict(
    "CreateFlowAliasResponseTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "description": str,
        "flowId": str,
        "id": str,
        "name": str,
        "routingConfiguration": List[FlowAliasRoutingConfigurationListItemTypeDef],
        "updatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
FlowAliasSummaryTypeDef = TypedDict(
    "FlowAliasSummaryTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "flowId": str,
        "id": str,
        "name": str,
        "routingConfiguration": List[FlowAliasRoutingConfigurationListItemTypeDef],
        "updatedAt": datetime,
        "description": NotRequired[str],
    },
)
GetFlowAliasResponseTypeDef = TypedDict(
    "GetFlowAliasResponseTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "description": str,
        "flowId": str,
        "id": str,
        "name": str,
        "routingConfiguration": List[FlowAliasRoutingConfigurationListItemTypeDef],
        "updatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateFlowAliasRequestRequestTypeDef = TypedDict(
    "UpdateFlowAliasRequestRequestTypeDef",
    {
        "aliasIdentifier": str,
        "flowIdentifier": str,
        "name": str,
        "routingConfiguration": Sequence[FlowAliasRoutingConfigurationListItemTypeDef],
        "description": NotRequired[str],
    },
)
UpdateFlowAliasResponseTypeDef = TypedDict(
    "UpdateFlowAliasResponseTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "description": str,
        "flowId": str,
        "id": str,
        "name": str,
        "routingConfiguration": List[FlowAliasRoutingConfigurationListItemTypeDef],
        "updatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListDataSourcesResponseTypeDef = TypedDict(
    "ListDataSourcesResponseTypeDef",
    {
        "dataSourceSummaries": List[DataSourceSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
FlowConnectionConfigurationTypeDef = TypedDict(
    "FlowConnectionConfigurationTypeDef",
    {
        "conditional": NotRequired[FlowConditionalConnectionConfigurationTypeDef],
        "data": NotRequired[FlowDataConnectionConfigurationTypeDef],
    },
)
ListFlowsResponseTypeDef = TypedDict(
    "ListFlowsResponseTypeDef",
    {
        "flowSummaries": List[FlowSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListFlowVersionsResponseTypeDef = TypedDict(
    "ListFlowVersionsResponseTypeDef",
    {
        "flowVersionSummaries": List[FlowVersionSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
FunctionOutputTypeDef = TypedDict(
    "FunctionOutputTypeDef",
    {
        "name": str,
        "description": NotRequired[str],
        "parameters": NotRequired[Dict[str, ParameterDetailTypeDef]],
        "requireConfirmation": NotRequired[RequireConfirmationType],
    },
)
FunctionTypeDef = TypedDict(
    "FunctionTypeDef",
    {
        "name": str,
        "description": NotRequired[str],
        "parameters": NotRequired[Mapping[str, ParameterDetailTypeDef]],
        "requireConfirmation": NotRequired[RequireConfirmationType],
    },
)
HierarchicalChunkingConfigurationOutputTypeDef = TypedDict(
    "HierarchicalChunkingConfigurationOutputTypeDef",
    {
        "levelConfigurations": List[HierarchicalChunkingLevelConfigurationTypeDef],
        "overlapTokens": int,
    },
)
HierarchicalChunkingConfigurationTypeDef = TypedDict(
    "HierarchicalChunkingConfigurationTypeDef",
    {
        "levelConfigurations": Sequence[HierarchicalChunkingLevelConfigurationTypeDef],
        "overlapTokens": int,
    },
)
PromptConfigurationOutputTypeDef = TypedDict(
    "PromptConfigurationOutputTypeDef",
    {
        "basePromptTemplate": NotRequired[str],
        "inferenceConfiguration": NotRequired[InferenceConfigurationOutputTypeDef],
        "parserMode": NotRequired[CreationModeType],
        "promptCreationMode": NotRequired[CreationModeType],
        "promptState": NotRequired[PromptStateType],
        "promptType": NotRequired[PromptTypeType],
    },
)
PromptConfigurationTypeDef = TypedDict(
    "PromptConfigurationTypeDef",
    {
        "basePromptTemplate": NotRequired[str],
        "inferenceConfiguration": NotRequired[InferenceConfigurationTypeDef],
        "parserMode": NotRequired[CreationModeType],
        "promptCreationMode": NotRequired[CreationModeType],
        "promptState": NotRequired[PromptStateType],
        "promptType": NotRequired[PromptTypeType],
    },
)
ListIngestionJobsRequestRequestTypeDef = TypedDict(
    "ListIngestionJobsRequestRequestTypeDef",
    {
        "dataSourceId": str,
        "knowledgeBaseId": str,
        "filters": NotRequired[Sequence[IngestionJobFilterTypeDef]],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
        "sortBy": NotRequired[IngestionJobSortByTypeDef],
    },
)
IngestionJobSummaryTypeDef = TypedDict(
    "IngestionJobSummaryTypeDef",
    {
        "dataSourceId": str,
        "ingestionJobId": str,
        "knowledgeBaseId": str,
        "startedAt": datetime,
        "status": IngestionJobStatusType,
        "updatedAt": datetime,
        "description": NotRequired[str],
        "statistics": NotRequired[IngestionJobStatisticsTypeDef],
    },
)
IngestionJobTypeDef = TypedDict(
    "IngestionJobTypeDef",
    {
        "dataSourceId": str,
        "ingestionJobId": str,
        "knowledgeBaseId": str,
        "startedAt": datetime,
        "status": IngestionJobStatusType,
        "updatedAt": datetime,
        "description": NotRequired[str],
        "failureReasons": NotRequired[List[str]],
        "statistics": NotRequired[IngestionJobStatisticsTypeDef],
    },
)
IntermediateStorageTypeDef = TypedDict(
    "IntermediateStorageTypeDef",
    {
        "s3Location": S3LocationTypeDef,
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
ListAgentActionGroupsRequestListAgentActionGroupsPaginateTypeDef = TypedDict(
    "ListAgentActionGroupsRequestListAgentActionGroupsPaginateTypeDef",
    {
        "agentId": str,
        "agentVersion": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListAgentAliasesRequestListAgentAliasesPaginateTypeDef = TypedDict(
    "ListAgentAliasesRequestListAgentAliasesPaginateTypeDef",
    {
        "agentId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListAgentKnowledgeBasesRequestListAgentKnowledgeBasesPaginateTypeDef = TypedDict(
    "ListAgentKnowledgeBasesRequestListAgentKnowledgeBasesPaginateTypeDef",
    {
        "agentId": str,
        "agentVersion": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListAgentVersionsRequestListAgentVersionsPaginateTypeDef = TypedDict(
    "ListAgentVersionsRequestListAgentVersionsPaginateTypeDef",
    {
        "agentId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListAgentsRequestListAgentsPaginateTypeDef = TypedDict(
    "ListAgentsRequestListAgentsPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListDataSourcesRequestListDataSourcesPaginateTypeDef = TypedDict(
    "ListDataSourcesRequestListDataSourcesPaginateTypeDef",
    {
        "knowledgeBaseId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListFlowAliasesRequestListFlowAliasesPaginateTypeDef = TypedDict(
    "ListFlowAliasesRequestListFlowAliasesPaginateTypeDef",
    {
        "flowIdentifier": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListFlowVersionsRequestListFlowVersionsPaginateTypeDef = TypedDict(
    "ListFlowVersionsRequestListFlowVersionsPaginateTypeDef",
    {
        "flowIdentifier": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListFlowsRequestListFlowsPaginateTypeDef = TypedDict(
    "ListFlowsRequestListFlowsPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListIngestionJobsRequestListIngestionJobsPaginateTypeDef = TypedDict(
    "ListIngestionJobsRequestListIngestionJobsPaginateTypeDef",
    {
        "dataSourceId": str,
        "knowledgeBaseId": str,
        "filters": NotRequired[Sequence[IngestionJobFilterTypeDef]],
        "sortBy": NotRequired[IngestionJobSortByTypeDef],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListKnowledgeBasesRequestListKnowledgeBasesPaginateTypeDef = TypedDict(
    "ListKnowledgeBasesRequestListKnowledgeBasesPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListPromptsRequestListPromptsPaginateTypeDef = TypedDict(
    "ListPromptsRequestListPromptsPaginateTypeDef",
    {
        "promptIdentifier": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListPromptsResponseTypeDef = TypedDict(
    "ListPromptsResponseTypeDef",
    {
        "nextToken": str,
        "promptSummaries": List[PromptSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
MongoDbAtlasConfigurationTypeDef = TypedDict(
    "MongoDbAtlasConfigurationTypeDef",
    {
        "collectionName": str,
        "credentialsSecretArn": str,
        "databaseName": str,
        "endpoint": str,
        "fieldMapping": MongoDbAtlasFieldMappingTypeDef,
        "vectorIndexName": str,
        "endpointServiceName": NotRequired[str],
    },
)
OpenSearchServerlessConfigurationTypeDef = TypedDict(
    "OpenSearchServerlessConfigurationTypeDef",
    {
        "collectionArn": str,
        "fieldMapping": OpenSearchServerlessFieldMappingTypeDef,
        "vectorIndexName": str,
    },
)
PatternObjectFilterConfigurationOutputTypeDef = TypedDict(
    "PatternObjectFilterConfigurationOutputTypeDef",
    {
        "filters": List[PatternObjectFilterOutputTypeDef],
    },
)
PatternObjectFilterConfigurationTypeDef = TypedDict(
    "PatternObjectFilterConfigurationTypeDef",
    {
        "filters": Sequence[PatternObjectFilterTypeDef],
    },
)
PineconeConfigurationTypeDef = TypedDict(
    "PineconeConfigurationTypeDef",
    {
        "connectionString": str,
        "credentialsSecretArn": str,
        "fieldMapping": PineconeFieldMappingTypeDef,
        "namespace": NotRequired[str],
    },
)
PromptInferenceConfigurationOutputTypeDef = TypedDict(
    "PromptInferenceConfigurationOutputTypeDef",
    {
        "text": NotRequired[PromptModelInferenceConfigurationOutputTypeDef],
    },
)
PromptInferenceConfigurationTypeDef = TypedDict(
    "PromptInferenceConfigurationTypeDef",
    {
        "text": NotRequired[PromptModelInferenceConfigurationTypeDef],
    },
)
TextPromptTemplateConfigurationOutputTypeDef = TypedDict(
    "TextPromptTemplateConfigurationOutputTypeDef",
    {
        "text": str,
        "inputVariables": NotRequired[List[PromptInputVariableTypeDef]],
    },
)
TextPromptTemplateConfigurationTypeDef = TypedDict(
    "TextPromptTemplateConfigurationTypeDef",
    {
        "text": str,
        "inputVariables": NotRequired[Sequence[PromptInputVariableTypeDef]],
    },
)
RdsConfigurationTypeDef = TypedDict(
    "RdsConfigurationTypeDef",
    {
        "credentialsSecretArn": str,
        "databaseName": str,
        "fieldMapping": RdsFieldMappingTypeDef,
        "resourceArn": str,
        "tableName": str,
    },
)
RedisEnterpriseCloudConfigurationTypeDef = TypedDict(
    "RedisEnterpriseCloudConfigurationTypeDef",
    {
        "credentialsSecretArn": str,
        "endpoint": str,
        "fieldMapping": RedisEnterpriseCloudFieldMappingTypeDef,
        "vectorIndexName": str,
    },
)
RetrievalFlowNodeServiceConfigurationTypeDef = TypedDict(
    "RetrievalFlowNodeServiceConfigurationTypeDef",
    {
        "s3": NotRequired[RetrievalFlowNodeS3ConfigurationTypeDef],
    },
)
UrlConfigurationOutputTypeDef = TypedDict(
    "UrlConfigurationOutputTypeDef",
    {
        "seedUrls": NotRequired[List[SeedUrlTypeDef]],
    },
)
UrlConfigurationTypeDef = TypedDict(
    "UrlConfigurationTypeDef",
    {
        "seedUrls": NotRequired[Sequence[SeedUrlTypeDef]],
    },
)
StorageFlowNodeServiceConfigurationTypeDef = TypedDict(
    "StorageFlowNodeServiceConfigurationTypeDef",
    {
        "s3": NotRequired[StorageFlowNodeS3ConfigurationTypeDef],
    },
)
TransformationFunctionTypeDef = TypedDict(
    "TransformationFunctionTypeDef",
    {
        "transformationLambdaConfiguration": TransformationLambdaConfigurationTypeDef,
    },
)
WebCrawlerConfigurationOutputTypeDef = TypedDict(
    "WebCrawlerConfigurationOutputTypeDef",
    {
        "crawlerLimits": NotRequired[WebCrawlerLimitsTypeDef],
        "exclusionFilters": NotRequired[List[str]],
        "inclusionFilters": NotRequired[List[str]],
        "scope": NotRequired[WebScopeTypeType],
    },
)
WebCrawlerConfigurationTypeDef = TypedDict(
    "WebCrawlerConfigurationTypeDef",
    {
        "crawlerLimits": NotRequired[WebCrawlerLimitsTypeDef],
        "exclusionFilters": NotRequired[Sequence[str]],
        "inclusionFilters": NotRequired[Sequence[str]],
        "scope": NotRequired[WebScopeTypeType],
    },
)
AgentAliasTypeDef = TypedDict(
    "AgentAliasTypeDef",
    {
        "agentAliasArn": str,
        "agentAliasId": str,
        "agentAliasName": str,
        "agentAliasStatus": AgentAliasStatusType,
        "agentId": str,
        "createdAt": datetime,
        "routingConfiguration": List[AgentAliasRoutingConfigurationListItemTypeDef],
        "updatedAt": datetime,
        "agentAliasHistoryEvents": NotRequired[List[AgentAliasHistoryEventTypeDef]],
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
        "failureReasons": NotRequired[List[str]],
    },
)
ListAgentAliasesResponseTypeDef = TypedDict(
    "ListAgentAliasesResponseTypeDef",
    {
        "agentAliasSummaries": List[AgentAliasSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListAgentsResponseTypeDef = TypedDict(
    "ListAgentsResponseTypeDef",
    {
        "agentSummaries": List[AgentSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListAgentVersionsResponseTypeDef = TypedDict(
    "ListAgentVersionsResponseTypeDef",
    {
        "agentVersionSummaries": List[AgentVersionSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
VectorKnowledgeBaseConfigurationTypeDef = TypedDict(
    "VectorKnowledgeBaseConfigurationTypeDef",
    {
        "embeddingModelArn": str,
        "embeddingModelConfiguration": NotRequired[EmbeddingModelConfigurationTypeDef],
    },
)
ParsingConfigurationTypeDef = TypedDict(
    "ParsingConfigurationTypeDef",
    {
        "parsingStrategy": Literal["BEDROCK_FOUNDATION_MODEL"],
        "bedrockFoundationModelConfiguration": NotRequired[
            BedrockFoundationModelConfigurationTypeDef
        ],
    },
)
ListFlowAliasesResponseTypeDef = TypedDict(
    "ListFlowAliasesResponseTypeDef",
    {
        "flowAliasSummaries": List[FlowAliasSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
FlowConnectionTypeDef = TypedDict(
    "FlowConnectionTypeDef",
    {
        "name": str,
        "source": str,
        "target": str,
        "type": FlowConnectionTypeType,
        "configuration": NotRequired[FlowConnectionConfigurationTypeDef],
    },
)
FunctionSchemaOutputTypeDef = TypedDict(
    "FunctionSchemaOutputTypeDef",
    {
        "functions": NotRequired[List[FunctionOutputTypeDef]],
    },
)
FunctionSchemaTypeDef = TypedDict(
    "FunctionSchemaTypeDef",
    {
        "functions": NotRequired[Sequence[FunctionTypeDef]],
    },
)
ChunkingConfigurationOutputTypeDef = TypedDict(
    "ChunkingConfigurationOutputTypeDef",
    {
        "chunkingStrategy": ChunkingStrategyType,
        "fixedSizeChunkingConfiguration": NotRequired[FixedSizeChunkingConfigurationTypeDef],
        "hierarchicalChunkingConfiguration": NotRequired[
            HierarchicalChunkingConfigurationOutputTypeDef
        ],
        "semanticChunkingConfiguration": NotRequired[SemanticChunkingConfigurationTypeDef],
    },
)
ChunkingConfigurationTypeDef = TypedDict(
    "ChunkingConfigurationTypeDef",
    {
        "chunkingStrategy": ChunkingStrategyType,
        "fixedSizeChunkingConfiguration": NotRequired[FixedSizeChunkingConfigurationTypeDef],
        "hierarchicalChunkingConfiguration": NotRequired[HierarchicalChunkingConfigurationTypeDef],
        "semanticChunkingConfiguration": NotRequired[SemanticChunkingConfigurationTypeDef],
    },
)
PromptOverrideConfigurationOutputTypeDef = TypedDict(
    "PromptOverrideConfigurationOutputTypeDef",
    {
        "promptConfigurations": List[PromptConfigurationOutputTypeDef],
        "overrideLambda": NotRequired[str],
    },
)
PromptOverrideConfigurationTypeDef = TypedDict(
    "PromptOverrideConfigurationTypeDef",
    {
        "promptConfigurations": Sequence[PromptConfigurationTypeDef],
        "overrideLambda": NotRequired[str],
    },
)
ListIngestionJobsResponseTypeDef = TypedDict(
    "ListIngestionJobsResponseTypeDef",
    {
        "ingestionJobSummaries": List[IngestionJobSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetIngestionJobResponseTypeDef = TypedDict(
    "GetIngestionJobResponseTypeDef",
    {
        "ingestionJob": IngestionJobTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
StartIngestionJobResponseTypeDef = TypedDict(
    "StartIngestionJobResponseTypeDef",
    {
        "ingestionJob": IngestionJobTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CrawlFilterConfigurationOutputTypeDef = TypedDict(
    "CrawlFilterConfigurationOutputTypeDef",
    {
        "type": Literal["PATTERN"],
        "patternObjectFilter": NotRequired[PatternObjectFilterConfigurationOutputTypeDef],
    },
)
CrawlFilterConfigurationTypeDef = TypedDict(
    "CrawlFilterConfigurationTypeDef",
    {
        "type": Literal["PATTERN"],
        "patternObjectFilter": NotRequired[PatternObjectFilterConfigurationTypeDef],
    },
)
PromptTemplateConfigurationOutputTypeDef = TypedDict(
    "PromptTemplateConfigurationOutputTypeDef",
    {
        "text": NotRequired[TextPromptTemplateConfigurationOutputTypeDef],
    },
)
PromptTemplateConfigurationTypeDef = TypedDict(
    "PromptTemplateConfigurationTypeDef",
    {
        "text": NotRequired[TextPromptTemplateConfigurationTypeDef],
    },
)
StorageConfigurationTypeDef = TypedDict(
    "StorageConfigurationTypeDef",
    {
        "type": KnowledgeBaseStorageTypeType,
        "mongoDbAtlasConfiguration": NotRequired[MongoDbAtlasConfigurationTypeDef],
        "opensearchServerlessConfiguration": NotRequired[OpenSearchServerlessConfigurationTypeDef],
        "pineconeConfiguration": NotRequired[PineconeConfigurationTypeDef],
        "rdsConfiguration": NotRequired[RdsConfigurationTypeDef],
        "redisEnterpriseCloudConfiguration": NotRequired[RedisEnterpriseCloudConfigurationTypeDef],
    },
)
RetrievalFlowNodeConfigurationTypeDef = TypedDict(
    "RetrievalFlowNodeConfigurationTypeDef",
    {
        "serviceConfiguration": RetrievalFlowNodeServiceConfigurationTypeDef,
    },
)
WebSourceConfigurationOutputTypeDef = TypedDict(
    "WebSourceConfigurationOutputTypeDef",
    {
        "urlConfiguration": UrlConfigurationOutputTypeDef,
    },
)
WebSourceConfigurationTypeDef = TypedDict(
    "WebSourceConfigurationTypeDef",
    {
        "urlConfiguration": UrlConfigurationTypeDef,
    },
)
StorageFlowNodeConfigurationTypeDef = TypedDict(
    "StorageFlowNodeConfigurationTypeDef",
    {
        "serviceConfiguration": StorageFlowNodeServiceConfigurationTypeDef,
    },
)
TransformationTypeDef = TypedDict(
    "TransformationTypeDef",
    {
        "stepToApply": Literal["POST_CHUNKING"],
        "transformationFunction": TransformationFunctionTypeDef,
    },
)
CreateAgentAliasResponseTypeDef = TypedDict(
    "CreateAgentAliasResponseTypeDef",
    {
        "agentAlias": AgentAliasTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetAgentAliasResponseTypeDef = TypedDict(
    "GetAgentAliasResponseTypeDef",
    {
        "agentAlias": AgentAliasTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateAgentAliasResponseTypeDef = TypedDict(
    "UpdateAgentAliasResponseTypeDef",
    {
        "agentAlias": AgentAliasTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
KnowledgeBaseConfigurationTypeDef = TypedDict(
    "KnowledgeBaseConfigurationTypeDef",
    {
        "type": Literal["VECTOR"],
        "vectorKnowledgeBaseConfiguration": NotRequired[VectorKnowledgeBaseConfigurationTypeDef],
    },
)
AgentActionGroupTypeDef = TypedDict(
    "AgentActionGroupTypeDef",
    {
        "actionGroupId": str,
        "actionGroupName": str,
        "actionGroupState": ActionGroupStateType,
        "agentId": str,
        "agentVersion": str,
        "createdAt": datetime,
        "updatedAt": datetime,
        "actionGroupExecutor": NotRequired[ActionGroupExecutorTypeDef],
        "apiSchema": NotRequired[APISchemaTypeDef],
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
        "functionSchema": NotRequired[FunctionSchemaOutputTypeDef],
        "parentActionSignature": NotRequired[ActionGroupSignatureType],
    },
)
CreateAgentActionGroupRequestRequestTypeDef = TypedDict(
    "CreateAgentActionGroupRequestRequestTypeDef",
    {
        "actionGroupName": str,
        "agentId": str,
        "agentVersion": str,
        "actionGroupExecutor": NotRequired[ActionGroupExecutorTypeDef],
        "actionGroupState": NotRequired[ActionGroupStateType],
        "apiSchema": NotRequired[APISchemaTypeDef],
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
        "functionSchema": NotRequired[FunctionSchemaTypeDef],
        "parentActionGroupSignature": NotRequired[ActionGroupSignatureType],
    },
)
UpdateAgentActionGroupRequestRequestTypeDef = TypedDict(
    "UpdateAgentActionGroupRequestRequestTypeDef",
    {
        "actionGroupId": str,
        "actionGroupName": str,
        "agentId": str,
        "agentVersion": str,
        "actionGroupExecutor": NotRequired[ActionGroupExecutorTypeDef],
        "actionGroupState": NotRequired[ActionGroupStateType],
        "apiSchema": NotRequired[APISchemaTypeDef],
        "description": NotRequired[str],
        "functionSchema": NotRequired[FunctionSchemaTypeDef],
        "parentActionGroupSignature": NotRequired[ActionGroupSignatureType],
    },
)
AgentTypeDef = TypedDict(
    "AgentTypeDef",
    {
        "agentArn": str,
        "agentId": str,
        "agentName": str,
        "agentResourceRoleArn": str,
        "agentStatus": AgentStatusType,
        "agentVersion": str,
        "createdAt": datetime,
        "idleSessionTTLInSeconds": int,
        "updatedAt": datetime,
        "clientToken": NotRequired[str],
        "customerEncryptionKeyArn": NotRequired[str],
        "description": NotRequired[str],
        "failureReasons": NotRequired[List[str]],
        "foundationModel": NotRequired[str],
        "guardrailConfiguration": NotRequired[GuardrailConfigurationTypeDef],
        "instruction": NotRequired[str],
        "memoryConfiguration": NotRequired[MemoryConfigurationOutputTypeDef],
        "preparedAt": NotRequired[datetime],
        "promptOverrideConfiguration": NotRequired[PromptOverrideConfigurationOutputTypeDef],
        "recommendedActions": NotRequired[List[str]],
    },
)
AgentVersionTypeDef = TypedDict(
    "AgentVersionTypeDef",
    {
        "agentArn": str,
        "agentId": str,
        "agentName": str,
        "agentResourceRoleArn": str,
        "agentStatus": AgentStatusType,
        "createdAt": datetime,
        "idleSessionTTLInSeconds": int,
        "updatedAt": datetime,
        "version": str,
        "customerEncryptionKeyArn": NotRequired[str],
        "description": NotRequired[str],
        "failureReasons": NotRequired[List[str]],
        "foundationModel": NotRequired[str],
        "guardrailConfiguration": NotRequired[GuardrailConfigurationTypeDef],
        "instruction": NotRequired[str],
        "memoryConfiguration": NotRequired[MemoryConfigurationOutputTypeDef],
        "promptOverrideConfiguration": NotRequired[PromptOverrideConfigurationOutputTypeDef],
        "recommendedActions": NotRequired[List[str]],
    },
)
CreateAgentRequestRequestTypeDef = TypedDict(
    "CreateAgentRequestRequestTypeDef",
    {
        "agentName": str,
        "agentResourceRoleArn": NotRequired[str],
        "clientToken": NotRequired[str],
        "customerEncryptionKeyArn": NotRequired[str],
        "description": NotRequired[str],
        "foundationModel": NotRequired[str],
        "guardrailConfiguration": NotRequired[GuardrailConfigurationTypeDef],
        "idleSessionTTLInSeconds": NotRequired[int],
        "instruction": NotRequired[str],
        "memoryConfiguration": NotRequired[MemoryConfigurationTypeDef],
        "promptOverrideConfiguration": NotRequired[PromptOverrideConfigurationTypeDef],
        "tags": NotRequired[Mapping[str, str]],
    },
)
UpdateAgentRequestRequestTypeDef = TypedDict(
    "UpdateAgentRequestRequestTypeDef",
    {
        "agentId": str,
        "agentName": str,
        "agentResourceRoleArn": str,
        "foundationModel": str,
        "customerEncryptionKeyArn": NotRequired[str],
        "description": NotRequired[str],
        "guardrailConfiguration": NotRequired[GuardrailConfigurationTypeDef],
        "idleSessionTTLInSeconds": NotRequired[int],
        "instruction": NotRequired[str],
        "memoryConfiguration": NotRequired[MemoryConfigurationTypeDef],
        "promptOverrideConfiguration": NotRequired[PromptOverrideConfigurationTypeDef],
    },
)
ConfluenceCrawlerConfigurationOutputTypeDef = TypedDict(
    "ConfluenceCrawlerConfigurationOutputTypeDef",
    {
        "filterConfiguration": NotRequired[CrawlFilterConfigurationOutputTypeDef],
    },
)
SalesforceCrawlerConfigurationOutputTypeDef = TypedDict(
    "SalesforceCrawlerConfigurationOutputTypeDef",
    {
        "filterConfiguration": NotRequired[CrawlFilterConfigurationOutputTypeDef],
    },
)
SharePointCrawlerConfigurationOutputTypeDef = TypedDict(
    "SharePointCrawlerConfigurationOutputTypeDef",
    {
        "filterConfiguration": NotRequired[CrawlFilterConfigurationOutputTypeDef],
    },
)
ConfluenceCrawlerConfigurationTypeDef = TypedDict(
    "ConfluenceCrawlerConfigurationTypeDef",
    {
        "filterConfiguration": NotRequired[CrawlFilterConfigurationTypeDef],
    },
)
SalesforceCrawlerConfigurationTypeDef = TypedDict(
    "SalesforceCrawlerConfigurationTypeDef",
    {
        "filterConfiguration": NotRequired[CrawlFilterConfigurationTypeDef],
    },
)
SharePointCrawlerConfigurationTypeDef = TypedDict(
    "SharePointCrawlerConfigurationTypeDef",
    {
        "filterConfiguration": NotRequired[CrawlFilterConfigurationTypeDef],
    },
)
PromptFlowNodeInlineConfigurationOutputTypeDef = TypedDict(
    "PromptFlowNodeInlineConfigurationOutputTypeDef",
    {
        "modelId": str,
        "templateConfiguration": PromptTemplateConfigurationOutputTypeDef,
        "templateType": Literal["TEXT"],
        "inferenceConfiguration": NotRequired[PromptInferenceConfigurationOutputTypeDef],
    },
)
PromptVariantOutputTypeDef = TypedDict(
    "PromptVariantOutputTypeDef",
    {
        "name": str,
        "templateType": Literal["TEXT"],
        "inferenceConfiguration": NotRequired[PromptInferenceConfigurationOutputTypeDef],
        "metadata": NotRequired[List[PromptMetadataEntryTypeDef]],
        "modelId": NotRequired[str],
        "templateConfiguration": NotRequired[PromptTemplateConfigurationOutputTypeDef],
    },
)
PromptFlowNodeInlineConfigurationTypeDef = TypedDict(
    "PromptFlowNodeInlineConfigurationTypeDef",
    {
        "modelId": str,
        "templateConfiguration": PromptTemplateConfigurationTypeDef,
        "templateType": Literal["TEXT"],
        "inferenceConfiguration": NotRequired[PromptInferenceConfigurationTypeDef],
    },
)
PromptVariantTypeDef = TypedDict(
    "PromptVariantTypeDef",
    {
        "name": str,
        "templateType": Literal["TEXT"],
        "inferenceConfiguration": NotRequired[PromptInferenceConfigurationTypeDef],
        "metadata": NotRequired[Sequence[PromptMetadataEntryTypeDef]],
        "modelId": NotRequired[str],
        "templateConfiguration": NotRequired[PromptTemplateConfigurationTypeDef],
    },
)
WebDataSourceConfigurationOutputTypeDef = TypedDict(
    "WebDataSourceConfigurationOutputTypeDef",
    {
        "sourceConfiguration": WebSourceConfigurationOutputTypeDef,
        "crawlerConfiguration": NotRequired[WebCrawlerConfigurationOutputTypeDef],
    },
)
WebDataSourceConfigurationTypeDef = TypedDict(
    "WebDataSourceConfigurationTypeDef",
    {
        "sourceConfiguration": WebSourceConfigurationTypeDef,
        "crawlerConfiguration": NotRequired[WebCrawlerConfigurationTypeDef],
    },
)
CustomTransformationConfigurationOutputTypeDef = TypedDict(
    "CustomTransformationConfigurationOutputTypeDef",
    {
        "intermediateStorage": IntermediateStorageTypeDef,
        "transformations": List[TransformationTypeDef],
    },
)
CustomTransformationConfigurationTypeDef = TypedDict(
    "CustomTransformationConfigurationTypeDef",
    {
        "intermediateStorage": IntermediateStorageTypeDef,
        "transformations": Sequence[TransformationTypeDef],
    },
)
CreateKnowledgeBaseRequestRequestTypeDef = TypedDict(
    "CreateKnowledgeBaseRequestRequestTypeDef",
    {
        "knowledgeBaseConfiguration": KnowledgeBaseConfigurationTypeDef,
        "name": str,
        "roleArn": str,
        "storageConfiguration": StorageConfigurationTypeDef,
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
    },
)
KnowledgeBaseTypeDef = TypedDict(
    "KnowledgeBaseTypeDef",
    {
        "createdAt": datetime,
        "knowledgeBaseArn": str,
        "knowledgeBaseConfiguration": KnowledgeBaseConfigurationTypeDef,
        "knowledgeBaseId": str,
        "name": str,
        "roleArn": str,
        "status": KnowledgeBaseStatusType,
        "storageConfiguration": StorageConfigurationTypeDef,
        "updatedAt": datetime,
        "description": NotRequired[str],
        "failureReasons": NotRequired[List[str]],
    },
)
UpdateKnowledgeBaseRequestRequestTypeDef = TypedDict(
    "UpdateKnowledgeBaseRequestRequestTypeDef",
    {
        "knowledgeBaseConfiguration": KnowledgeBaseConfigurationTypeDef,
        "knowledgeBaseId": str,
        "name": str,
        "roleArn": str,
        "storageConfiguration": StorageConfigurationTypeDef,
        "description": NotRequired[str],
    },
)
CreateAgentActionGroupResponseTypeDef = TypedDict(
    "CreateAgentActionGroupResponseTypeDef",
    {
        "agentActionGroup": AgentActionGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetAgentActionGroupResponseTypeDef = TypedDict(
    "GetAgentActionGroupResponseTypeDef",
    {
        "agentActionGroup": AgentActionGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateAgentActionGroupResponseTypeDef = TypedDict(
    "UpdateAgentActionGroupResponseTypeDef",
    {
        "agentActionGroup": AgentActionGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateAgentResponseTypeDef = TypedDict(
    "CreateAgentResponseTypeDef",
    {
        "agent": AgentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetAgentResponseTypeDef = TypedDict(
    "GetAgentResponseTypeDef",
    {
        "agent": AgentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateAgentResponseTypeDef = TypedDict(
    "UpdateAgentResponseTypeDef",
    {
        "agent": AgentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetAgentVersionResponseTypeDef = TypedDict(
    "GetAgentVersionResponseTypeDef",
    {
        "agentVersion": AgentVersionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ConfluenceDataSourceConfigurationOutputTypeDef = TypedDict(
    "ConfluenceDataSourceConfigurationOutputTypeDef",
    {
        "sourceConfiguration": ConfluenceSourceConfigurationTypeDef,
        "crawlerConfiguration": NotRequired[ConfluenceCrawlerConfigurationOutputTypeDef],
    },
)
SalesforceDataSourceConfigurationOutputTypeDef = TypedDict(
    "SalesforceDataSourceConfigurationOutputTypeDef",
    {
        "sourceConfiguration": SalesforceSourceConfigurationTypeDef,
        "crawlerConfiguration": NotRequired[SalesforceCrawlerConfigurationOutputTypeDef],
    },
)
SharePointDataSourceConfigurationOutputTypeDef = TypedDict(
    "SharePointDataSourceConfigurationOutputTypeDef",
    {
        "sourceConfiguration": SharePointSourceConfigurationOutputTypeDef,
        "crawlerConfiguration": NotRequired[SharePointCrawlerConfigurationOutputTypeDef],
    },
)
ConfluenceDataSourceConfigurationTypeDef = TypedDict(
    "ConfluenceDataSourceConfigurationTypeDef",
    {
        "sourceConfiguration": ConfluenceSourceConfigurationTypeDef,
        "crawlerConfiguration": NotRequired[ConfluenceCrawlerConfigurationTypeDef],
    },
)
SalesforceDataSourceConfigurationTypeDef = TypedDict(
    "SalesforceDataSourceConfigurationTypeDef",
    {
        "sourceConfiguration": SalesforceSourceConfigurationTypeDef,
        "crawlerConfiguration": NotRequired[SalesforceCrawlerConfigurationTypeDef],
    },
)
SharePointDataSourceConfigurationTypeDef = TypedDict(
    "SharePointDataSourceConfigurationTypeDef",
    {
        "sourceConfiguration": SharePointSourceConfigurationTypeDef,
        "crawlerConfiguration": NotRequired[SharePointCrawlerConfigurationTypeDef],
    },
)
PromptFlowNodeSourceConfigurationOutputTypeDef = TypedDict(
    "PromptFlowNodeSourceConfigurationOutputTypeDef",
    {
        "inline": NotRequired[PromptFlowNodeInlineConfigurationOutputTypeDef],
        "resource": NotRequired[PromptFlowNodeResourceConfigurationTypeDef],
    },
)
CreatePromptResponseTypeDef = TypedDict(
    "CreatePromptResponseTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "customerEncryptionKeyArn": str,
        "defaultVariant": str,
        "description": str,
        "id": str,
        "name": str,
        "updatedAt": datetime,
        "variants": List[PromptVariantOutputTypeDef],
        "version": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreatePromptVersionResponseTypeDef = TypedDict(
    "CreatePromptVersionResponseTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "customerEncryptionKeyArn": str,
        "defaultVariant": str,
        "description": str,
        "id": str,
        "name": str,
        "updatedAt": datetime,
        "variants": List[PromptVariantOutputTypeDef],
        "version": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetPromptResponseTypeDef = TypedDict(
    "GetPromptResponseTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "customerEncryptionKeyArn": str,
        "defaultVariant": str,
        "description": str,
        "id": str,
        "name": str,
        "updatedAt": datetime,
        "variants": List[PromptVariantOutputTypeDef],
        "version": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdatePromptResponseTypeDef = TypedDict(
    "UpdatePromptResponseTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "customerEncryptionKeyArn": str,
        "defaultVariant": str,
        "description": str,
        "id": str,
        "name": str,
        "updatedAt": datetime,
        "variants": List[PromptVariantOutputTypeDef],
        "version": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
PromptFlowNodeSourceConfigurationTypeDef = TypedDict(
    "PromptFlowNodeSourceConfigurationTypeDef",
    {
        "inline": NotRequired[PromptFlowNodeInlineConfigurationTypeDef],
        "resource": NotRequired[PromptFlowNodeResourceConfigurationTypeDef],
    },
)
PromptVariantUnionTypeDef = Union[PromptVariantTypeDef, PromptVariantOutputTypeDef]
VectorIngestionConfigurationOutputTypeDef = TypedDict(
    "VectorIngestionConfigurationOutputTypeDef",
    {
        "chunkingConfiguration": NotRequired[ChunkingConfigurationOutputTypeDef],
        "customTransformationConfiguration": NotRequired[
            CustomTransformationConfigurationOutputTypeDef
        ],
        "parsingConfiguration": NotRequired[ParsingConfigurationTypeDef],
    },
)
VectorIngestionConfigurationTypeDef = TypedDict(
    "VectorIngestionConfigurationTypeDef",
    {
        "chunkingConfiguration": NotRequired[ChunkingConfigurationTypeDef],
        "customTransformationConfiguration": NotRequired[CustomTransformationConfigurationTypeDef],
        "parsingConfiguration": NotRequired[ParsingConfigurationTypeDef],
    },
)
CreateKnowledgeBaseResponseTypeDef = TypedDict(
    "CreateKnowledgeBaseResponseTypeDef",
    {
        "knowledgeBase": KnowledgeBaseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetKnowledgeBaseResponseTypeDef = TypedDict(
    "GetKnowledgeBaseResponseTypeDef",
    {
        "knowledgeBase": KnowledgeBaseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateKnowledgeBaseResponseTypeDef = TypedDict(
    "UpdateKnowledgeBaseResponseTypeDef",
    {
        "knowledgeBase": KnowledgeBaseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DataSourceConfigurationOutputTypeDef = TypedDict(
    "DataSourceConfigurationOutputTypeDef",
    {
        "type": DataSourceTypeType,
        "confluenceConfiguration": NotRequired[ConfluenceDataSourceConfigurationOutputTypeDef],
        "s3Configuration": NotRequired[S3DataSourceConfigurationOutputTypeDef],
        "salesforceConfiguration": NotRequired[SalesforceDataSourceConfigurationOutputTypeDef],
        "sharePointConfiguration": NotRequired[SharePointDataSourceConfigurationOutputTypeDef],
        "webConfiguration": NotRequired[WebDataSourceConfigurationOutputTypeDef],
    },
)
DataSourceConfigurationTypeDef = TypedDict(
    "DataSourceConfigurationTypeDef",
    {
        "type": DataSourceTypeType,
        "confluenceConfiguration": NotRequired[ConfluenceDataSourceConfigurationTypeDef],
        "s3Configuration": NotRequired[S3DataSourceConfigurationTypeDef],
        "salesforceConfiguration": NotRequired[SalesforceDataSourceConfigurationTypeDef],
        "sharePointConfiguration": NotRequired[SharePointDataSourceConfigurationTypeDef],
        "webConfiguration": NotRequired[WebDataSourceConfigurationTypeDef],
    },
)
PromptFlowNodeConfigurationOutputTypeDef = TypedDict(
    "PromptFlowNodeConfigurationOutputTypeDef",
    {
        "sourceConfiguration": PromptFlowNodeSourceConfigurationOutputTypeDef,
    },
)
PromptFlowNodeConfigurationTypeDef = TypedDict(
    "PromptFlowNodeConfigurationTypeDef",
    {
        "sourceConfiguration": PromptFlowNodeSourceConfigurationTypeDef,
    },
)
CreatePromptRequestRequestTypeDef = TypedDict(
    "CreatePromptRequestRequestTypeDef",
    {
        "name": str,
        "clientToken": NotRequired[str],
        "customerEncryptionKeyArn": NotRequired[str],
        "defaultVariant": NotRequired[str],
        "description": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
        "variants": NotRequired[Sequence[PromptVariantUnionTypeDef]],
    },
)
UpdatePromptRequestRequestTypeDef = TypedDict(
    "UpdatePromptRequestRequestTypeDef",
    {
        "name": str,
        "promptIdentifier": str,
        "customerEncryptionKeyArn": NotRequired[str],
        "defaultVariant": NotRequired[str],
        "description": NotRequired[str],
        "variants": NotRequired[Sequence[PromptVariantUnionTypeDef]],
    },
)
DataSourceTypeDef = TypedDict(
    "DataSourceTypeDef",
    {
        "createdAt": datetime,
        "dataSourceConfiguration": DataSourceConfigurationOutputTypeDef,
        "dataSourceId": str,
        "knowledgeBaseId": str,
        "name": str,
        "status": DataSourceStatusType,
        "updatedAt": datetime,
        "dataDeletionPolicy": NotRequired[DataDeletionPolicyType],
        "description": NotRequired[str],
        "failureReasons": NotRequired[List[str]],
        "serverSideEncryptionConfiguration": NotRequired[ServerSideEncryptionConfigurationTypeDef],
        "vectorIngestionConfiguration": NotRequired[VectorIngestionConfigurationOutputTypeDef],
    },
)
CreateDataSourceRequestRequestTypeDef = TypedDict(
    "CreateDataSourceRequestRequestTypeDef",
    {
        "dataSourceConfiguration": DataSourceConfigurationTypeDef,
        "knowledgeBaseId": str,
        "name": str,
        "clientToken": NotRequired[str],
        "dataDeletionPolicy": NotRequired[DataDeletionPolicyType],
        "description": NotRequired[str],
        "serverSideEncryptionConfiguration": NotRequired[ServerSideEncryptionConfigurationTypeDef],
        "vectorIngestionConfiguration": NotRequired[VectorIngestionConfigurationTypeDef],
    },
)
UpdateDataSourceRequestRequestTypeDef = TypedDict(
    "UpdateDataSourceRequestRequestTypeDef",
    {
        "dataSourceConfiguration": DataSourceConfigurationTypeDef,
        "dataSourceId": str,
        "knowledgeBaseId": str,
        "name": str,
        "dataDeletionPolicy": NotRequired[DataDeletionPolicyType],
        "description": NotRequired[str],
        "serverSideEncryptionConfiguration": NotRequired[ServerSideEncryptionConfigurationTypeDef],
        "vectorIngestionConfiguration": NotRequired[VectorIngestionConfigurationTypeDef],
    },
)
FlowNodeConfigurationOutputTypeDef = TypedDict(
    "FlowNodeConfigurationOutputTypeDef",
    {
        "agent": NotRequired[AgentFlowNodeConfigurationTypeDef],
        "collector": NotRequired[Dict[str, Any]],
        "condition": NotRequired[ConditionFlowNodeConfigurationOutputTypeDef],
        "input": NotRequired[Dict[str, Any]],
        "iterator": NotRequired[Dict[str, Any]],
        "knowledgeBase": NotRequired[KnowledgeBaseFlowNodeConfigurationTypeDef],
        "lambdaFunction": NotRequired[LambdaFunctionFlowNodeConfigurationTypeDef],
        "lex": NotRequired[LexFlowNodeConfigurationTypeDef],
        "output": NotRequired[Dict[str, Any]],
        "prompt": NotRequired[PromptFlowNodeConfigurationOutputTypeDef],
        "retrieval": NotRequired[RetrievalFlowNodeConfigurationTypeDef],
        "storage": NotRequired[StorageFlowNodeConfigurationTypeDef],
    },
)
FlowNodeConfigurationTypeDef = TypedDict(
    "FlowNodeConfigurationTypeDef",
    {
        "agent": NotRequired[AgentFlowNodeConfigurationTypeDef],
        "collector": NotRequired[Mapping[str, Any]],
        "condition": NotRequired[ConditionFlowNodeConfigurationTypeDef],
        "input": NotRequired[Mapping[str, Any]],
        "iterator": NotRequired[Mapping[str, Any]],
        "knowledgeBase": NotRequired[KnowledgeBaseFlowNodeConfigurationTypeDef],
        "lambdaFunction": NotRequired[LambdaFunctionFlowNodeConfigurationTypeDef],
        "lex": NotRequired[LexFlowNodeConfigurationTypeDef],
        "output": NotRequired[Mapping[str, Any]],
        "prompt": NotRequired[PromptFlowNodeConfigurationTypeDef],
        "retrieval": NotRequired[RetrievalFlowNodeConfigurationTypeDef],
        "storage": NotRequired[StorageFlowNodeConfigurationTypeDef],
    },
)
CreateDataSourceResponseTypeDef = TypedDict(
    "CreateDataSourceResponseTypeDef",
    {
        "dataSource": DataSourceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetDataSourceResponseTypeDef = TypedDict(
    "GetDataSourceResponseTypeDef",
    {
        "dataSource": DataSourceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateDataSourceResponseTypeDef = TypedDict(
    "UpdateDataSourceResponseTypeDef",
    {
        "dataSource": DataSourceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
FlowNodeExtraOutputTypeDef = TypedDict(
    "FlowNodeExtraOutputTypeDef",
    {
        "name": str,
        "type": FlowNodeTypeType,
        "configuration": NotRequired[FlowNodeConfigurationOutputTypeDef],
        "inputs": NotRequired[List[FlowNodeInputTypeDef]],
        "outputs": NotRequired[List[FlowNodeOutputTypeDef]],
    },
)
FlowNodeTypeDef = TypedDict(
    "FlowNodeTypeDef",
    {
        "name": str,
        "type": FlowNodeTypeType,
        "configuration": NotRequired[FlowNodeConfigurationTypeDef],
        "inputs": NotRequired[Sequence[FlowNodeInputTypeDef]],
        "outputs": NotRequired[Sequence[FlowNodeOutputTypeDef]],
    },
)
FlowDefinitionOutputTypeDef = TypedDict(
    "FlowDefinitionOutputTypeDef",
    {
        "connections": NotRequired[List[FlowConnectionTypeDef]],
        "nodes": NotRequired[List[FlowNodeExtraOutputTypeDef]],
    },
)
FlowDefinitionTypeDef = TypedDict(
    "FlowDefinitionTypeDef",
    {
        "connections": NotRequired[Sequence[FlowConnectionTypeDef]],
        "nodes": NotRequired[Sequence[FlowNodeTypeDef]],
    },
)
CreateFlowResponseTypeDef = TypedDict(
    "CreateFlowResponseTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "customerEncryptionKeyArn": str,
        "definition": FlowDefinitionOutputTypeDef,
        "description": str,
        "executionRoleArn": str,
        "id": str,
        "name": str,
        "status": FlowStatusType,
        "updatedAt": datetime,
        "version": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateFlowVersionResponseTypeDef = TypedDict(
    "CreateFlowVersionResponseTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "customerEncryptionKeyArn": str,
        "definition": FlowDefinitionOutputTypeDef,
        "description": str,
        "executionRoleArn": str,
        "id": str,
        "name": str,
        "status": FlowStatusType,
        "version": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetFlowResponseTypeDef = TypedDict(
    "GetFlowResponseTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "customerEncryptionKeyArn": str,
        "definition": FlowDefinitionOutputTypeDef,
        "description": str,
        "executionRoleArn": str,
        "id": str,
        "name": str,
        "status": FlowStatusType,
        "updatedAt": datetime,
        "validations": List[FlowValidationTypeDef],
        "version": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetFlowVersionResponseTypeDef = TypedDict(
    "GetFlowVersionResponseTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "customerEncryptionKeyArn": str,
        "definition": FlowDefinitionOutputTypeDef,
        "description": str,
        "executionRoleArn": str,
        "id": str,
        "name": str,
        "status": FlowStatusType,
        "version": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateFlowResponseTypeDef = TypedDict(
    "UpdateFlowResponseTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "customerEncryptionKeyArn": str,
        "definition": FlowDefinitionOutputTypeDef,
        "description": str,
        "executionRoleArn": str,
        "id": str,
        "name": str,
        "status": FlowStatusType,
        "updatedAt": datetime,
        "version": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateFlowRequestRequestTypeDef = TypedDict(
    "CreateFlowRequestRequestTypeDef",
    {
        "executionRoleArn": str,
        "name": str,
        "clientToken": NotRequired[str],
        "customerEncryptionKeyArn": NotRequired[str],
        "definition": NotRequired[FlowDefinitionTypeDef],
        "description": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
    },
)
UpdateFlowRequestRequestTypeDef = TypedDict(
    "UpdateFlowRequestRequestTypeDef",
    {
        "executionRoleArn": str,
        "flowIdentifier": str,
        "name": str,
        "customerEncryptionKeyArn": NotRequired[str],
        "definition": NotRequired[FlowDefinitionTypeDef],
        "description": NotRequired[str],
    },
)
