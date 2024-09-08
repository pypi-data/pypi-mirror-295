# coding=utf-8
# *** WARNING: this file was generated by pulumigen. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload, Awaitable
from ... import _utilities

__all__ = [
    'NeighborIds',
    'AwaitableNeighborIds',
    'list_droplets_neighbors_ids',
    'list_droplets_neighbors_ids_output',
]

@pulumi.output_type
class NeighborIds:
    def __init__(__self__, neighbor_ids=None):
        if neighbor_ids and not isinstance(neighbor_ids, list):
            raise TypeError("Expected argument 'neighbor_ids' to be a list")
        pulumi.set(__self__, "neighbor_ids", neighbor_ids)

    @property
    @pulumi.getter(name="neighborIds")
    def neighbor_ids(self) -> Optional[Sequence[Sequence[int]]]:
        """
        An array of arrays. Each array will contain a set of Droplet IDs for Droplets that share a physical server.
        """
        return pulumi.get(self, "neighbor_ids")


class AwaitableNeighborIds(NeighborIds):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return NeighborIds(
            neighbor_ids=self.neighbor_ids)


def list_droplets_neighbors_ids(opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableNeighborIds:
    """
    Use this data source to access information about an existing resource.
    """
    __args__ = dict()
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('digitalocean-native:reports/v2:listDropletsNeighborsIds', __args__, opts=opts, typ=NeighborIds).value

    return AwaitableNeighborIds(
        neighbor_ids=pulumi.get(__ret__, 'neighbor_ids'))


@_utilities.lift_output_func(list_droplets_neighbors_ids)
def list_droplets_neighbors_ids_output(opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[NeighborIds]:
    """
    Use this data source to access information about an existing resource.
    """
    ...
