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
    'ListDropletsAssociatedResourcesItems',
    'AwaitableListDropletsAssociatedResourcesItems',
    'list_droplets_associated_resources',
    'list_droplets_associated_resources_output',
]

@pulumi.output_type
class ListDropletsAssociatedResourcesItems:
    def __init__(__self__, floating_ips=None, reserved_ips=None, snapshots=None, volume_snapshots=None, volumes=None):
        if floating_ips and not isinstance(floating_ips, list):
            raise TypeError("Expected argument 'floating_ips' to be a list")
        pulumi.set(__self__, "floating_ips", floating_ips)
        if reserved_ips and not isinstance(reserved_ips, list):
            raise TypeError("Expected argument 'reserved_ips' to be a list")
        pulumi.set(__self__, "reserved_ips", reserved_ips)
        if snapshots and not isinstance(snapshots, list):
            raise TypeError("Expected argument 'snapshots' to be a list")
        pulumi.set(__self__, "snapshots", snapshots)
        if volume_snapshots and not isinstance(volume_snapshots, list):
            raise TypeError("Expected argument 'volume_snapshots' to be a list")
        pulumi.set(__self__, "volume_snapshots", volume_snapshots)
        if volumes and not isinstance(volumes, list):
            raise TypeError("Expected argument 'volumes' to be a list")
        pulumi.set(__self__, "volumes", volumes)

    @property
    @pulumi.getter(name="floatingIps")
    def floating_ips(self) -> Optional[Sequence['outputs.AssociatedResource']]:
        return pulumi.get(self, "floating_ips")

    @property
    @pulumi.getter(name="reservedIps")
    def reserved_ips(self) -> Optional[Sequence['outputs.AssociatedResource']]:
        return pulumi.get(self, "reserved_ips")

    @property
    @pulumi.getter
    def snapshots(self) -> Optional[Sequence['outputs.AssociatedResource']]:
        return pulumi.get(self, "snapshots")

    @property
    @pulumi.getter(name="volumeSnapshots")
    def volume_snapshots(self) -> Optional[Sequence['outputs.AssociatedResource']]:
        return pulumi.get(self, "volume_snapshots")

    @property
    @pulumi.getter
    def volumes(self) -> Optional[Sequence['outputs.AssociatedResource']]:
        return pulumi.get(self, "volumes")


class AwaitableListDropletsAssociatedResourcesItems(ListDropletsAssociatedResourcesItems):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListDropletsAssociatedResourcesItems(
            floating_ips=self.floating_ips,
            reserved_ips=self.reserved_ips,
            snapshots=self.snapshots,
            volume_snapshots=self.volume_snapshots,
            volumes=self.volumes)


def list_droplets_associated_resources(droplet_id: Optional[str] = None,
                                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListDropletsAssociatedResourcesItems:
    """
    Use this data source to access information about an existing resource.

    :param str droplet_id: A unique identifier for a Droplet instance.
    """
    __args__ = dict()
    __args__['dropletId'] = droplet_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('digitalocean-native:droplets/v2:listDropletsAssociatedResources', __args__, opts=opts, typ=ListDropletsAssociatedResourcesItems).value

    return AwaitableListDropletsAssociatedResourcesItems(
        floating_ips=pulumi.get(__ret__, 'floating_ips'),
        reserved_ips=pulumi.get(__ret__, 'reserved_ips'),
        snapshots=pulumi.get(__ret__, 'snapshots'),
        volume_snapshots=pulumi.get(__ret__, 'volume_snapshots'),
        volumes=pulumi.get(__ret__, 'volumes'))


@_utilities.lift_output_func(list_droplets_associated_resources)
def list_droplets_associated_resources_output(droplet_id: Optional[pulumi.Input[str]] = None,
                                              opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[ListDropletsAssociatedResourcesItems]:
    """
    Use this data source to access information about an existing resource.

    :param str droplet_id: A unique identifier for a Droplet instance.
    """
    ...
