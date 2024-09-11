"""
Type annotations for autoscaling-plans service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling_plans/type_defs/)

Usage::

    ```python
    from types_aiobotocore_autoscaling_plans.type_defs import TagFilterOutputTypeDef

    data: TagFilterOutputTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import (
    ForecastDataTypeType,
    LoadMetricTypeType,
    MetricStatisticType,
    PredictiveScalingMaxCapacityBehaviorType,
    PredictiveScalingModeType,
    ScalableDimensionType,
    ScalingMetricTypeType,
    ScalingPlanStatusCodeType,
    ScalingPolicyUpdateBehaviorType,
    ScalingStatusCodeType,
    ServiceNamespaceType,
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
    "TagFilterOutputTypeDef",
    "TagFilterTypeDef",
    "ResponseMetadataTypeDef",
    "MetricDimensionTypeDef",
    "DatapointTypeDef",
    "DeleteScalingPlanRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "DescribeScalingPlanResourcesRequestRequestTypeDef",
    "TimestampTypeDef",
    "PredefinedLoadMetricSpecificationTypeDef",
    "PredefinedScalingMetricSpecificationTypeDef",
    "ApplicationSourceOutputTypeDef",
    "ApplicationSourceTypeDef",
    "CreateScalingPlanResponseTypeDef",
    "CustomizedLoadMetricSpecificationOutputTypeDef",
    "CustomizedLoadMetricSpecificationTypeDef",
    "CustomizedScalingMetricSpecificationOutputTypeDef",
    "CustomizedScalingMetricSpecificationTypeDef",
    "GetScalingPlanResourceForecastDataResponseTypeDef",
    "DescribeScalingPlanResourcesRequestDescribeScalingPlanResourcesPaginateTypeDef",
    "GetScalingPlanResourceForecastDataRequestRequestTypeDef",
    "ApplicationSourceUnionTypeDef",
    "TargetTrackingConfigurationOutputTypeDef",
    "TargetTrackingConfigurationTypeDef",
    "DescribeScalingPlansRequestDescribeScalingPlansPaginateTypeDef",
    "DescribeScalingPlansRequestRequestTypeDef",
    "ScalingInstructionOutputTypeDef",
    "ScalingPolicyTypeDef",
    "ScalingInstructionTypeDef",
    "ScalingPlanTypeDef",
    "ScalingPlanResourceTypeDef",
    "ScalingInstructionUnionTypeDef",
    "DescribeScalingPlansResponseTypeDef",
    "DescribeScalingPlanResourcesResponseTypeDef",
    "CreateScalingPlanRequestRequestTypeDef",
    "UpdateScalingPlanRequestRequestTypeDef",
)

TagFilterOutputTypeDef = TypedDict(
    "TagFilterOutputTypeDef",
    {
        "Key": NotRequired[str],
        "Values": NotRequired[List[str]],
    },
)
TagFilterTypeDef = TypedDict(
    "TagFilterTypeDef",
    {
        "Key": NotRequired[str],
        "Values": NotRequired[Sequence[str]],
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
MetricDimensionTypeDef = TypedDict(
    "MetricDimensionTypeDef",
    {
        "Name": str,
        "Value": str,
    },
)
DatapointTypeDef = TypedDict(
    "DatapointTypeDef",
    {
        "Timestamp": NotRequired[datetime],
        "Value": NotRequired[float],
    },
)
DeleteScalingPlanRequestRequestTypeDef = TypedDict(
    "DeleteScalingPlanRequestRequestTypeDef",
    {
        "ScalingPlanName": str,
        "ScalingPlanVersion": int,
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
DescribeScalingPlanResourcesRequestRequestTypeDef = TypedDict(
    "DescribeScalingPlanResourcesRequestRequestTypeDef",
    {
        "ScalingPlanName": str,
        "ScalingPlanVersion": int,
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)
TimestampTypeDef = Union[datetime, str]
PredefinedLoadMetricSpecificationTypeDef = TypedDict(
    "PredefinedLoadMetricSpecificationTypeDef",
    {
        "PredefinedLoadMetricType": LoadMetricTypeType,
        "ResourceLabel": NotRequired[str],
    },
)
PredefinedScalingMetricSpecificationTypeDef = TypedDict(
    "PredefinedScalingMetricSpecificationTypeDef",
    {
        "PredefinedScalingMetricType": ScalingMetricTypeType,
        "ResourceLabel": NotRequired[str],
    },
)
ApplicationSourceOutputTypeDef = TypedDict(
    "ApplicationSourceOutputTypeDef",
    {
        "CloudFormationStackARN": NotRequired[str],
        "TagFilters": NotRequired[List[TagFilterOutputTypeDef]],
    },
)
ApplicationSourceTypeDef = TypedDict(
    "ApplicationSourceTypeDef",
    {
        "CloudFormationStackARN": NotRequired[str],
        "TagFilters": NotRequired[Sequence[TagFilterTypeDef]],
    },
)
CreateScalingPlanResponseTypeDef = TypedDict(
    "CreateScalingPlanResponseTypeDef",
    {
        "ScalingPlanVersion": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CustomizedLoadMetricSpecificationOutputTypeDef = TypedDict(
    "CustomizedLoadMetricSpecificationOutputTypeDef",
    {
        "MetricName": str,
        "Namespace": str,
        "Statistic": MetricStatisticType,
        "Dimensions": NotRequired[List[MetricDimensionTypeDef]],
        "Unit": NotRequired[str],
    },
)
CustomizedLoadMetricSpecificationTypeDef = TypedDict(
    "CustomizedLoadMetricSpecificationTypeDef",
    {
        "MetricName": str,
        "Namespace": str,
        "Statistic": MetricStatisticType,
        "Dimensions": NotRequired[Sequence[MetricDimensionTypeDef]],
        "Unit": NotRequired[str],
    },
)
CustomizedScalingMetricSpecificationOutputTypeDef = TypedDict(
    "CustomizedScalingMetricSpecificationOutputTypeDef",
    {
        "MetricName": str,
        "Namespace": str,
        "Statistic": MetricStatisticType,
        "Dimensions": NotRequired[List[MetricDimensionTypeDef]],
        "Unit": NotRequired[str],
    },
)
CustomizedScalingMetricSpecificationTypeDef = TypedDict(
    "CustomizedScalingMetricSpecificationTypeDef",
    {
        "MetricName": str,
        "Namespace": str,
        "Statistic": MetricStatisticType,
        "Dimensions": NotRequired[Sequence[MetricDimensionTypeDef]],
        "Unit": NotRequired[str],
    },
)
GetScalingPlanResourceForecastDataResponseTypeDef = TypedDict(
    "GetScalingPlanResourceForecastDataResponseTypeDef",
    {
        "Datapoints": List[DatapointTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DescribeScalingPlanResourcesRequestDescribeScalingPlanResourcesPaginateTypeDef = TypedDict(
    "DescribeScalingPlanResourcesRequestDescribeScalingPlanResourcesPaginateTypeDef",
    {
        "ScalingPlanName": str,
        "ScalingPlanVersion": int,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
GetScalingPlanResourceForecastDataRequestRequestTypeDef = TypedDict(
    "GetScalingPlanResourceForecastDataRequestRequestTypeDef",
    {
        "ScalingPlanName": str,
        "ScalingPlanVersion": int,
        "ServiceNamespace": ServiceNamespaceType,
        "ResourceId": str,
        "ScalableDimension": ScalableDimensionType,
        "ForecastDataType": ForecastDataTypeType,
        "StartTime": TimestampTypeDef,
        "EndTime": TimestampTypeDef,
    },
)
ApplicationSourceUnionTypeDef = Union[ApplicationSourceTypeDef, ApplicationSourceOutputTypeDef]
TargetTrackingConfigurationOutputTypeDef = TypedDict(
    "TargetTrackingConfigurationOutputTypeDef",
    {
        "TargetValue": float,
        "PredefinedScalingMetricSpecification": NotRequired[
            PredefinedScalingMetricSpecificationTypeDef
        ],
        "CustomizedScalingMetricSpecification": NotRequired[
            CustomizedScalingMetricSpecificationOutputTypeDef
        ],
        "DisableScaleIn": NotRequired[bool],
        "ScaleOutCooldown": NotRequired[int],
        "ScaleInCooldown": NotRequired[int],
        "EstimatedInstanceWarmup": NotRequired[int],
    },
)
TargetTrackingConfigurationTypeDef = TypedDict(
    "TargetTrackingConfigurationTypeDef",
    {
        "TargetValue": float,
        "PredefinedScalingMetricSpecification": NotRequired[
            PredefinedScalingMetricSpecificationTypeDef
        ],
        "CustomizedScalingMetricSpecification": NotRequired[
            CustomizedScalingMetricSpecificationTypeDef
        ],
        "DisableScaleIn": NotRequired[bool],
        "ScaleOutCooldown": NotRequired[int],
        "ScaleInCooldown": NotRequired[int],
        "EstimatedInstanceWarmup": NotRequired[int],
    },
)
DescribeScalingPlansRequestDescribeScalingPlansPaginateTypeDef = TypedDict(
    "DescribeScalingPlansRequestDescribeScalingPlansPaginateTypeDef",
    {
        "ScalingPlanNames": NotRequired[Sequence[str]],
        "ScalingPlanVersion": NotRequired[int],
        "ApplicationSources": NotRequired[Sequence[ApplicationSourceUnionTypeDef]],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
DescribeScalingPlansRequestRequestTypeDef = TypedDict(
    "DescribeScalingPlansRequestRequestTypeDef",
    {
        "ScalingPlanNames": NotRequired[Sequence[str]],
        "ScalingPlanVersion": NotRequired[int],
        "ApplicationSources": NotRequired[Sequence[ApplicationSourceUnionTypeDef]],
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)
ScalingInstructionOutputTypeDef = TypedDict(
    "ScalingInstructionOutputTypeDef",
    {
        "ServiceNamespace": ServiceNamespaceType,
        "ResourceId": str,
        "ScalableDimension": ScalableDimensionType,
        "MinCapacity": int,
        "MaxCapacity": int,
        "TargetTrackingConfigurations": List[TargetTrackingConfigurationOutputTypeDef],
        "PredefinedLoadMetricSpecification": NotRequired[PredefinedLoadMetricSpecificationTypeDef],
        "CustomizedLoadMetricSpecification": NotRequired[
            CustomizedLoadMetricSpecificationOutputTypeDef
        ],
        "ScheduledActionBufferTime": NotRequired[int],
        "PredictiveScalingMaxCapacityBehavior": NotRequired[
            PredictiveScalingMaxCapacityBehaviorType
        ],
        "PredictiveScalingMaxCapacityBuffer": NotRequired[int],
        "PredictiveScalingMode": NotRequired[PredictiveScalingModeType],
        "ScalingPolicyUpdateBehavior": NotRequired[ScalingPolicyUpdateBehaviorType],
        "DisableDynamicScaling": NotRequired[bool],
    },
)
ScalingPolicyTypeDef = TypedDict(
    "ScalingPolicyTypeDef",
    {
        "PolicyName": str,
        "PolicyType": Literal["TargetTrackingScaling"],
        "TargetTrackingConfiguration": NotRequired[TargetTrackingConfigurationOutputTypeDef],
    },
)
ScalingInstructionTypeDef = TypedDict(
    "ScalingInstructionTypeDef",
    {
        "ServiceNamespace": ServiceNamespaceType,
        "ResourceId": str,
        "ScalableDimension": ScalableDimensionType,
        "MinCapacity": int,
        "MaxCapacity": int,
        "TargetTrackingConfigurations": Sequence[TargetTrackingConfigurationTypeDef],
        "PredefinedLoadMetricSpecification": NotRequired[PredefinedLoadMetricSpecificationTypeDef],
        "CustomizedLoadMetricSpecification": NotRequired[CustomizedLoadMetricSpecificationTypeDef],
        "ScheduledActionBufferTime": NotRequired[int],
        "PredictiveScalingMaxCapacityBehavior": NotRequired[
            PredictiveScalingMaxCapacityBehaviorType
        ],
        "PredictiveScalingMaxCapacityBuffer": NotRequired[int],
        "PredictiveScalingMode": NotRequired[PredictiveScalingModeType],
        "ScalingPolicyUpdateBehavior": NotRequired[ScalingPolicyUpdateBehaviorType],
        "DisableDynamicScaling": NotRequired[bool],
    },
)
ScalingPlanTypeDef = TypedDict(
    "ScalingPlanTypeDef",
    {
        "ScalingPlanName": str,
        "ScalingPlanVersion": int,
        "ApplicationSource": ApplicationSourceOutputTypeDef,
        "ScalingInstructions": List[ScalingInstructionOutputTypeDef],
        "StatusCode": ScalingPlanStatusCodeType,
        "StatusMessage": NotRequired[str],
        "StatusStartTime": NotRequired[datetime],
        "CreationTime": NotRequired[datetime],
    },
)
ScalingPlanResourceTypeDef = TypedDict(
    "ScalingPlanResourceTypeDef",
    {
        "ScalingPlanName": str,
        "ScalingPlanVersion": int,
        "ServiceNamespace": ServiceNamespaceType,
        "ResourceId": str,
        "ScalableDimension": ScalableDimensionType,
        "ScalingStatusCode": ScalingStatusCodeType,
        "ScalingPolicies": NotRequired[List[ScalingPolicyTypeDef]],
        "ScalingStatusMessage": NotRequired[str],
    },
)
ScalingInstructionUnionTypeDef = Union[ScalingInstructionTypeDef, ScalingInstructionOutputTypeDef]
DescribeScalingPlansResponseTypeDef = TypedDict(
    "DescribeScalingPlansResponseTypeDef",
    {
        "ScalingPlans": List[ScalingPlanTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
DescribeScalingPlanResourcesResponseTypeDef = TypedDict(
    "DescribeScalingPlanResourcesResponseTypeDef",
    {
        "ScalingPlanResources": List[ScalingPlanResourceTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
        "NextToken": NotRequired[str],
    },
)
CreateScalingPlanRequestRequestTypeDef = TypedDict(
    "CreateScalingPlanRequestRequestTypeDef",
    {
        "ScalingPlanName": str,
        "ApplicationSource": ApplicationSourceTypeDef,
        "ScalingInstructions": Sequence[ScalingInstructionUnionTypeDef],
    },
)
UpdateScalingPlanRequestRequestTypeDef = TypedDict(
    "UpdateScalingPlanRequestRequestTypeDef",
    {
        "ScalingPlanName": str,
        "ScalingPlanVersion": int,
        "ApplicationSource": NotRequired[ApplicationSourceTypeDef],
        "ScalingInstructions": NotRequired[Sequence[ScalingInstructionUnionTypeDef]],
    },
)
