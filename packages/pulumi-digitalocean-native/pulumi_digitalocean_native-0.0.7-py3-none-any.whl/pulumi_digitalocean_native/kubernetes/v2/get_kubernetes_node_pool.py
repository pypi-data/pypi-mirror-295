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
    'GetKubernetesNodePoolProperties',
    'AwaitableGetKubernetesNodePoolProperties',
    'get_kubernetes_node_pool',
    'get_kubernetes_node_pool_output',
]

@pulumi.output_type
class GetKubernetesNodePoolProperties:
    def __init__(__self__, node_pool=None):
        if node_pool and not isinstance(node_pool, dict):
            raise TypeError("Expected argument 'node_pool' to be a dict")
        pulumi.set(__self__, "node_pool", node_pool)

    @property
    @pulumi.getter(name="nodePool")
    def node_pool(self) -> Optional['outputs.KubernetesNodePool']:
        return pulumi.get(self, "node_pool")


class AwaitableGetKubernetesNodePoolProperties(GetKubernetesNodePoolProperties):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetKubernetesNodePoolProperties(
            node_pool=self.node_pool)


def get_kubernetes_node_pool(cluster_id: Optional[str] = None,
                             node_pool_id: Optional[str] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetKubernetesNodePoolProperties:
    """
    Use this data source to access information about an existing resource.

    :param str cluster_id: A unique ID that can be used to reference a Kubernetes cluster.
    :param str node_pool_id: A unique ID that can be used to reference a Kubernetes node pool.
    """
    __args__ = dict()
    __args__['clusterId'] = cluster_id
    __args__['nodePoolId'] = node_pool_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('digitalocean-native:kubernetes/v2:getKubernetesNodePool', __args__, opts=opts, typ=GetKubernetesNodePoolProperties).value

    return AwaitableGetKubernetesNodePoolProperties(
        node_pool=pulumi.get(__ret__, 'node_pool'))


@_utilities.lift_output_func(get_kubernetes_node_pool)
def get_kubernetes_node_pool_output(cluster_id: Optional[pulumi.Input[str]] = None,
                                    node_pool_id: Optional[pulumi.Input[str]] = None,
                                    opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetKubernetesNodePoolProperties]:
    """
    Use this data source to access information about an existing resource.

    :param str cluster_id: A unique ID that can be used to reference a Kubernetes cluster.
    :param str node_pool_id: A unique ID that can be used to reference a Kubernetes node pool.
    """
    ...
