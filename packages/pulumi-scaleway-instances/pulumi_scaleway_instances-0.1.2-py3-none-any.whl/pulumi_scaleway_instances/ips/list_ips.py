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

__all__ = [
    'ScalewayInstanceV1ListIpsResponse',
    'AwaitableScalewayInstanceV1ListIpsResponse',
    'list_ips',
    'list_ips_output',
]

@pulumi.output_type
class ScalewayInstanceV1ListIpsResponse:
    def __init__(__self__, ips=None):
        if ips and not isinstance(ips, list):
            raise TypeError("Expected argument 'ips' to be a list")
        pulumi.set(__self__, "ips", ips)

    @property
    @pulumi.getter
    def ips(self) -> Optional[Sequence['outputs.ScalewayInstanceV1Ip']]:
        """
        List of ips
        """
        return pulumi.get(self, "ips")


class AwaitableScalewayInstanceV1ListIpsResponse(ScalewayInstanceV1ListIpsResponse):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ScalewayInstanceV1ListIpsResponse(
            ips=self.ips)


def list_ips(zone: Optional[str] = None,
             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableScalewayInstanceV1ListIpsResponse:
    """
    Use this data source to access information about an existing resource.

    :param str zone: The zone you want to target
    """
    __args__ = dict()
    __args__['zone'] = zone
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('scaleway-instances:ips:listIps', __args__, opts=opts, typ=ScalewayInstanceV1ListIpsResponse).value

    return AwaitableScalewayInstanceV1ListIpsResponse(
        ips=pulumi.get(__ret__, 'ips'))


@_utilities.lift_output_func(list_ips)
def list_ips_output(zone: Optional[pulumi.Input[str]] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[ScalewayInstanceV1ListIpsResponse]:
    """
    Use this data source to access information about an existing resource.

    :param str zone: The zone you want to target
    """
    ...
