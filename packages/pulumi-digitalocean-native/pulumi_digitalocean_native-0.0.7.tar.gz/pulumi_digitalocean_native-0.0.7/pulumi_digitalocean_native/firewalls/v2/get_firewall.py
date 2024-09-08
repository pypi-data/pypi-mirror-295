# coding=utf-8
# *** WARNING: this file was generated by pulumigen. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload, Awaitable
from ... import _utilities
from . import outputs
from ._enums import *

__all__ = [
    'GetFirewallProperties',
    'AwaitableGetFirewallProperties',
    'get_firewall',
    'get_firewall_output',
]

@pulumi.output_type
class GetFirewallProperties:
    def __init__(__self__, firewall=None):
        if firewall and not isinstance(firewall, dict):
            raise TypeError("Expected argument 'firewall' to be a dict")
        pulumi.set(__self__, "firewall", firewall)

    @property
    @pulumi.getter
    def firewall(self) -> Optional['outputs.Firewall']:
        return pulumi.get(self, "firewall")


class AwaitableGetFirewallProperties(GetFirewallProperties):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetFirewallProperties(
            firewall=self.firewall)


def get_firewall(firewall_id: Optional[str] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetFirewallProperties:
    """
    Use this data source to access information about an existing resource.

    :param str firewall_id: A unique ID that can be used to identify and reference a firewall.
    """
    __args__ = dict()
    __args__['firewallId'] = firewall_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('digitalocean-native:firewalls/v2:getFirewall', __args__, opts=opts, typ=GetFirewallProperties).value

    return AwaitableGetFirewallProperties(
        firewall=pulumi.get(__ret__, 'firewall'))


@_utilities.lift_output_func(get_firewall)
def get_firewall_output(firewall_id: Optional[pulumi.Input[str]] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetFirewallProperties]:
    """
    Use this data source to access information about an existing resource.

    :param str firewall_id: A unique ID that can be used to identify and reference a firewall.
    """
    ...
