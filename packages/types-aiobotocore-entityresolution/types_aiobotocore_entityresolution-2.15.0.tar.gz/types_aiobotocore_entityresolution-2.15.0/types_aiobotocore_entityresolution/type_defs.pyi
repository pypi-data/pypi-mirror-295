"""
Type annotations for entityresolution service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/type_defs/)

Usage::

    ```python
    from types_aiobotocore_entityresolution.type_defs import AddPolicyStatementInputRequestTypeDef

    data: AddPolicyStatementInputRequestTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence, Union

from .literals import (
    AttributeMatchingModelType,
    DeleteUniqueIdErrorTypeType,
    DeleteUniqueIdStatusType,
    IdMappingTypeType,
    IdMappingWorkflowRuleDefinitionTypeType,
    IdNamespaceTypeType,
    JobStatusType,
    MatchPurposeType,
    RecordMatchingModelType,
    ResolutionTypeType,
    SchemaAttributeTypeType,
    ServiceTypeType,
    StatementEffectType,
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
    "AddPolicyStatementInputRequestTypeDef",
    "ResponseMetadataTypeDef",
    "BatchDeleteUniqueIdInputRequestTypeDef",
    "DeleteUniqueIdErrorTypeDef",
    "DeletedUniqueIdTypeDef",
    "IdMappingWorkflowInputSourceTypeDef",
    "IdMappingWorkflowOutputSourceTypeDef",
    "IdNamespaceInputSourceTypeDef",
    "IncrementalRunConfigTypeDef",
    "InputSourceTypeDef",
    "SchemaInputAttributeTypeDef",
    "DeleteIdMappingWorkflowInputRequestTypeDef",
    "DeleteIdNamespaceInputRequestTypeDef",
    "DeleteMatchingWorkflowInputRequestTypeDef",
    "DeletePolicyStatementInputRequestTypeDef",
    "DeleteSchemaMappingInputRequestTypeDef",
    "ErrorDetailsTypeDef",
    "GetIdMappingJobInputRequestTypeDef",
    "IdMappingJobMetricsTypeDef",
    "IdMappingJobOutputSourceTypeDef",
    "GetIdMappingWorkflowInputRequestTypeDef",
    "GetIdNamespaceInputRequestTypeDef",
    "GetMatchIdInputRequestTypeDef",
    "GetMatchingJobInputRequestTypeDef",
    "JobMetricsTypeDef",
    "JobOutputSourceTypeDef",
    "GetMatchingWorkflowInputRequestTypeDef",
    "GetPolicyInputRequestTypeDef",
    "GetProviderServiceInputRequestTypeDef",
    "ProviderIdNameSpaceConfigurationTypeDef",
    "ProviderIntermediateDataAccessConfigurationTypeDef",
    "GetSchemaMappingInputRequestTypeDef",
    "RuleOutputTypeDef",
    "RuleTypeDef",
    "IdMappingWorkflowSummaryTypeDef",
    "IdNamespaceIdMappingWorkflowMetadataTypeDef",
    "NamespaceProviderPropertiesOutputTypeDef",
    "NamespaceProviderPropertiesTypeDef",
    "IntermediateSourceConfigurationTypeDef",
    "JobSummaryTypeDef",
    "PaginatorConfigTypeDef",
    "ListIdMappingJobsInputRequestTypeDef",
    "ListIdMappingWorkflowsInputRequestTypeDef",
    "ListIdNamespacesInputRequestTypeDef",
    "ListMatchingJobsInputRequestTypeDef",
    "ListMatchingWorkflowsInputRequestTypeDef",
    "MatchingWorkflowSummaryTypeDef",
    "ListProviderServicesInputRequestTypeDef",
    "ProviderServiceSummaryTypeDef",
    "ListSchemaMappingsInputRequestTypeDef",
    "SchemaMappingSummaryTypeDef",
    "ListTagsForResourceInputRequestTypeDef",
    "OutputAttributeTypeDef",
    "ProviderSchemaAttributeTypeDef",
    "ProviderMarketplaceConfigurationTypeDef",
    "PutPolicyInputRequestTypeDef",
    "StartMatchingJobInputRequestTypeDef",
    "TagResourceInputRequestTypeDef",
    "UntagResourceInputRequestTypeDef",
    "AddPolicyStatementOutputTypeDef",
    "DeleteIdMappingWorkflowOutputTypeDef",
    "DeleteIdNamespaceOutputTypeDef",
    "DeleteMatchingWorkflowOutputTypeDef",
    "DeletePolicyStatementOutputTypeDef",
    "DeleteSchemaMappingOutputTypeDef",
    "GetMatchIdOutputTypeDef",
    "GetPolicyOutputTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "PutPolicyOutputTypeDef",
    "StartMatchingJobOutputTypeDef",
    "BatchDeleteUniqueIdOutputTypeDef",
    "CreateSchemaMappingInputRequestTypeDef",
    "CreateSchemaMappingOutputTypeDef",
    "GetSchemaMappingOutputTypeDef",
    "UpdateSchemaMappingInputRequestTypeDef",
    "UpdateSchemaMappingOutputTypeDef",
    "GetIdMappingJobOutputTypeDef",
    "StartIdMappingJobInputRequestTypeDef",
    "StartIdMappingJobOutputTypeDef",
    "GetMatchingJobOutputTypeDef",
    "IdMappingRuleBasedPropertiesOutputTypeDef",
    "NamespaceRuleBasedPropertiesOutputTypeDef",
    "RuleBasedPropertiesOutputTypeDef",
    "IdMappingRuleBasedPropertiesTypeDef",
    "NamespaceRuleBasedPropertiesTypeDef",
    "RuleBasedPropertiesTypeDef",
    "ListIdMappingWorkflowsOutputTypeDef",
    "IdNamespaceSummaryTypeDef",
    "ProviderPropertiesOutputTypeDef",
    "ProviderPropertiesTypeDef",
    "ListIdMappingJobsOutputTypeDef",
    "ListMatchingJobsOutputTypeDef",
    "ListIdMappingJobsInputListIdMappingJobsPaginateTypeDef",
    "ListIdMappingWorkflowsInputListIdMappingWorkflowsPaginateTypeDef",
    "ListIdNamespacesInputListIdNamespacesPaginateTypeDef",
    "ListMatchingJobsInputListMatchingJobsPaginateTypeDef",
    "ListMatchingWorkflowsInputListMatchingWorkflowsPaginateTypeDef",
    "ListProviderServicesInputListProviderServicesPaginateTypeDef",
    "ListSchemaMappingsInputListSchemaMappingsPaginateTypeDef",
    "ListMatchingWorkflowsOutputTypeDef",
    "ListProviderServicesOutputTypeDef",
    "ListSchemaMappingsOutputTypeDef",
    "OutputSourceOutputTypeDef",
    "OutputSourceTypeDef",
    "ProviderComponentSchemaTypeDef",
    "ProviderEndpointConfigurationTypeDef",
    "IdNamespaceIdMappingWorkflowPropertiesOutputTypeDef",
    "IdNamespaceIdMappingWorkflowPropertiesTypeDef",
    "ListIdNamespacesOutputTypeDef",
    "IdMappingTechniquesOutputTypeDef",
    "ResolutionTechniquesOutputTypeDef",
    "IdMappingTechniquesTypeDef",
    "ResolutionTechniquesTypeDef",
    "OutputSourceUnionTypeDef",
    "GetProviderServiceOutputTypeDef",
    "CreateIdNamespaceOutputTypeDef",
    "GetIdNamespaceOutputTypeDef",
    "UpdateIdNamespaceOutputTypeDef",
    "IdNamespaceIdMappingWorkflowPropertiesUnionTypeDef",
    "CreateIdMappingWorkflowOutputTypeDef",
    "GetIdMappingWorkflowOutputTypeDef",
    "UpdateIdMappingWorkflowOutputTypeDef",
    "CreateMatchingWorkflowOutputTypeDef",
    "GetMatchingWorkflowOutputTypeDef",
    "UpdateMatchingWorkflowOutputTypeDef",
    "CreateIdMappingWorkflowInputRequestTypeDef",
    "UpdateIdMappingWorkflowInputRequestTypeDef",
    "CreateMatchingWorkflowInputRequestTypeDef",
    "UpdateMatchingWorkflowInputRequestTypeDef",
    "CreateIdNamespaceInputRequestTypeDef",
    "UpdateIdNamespaceInputRequestTypeDef",
)

AddPolicyStatementInputRequestTypeDef = TypedDict(
    "AddPolicyStatementInputRequestTypeDef",
    {
        "action": Sequence[str],
        "arn": str,
        "effect": StatementEffectType,
        "principal": Sequence[str],
        "statementId": str,
        "condition": NotRequired[str],
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
BatchDeleteUniqueIdInputRequestTypeDef = TypedDict(
    "BatchDeleteUniqueIdInputRequestTypeDef",
    {
        "uniqueIds": Sequence[str],
        "workflowName": str,
        "inputSource": NotRequired[str],
    },
)
DeleteUniqueIdErrorTypeDef = TypedDict(
    "DeleteUniqueIdErrorTypeDef",
    {
        "errorType": DeleteUniqueIdErrorTypeType,
        "uniqueId": str,
    },
)
DeletedUniqueIdTypeDef = TypedDict(
    "DeletedUniqueIdTypeDef",
    {
        "uniqueId": str,
    },
)
IdMappingWorkflowInputSourceTypeDef = TypedDict(
    "IdMappingWorkflowInputSourceTypeDef",
    {
        "inputSourceARN": str,
        "schemaName": NotRequired[str],
        "type": NotRequired[IdNamespaceTypeType],
    },
)
IdMappingWorkflowOutputSourceTypeDef = TypedDict(
    "IdMappingWorkflowOutputSourceTypeDef",
    {
        "outputS3Path": str,
        "KMSArn": NotRequired[str],
    },
)
IdNamespaceInputSourceTypeDef = TypedDict(
    "IdNamespaceInputSourceTypeDef",
    {
        "inputSourceARN": str,
        "schemaName": NotRequired[str],
    },
)
IncrementalRunConfigTypeDef = TypedDict(
    "IncrementalRunConfigTypeDef",
    {
        "incrementalRunType": NotRequired[Literal["IMMEDIATE"]],
    },
)
InputSourceTypeDef = TypedDict(
    "InputSourceTypeDef",
    {
        "inputSourceARN": str,
        "schemaName": str,
        "applyNormalization": NotRequired[bool],
    },
)
SchemaInputAttributeTypeDef = TypedDict(
    "SchemaInputAttributeTypeDef",
    {
        "fieldName": str,
        "type": SchemaAttributeTypeType,
        "groupName": NotRequired[str],
        "hashed": NotRequired[bool],
        "matchKey": NotRequired[str],
        "subType": NotRequired[str],
    },
)
DeleteIdMappingWorkflowInputRequestTypeDef = TypedDict(
    "DeleteIdMappingWorkflowInputRequestTypeDef",
    {
        "workflowName": str,
    },
)
DeleteIdNamespaceInputRequestTypeDef = TypedDict(
    "DeleteIdNamespaceInputRequestTypeDef",
    {
        "idNamespaceName": str,
    },
)
DeleteMatchingWorkflowInputRequestTypeDef = TypedDict(
    "DeleteMatchingWorkflowInputRequestTypeDef",
    {
        "workflowName": str,
    },
)
DeletePolicyStatementInputRequestTypeDef = TypedDict(
    "DeletePolicyStatementInputRequestTypeDef",
    {
        "arn": str,
        "statementId": str,
    },
)
DeleteSchemaMappingInputRequestTypeDef = TypedDict(
    "DeleteSchemaMappingInputRequestTypeDef",
    {
        "schemaName": str,
    },
)
ErrorDetailsTypeDef = TypedDict(
    "ErrorDetailsTypeDef",
    {
        "errorMessage": NotRequired[str],
    },
)
GetIdMappingJobInputRequestTypeDef = TypedDict(
    "GetIdMappingJobInputRequestTypeDef",
    {
        "jobId": str,
        "workflowName": str,
    },
)
IdMappingJobMetricsTypeDef = TypedDict(
    "IdMappingJobMetricsTypeDef",
    {
        "inputRecords": NotRequired[int],
        "recordsNotProcessed": NotRequired[int],
        "totalMappedRecords": NotRequired[int],
        "totalMappedSourceRecords": NotRequired[int],
        "totalMappedTargetRecords": NotRequired[int],
        "totalRecordsProcessed": NotRequired[int],
    },
)
IdMappingJobOutputSourceTypeDef = TypedDict(
    "IdMappingJobOutputSourceTypeDef",
    {
        "outputS3Path": str,
        "roleArn": str,
        "KMSArn": NotRequired[str],
    },
)
GetIdMappingWorkflowInputRequestTypeDef = TypedDict(
    "GetIdMappingWorkflowInputRequestTypeDef",
    {
        "workflowName": str,
    },
)
GetIdNamespaceInputRequestTypeDef = TypedDict(
    "GetIdNamespaceInputRequestTypeDef",
    {
        "idNamespaceName": str,
    },
)
GetMatchIdInputRequestTypeDef = TypedDict(
    "GetMatchIdInputRequestTypeDef",
    {
        "record": Mapping[str, str],
        "workflowName": str,
        "applyNormalization": NotRequired[bool],
    },
)
GetMatchingJobInputRequestTypeDef = TypedDict(
    "GetMatchingJobInputRequestTypeDef",
    {
        "jobId": str,
        "workflowName": str,
    },
)
JobMetricsTypeDef = TypedDict(
    "JobMetricsTypeDef",
    {
        "inputRecords": NotRequired[int],
        "matchIDs": NotRequired[int],
        "recordsNotProcessed": NotRequired[int],
        "totalRecordsProcessed": NotRequired[int],
    },
)
JobOutputSourceTypeDef = TypedDict(
    "JobOutputSourceTypeDef",
    {
        "outputS3Path": str,
        "roleArn": str,
        "KMSArn": NotRequired[str],
    },
)
GetMatchingWorkflowInputRequestTypeDef = TypedDict(
    "GetMatchingWorkflowInputRequestTypeDef",
    {
        "workflowName": str,
    },
)
GetPolicyInputRequestTypeDef = TypedDict(
    "GetPolicyInputRequestTypeDef",
    {
        "arn": str,
    },
)
GetProviderServiceInputRequestTypeDef = TypedDict(
    "GetProviderServiceInputRequestTypeDef",
    {
        "providerName": str,
        "providerServiceName": str,
    },
)
ProviderIdNameSpaceConfigurationTypeDef = TypedDict(
    "ProviderIdNameSpaceConfigurationTypeDef",
    {
        "description": NotRequired[str],
        "providerSourceConfigurationDefinition": NotRequired[Dict[str, Any]],
        "providerTargetConfigurationDefinition": NotRequired[Dict[str, Any]],
    },
)
ProviderIntermediateDataAccessConfigurationTypeDef = TypedDict(
    "ProviderIntermediateDataAccessConfigurationTypeDef",
    {
        "awsAccountIds": NotRequired[List[str]],
        "requiredBucketActions": NotRequired[List[str]],
    },
)
GetSchemaMappingInputRequestTypeDef = TypedDict(
    "GetSchemaMappingInputRequestTypeDef",
    {
        "schemaName": str,
    },
)
RuleOutputTypeDef = TypedDict(
    "RuleOutputTypeDef",
    {
        "matchingKeys": List[str],
        "ruleName": str,
    },
)
RuleTypeDef = TypedDict(
    "RuleTypeDef",
    {
        "matchingKeys": Sequence[str],
        "ruleName": str,
    },
)
IdMappingWorkflowSummaryTypeDef = TypedDict(
    "IdMappingWorkflowSummaryTypeDef",
    {
        "createdAt": datetime,
        "updatedAt": datetime,
        "workflowArn": str,
        "workflowName": str,
    },
)
IdNamespaceIdMappingWorkflowMetadataTypeDef = TypedDict(
    "IdNamespaceIdMappingWorkflowMetadataTypeDef",
    {
        "idMappingType": IdMappingTypeType,
    },
)
NamespaceProviderPropertiesOutputTypeDef = TypedDict(
    "NamespaceProviderPropertiesOutputTypeDef",
    {
        "providerServiceArn": str,
        "providerConfiguration": NotRequired[Dict[str, Any]],
    },
)
NamespaceProviderPropertiesTypeDef = TypedDict(
    "NamespaceProviderPropertiesTypeDef",
    {
        "providerServiceArn": str,
        "providerConfiguration": NotRequired[Mapping[str, Any]],
    },
)
IntermediateSourceConfigurationTypeDef = TypedDict(
    "IntermediateSourceConfigurationTypeDef",
    {
        "intermediateS3Path": str,
    },
)
JobSummaryTypeDef = TypedDict(
    "JobSummaryTypeDef",
    {
        "jobId": str,
        "startTime": datetime,
        "status": JobStatusType,
        "endTime": NotRequired[datetime],
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
ListIdMappingJobsInputRequestTypeDef = TypedDict(
    "ListIdMappingJobsInputRequestTypeDef",
    {
        "workflowName": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
ListIdMappingWorkflowsInputRequestTypeDef = TypedDict(
    "ListIdMappingWorkflowsInputRequestTypeDef",
    {
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
ListIdNamespacesInputRequestTypeDef = TypedDict(
    "ListIdNamespacesInputRequestTypeDef",
    {
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
ListMatchingJobsInputRequestTypeDef = TypedDict(
    "ListMatchingJobsInputRequestTypeDef",
    {
        "workflowName": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
ListMatchingWorkflowsInputRequestTypeDef = TypedDict(
    "ListMatchingWorkflowsInputRequestTypeDef",
    {
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
MatchingWorkflowSummaryTypeDef = TypedDict(
    "MatchingWorkflowSummaryTypeDef",
    {
        "createdAt": datetime,
        "resolutionType": ResolutionTypeType,
        "updatedAt": datetime,
        "workflowArn": str,
        "workflowName": str,
    },
)
ListProviderServicesInputRequestTypeDef = TypedDict(
    "ListProviderServicesInputRequestTypeDef",
    {
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
        "providerName": NotRequired[str],
    },
)
ProviderServiceSummaryTypeDef = TypedDict(
    "ProviderServiceSummaryTypeDef",
    {
        "providerName": str,
        "providerServiceArn": str,
        "providerServiceDisplayName": str,
        "providerServiceName": str,
        "providerServiceType": ServiceTypeType,
    },
)
ListSchemaMappingsInputRequestTypeDef = TypedDict(
    "ListSchemaMappingsInputRequestTypeDef",
    {
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
SchemaMappingSummaryTypeDef = TypedDict(
    "SchemaMappingSummaryTypeDef",
    {
        "createdAt": datetime,
        "hasWorkflows": bool,
        "schemaArn": str,
        "schemaName": str,
        "updatedAt": datetime,
    },
)
ListTagsForResourceInputRequestTypeDef = TypedDict(
    "ListTagsForResourceInputRequestTypeDef",
    {
        "resourceArn": str,
    },
)
OutputAttributeTypeDef = TypedDict(
    "OutputAttributeTypeDef",
    {
        "name": str,
        "hashed": NotRequired[bool],
    },
)
ProviderSchemaAttributeTypeDef = TypedDict(
    "ProviderSchemaAttributeTypeDef",
    {
        "fieldName": str,
        "type": SchemaAttributeTypeType,
        "hashing": NotRequired[bool],
        "subType": NotRequired[str],
    },
)
ProviderMarketplaceConfigurationTypeDef = TypedDict(
    "ProviderMarketplaceConfigurationTypeDef",
    {
        "assetId": str,
        "dataSetId": str,
        "listingId": str,
        "revisionId": str,
    },
)
PutPolicyInputRequestTypeDef = TypedDict(
    "PutPolicyInputRequestTypeDef",
    {
        "arn": str,
        "policy": str,
        "token": NotRequired[str],
    },
)
StartMatchingJobInputRequestTypeDef = TypedDict(
    "StartMatchingJobInputRequestTypeDef",
    {
        "workflowName": str,
    },
)
TagResourceInputRequestTypeDef = TypedDict(
    "TagResourceInputRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Mapping[str, str],
    },
)
UntagResourceInputRequestTypeDef = TypedDict(
    "UntagResourceInputRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)
AddPolicyStatementOutputTypeDef = TypedDict(
    "AddPolicyStatementOutputTypeDef",
    {
        "arn": str,
        "policy": str,
        "token": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteIdMappingWorkflowOutputTypeDef = TypedDict(
    "DeleteIdMappingWorkflowOutputTypeDef",
    {
        "message": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteIdNamespaceOutputTypeDef = TypedDict(
    "DeleteIdNamespaceOutputTypeDef",
    {
        "message": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteMatchingWorkflowOutputTypeDef = TypedDict(
    "DeleteMatchingWorkflowOutputTypeDef",
    {
        "message": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeletePolicyStatementOutputTypeDef = TypedDict(
    "DeletePolicyStatementOutputTypeDef",
    {
        "arn": str,
        "policy": str,
        "token": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteSchemaMappingOutputTypeDef = TypedDict(
    "DeleteSchemaMappingOutputTypeDef",
    {
        "message": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetMatchIdOutputTypeDef = TypedDict(
    "GetMatchIdOutputTypeDef",
    {
        "matchId": str,
        "matchRule": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetPolicyOutputTypeDef = TypedDict(
    "GetPolicyOutputTypeDef",
    {
        "arn": str,
        "policy": str,
        "token": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListTagsForResourceOutputTypeDef = TypedDict(
    "ListTagsForResourceOutputTypeDef",
    {
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
PutPolicyOutputTypeDef = TypedDict(
    "PutPolicyOutputTypeDef",
    {
        "arn": str,
        "policy": str,
        "token": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
StartMatchingJobOutputTypeDef = TypedDict(
    "StartMatchingJobOutputTypeDef",
    {
        "jobId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
BatchDeleteUniqueIdOutputTypeDef = TypedDict(
    "BatchDeleteUniqueIdOutputTypeDef",
    {
        "deleted": List[DeletedUniqueIdTypeDef],
        "disconnectedUniqueIds": List[str],
        "errors": List[DeleteUniqueIdErrorTypeDef],
        "status": DeleteUniqueIdStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateSchemaMappingInputRequestTypeDef = TypedDict(
    "CreateSchemaMappingInputRequestTypeDef",
    {
        "mappedInputFields": Sequence[SchemaInputAttributeTypeDef],
        "schemaName": str,
        "description": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
    },
)
CreateSchemaMappingOutputTypeDef = TypedDict(
    "CreateSchemaMappingOutputTypeDef",
    {
        "description": str,
        "mappedInputFields": List[SchemaInputAttributeTypeDef],
        "schemaArn": str,
        "schemaName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetSchemaMappingOutputTypeDef = TypedDict(
    "GetSchemaMappingOutputTypeDef",
    {
        "createdAt": datetime,
        "description": str,
        "hasWorkflows": bool,
        "mappedInputFields": List[SchemaInputAttributeTypeDef],
        "schemaArn": str,
        "schemaName": str,
        "tags": Dict[str, str],
        "updatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateSchemaMappingInputRequestTypeDef = TypedDict(
    "UpdateSchemaMappingInputRequestTypeDef",
    {
        "mappedInputFields": Sequence[SchemaInputAttributeTypeDef],
        "schemaName": str,
        "description": NotRequired[str],
    },
)
UpdateSchemaMappingOutputTypeDef = TypedDict(
    "UpdateSchemaMappingOutputTypeDef",
    {
        "description": str,
        "mappedInputFields": List[SchemaInputAttributeTypeDef],
        "schemaArn": str,
        "schemaName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetIdMappingJobOutputTypeDef = TypedDict(
    "GetIdMappingJobOutputTypeDef",
    {
        "endTime": datetime,
        "errorDetails": ErrorDetailsTypeDef,
        "jobId": str,
        "metrics": IdMappingJobMetricsTypeDef,
        "outputSourceConfig": List[IdMappingJobOutputSourceTypeDef],
        "startTime": datetime,
        "status": JobStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
StartIdMappingJobInputRequestTypeDef = TypedDict(
    "StartIdMappingJobInputRequestTypeDef",
    {
        "workflowName": str,
        "outputSourceConfig": NotRequired[Sequence[IdMappingJobOutputSourceTypeDef]],
    },
)
StartIdMappingJobOutputTypeDef = TypedDict(
    "StartIdMappingJobOutputTypeDef",
    {
        "jobId": str,
        "outputSourceConfig": List[IdMappingJobOutputSourceTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetMatchingJobOutputTypeDef = TypedDict(
    "GetMatchingJobOutputTypeDef",
    {
        "endTime": datetime,
        "errorDetails": ErrorDetailsTypeDef,
        "jobId": str,
        "metrics": JobMetricsTypeDef,
        "outputSourceConfig": List[JobOutputSourceTypeDef],
        "startTime": datetime,
        "status": JobStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
IdMappingRuleBasedPropertiesOutputTypeDef = TypedDict(
    "IdMappingRuleBasedPropertiesOutputTypeDef",
    {
        "attributeMatchingModel": AttributeMatchingModelType,
        "recordMatchingModel": RecordMatchingModelType,
        "ruleDefinitionType": IdMappingWorkflowRuleDefinitionTypeType,
        "rules": NotRequired[List[RuleOutputTypeDef]],
    },
)
NamespaceRuleBasedPropertiesOutputTypeDef = TypedDict(
    "NamespaceRuleBasedPropertiesOutputTypeDef",
    {
        "attributeMatchingModel": NotRequired[AttributeMatchingModelType],
        "recordMatchingModels": NotRequired[List[RecordMatchingModelType]],
        "ruleDefinitionTypes": NotRequired[List[IdMappingWorkflowRuleDefinitionTypeType]],
        "rules": NotRequired[List[RuleOutputTypeDef]],
    },
)
RuleBasedPropertiesOutputTypeDef = TypedDict(
    "RuleBasedPropertiesOutputTypeDef",
    {
        "attributeMatchingModel": AttributeMatchingModelType,
        "rules": List[RuleOutputTypeDef],
        "matchPurpose": NotRequired[MatchPurposeType],
    },
)
IdMappingRuleBasedPropertiesTypeDef = TypedDict(
    "IdMappingRuleBasedPropertiesTypeDef",
    {
        "attributeMatchingModel": AttributeMatchingModelType,
        "recordMatchingModel": RecordMatchingModelType,
        "ruleDefinitionType": IdMappingWorkflowRuleDefinitionTypeType,
        "rules": NotRequired[Sequence[RuleTypeDef]],
    },
)
NamespaceRuleBasedPropertiesTypeDef = TypedDict(
    "NamespaceRuleBasedPropertiesTypeDef",
    {
        "attributeMatchingModel": NotRequired[AttributeMatchingModelType],
        "recordMatchingModels": NotRequired[Sequence[RecordMatchingModelType]],
        "ruleDefinitionTypes": NotRequired[Sequence[IdMappingWorkflowRuleDefinitionTypeType]],
        "rules": NotRequired[Sequence[RuleTypeDef]],
    },
)
RuleBasedPropertiesTypeDef = TypedDict(
    "RuleBasedPropertiesTypeDef",
    {
        "attributeMatchingModel": AttributeMatchingModelType,
        "rules": Sequence[RuleTypeDef],
        "matchPurpose": NotRequired[MatchPurposeType],
    },
)
ListIdMappingWorkflowsOutputTypeDef = TypedDict(
    "ListIdMappingWorkflowsOutputTypeDef",
    {
        "nextToken": str,
        "workflowSummaries": List[IdMappingWorkflowSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
IdNamespaceSummaryTypeDef = TypedDict(
    "IdNamespaceSummaryTypeDef",
    {
        "createdAt": datetime,
        "idNamespaceArn": str,
        "idNamespaceName": str,
        "type": IdNamespaceTypeType,
        "updatedAt": datetime,
        "description": NotRequired[str],
        "idMappingWorkflowProperties": NotRequired[
            List[IdNamespaceIdMappingWorkflowMetadataTypeDef]
        ],
    },
)
ProviderPropertiesOutputTypeDef = TypedDict(
    "ProviderPropertiesOutputTypeDef",
    {
        "providerServiceArn": str,
        "intermediateSourceConfiguration": NotRequired[IntermediateSourceConfigurationTypeDef],
        "providerConfiguration": NotRequired[Dict[str, Any]],
    },
)
ProviderPropertiesTypeDef = TypedDict(
    "ProviderPropertiesTypeDef",
    {
        "providerServiceArn": str,
        "intermediateSourceConfiguration": NotRequired[IntermediateSourceConfigurationTypeDef],
        "providerConfiguration": NotRequired[Mapping[str, Any]],
    },
)
ListIdMappingJobsOutputTypeDef = TypedDict(
    "ListIdMappingJobsOutputTypeDef",
    {
        "jobs": List[JobSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListMatchingJobsOutputTypeDef = TypedDict(
    "ListMatchingJobsOutputTypeDef",
    {
        "jobs": List[JobSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListIdMappingJobsInputListIdMappingJobsPaginateTypeDef = TypedDict(
    "ListIdMappingJobsInputListIdMappingJobsPaginateTypeDef",
    {
        "workflowName": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListIdMappingWorkflowsInputListIdMappingWorkflowsPaginateTypeDef = TypedDict(
    "ListIdMappingWorkflowsInputListIdMappingWorkflowsPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListIdNamespacesInputListIdNamespacesPaginateTypeDef = TypedDict(
    "ListIdNamespacesInputListIdNamespacesPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListMatchingJobsInputListMatchingJobsPaginateTypeDef = TypedDict(
    "ListMatchingJobsInputListMatchingJobsPaginateTypeDef",
    {
        "workflowName": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListMatchingWorkflowsInputListMatchingWorkflowsPaginateTypeDef = TypedDict(
    "ListMatchingWorkflowsInputListMatchingWorkflowsPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListProviderServicesInputListProviderServicesPaginateTypeDef = TypedDict(
    "ListProviderServicesInputListProviderServicesPaginateTypeDef",
    {
        "providerName": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListSchemaMappingsInputListSchemaMappingsPaginateTypeDef = TypedDict(
    "ListSchemaMappingsInputListSchemaMappingsPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListMatchingWorkflowsOutputTypeDef = TypedDict(
    "ListMatchingWorkflowsOutputTypeDef",
    {
        "nextToken": str,
        "workflowSummaries": List[MatchingWorkflowSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListProviderServicesOutputTypeDef = TypedDict(
    "ListProviderServicesOutputTypeDef",
    {
        "nextToken": str,
        "providerServiceSummaries": List[ProviderServiceSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListSchemaMappingsOutputTypeDef = TypedDict(
    "ListSchemaMappingsOutputTypeDef",
    {
        "nextToken": str,
        "schemaList": List[SchemaMappingSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
OutputSourceOutputTypeDef = TypedDict(
    "OutputSourceOutputTypeDef",
    {
        "output": List[OutputAttributeTypeDef],
        "outputS3Path": str,
        "KMSArn": NotRequired[str],
        "applyNormalization": NotRequired[bool],
    },
)
OutputSourceTypeDef = TypedDict(
    "OutputSourceTypeDef",
    {
        "output": Sequence[OutputAttributeTypeDef],
        "outputS3Path": str,
        "KMSArn": NotRequired[str],
        "applyNormalization": NotRequired[bool],
    },
)
ProviderComponentSchemaTypeDef = TypedDict(
    "ProviderComponentSchemaTypeDef",
    {
        "providerSchemaAttributes": NotRequired[List[ProviderSchemaAttributeTypeDef]],
        "schemas": NotRequired[List[List[str]]],
    },
)
ProviderEndpointConfigurationTypeDef = TypedDict(
    "ProviderEndpointConfigurationTypeDef",
    {
        "marketplaceConfiguration": NotRequired[ProviderMarketplaceConfigurationTypeDef],
    },
)
IdNamespaceIdMappingWorkflowPropertiesOutputTypeDef = TypedDict(
    "IdNamespaceIdMappingWorkflowPropertiesOutputTypeDef",
    {
        "idMappingType": IdMappingTypeType,
        "providerProperties": NotRequired[NamespaceProviderPropertiesOutputTypeDef],
        "ruleBasedProperties": NotRequired[NamespaceRuleBasedPropertiesOutputTypeDef],
    },
)
IdNamespaceIdMappingWorkflowPropertiesTypeDef = TypedDict(
    "IdNamespaceIdMappingWorkflowPropertiesTypeDef",
    {
        "idMappingType": IdMappingTypeType,
        "providerProperties": NotRequired[NamespaceProviderPropertiesTypeDef],
        "ruleBasedProperties": NotRequired[NamespaceRuleBasedPropertiesTypeDef],
    },
)
ListIdNamespacesOutputTypeDef = TypedDict(
    "ListIdNamespacesOutputTypeDef",
    {
        "idNamespaceSummaries": List[IdNamespaceSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
IdMappingTechniquesOutputTypeDef = TypedDict(
    "IdMappingTechniquesOutputTypeDef",
    {
        "idMappingType": IdMappingTypeType,
        "providerProperties": NotRequired[ProviderPropertiesOutputTypeDef],
        "ruleBasedProperties": NotRequired[IdMappingRuleBasedPropertiesOutputTypeDef],
    },
)
ResolutionTechniquesOutputTypeDef = TypedDict(
    "ResolutionTechniquesOutputTypeDef",
    {
        "resolutionType": ResolutionTypeType,
        "providerProperties": NotRequired[ProviderPropertiesOutputTypeDef],
        "ruleBasedProperties": NotRequired[RuleBasedPropertiesOutputTypeDef],
    },
)
IdMappingTechniquesTypeDef = TypedDict(
    "IdMappingTechniquesTypeDef",
    {
        "idMappingType": IdMappingTypeType,
        "providerProperties": NotRequired[ProviderPropertiesTypeDef],
        "ruleBasedProperties": NotRequired[IdMappingRuleBasedPropertiesTypeDef],
    },
)
ResolutionTechniquesTypeDef = TypedDict(
    "ResolutionTechniquesTypeDef",
    {
        "resolutionType": ResolutionTypeType,
        "providerProperties": NotRequired[ProviderPropertiesTypeDef],
        "ruleBasedProperties": NotRequired[RuleBasedPropertiesTypeDef],
    },
)
OutputSourceUnionTypeDef = Union[OutputSourceTypeDef, OutputSourceOutputTypeDef]
GetProviderServiceOutputTypeDef = TypedDict(
    "GetProviderServiceOutputTypeDef",
    {
        "anonymizedOutput": bool,
        "providerComponentSchema": ProviderComponentSchemaTypeDef,
        "providerConfigurationDefinition": Dict[str, Any],
        "providerEndpointConfiguration": ProviderEndpointConfigurationTypeDef,
        "providerEntityOutputDefinition": Dict[str, Any],
        "providerIdNameSpaceConfiguration": ProviderIdNameSpaceConfigurationTypeDef,
        "providerIntermediateDataAccessConfiguration": ProviderIntermediateDataAccessConfigurationTypeDef,
        "providerJobConfiguration": Dict[str, Any],
        "providerName": str,
        "providerServiceArn": str,
        "providerServiceDisplayName": str,
        "providerServiceName": str,
        "providerServiceType": ServiceTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateIdNamespaceOutputTypeDef = TypedDict(
    "CreateIdNamespaceOutputTypeDef",
    {
        "createdAt": datetime,
        "description": str,
        "idMappingWorkflowProperties": List[IdNamespaceIdMappingWorkflowPropertiesOutputTypeDef],
        "idNamespaceArn": str,
        "idNamespaceName": str,
        "inputSourceConfig": List[IdNamespaceInputSourceTypeDef],
        "roleArn": str,
        "tags": Dict[str, str],
        "type": IdNamespaceTypeType,
        "updatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetIdNamespaceOutputTypeDef = TypedDict(
    "GetIdNamespaceOutputTypeDef",
    {
        "createdAt": datetime,
        "description": str,
        "idMappingWorkflowProperties": List[IdNamespaceIdMappingWorkflowPropertiesOutputTypeDef],
        "idNamespaceArn": str,
        "idNamespaceName": str,
        "inputSourceConfig": List[IdNamespaceInputSourceTypeDef],
        "roleArn": str,
        "tags": Dict[str, str],
        "type": IdNamespaceTypeType,
        "updatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateIdNamespaceOutputTypeDef = TypedDict(
    "UpdateIdNamespaceOutputTypeDef",
    {
        "createdAt": datetime,
        "description": str,
        "idMappingWorkflowProperties": List[IdNamespaceIdMappingWorkflowPropertiesOutputTypeDef],
        "idNamespaceArn": str,
        "idNamespaceName": str,
        "inputSourceConfig": List[IdNamespaceInputSourceTypeDef],
        "roleArn": str,
        "type": IdNamespaceTypeType,
        "updatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
IdNamespaceIdMappingWorkflowPropertiesUnionTypeDef = Union[
    IdNamespaceIdMappingWorkflowPropertiesTypeDef,
    IdNamespaceIdMappingWorkflowPropertiesOutputTypeDef,
]
CreateIdMappingWorkflowOutputTypeDef = TypedDict(
    "CreateIdMappingWorkflowOutputTypeDef",
    {
        "description": str,
        "idMappingTechniques": IdMappingTechniquesOutputTypeDef,
        "inputSourceConfig": List[IdMappingWorkflowInputSourceTypeDef],
        "outputSourceConfig": List[IdMappingWorkflowOutputSourceTypeDef],
        "roleArn": str,
        "workflowArn": str,
        "workflowName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetIdMappingWorkflowOutputTypeDef = TypedDict(
    "GetIdMappingWorkflowOutputTypeDef",
    {
        "createdAt": datetime,
        "description": str,
        "idMappingTechniques": IdMappingTechniquesOutputTypeDef,
        "inputSourceConfig": List[IdMappingWorkflowInputSourceTypeDef],
        "outputSourceConfig": List[IdMappingWorkflowOutputSourceTypeDef],
        "roleArn": str,
        "tags": Dict[str, str],
        "updatedAt": datetime,
        "workflowArn": str,
        "workflowName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateIdMappingWorkflowOutputTypeDef = TypedDict(
    "UpdateIdMappingWorkflowOutputTypeDef",
    {
        "description": str,
        "idMappingTechniques": IdMappingTechniquesOutputTypeDef,
        "inputSourceConfig": List[IdMappingWorkflowInputSourceTypeDef],
        "outputSourceConfig": List[IdMappingWorkflowOutputSourceTypeDef],
        "roleArn": str,
        "workflowArn": str,
        "workflowName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateMatchingWorkflowOutputTypeDef = TypedDict(
    "CreateMatchingWorkflowOutputTypeDef",
    {
        "description": str,
        "incrementalRunConfig": IncrementalRunConfigTypeDef,
        "inputSourceConfig": List[InputSourceTypeDef],
        "outputSourceConfig": List[OutputSourceOutputTypeDef],
        "resolutionTechniques": ResolutionTechniquesOutputTypeDef,
        "roleArn": str,
        "workflowArn": str,
        "workflowName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetMatchingWorkflowOutputTypeDef = TypedDict(
    "GetMatchingWorkflowOutputTypeDef",
    {
        "createdAt": datetime,
        "description": str,
        "incrementalRunConfig": IncrementalRunConfigTypeDef,
        "inputSourceConfig": List[InputSourceTypeDef],
        "outputSourceConfig": List[OutputSourceOutputTypeDef],
        "resolutionTechniques": ResolutionTechniquesOutputTypeDef,
        "roleArn": str,
        "tags": Dict[str, str],
        "updatedAt": datetime,
        "workflowArn": str,
        "workflowName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateMatchingWorkflowOutputTypeDef = TypedDict(
    "UpdateMatchingWorkflowOutputTypeDef",
    {
        "description": str,
        "incrementalRunConfig": IncrementalRunConfigTypeDef,
        "inputSourceConfig": List[InputSourceTypeDef],
        "outputSourceConfig": List[OutputSourceOutputTypeDef],
        "resolutionTechniques": ResolutionTechniquesOutputTypeDef,
        "roleArn": str,
        "workflowName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateIdMappingWorkflowInputRequestTypeDef = TypedDict(
    "CreateIdMappingWorkflowInputRequestTypeDef",
    {
        "idMappingTechniques": IdMappingTechniquesTypeDef,
        "inputSourceConfig": Sequence[IdMappingWorkflowInputSourceTypeDef],
        "workflowName": str,
        "description": NotRequired[str],
        "outputSourceConfig": NotRequired[Sequence[IdMappingWorkflowOutputSourceTypeDef]],
        "roleArn": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
    },
)
UpdateIdMappingWorkflowInputRequestTypeDef = TypedDict(
    "UpdateIdMappingWorkflowInputRequestTypeDef",
    {
        "idMappingTechniques": IdMappingTechniquesTypeDef,
        "inputSourceConfig": Sequence[IdMappingWorkflowInputSourceTypeDef],
        "workflowName": str,
        "description": NotRequired[str],
        "outputSourceConfig": NotRequired[Sequence[IdMappingWorkflowOutputSourceTypeDef]],
        "roleArn": NotRequired[str],
    },
)
CreateMatchingWorkflowInputRequestTypeDef = TypedDict(
    "CreateMatchingWorkflowInputRequestTypeDef",
    {
        "inputSourceConfig": Sequence[InputSourceTypeDef],
        "outputSourceConfig": Sequence[OutputSourceUnionTypeDef],
        "resolutionTechniques": ResolutionTechniquesTypeDef,
        "roleArn": str,
        "workflowName": str,
        "description": NotRequired[str],
        "incrementalRunConfig": NotRequired[IncrementalRunConfigTypeDef],
        "tags": NotRequired[Mapping[str, str]],
    },
)
UpdateMatchingWorkflowInputRequestTypeDef = TypedDict(
    "UpdateMatchingWorkflowInputRequestTypeDef",
    {
        "inputSourceConfig": Sequence[InputSourceTypeDef],
        "outputSourceConfig": Sequence[OutputSourceUnionTypeDef],
        "resolutionTechniques": ResolutionTechniquesTypeDef,
        "roleArn": str,
        "workflowName": str,
        "description": NotRequired[str],
        "incrementalRunConfig": NotRequired[IncrementalRunConfigTypeDef],
    },
)
CreateIdNamespaceInputRequestTypeDef = TypedDict(
    "CreateIdNamespaceInputRequestTypeDef",
    {
        "idNamespaceName": str,
        "type": IdNamespaceTypeType,
        "description": NotRequired[str],
        "idMappingWorkflowProperties": NotRequired[
            Sequence[IdNamespaceIdMappingWorkflowPropertiesUnionTypeDef]
        ],
        "inputSourceConfig": NotRequired[Sequence[IdNamespaceInputSourceTypeDef]],
        "roleArn": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
    },
)
UpdateIdNamespaceInputRequestTypeDef = TypedDict(
    "UpdateIdNamespaceInputRequestTypeDef",
    {
        "idNamespaceName": str,
        "description": NotRequired[str],
        "idMappingWorkflowProperties": NotRequired[
            Sequence[IdNamespaceIdMappingWorkflowPropertiesUnionTypeDef]
        ],
        "inputSourceConfig": NotRequired[Sequence[IdNamespaceInputSourceTypeDef]],
        "roleArn": NotRequired[str],
    },
)
