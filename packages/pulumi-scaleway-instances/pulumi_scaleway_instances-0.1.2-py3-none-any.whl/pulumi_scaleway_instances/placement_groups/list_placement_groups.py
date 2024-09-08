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
    'ScalewayInstanceV1ListPlacementGroupsResponse',
    'AwaitableScalewayInstanceV1ListPlacementGroupsResponse',
    'list_placement_groups',
    'list_placement_groups_output',
]

@pulumi.output_type
class ScalewayInstanceV1ListPlacementGroupsResponse:
    def __init__(__self__, placement_groups=None):
        if placement_groups and not isinstance(placement_groups, list):
            raise TypeError("Expected argument 'placement_groups' to be a list")
        pulumi.set(__self__, "placement_groups", placement_groups)

    @property
    @pulumi.getter(name="placementGroups")
    def placement_groups(self) -> Optional[Sequence['outputs.ScalewayInstanceV1PlacementGroup']]:
        """
        List of placement groups
        """
        return pulumi.get(self, "placement_groups")


class AwaitableScalewayInstanceV1ListPlacementGroupsResponse(ScalewayInstanceV1ListPlacementGroupsResponse):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ScalewayInstanceV1ListPlacementGroupsResponse(
            placement_groups=self.placement_groups)


def list_placement_groups(zone: Optional[str] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableScalewayInstanceV1ListPlacementGroupsResponse:
    """
    Use this data source to access information about an existing resource.

    :param str zone: The zone you want to target
    """
    __args__ = dict()
    __args__['zone'] = zone
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('scaleway-instances:placement_groups:listPlacementGroups', __args__, opts=opts, typ=ScalewayInstanceV1ListPlacementGroupsResponse).value

    return AwaitableScalewayInstanceV1ListPlacementGroupsResponse(
        placement_groups=pulumi.get(__ret__, 'placement_groups'))


@_utilities.lift_output_func(list_placement_groups)
def list_placement_groups_output(zone: Optional[pulumi.Input[str]] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[ScalewayInstanceV1ListPlacementGroupsResponse]:
    """
    Use this data source to access information about an existing resource.

    :param str zone: The zone you want to target
    """
    ...
