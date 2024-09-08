# coding=utf-8
# *** WARNING: this file was generated by pulumigen. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from ._enums import *

__all__ = [
    'ScalewayInstanceV1PrivateNIC',
]

@pulumi.output_type
class ScalewayInstanceV1PrivateNIC(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "macAddress":
            suggest = "mac_address"
        elif key == "privateNetworkId":
            suggest = "private_network_id"
        elif key == "serverId":
            suggest = "server_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ScalewayInstanceV1PrivateNIC. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ScalewayInstanceV1PrivateNIC.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ScalewayInstanceV1PrivateNIC.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 id: Optional[str] = None,
                 mac_address: Optional[str] = None,
                 private_network_id: Optional[str] = None,
                 server_id: Optional[str] = None,
                 state: Optional['ScalewayInstanceV1PrivateNICState'] = None):
        """
        :param str id: The private NIC unique ID
        :param str mac_address: The private NIC MAC address
        :param str private_network_id: The private network where the private NIC is attached
        :param str server_id: The server the private NIC is attached to
        :param 'ScalewayInstanceV1PrivateNICState' state: The private NIC state
        """
        if id is not None:
            pulumi.set(__self__, "id", id)
        if mac_address is not None:
            pulumi.set(__self__, "mac_address", mac_address)
        if private_network_id is not None:
            pulumi.set(__self__, "private_network_id", private_network_id)
        if server_id is not None:
            pulumi.set(__self__, "server_id", server_id)
        if state is None:
            state = 'available'
        if state is not None:
            pulumi.set(__self__, "state", state)

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The private NIC unique ID
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="macAddress")
    def mac_address(self) -> Optional[str]:
        """
        The private NIC MAC address
        """
        return pulumi.get(self, "mac_address")

    @property
    @pulumi.getter(name="privateNetworkId")
    def private_network_id(self) -> Optional[str]:
        """
        The private network where the private NIC is attached
        """
        return pulumi.get(self, "private_network_id")

    @property
    @pulumi.getter(name="serverId")
    def server_id(self) -> Optional[str]:
        """
        The server the private NIC is attached to
        """
        return pulumi.get(self, "server_id")

    @property
    @pulumi.getter
    def state(self) -> Optional['ScalewayInstanceV1PrivateNICState']:
        """
        The private NIC state
        """
        return pulumi.get(self, "state")


