"""
Type annotations for emr-serverless service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_serverless/type_defs/)

Usage::

    ```python
    from types_aiobotocore_emr_serverless.type_defs import ApplicationSummaryTypeDef

    data: ApplicationSummaryTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence, Union

from .literals import ApplicationStateType, ArchitectureType, JobRunModeType, JobRunStateType

if sys.version_info >= (3, 12):
    from typing import NotRequired
else:
    from typing_extensions import NotRequired
if sys.version_info >= (3, 12):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "ApplicationSummaryTypeDef",
    "AutoStartConfigTypeDef",
    "AutoStopConfigTypeDef",
    "ImageConfigurationTypeDef",
    "InteractiveConfigurationTypeDef",
    "MaximumAllowedResourcesTypeDef",
    "NetworkConfigurationOutputTypeDef",
    "CancelJobRunRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "CloudWatchLoggingConfigurationOutputTypeDef",
    "CloudWatchLoggingConfigurationTypeDef",
    "ConfigurationOutputTypeDef",
    "ConfigurationTypeDef",
    "ConfigurationUnionTypeDef",
    "ImageConfigurationInputTypeDef",
    "NetworkConfigurationTypeDef",
    "DeleteApplicationRequestRequestTypeDef",
    "GetApplicationRequestRequestTypeDef",
    "GetDashboardForJobRunRequestRequestTypeDef",
    "GetJobRunRequestRequestTypeDef",
    "HiveTypeDef",
    "WorkerResourceConfigTypeDef",
    "SparkSubmitOutputTypeDef",
    "SparkSubmitTypeDef",
    "JobRunAttemptSummaryTypeDef",
    "JobRunSummaryTypeDef",
    "ResourceUtilizationTypeDef",
    "RetryPolicyTypeDef",
    "TotalResourceUtilizationTypeDef",
    "PaginatorConfigTypeDef",
    "ListApplicationsRequestRequestTypeDef",
    "ListJobRunAttemptsRequestRequestTypeDef",
    "TimestampTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ManagedPersistenceMonitoringConfigurationTypeDef",
    "PrometheusMonitoringConfigurationTypeDef",
    "S3MonitoringConfigurationTypeDef",
    "StartApplicationRequestRequestTypeDef",
    "StopApplicationRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "WorkerTypeSpecificationTypeDef",
    "CancelJobRunResponseTypeDef",
    "CreateApplicationResponseTypeDef",
    "GetDashboardForJobRunResponseTypeDef",
    "ListApplicationsResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "StartJobRunResponseTypeDef",
    "WorkerTypeSpecificationInputTypeDef",
    "InitialCapacityConfigTypeDef",
    "JobDriverOutputTypeDef",
    "JobDriverTypeDef",
    "ListJobRunAttemptsResponseTypeDef",
    "ListJobRunsResponseTypeDef",
    "ListApplicationsRequestListApplicationsPaginateTypeDef",
    "ListJobRunAttemptsRequestListJobRunAttemptsPaginateTypeDef",
    "ListJobRunsRequestListJobRunsPaginateTypeDef",
    "ListJobRunsRequestRequestTypeDef",
    "MonitoringConfigurationOutputTypeDef",
    "MonitoringConfigurationTypeDef",
    "ApplicationTypeDef",
    "ConfigurationOverridesOutputTypeDef",
    "ConfigurationOverridesTypeDef",
    "CreateApplicationRequestRequestTypeDef",
    "UpdateApplicationRequestRequestTypeDef",
    "GetApplicationResponseTypeDef",
    "UpdateApplicationResponseTypeDef",
    "JobRunTypeDef",
    "StartJobRunRequestRequestTypeDef",
    "GetJobRunResponseTypeDef",
)

ApplicationSummaryTypeDef = TypedDict(
    "ApplicationSummaryTypeDef",
    {
        "id": str,
        "arn": str,
        "releaseLabel": str,
        "type": str,
        "state": ApplicationStateType,
        "createdAt": datetime,
        "updatedAt": datetime,
        "name": NotRequired[str],
        "stateDetails": NotRequired[str],
        "architecture": NotRequired[ArchitectureType],
    },
)
AutoStartConfigTypeDef = TypedDict(
    "AutoStartConfigTypeDef",
    {
        "enabled": NotRequired[bool],
    },
)
AutoStopConfigTypeDef = TypedDict(
    "AutoStopConfigTypeDef",
    {
        "enabled": NotRequired[bool],
        "idleTimeoutMinutes": NotRequired[int],
    },
)
ImageConfigurationTypeDef = TypedDict(
    "ImageConfigurationTypeDef",
    {
        "imageUri": str,
        "resolvedImageDigest": NotRequired[str],
    },
)
InteractiveConfigurationTypeDef = TypedDict(
    "InteractiveConfigurationTypeDef",
    {
        "studioEnabled": NotRequired[bool],
        "livyEndpointEnabled": NotRequired[bool],
    },
)
MaximumAllowedResourcesTypeDef = TypedDict(
    "MaximumAllowedResourcesTypeDef",
    {
        "cpu": str,
        "memory": str,
        "disk": NotRequired[str],
    },
)
NetworkConfigurationOutputTypeDef = TypedDict(
    "NetworkConfigurationOutputTypeDef",
    {
        "subnetIds": NotRequired[List[str]],
        "securityGroupIds": NotRequired[List[str]],
    },
)
CancelJobRunRequestRequestTypeDef = TypedDict(
    "CancelJobRunRequestRequestTypeDef",
    {
        "applicationId": str,
        "jobRunId": str,
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
CloudWatchLoggingConfigurationOutputTypeDef = TypedDict(
    "CloudWatchLoggingConfigurationOutputTypeDef",
    {
        "enabled": bool,
        "logGroupName": NotRequired[str],
        "logStreamNamePrefix": NotRequired[str],
        "encryptionKeyArn": NotRequired[str],
        "logTypes": NotRequired[Dict[str, List[str]]],
    },
)
CloudWatchLoggingConfigurationTypeDef = TypedDict(
    "CloudWatchLoggingConfigurationTypeDef",
    {
        "enabled": bool,
        "logGroupName": NotRequired[str],
        "logStreamNamePrefix": NotRequired[str],
        "encryptionKeyArn": NotRequired[str],
        "logTypes": NotRequired[Mapping[str, Sequence[str]]],
    },
)
ConfigurationOutputTypeDef = TypedDict(
    "ConfigurationOutputTypeDef",
    {
        "classification": str,
        "properties": NotRequired[Dict[str, str]],
        "configurations": NotRequired[List[Dict[str, Any]]],
    },
)
ConfigurationTypeDef = TypedDict(
    "ConfigurationTypeDef",
    {
        "classification": str,
        "properties": NotRequired[Mapping[str, str]],
        "configurations": NotRequired[Sequence[Dict[str, Any]]],
    },
)
ConfigurationUnionTypeDef = Union["ConfigurationTypeDef", "ConfigurationOutputTypeDef"]
ImageConfigurationInputTypeDef = TypedDict(
    "ImageConfigurationInputTypeDef",
    {
        "imageUri": NotRequired[str],
    },
)
NetworkConfigurationTypeDef = TypedDict(
    "NetworkConfigurationTypeDef",
    {
        "subnetIds": NotRequired[Sequence[str]],
        "securityGroupIds": NotRequired[Sequence[str]],
    },
)
DeleteApplicationRequestRequestTypeDef = TypedDict(
    "DeleteApplicationRequestRequestTypeDef",
    {
        "applicationId": str,
    },
)
GetApplicationRequestRequestTypeDef = TypedDict(
    "GetApplicationRequestRequestTypeDef",
    {
        "applicationId": str,
    },
)
GetDashboardForJobRunRequestRequestTypeDef = TypedDict(
    "GetDashboardForJobRunRequestRequestTypeDef",
    {
        "applicationId": str,
        "jobRunId": str,
        "attempt": NotRequired[int],
    },
)
GetJobRunRequestRequestTypeDef = TypedDict(
    "GetJobRunRequestRequestTypeDef",
    {
        "applicationId": str,
        "jobRunId": str,
        "attempt": NotRequired[int],
    },
)
HiveTypeDef = TypedDict(
    "HiveTypeDef",
    {
        "query": str,
        "initQueryFile": NotRequired[str],
        "parameters": NotRequired[str],
    },
)
WorkerResourceConfigTypeDef = TypedDict(
    "WorkerResourceConfigTypeDef",
    {
        "cpu": str,
        "memory": str,
        "disk": NotRequired[str],
        "diskType": NotRequired[str],
    },
)
SparkSubmitOutputTypeDef = TypedDict(
    "SparkSubmitOutputTypeDef",
    {
        "entryPoint": str,
        "entryPointArguments": NotRequired[List[str]],
        "sparkSubmitParameters": NotRequired[str],
    },
)
SparkSubmitTypeDef = TypedDict(
    "SparkSubmitTypeDef",
    {
        "entryPoint": str,
        "entryPointArguments": NotRequired[Sequence[str]],
        "sparkSubmitParameters": NotRequired[str],
    },
)
JobRunAttemptSummaryTypeDef = TypedDict(
    "JobRunAttemptSummaryTypeDef",
    {
        "applicationId": str,
        "id": str,
        "arn": str,
        "createdBy": str,
        "jobCreatedAt": datetime,
        "createdAt": datetime,
        "updatedAt": datetime,
        "executionRole": str,
        "state": JobRunStateType,
        "stateDetails": str,
        "releaseLabel": str,
        "name": NotRequired[str],
        "mode": NotRequired[JobRunModeType],
        "type": NotRequired[str],
        "attempt": NotRequired[int],
    },
)
JobRunSummaryTypeDef = TypedDict(
    "JobRunSummaryTypeDef",
    {
        "applicationId": str,
        "id": str,
        "arn": str,
        "createdBy": str,
        "createdAt": datetime,
        "updatedAt": datetime,
        "executionRole": str,
        "state": JobRunStateType,
        "stateDetails": str,
        "releaseLabel": str,
        "name": NotRequired[str],
        "mode": NotRequired[JobRunModeType],
        "type": NotRequired[str],
        "attempt": NotRequired[int],
        "attemptCreatedAt": NotRequired[datetime],
        "attemptUpdatedAt": NotRequired[datetime],
    },
)
ResourceUtilizationTypeDef = TypedDict(
    "ResourceUtilizationTypeDef",
    {
        "vCPUHour": NotRequired[float],
        "memoryGBHour": NotRequired[float],
        "storageGBHour": NotRequired[float],
    },
)
RetryPolicyTypeDef = TypedDict(
    "RetryPolicyTypeDef",
    {
        "maxAttempts": NotRequired[int],
        "maxFailedAttemptsPerHour": NotRequired[int],
    },
)
TotalResourceUtilizationTypeDef = TypedDict(
    "TotalResourceUtilizationTypeDef",
    {
        "vCPUHour": NotRequired[float],
        "memoryGBHour": NotRequired[float],
        "storageGBHour": NotRequired[float],
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
ListApplicationsRequestRequestTypeDef = TypedDict(
    "ListApplicationsRequestRequestTypeDef",
    {
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
        "states": NotRequired[Sequence[ApplicationStateType]],
    },
)
ListJobRunAttemptsRequestRequestTypeDef = TypedDict(
    "ListJobRunAttemptsRequestRequestTypeDef",
    {
        "applicationId": str,
        "jobRunId": str,
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)
TimestampTypeDef = Union[datetime, str]
ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)
ManagedPersistenceMonitoringConfigurationTypeDef = TypedDict(
    "ManagedPersistenceMonitoringConfigurationTypeDef",
    {
        "enabled": NotRequired[bool],
        "encryptionKeyArn": NotRequired[str],
    },
)
PrometheusMonitoringConfigurationTypeDef = TypedDict(
    "PrometheusMonitoringConfigurationTypeDef",
    {
        "remoteWriteUrl": NotRequired[str],
    },
)
S3MonitoringConfigurationTypeDef = TypedDict(
    "S3MonitoringConfigurationTypeDef",
    {
        "logUri": NotRequired[str],
        "encryptionKeyArn": NotRequired[str],
    },
)
StartApplicationRequestRequestTypeDef = TypedDict(
    "StartApplicationRequestRequestTypeDef",
    {
        "applicationId": str,
    },
)
StopApplicationRequestRequestTypeDef = TypedDict(
    "StopApplicationRequestRequestTypeDef",
    {
        "applicationId": str,
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
WorkerTypeSpecificationTypeDef = TypedDict(
    "WorkerTypeSpecificationTypeDef",
    {
        "imageConfiguration": NotRequired[ImageConfigurationTypeDef],
    },
)
CancelJobRunResponseTypeDef = TypedDict(
    "CancelJobRunResponseTypeDef",
    {
        "applicationId": str,
        "jobRunId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateApplicationResponseTypeDef = TypedDict(
    "CreateApplicationResponseTypeDef",
    {
        "applicationId": str,
        "name": str,
        "arn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetDashboardForJobRunResponseTypeDef = TypedDict(
    "GetDashboardForJobRunResponseTypeDef",
    {
        "url": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListApplicationsResponseTypeDef = TypedDict(
    "ListApplicationsResponseTypeDef",
    {
        "applications": List[ApplicationSummaryTypeDef],
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
StartJobRunResponseTypeDef = TypedDict(
    "StartJobRunResponseTypeDef",
    {
        "applicationId": str,
        "jobRunId": str,
        "arn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
WorkerTypeSpecificationInputTypeDef = TypedDict(
    "WorkerTypeSpecificationInputTypeDef",
    {
        "imageConfiguration": NotRequired[ImageConfigurationInputTypeDef],
    },
)
InitialCapacityConfigTypeDef = TypedDict(
    "InitialCapacityConfigTypeDef",
    {
        "workerCount": int,
        "workerConfiguration": NotRequired[WorkerResourceConfigTypeDef],
    },
)
JobDriverOutputTypeDef = TypedDict(
    "JobDriverOutputTypeDef",
    {
        "sparkSubmit": NotRequired[SparkSubmitOutputTypeDef],
        "hive": NotRequired[HiveTypeDef],
    },
)
JobDriverTypeDef = TypedDict(
    "JobDriverTypeDef",
    {
        "sparkSubmit": NotRequired[SparkSubmitTypeDef],
        "hive": NotRequired[HiveTypeDef],
    },
)
ListJobRunAttemptsResponseTypeDef = TypedDict(
    "ListJobRunAttemptsResponseTypeDef",
    {
        "jobRunAttempts": List[JobRunAttemptSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListJobRunsResponseTypeDef = TypedDict(
    "ListJobRunsResponseTypeDef",
    {
        "jobRuns": List[JobRunSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListApplicationsRequestListApplicationsPaginateTypeDef = TypedDict(
    "ListApplicationsRequestListApplicationsPaginateTypeDef",
    {
        "states": NotRequired[Sequence[ApplicationStateType]],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListJobRunAttemptsRequestListJobRunAttemptsPaginateTypeDef = TypedDict(
    "ListJobRunAttemptsRequestListJobRunAttemptsPaginateTypeDef",
    {
        "applicationId": str,
        "jobRunId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListJobRunsRequestListJobRunsPaginateTypeDef = TypedDict(
    "ListJobRunsRequestListJobRunsPaginateTypeDef",
    {
        "applicationId": str,
        "createdAtAfter": NotRequired[TimestampTypeDef],
        "createdAtBefore": NotRequired[TimestampTypeDef],
        "states": NotRequired[Sequence[JobRunStateType]],
        "mode": NotRequired[JobRunModeType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListJobRunsRequestRequestTypeDef = TypedDict(
    "ListJobRunsRequestRequestTypeDef",
    {
        "applicationId": str,
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
        "createdAtAfter": NotRequired[TimestampTypeDef],
        "createdAtBefore": NotRequired[TimestampTypeDef],
        "states": NotRequired[Sequence[JobRunStateType]],
        "mode": NotRequired[JobRunModeType],
    },
)
MonitoringConfigurationOutputTypeDef = TypedDict(
    "MonitoringConfigurationOutputTypeDef",
    {
        "s3MonitoringConfiguration": NotRequired[S3MonitoringConfigurationTypeDef],
        "managedPersistenceMonitoringConfiguration": NotRequired[
            ManagedPersistenceMonitoringConfigurationTypeDef
        ],
        "cloudWatchLoggingConfiguration": NotRequired[CloudWatchLoggingConfigurationOutputTypeDef],
        "prometheusMonitoringConfiguration": NotRequired[PrometheusMonitoringConfigurationTypeDef],
    },
)
MonitoringConfigurationTypeDef = TypedDict(
    "MonitoringConfigurationTypeDef",
    {
        "s3MonitoringConfiguration": NotRequired[S3MonitoringConfigurationTypeDef],
        "managedPersistenceMonitoringConfiguration": NotRequired[
            ManagedPersistenceMonitoringConfigurationTypeDef
        ],
        "cloudWatchLoggingConfiguration": NotRequired[CloudWatchLoggingConfigurationTypeDef],
        "prometheusMonitoringConfiguration": NotRequired[PrometheusMonitoringConfigurationTypeDef],
    },
)
ApplicationTypeDef = TypedDict(
    "ApplicationTypeDef",
    {
        "applicationId": str,
        "arn": str,
        "releaseLabel": str,
        "type": str,
        "state": ApplicationStateType,
        "createdAt": datetime,
        "updatedAt": datetime,
        "name": NotRequired[str],
        "stateDetails": NotRequired[str],
        "initialCapacity": NotRequired[Dict[str, InitialCapacityConfigTypeDef]],
        "maximumCapacity": NotRequired[MaximumAllowedResourcesTypeDef],
        "tags": NotRequired[Dict[str, str]],
        "autoStartConfiguration": NotRequired[AutoStartConfigTypeDef],
        "autoStopConfiguration": NotRequired[AutoStopConfigTypeDef],
        "networkConfiguration": NotRequired[NetworkConfigurationOutputTypeDef],
        "architecture": NotRequired[ArchitectureType],
        "imageConfiguration": NotRequired[ImageConfigurationTypeDef],
        "workerTypeSpecifications": NotRequired[Dict[str, WorkerTypeSpecificationTypeDef]],
        "runtimeConfiguration": NotRequired[List["ConfigurationOutputTypeDef"]],
        "monitoringConfiguration": NotRequired[MonitoringConfigurationOutputTypeDef],
        "interactiveConfiguration": NotRequired[InteractiveConfigurationTypeDef],
    },
)
ConfigurationOverridesOutputTypeDef = TypedDict(
    "ConfigurationOverridesOutputTypeDef",
    {
        "applicationConfiguration": NotRequired[List["ConfigurationOutputTypeDef"]],
        "monitoringConfiguration": NotRequired[MonitoringConfigurationOutputTypeDef],
    },
)
ConfigurationOverridesTypeDef = TypedDict(
    "ConfigurationOverridesTypeDef",
    {
        "applicationConfiguration": NotRequired[Sequence["ConfigurationTypeDef"]],
        "monitoringConfiguration": NotRequired[MonitoringConfigurationTypeDef],
    },
)
CreateApplicationRequestRequestTypeDef = TypedDict(
    "CreateApplicationRequestRequestTypeDef",
    {
        "releaseLabel": str,
        "type": str,
        "clientToken": str,
        "name": NotRequired[str],
        "initialCapacity": NotRequired[Mapping[str, InitialCapacityConfigTypeDef]],
        "maximumCapacity": NotRequired[MaximumAllowedResourcesTypeDef],
        "tags": NotRequired[Mapping[str, str]],
        "autoStartConfiguration": NotRequired[AutoStartConfigTypeDef],
        "autoStopConfiguration": NotRequired[AutoStopConfigTypeDef],
        "networkConfiguration": NotRequired[NetworkConfigurationTypeDef],
        "architecture": NotRequired[ArchitectureType],
        "imageConfiguration": NotRequired[ImageConfigurationInputTypeDef],
        "workerTypeSpecifications": NotRequired[Mapping[str, WorkerTypeSpecificationInputTypeDef]],
        "runtimeConfiguration": NotRequired[Sequence[ConfigurationUnionTypeDef]],
        "monitoringConfiguration": NotRequired[MonitoringConfigurationTypeDef],
        "interactiveConfiguration": NotRequired[InteractiveConfigurationTypeDef],
    },
)
UpdateApplicationRequestRequestTypeDef = TypedDict(
    "UpdateApplicationRequestRequestTypeDef",
    {
        "applicationId": str,
        "clientToken": str,
        "initialCapacity": NotRequired[Mapping[str, InitialCapacityConfigTypeDef]],
        "maximumCapacity": NotRequired[MaximumAllowedResourcesTypeDef],
        "autoStartConfiguration": NotRequired[AutoStartConfigTypeDef],
        "autoStopConfiguration": NotRequired[AutoStopConfigTypeDef],
        "networkConfiguration": NotRequired[NetworkConfigurationTypeDef],
        "architecture": NotRequired[ArchitectureType],
        "imageConfiguration": NotRequired[ImageConfigurationInputTypeDef],
        "workerTypeSpecifications": NotRequired[Mapping[str, WorkerTypeSpecificationInputTypeDef]],
        "interactiveConfiguration": NotRequired[InteractiveConfigurationTypeDef],
        "releaseLabel": NotRequired[str],
        "runtimeConfiguration": NotRequired[Sequence[ConfigurationUnionTypeDef]],
        "monitoringConfiguration": NotRequired[MonitoringConfigurationTypeDef],
    },
)
GetApplicationResponseTypeDef = TypedDict(
    "GetApplicationResponseTypeDef",
    {
        "application": ApplicationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateApplicationResponseTypeDef = TypedDict(
    "UpdateApplicationResponseTypeDef",
    {
        "application": ApplicationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
JobRunTypeDef = TypedDict(
    "JobRunTypeDef",
    {
        "applicationId": str,
        "jobRunId": str,
        "arn": str,
        "createdBy": str,
        "createdAt": datetime,
        "updatedAt": datetime,
        "executionRole": str,
        "state": JobRunStateType,
        "stateDetails": str,
        "releaseLabel": str,
        "jobDriver": JobDriverOutputTypeDef,
        "name": NotRequired[str],
        "configurationOverrides": NotRequired[ConfigurationOverridesOutputTypeDef],
        "tags": NotRequired[Dict[str, str]],
        "totalResourceUtilization": NotRequired[TotalResourceUtilizationTypeDef],
        "networkConfiguration": NotRequired[NetworkConfigurationOutputTypeDef],
        "totalExecutionDurationSeconds": NotRequired[int],
        "executionTimeoutMinutes": NotRequired[int],
        "billedResourceUtilization": NotRequired[ResourceUtilizationTypeDef],
        "mode": NotRequired[JobRunModeType],
        "retryPolicy": NotRequired[RetryPolicyTypeDef],
        "attempt": NotRequired[int],
        "attemptCreatedAt": NotRequired[datetime],
        "attemptUpdatedAt": NotRequired[datetime],
    },
)
StartJobRunRequestRequestTypeDef = TypedDict(
    "StartJobRunRequestRequestTypeDef",
    {
        "applicationId": str,
        "clientToken": str,
        "executionRoleArn": str,
        "jobDriver": NotRequired[JobDriverTypeDef],
        "configurationOverrides": NotRequired[ConfigurationOverridesTypeDef],
        "tags": NotRequired[Mapping[str, str]],
        "executionTimeoutMinutes": NotRequired[int],
        "name": NotRequired[str],
        "mode": NotRequired[JobRunModeType],
        "retryPolicy": NotRequired[RetryPolicyTypeDef],
    },
)
GetJobRunResponseTypeDef = TypedDict(
    "GetJobRunResponseTypeDef",
    {
        "jobRun": JobRunTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
