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
    'ScalewayInstanceV1ListSecurityGroupRulesResponse',
    'AwaitableScalewayInstanceV1ListSecurityGroupRulesResponse',
    'list_default_security_group_rules',
    'list_default_security_group_rules_output',
]

@pulumi.output_type
class ScalewayInstanceV1ListSecurityGroupRulesResponse:
    def __init__(__self__, rules=None):
        if rules and not isinstance(rules, list):
            raise TypeError("Expected argument 'rules' to be a list")
        pulumi.set(__self__, "rules", rules)

    @property
    @pulumi.getter
    def rules(self) -> Optional[Sequence['outputs.ScalewayInstanceV1SecurityGroupRule']]:
        """
        List of security rules
        """
        return pulumi.get(self, "rules")


class AwaitableScalewayInstanceV1ListSecurityGroupRulesResponse(ScalewayInstanceV1ListSecurityGroupRulesResponse):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ScalewayInstanceV1ListSecurityGroupRulesResponse(
            rules=self.rules)


def list_default_security_group_rules(zone: Optional[str] = None,
                                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableScalewayInstanceV1ListSecurityGroupRulesResponse:
    """
    Use this data source to access information about an existing resource.

    :param str zone: The zone you want to target
    """
    __args__ = dict()
    __args__['zone'] = zone
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('scaleway-instances:rules:listDefaultSecurityGroupRules', __args__, opts=opts, typ=ScalewayInstanceV1ListSecurityGroupRulesResponse).value

    return AwaitableScalewayInstanceV1ListSecurityGroupRulesResponse(
        rules=pulumi.get(__ret__, 'rules'))


@_utilities.lift_output_func(list_default_security_group_rules)
def list_default_security_group_rules_output(zone: Optional[pulumi.Input[str]] = None,
                                             opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[ScalewayInstanceV1ListSecurityGroupRulesResponse]:
    """
    Use this data source to access information about an existing resource.

    :param str zone: The zone you want to target
    """
    ...
