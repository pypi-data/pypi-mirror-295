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
    'GetLoadBalancerProperties',
    'AwaitableGetLoadBalancerProperties',
    'get_load_balancer',
    'get_load_balancer_output',
]

@pulumi.output_type
class GetLoadBalancerProperties:
    def __init__(__self__, load_balancer=None):
        if load_balancer and not isinstance(load_balancer, dict):
            raise TypeError("Expected argument 'load_balancer' to be a dict")
        pulumi.set(__self__, "load_balancer", load_balancer)

    @property
    @pulumi.getter(name="loadBalancer")
    def load_balancer(self) -> Optional['outputs.LoadBalancer']:
        return pulumi.get(self, "load_balancer")


class AwaitableGetLoadBalancerProperties(GetLoadBalancerProperties):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetLoadBalancerProperties(
            load_balancer=self.load_balancer)


def get_load_balancer(lb_id: Optional[str] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetLoadBalancerProperties:
    """
    Use this data source to access information about an existing resource.

    :param str lb_id: A unique identifier for a load balancer.
    """
    __args__ = dict()
    __args__['lbId'] = lb_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('digitalocean-native:load_balancers/v2:getLoadBalancer', __args__, opts=opts, typ=GetLoadBalancerProperties).value

    return AwaitableGetLoadBalancerProperties(
        load_balancer=pulumi.get(__ret__, 'load_balancer'))


@_utilities.lift_output_func(get_load_balancer)
def get_load_balancer_output(lb_id: Optional[pulumi.Input[str]] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetLoadBalancerProperties]:
    """
    Use this data source to access information about an existing resource.

    :param str lb_id: A unique identifier for a load balancer.
    """
    ...
