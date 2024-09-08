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

__all__ = [
    'ListVpcsItems',
    'AwaitableListVpcsItems',
    'list_vpcs',
    'list_vpcs_output',
]

@pulumi.output_type
class ListVpcsItems:
    def __init__(__self__, links=None, meta=None, vpcs=None):
        if links and not isinstance(links, dict):
            raise TypeError("Expected argument 'links' to be a dict")
        pulumi.set(__self__, "links", links)
        if meta and not isinstance(meta, dict):
            raise TypeError("Expected argument 'meta' to be a dict")
        pulumi.set(__self__, "meta", meta)
        if vpcs and not isinstance(vpcs, list):
            raise TypeError("Expected argument 'vpcs' to be a list")
        pulumi.set(__self__, "vpcs", vpcs)

    @property
    @pulumi.getter
    def links(self) -> Optional['outputs.PageLinks']:
        return pulumi.get(self, "links")

    @property
    @pulumi.getter
    def meta(self) -> 'outputs.MetaMeta':
        return pulumi.get(self, "meta")

    @property
    @pulumi.getter
    def vpcs(self) -> Optional[Sequence['outputs.Vpc']]:
        return pulumi.get(self, "vpcs")


class AwaitableListVpcsItems(ListVpcsItems):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListVpcsItems(
            links=self.links,
            meta=self.meta,
            vpcs=self.vpcs)


def list_vpcs(opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListVpcsItems:
    """
    Use this data source to access information about an existing resource.
    """
    __args__ = dict()
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('digitalocean-native:vpcs/v2:listVpcs', __args__, opts=opts, typ=ListVpcsItems).value

    return AwaitableListVpcsItems(
        links=pulumi.get(__ret__, 'links'),
        meta=pulumi.get(__ret__, 'meta'),
        vpcs=pulumi.get(__ret__, 'vpcs'))


@_utilities.lift_output_func(list_vpcs)
def list_vpcs_output(opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[ListVpcsItems]:
    """
    Use this data source to access information about an existing resource.
    """
    ...
