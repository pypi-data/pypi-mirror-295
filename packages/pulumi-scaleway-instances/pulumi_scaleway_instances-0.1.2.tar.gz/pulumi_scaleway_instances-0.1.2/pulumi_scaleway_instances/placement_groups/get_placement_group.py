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
    'ScalewayInstanceV1GetPlacementGroupResponse',
    'AwaitableScalewayInstanceV1GetPlacementGroupResponse',
    'get_placement_group',
    'get_placement_group_output',
]

@pulumi.output_type
class ScalewayInstanceV1GetPlacementGroupResponse:
    def __init__(__self__, placement_group=None):
        if placement_group and not isinstance(placement_group, dict):
            raise TypeError("Expected argument 'placement_group' to be a dict")
        pulumi.set(__self__, "placement_group", placement_group)

    @property
    @pulumi.getter(name="placementGroup")
    def placement_group(self) -> Optional['outputs.ScalewayInstanceV1PlacementGroup']:
        return pulumi.get(self, "placement_group")


class AwaitableScalewayInstanceV1GetPlacementGroupResponse(ScalewayInstanceV1GetPlacementGroupResponse):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ScalewayInstanceV1GetPlacementGroupResponse(
            placement_group=self.placement_group)


def get_placement_group(id: Optional[str] = None,
                        zone: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableScalewayInstanceV1GetPlacementGroupResponse:
    """
    Use this data source to access information about an existing resource.

    :param str id: UUID of the placement group you want to get
    :param str zone: The zone you want to target
    """
    __args__ = dict()
    __args__['id'] = id
    __args__['zone'] = zone
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('scaleway-instances:placement_groups:getPlacementGroup', __args__, opts=opts, typ=ScalewayInstanceV1GetPlacementGroupResponse).value

    return AwaitableScalewayInstanceV1GetPlacementGroupResponse(
        placement_group=pulumi.get(__ret__, 'placement_group'))


@_utilities.lift_output_func(get_placement_group)
def get_placement_group_output(id: Optional[pulumi.Input[str]] = None,
                               zone: Optional[pulumi.Input[str]] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[ScalewayInstanceV1GetPlacementGroupResponse]:
    """
    Use this data source to access information about an existing resource.

    :param str id: UUID of the placement group you want to get
    :param str zone: The zone you want to target
    """
    ...
