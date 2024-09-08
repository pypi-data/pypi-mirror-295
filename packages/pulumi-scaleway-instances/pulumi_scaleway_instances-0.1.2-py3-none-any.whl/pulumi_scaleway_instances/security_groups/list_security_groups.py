# coding=utf-8
# *** WARNING: this file was generated by pulumigen. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload, Awaitable
from .. import _utilities
from . import outputs
from ._enums import *

__all__ = [
    'ScalewayInstanceV1ListSecurityGroupsResponse',
    'AwaitableScalewayInstanceV1ListSecurityGroupsResponse',
    'list_security_groups',
    'list_security_groups_output',
]

@pulumi.output_type
class ScalewayInstanceV1ListSecurityGroupsResponse:
    def __init__(__self__, security_groups=None, total_count=None):
        if security_groups and not isinstance(security_groups, list):
            raise TypeError("Expected argument 'security_groups' to be a list")
        pulumi.set(__self__, "security_groups", security_groups)
        if total_count and not isinstance(total_count, float):
            raise TypeError("Expected argument 'total_count' to be a float")
        pulumi.set(__self__, "total_count", total_count)

    @property
    @pulumi.getter(name="securityGroups")
    def security_groups(self) -> Optional[Sequence['outputs.ScalewayInstanceV1SecurityGroup']]:
        return pulumi.get(self, "security_groups")

    @property
    @pulumi.getter(name="totalCount")
    def total_count(self) -> Optional[float]:
        return pulumi.get(self, "total_count")


class AwaitableScalewayInstanceV1ListSecurityGroupsResponse(ScalewayInstanceV1ListSecurityGroupsResponse):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ScalewayInstanceV1ListSecurityGroupsResponse(
            security_groups=self.security_groups,
            total_count=self.total_count)


def list_security_groups(zone: Optional[str] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableScalewayInstanceV1ListSecurityGroupsResponse:
    """
    Use this data source to access information about an existing resource.

    :param str zone: The zone you want to target
    """
    __args__ = dict()
    __args__['zone'] = zone
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('scaleway-instances:security_groups:listSecurityGroups', __args__, opts=opts, typ=ScalewayInstanceV1ListSecurityGroupsResponse).value

    return AwaitableScalewayInstanceV1ListSecurityGroupsResponse(
        security_groups=pulumi.get(__ret__, 'security_groups'),
        total_count=pulumi.get(__ret__, 'total_count'))


@_utilities.lift_output_func(list_security_groups)
def list_security_groups_output(zone: Optional[pulumi.Input[str]] = None,
                                opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[ScalewayInstanceV1ListSecurityGroupsResponse]:
    """
    Use this data source to access information about an existing resource.

    :param str zone: The zone you want to target
    """
    ...
