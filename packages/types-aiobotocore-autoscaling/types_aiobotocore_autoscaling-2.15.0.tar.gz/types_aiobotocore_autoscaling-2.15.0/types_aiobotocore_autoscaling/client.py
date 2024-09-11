"""
Type annotations for autoscaling service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_autoscaling.client import AutoScalingClient

    session = get_session()
    async with session.create_client("autoscaling") as client:
        client: AutoScalingClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import (
    DescribeAutoScalingGroupsPaginator,
    DescribeAutoScalingInstancesPaginator,
    DescribeLaunchConfigurationsPaginator,
    DescribeLoadBalancersPaginator,
    DescribeLoadBalancerTargetGroupsPaginator,
    DescribeNotificationConfigurationsPaginator,
    DescribePoliciesPaginator,
    DescribeScalingActivitiesPaginator,
    DescribeScheduledActionsPaginator,
    DescribeTagsPaginator,
    DescribeWarmPoolPaginator,
)
from .type_defs import (
    ActivitiesTypeTypeDef,
    ActivityTypeTypeDef,
    AttachInstancesQueryRequestTypeDef,
    AttachLoadBalancersTypeRequestTypeDef,
    AttachLoadBalancerTargetGroupsTypeRequestTypeDef,
    AttachTrafficSourcesTypeRequestTypeDef,
    AutoScalingGroupNamesTypeRequestTypeDef,
    AutoScalingGroupsTypeTypeDef,
    AutoScalingInstancesTypeTypeDef,
    BatchDeleteScheduledActionAnswerTypeDef,
    BatchDeleteScheduledActionTypeRequestTypeDef,
    BatchPutScheduledUpdateGroupActionAnswerTypeDef,
    BatchPutScheduledUpdateGroupActionTypeRequestTypeDef,
    CancelInstanceRefreshAnswerTypeDef,
    CancelInstanceRefreshTypeRequestTypeDef,
    CompleteLifecycleActionTypeRequestTypeDef,
    CreateAutoScalingGroupTypeRequestTypeDef,
    CreateLaunchConfigurationTypeRequestTypeDef,
    CreateOrUpdateTagsTypeRequestTypeDef,
    DeleteAutoScalingGroupTypeRequestTypeDef,
    DeleteLifecycleHookTypeRequestTypeDef,
    DeleteNotificationConfigurationTypeRequestTypeDef,
    DeletePolicyTypeRequestTypeDef,
    DeleteScheduledActionTypeRequestTypeDef,
    DeleteTagsTypeRequestTypeDef,
    DeleteWarmPoolTypeRequestTypeDef,
    DescribeAccountLimitsAnswerTypeDef,
    DescribeAdjustmentTypesAnswerTypeDef,
    DescribeAutoScalingInstancesTypeRequestTypeDef,
    DescribeAutoScalingNotificationTypesAnswerTypeDef,
    DescribeInstanceRefreshesAnswerTypeDef,
    DescribeInstanceRefreshesTypeRequestTypeDef,
    DescribeLifecycleHooksAnswerTypeDef,
    DescribeLifecycleHooksTypeRequestTypeDef,
    DescribeLifecycleHookTypesAnswerTypeDef,
    DescribeLoadBalancersRequestRequestTypeDef,
    DescribeLoadBalancersResponseTypeDef,
    DescribeLoadBalancerTargetGroupsRequestRequestTypeDef,
    DescribeLoadBalancerTargetGroupsResponseTypeDef,
    DescribeMetricCollectionTypesAnswerTypeDef,
    DescribeNotificationConfigurationsAnswerTypeDef,
    DescribeNotificationConfigurationsTypeRequestTypeDef,
    DescribePoliciesTypeRequestTypeDef,
    DescribeScalingActivitiesTypeRequestTypeDef,
    DescribeScheduledActionsTypeRequestTypeDef,
    DescribeTagsTypeRequestTypeDef,
    DescribeTerminationPolicyTypesAnswerTypeDef,
    DescribeTrafficSourcesRequestRequestTypeDef,
    DescribeTrafficSourcesResponseTypeDef,
    DescribeWarmPoolAnswerTypeDef,
    DescribeWarmPoolTypeRequestTypeDef,
    DetachInstancesAnswerTypeDef,
    DetachInstancesQueryRequestTypeDef,
    DetachLoadBalancersTypeRequestTypeDef,
    DetachLoadBalancerTargetGroupsTypeRequestTypeDef,
    DetachTrafficSourcesTypeRequestTypeDef,
    DisableMetricsCollectionQueryRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    EnableMetricsCollectionQueryRequestTypeDef,
    EnterStandbyAnswerTypeDef,
    EnterStandbyQueryRequestTypeDef,
    ExecutePolicyTypeRequestTypeDef,
    ExitStandbyAnswerTypeDef,
    ExitStandbyQueryRequestTypeDef,
    GetPredictiveScalingForecastAnswerTypeDef,
    GetPredictiveScalingForecastTypeRequestTypeDef,
    LaunchConfigurationNamesTypeRequestTypeDef,
    LaunchConfigurationNameTypeRequestTypeDef,
    LaunchConfigurationsTypeTypeDef,
    PoliciesTypeTypeDef,
    PolicyARNTypeTypeDef,
    ProcessesTypeTypeDef,
    PutLifecycleHookTypeRequestTypeDef,
    PutNotificationConfigurationTypeRequestTypeDef,
    PutScalingPolicyTypeRequestTypeDef,
    PutScheduledUpdateGroupActionTypeRequestTypeDef,
    PutWarmPoolTypeRequestTypeDef,
    RecordLifecycleActionHeartbeatTypeRequestTypeDef,
    RollbackInstanceRefreshAnswerTypeDef,
    RollbackInstanceRefreshTypeRequestTypeDef,
    ScalingProcessQueryRequestTypeDef,
    ScheduledActionsTypeTypeDef,
    SetDesiredCapacityTypeRequestTypeDef,
    SetInstanceHealthQueryRequestTypeDef,
    SetInstanceProtectionQueryRequestTypeDef,
    StartInstanceRefreshAnswerTypeDef,
    StartInstanceRefreshTypeRequestTypeDef,
    TagsTypeTypeDef,
    TerminateInstanceInAutoScalingGroupTypeRequestTypeDef,
    UpdateAutoScalingGroupTypeRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("AutoScalingClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ActiveInstanceRefreshNotFoundFault: Type[BotocoreClientError]
    AlreadyExistsFault: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InstanceRefreshInProgressFault: Type[BotocoreClientError]
    InvalidNextToken: Type[BotocoreClientError]
    IrreversibleInstanceRefreshFault: Type[BotocoreClientError]
    LimitExceededFault: Type[BotocoreClientError]
    ResourceContentionFault: Type[BotocoreClientError]
    ResourceInUseFault: Type[BotocoreClientError]
    ScalingActivityInProgressFault: Type[BotocoreClientError]
    ServiceLinkedRoleFailure: Type[BotocoreClientError]


class AutoScalingClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        AutoScalingClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#exceptions)
        """

    async def attach_instances(
        self, **kwargs: Unpack[AttachInstancesQueryRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Attaches one or more EC2 instances to the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.attach_instances)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#attach_instances)
        """

    async def attach_load_balancer_target_groups(
        self, **kwargs: Unpack[AttachLoadBalancerTargetGroupsTypeRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.attach_load_balancer_target_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#attach_load_balancer_target_groups)
        """

    async def attach_load_balancers(
        self, **kwargs: Unpack[AttachLoadBalancersTypeRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.attach_load_balancers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#attach_load_balancers)
        """

    async def attach_traffic_sources(
        self, **kwargs: Unpack[AttachTrafficSourcesTypeRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Attaches one or more traffic sources to the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.attach_traffic_sources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#attach_traffic_sources)
        """

    async def batch_delete_scheduled_action(
        self, **kwargs: Unpack[BatchDeleteScheduledActionTypeRequestTypeDef]
    ) -> BatchDeleteScheduledActionAnswerTypeDef:
        """
        Deletes one or more scheduled actions for the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.batch_delete_scheduled_action)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#batch_delete_scheduled_action)
        """

    async def batch_put_scheduled_update_group_action(
        self, **kwargs: Unpack[BatchPutScheduledUpdateGroupActionTypeRequestTypeDef]
    ) -> BatchPutScheduledUpdateGroupActionAnswerTypeDef:
        """
        Creates or updates one or more scheduled scaling actions for an Auto Scaling
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.batch_put_scheduled_update_group_action)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#batch_put_scheduled_update_group_action)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#can_paginate)
        """

    async def cancel_instance_refresh(
        self, **kwargs: Unpack[CancelInstanceRefreshTypeRequestTypeDef]
    ) -> CancelInstanceRefreshAnswerTypeDef:
        """
        Cancels an instance refresh or rollback that is in progress.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.cancel_instance_refresh)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#cancel_instance_refresh)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#close)
        """

    async def complete_lifecycle_action(
        self, **kwargs: Unpack[CompleteLifecycleActionTypeRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Completes the lifecycle action for the specified token or instance with the
        specified
        result.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.complete_lifecycle_action)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#complete_lifecycle_action)
        """

    async def create_auto_scaling_group(
        self, **kwargs: Unpack[CreateAutoScalingGroupTypeRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        **We strongly recommend using a launch template when calling this operation to
        ensure full functionality for Amazon EC2 Auto Scaling and Amazon EC2.** Creates
        an Auto Scaling group with the specified name and
        attributes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.create_auto_scaling_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#create_auto_scaling_group)
        """

    async def create_launch_configuration(
        self, **kwargs: Unpack[CreateLaunchConfigurationTypeRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates a launch configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.create_launch_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#create_launch_configuration)
        """

    async def create_or_update_tags(
        self, **kwargs: Unpack[CreateOrUpdateTagsTypeRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates or updates tags for the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.create_or_update_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#create_or_update_tags)
        """

    async def delete_auto_scaling_group(
        self, **kwargs: Unpack[DeleteAutoScalingGroupTypeRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.delete_auto_scaling_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#delete_auto_scaling_group)
        """

    async def delete_launch_configuration(
        self, **kwargs: Unpack[LaunchConfigurationNameTypeRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified launch configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.delete_launch_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#delete_launch_configuration)
        """

    async def delete_lifecycle_hook(
        self, **kwargs: Unpack[DeleteLifecycleHookTypeRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified lifecycle hook.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.delete_lifecycle_hook)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#delete_lifecycle_hook)
        """

    async def delete_notification_configuration(
        self, **kwargs: Unpack[DeleteNotificationConfigurationTypeRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified notification.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.delete_notification_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#delete_notification_configuration)
        """

    async def delete_policy(
        self, **kwargs: Unpack[DeletePolicyTypeRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified scaling policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.delete_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#delete_policy)
        """

    async def delete_scheduled_action(
        self, **kwargs: Unpack[DeleteScheduledActionTypeRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified scheduled action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.delete_scheduled_action)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#delete_scheduled_action)
        """

    async def delete_tags(
        self, **kwargs: Unpack[DeleteTagsTypeRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified tags.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.delete_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#delete_tags)
        """

    async def delete_warm_pool(
        self, **kwargs: Unpack[DeleteWarmPoolTypeRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the warm pool for the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.delete_warm_pool)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#delete_warm_pool)
        """

    async def describe_account_limits(self) -> DescribeAccountLimitsAnswerTypeDef:
        """
        Describes the current Amazon EC2 Auto Scaling resource quotas for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_account_limits)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#describe_account_limits)
        """

    async def describe_adjustment_types(self) -> DescribeAdjustmentTypesAnswerTypeDef:
        """
        Describes the available adjustment types for step scaling and simple scaling
        policies.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_adjustment_types)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#describe_adjustment_types)
        """

    async def describe_auto_scaling_groups(
        self, **kwargs: Unpack[AutoScalingGroupNamesTypeRequestTypeDef]
    ) -> AutoScalingGroupsTypeTypeDef:
        """
        Gets information about the Auto Scaling groups in the account and Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_auto_scaling_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#describe_auto_scaling_groups)
        """

    async def describe_auto_scaling_instances(
        self, **kwargs: Unpack[DescribeAutoScalingInstancesTypeRequestTypeDef]
    ) -> AutoScalingInstancesTypeTypeDef:
        """
        Gets information about the Auto Scaling instances in the account and Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_auto_scaling_instances)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#describe_auto_scaling_instances)
        """

    async def describe_auto_scaling_notification_types(
        self,
    ) -> DescribeAutoScalingNotificationTypesAnswerTypeDef:
        """
        Describes the notification types that are supported by Amazon EC2 Auto Scaling.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_auto_scaling_notification_types)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#describe_auto_scaling_notification_types)
        """

    async def describe_instance_refreshes(
        self, **kwargs: Unpack[DescribeInstanceRefreshesTypeRequestTypeDef]
    ) -> DescribeInstanceRefreshesAnswerTypeDef:
        """
        Gets information about the instance refreshes for the specified Auto Scaling
        group from the previous six
        weeks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_instance_refreshes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#describe_instance_refreshes)
        """

    async def describe_launch_configurations(
        self, **kwargs: Unpack[LaunchConfigurationNamesTypeRequestTypeDef]
    ) -> LaunchConfigurationsTypeTypeDef:
        """
        Gets information about the launch configurations in the account and Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_launch_configurations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#describe_launch_configurations)
        """

    async def describe_lifecycle_hook_types(self) -> DescribeLifecycleHookTypesAnswerTypeDef:
        """
        Describes the available types of lifecycle hooks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_lifecycle_hook_types)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#describe_lifecycle_hook_types)
        """

    async def describe_lifecycle_hooks(
        self, **kwargs: Unpack[DescribeLifecycleHooksTypeRequestTypeDef]
    ) -> DescribeLifecycleHooksAnswerTypeDef:
        """
        Gets information about the lifecycle hooks for the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_lifecycle_hooks)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#describe_lifecycle_hooks)
        """

    async def describe_load_balancer_target_groups(
        self, **kwargs: Unpack[DescribeLoadBalancerTargetGroupsRequestRequestTypeDef]
    ) -> DescribeLoadBalancerTargetGroupsResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_load_balancer_target_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#describe_load_balancer_target_groups)
        """

    async def describe_load_balancers(
        self, **kwargs: Unpack[DescribeLoadBalancersRequestRequestTypeDef]
    ) -> DescribeLoadBalancersResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_load_balancers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#describe_load_balancers)
        """

    async def describe_metric_collection_types(self) -> DescribeMetricCollectionTypesAnswerTypeDef:
        """
        Describes the available CloudWatch metrics for Amazon EC2 Auto Scaling.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_metric_collection_types)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#describe_metric_collection_types)
        """

    async def describe_notification_configurations(
        self, **kwargs: Unpack[DescribeNotificationConfigurationsTypeRequestTypeDef]
    ) -> DescribeNotificationConfigurationsAnswerTypeDef:
        """
        Gets information about the Amazon SNS notifications that are configured for one
        or more Auto Scaling
        groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_notification_configurations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#describe_notification_configurations)
        """

    async def describe_policies(
        self, **kwargs: Unpack[DescribePoliciesTypeRequestTypeDef]
    ) -> PoliciesTypeTypeDef:
        """
        Gets information about the scaling policies in the account and Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_policies)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#describe_policies)
        """

    async def describe_scaling_activities(
        self, **kwargs: Unpack[DescribeScalingActivitiesTypeRequestTypeDef]
    ) -> ActivitiesTypeTypeDef:
        """
        Gets information about the scaling activities in the account and Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_scaling_activities)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#describe_scaling_activities)
        """

    async def describe_scaling_process_types(self) -> ProcessesTypeTypeDef:
        """
        Describes the scaling process types for use with the  ResumeProcesses and
        SuspendProcesses
        APIs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_scaling_process_types)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#describe_scaling_process_types)
        """

    async def describe_scheduled_actions(
        self, **kwargs: Unpack[DescribeScheduledActionsTypeRequestTypeDef]
    ) -> ScheduledActionsTypeTypeDef:
        """
        Gets information about the scheduled actions that haven't run or that have not
        reached their end
        time.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_scheduled_actions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#describe_scheduled_actions)
        """

    async def describe_tags(
        self, **kwargs: Unpack[DescribeTagsTypeRequestTypeDef]
    ) -> TagsTypeTypeDef:
        """
        Describes the specified tags.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#describe_tags)
        """

    async def describe_termination_policy_types(
        self,
    ) -> DescribeTerminationPolicyTypesAnswerTypeDef:
        """
        Describes the termination policies supported by Amazon EC2 Auto Scaling.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_termination_policy_types)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#describe_termination_policy_types)
        """

    async def describe_traffic_sources(
        self, **kwargs: Unpack[DescribeTrafficSourcesRequestRequestTypeDef]
    ) -> DescribeTrafficSourcesResponseTypeDef:
        """
        Gets information about the traffic sources for the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_traffic_sources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#describe_traffic_sources)
        """

    async def describe_warm_pool(
        self, **kwargs: Unpack[DescribeWarmPoolTypeRequestTypeDef]
    ) -> DescribeWarmPoolAnswerTypeDef:
        """
        Gets information about a warm pool and its instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_warm_pool)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#describe_warm_pool)
        """

    async def detach_instances(
        self, **kwargs: Unpack[DetachInstancesQueryRequestTypeDef]
    ) -> DetachInstancesAnswerTypeDef:
        """
        Removes one or more instances from the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.detach_instances)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#detach_instances)
        """

    async def detach_load_balancer_target_groups(
        self, **kwargs: Unpack[DetachLoadBalancerTargetGroupsTypeRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.detach_load_balancer_target_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#detach_load_balancer_target_groups)
        """

    async def detach_load_balancers(
        self, **kwargs: Unpack[DetachLoadBalancersTypeRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.detach_load_balancers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#detach_load_balancers)
        """

    async def detach_traffic_sources(
        self, **kwargs: Unpack[DetachTrafficSourcesTypeRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Detaches one or more traffic sources from the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.detach_traffic_sources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#detach_traffic_sources)
        """

    async def disable_metrics_collection(
        self, **kwargs: Unpack[DisableMetricsCollectionQueryRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Disables group metrics collection for the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.disable_metrics_collection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#disable_metrics_collection)
        """

    async def enable_metrics_collection(
        self, **kwargs: Unpack[EnableMetricsCollectionQueryRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Enables group metrics collection for the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.enable_metrics_collection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#enable_metrics_collection)
        """

    async def enter_standby(
        self, **kwargs: Unpack[EnterStandbyQueryRequestTypeDef]
    ) -> EnterStandbyAnswerTypeDef:
        """
        Moves the specified instances into the standby state.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.enter_standby)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#enter_standby)
        """

    async def execute_policy(
        self, **kwargs: Unpack[ExecutePolicyTypeRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Executes the specified policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.execute_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#execute_policy)
        """

    async def exit_standby(
        self, **kwargs: Unpack[ExitStandbyQueryRequestTypeDef]
    ) -> ExitStandbyAnswerTypeDef:
        """
        Moves the specified instances out of the standby state.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.exit_standby)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#exit_standby)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#generate_presigned_url)
        """

    async def get_predictive_scaling_forecast(
        self, **kwargs: Unpack[GetPredictiveScalingForecastTypeRequestTypeDef]
    ) -> GetPredictiveScalingForecastAnswerTypeDef:
        """
        Retrieves the forecast data for a predictive scaling policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.get_predictive_scaling_forecast)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#get_predictive_scaling_forecast)
        """

    async def put_lifecycle_hook(
        self, **kwargs: Unpack[PutLifecycleHookTypeRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates or updates a lifecycle hook for the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.put_lifecycle_hook)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#put_lifecycle_hook)
        """

    async def put_notification_configuration(
        self, **kwargs: Unpack[PutNotificationConfigurationTypeRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Configures an Auto Scaling group to send notifications when specified events
        take
        place.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.put_notification_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#put_notification_configuration)
        """

    async def put_scaling_policy(
        self, **kwargs: Unpack[PutScalingPolicyTypeRequestTypeDef]
    ) -> PolicyARNTypeTypeDef:
        """
        Creates or updates a scaling policy for an Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.put_scaling_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#put_scaling_policy)
        """

    async def put_scheduled_update_group_action(
        self, **kwargs: Unpack[PutScheduledUpdateGroupActionTypeRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates or updates a scheduled scaling action for an Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.put_scheduled_update_group_action)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#put_scheduled_update_group_action)
        """

    async def put_warm_pool(
        self, **kwargs: Unpack[PutWarmPoolTypeRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates or updates a warm pool for the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.put_warm_pool)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#put_warm_pool)
        """

    async def record_lifecycle_action_heartbeat(
        self, **kwargs: Unpack[RecordLifecycleActionHeartbeatTypeRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Records a heartbeat for the lifecycle action associated with the specified
        token or
        instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.record_lifecycle_action_heartbeat)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#record_lifecycle_action_heartbeat)
        """

    async def resume_processes(
        self, **kwargs: Unpack[ScalingProcessQueryRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Resumes the specified suspended auto scaling processes, or all suspended
        process, for the specified Auto Scaling
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.resume_processes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#resume_processes)
        """

    async def rollback_instance_refresh(
        self, **kwargs: Unpack[RollbackInstanceRefreshTypeRequestTypeDef]
    ) -> RollbackInstanceRefreshAnswerTypeDef:
        """
        Cancels an instance refresh that is in progress and rolls back any changes that
        it
        made.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.rollback_instance_refresh)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#rollback_instance_refresh)
        """

    async def set_desired_capacity(
        self, **kwargs: Unpack[SetDesiredCapacityTypeRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Sets the size of the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.set_desired_capacity)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#set_desired_capacity)
        """

    async def set_instance_health(
        self, **kwargs: Unpack[SetInstanceHealthQueryRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Sets the health status of the specified instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.set_instance_health)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#set_instance_health)
        """

    async def set_instance_protection(
        self, **kwargs: Unpack[SetInstanceProtectionQueryRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the instance protection settings of the specified instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.set_instance_protection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#set_instance_protection)
        """

    async def start_instance_refresh(
        self, **kwargs: Unpack[StartInstanceRefreshTypeRequestTypeDef]
    ) -> StartInstanceRefreshAnswerTypeDef:
        """
        Starts an instance refresh.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.start_instance_refresh)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#start_instance_refresh)
        """

    async def suspend_processes(
        self, **kwargs: Unpack[ScalingProcessQueryRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Suspends the specified auto scaling processes, or all processes, for the
        specified Auto Scaling
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.suspend_processes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#suspend_processes)
        """

    async def terminate_instance_in_auto_scaling_group(
        self, **kwargs: Unpack[TerminateInstanceInAutoScalingGroupTypeRequestTypeDef]
    ) -> ActivityTypeTypeDef:
        """
        Terminates the specified instance and optionally adjusts the desired group size.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.terminate_instance_in_auto_scaling_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#terminate_instance_in_auto_scaling_group)
        """

    async def update_auto_scaling_group(
        self, **kwargs: Unpack[UpdateAutoScalingGroupTypeRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        **We strongly recommend that all Auto Scaling groups use launch templates to
        ensure full functionality for Amazon EC2 Auto Scaling and Amazon EC2.** Updates
        the configuration for the specified Auto Scaling
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.update_auto_scaling_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#update_auto_scaling_group)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_auto_scaling_groups"]
    ) -> DescribeAutoScalingGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_auto_scaling_instances"]
    ) -> DescribeAutoScalingInstancesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_launch_configurations"]
    ) -> DescribeLaunchConfigurationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_load_balancer_target_groups"]
    ) -> DescribeLoadBalancerTargetGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_load_balancers"]
    ) -> DescribeLoadBalancersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_notification_configurations"]
    ) -> DescribeNotificationConfigurationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_policies"]
    ) -> DescribePoliciesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_scaling_activities"]
    ) -> DescribeScalingActivitiesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_scheduled_actions"]
    ) -> DescribeScheduledActionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_tags"]) -> DescribeTagsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_warm_pool"]
    ) -> DescribeWarmPoolPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#get_paginator)
        """

    async def __aenter__(self) -> "AutoScalingClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/)
        """
