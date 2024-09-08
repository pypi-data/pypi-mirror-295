# coding=utf-8
# *** WARNING: this file was generated by pulumigen. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *

__all__ = ['Ext4Args', 'Ext4']

@pulumi.input_type
class Ext4Args:
    def __init__(__self__, *,
                 region: pulumi.Input['Ext4PropertiesRegion'],
                 created_at: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 droplet_ids: Optional[pulumi.Input[Sequence[pulumi.Input[int]]]] = None,
                 filesystem_label: Optional[pulumi.Input[str]] = None,
                 filesystem_type: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 size_gigabytes: Optional[pulumi.Input[int]] = None,
                 snapshot_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a Ext4 resource.
        :param pulumi.Input['Ext4PropertiesRegion'] region: The slug identifier for the region where the resource will initially be  available.
        :param pulumi.Input[str] created_at: A time value given in ISO8601 combined date and time format that represents when the block storage volume was created.
        :param pulumi.Input[str] description: An optional free-form text field to describe a block storage volume.
        :param pulumi.Input[Sequence[pulumi.Input[int]]] droplet_ids: An array containing the IDs of the Droplets the volume is attached to. Note that at this time, a volume can only be attached to a single Droplet.
        :param pulumi.Input[str] filesystem_type: The name of the filesystem type to be used on the volume. When provided, the volume will automatically be formatted to the specified filesystem type. Currently, the available options are `ext4` and `xfs`. Pre-formatted volumes are automatically mounted when attached to Ubuntu, Debian, Fedora, Fedora Atomic, and CentOS Droplets created on or after April 26, 2018. Attaching pre-formatted volumes to other Droplets is not recommended.
        :param pulumi.Input[str] name: A human-readable name for the block storage volume. Must be lowercase and be composed only of numbers, letters and "-", up to a limit of 64 characters. The name must begin with a letter.
        :param pulumi.Input[int] size_gigabytes: The size of the block storage volume in GiB (1024^3). This field does not apply  when creating a volume from a snapshot.
        :param pulumi.Input[str] snapshot_id: The unique identifier for the volume snapshot from which to create the volume.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tags: A flat array of tag names as strings to be applied to the resource. Tag names may be for either existing or new tags.
        """
        pulumi.set(__self__, "region", region)
        if created_at is not None:
            pulumi.set(__self__, "created_at", created_at)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if droplet_ids is not None:
            pulumi.set(__self__, "droplet_ids", droplet_ids)
        if filesystem_label is not None:
            pulumi.set(__self__, "filesystem_label", filesystem_label)
        if filesystem_type is not None:
            pulumi.set(__self__, "filesystem_type", filesystem_type)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if size_gigabytes is not None:
            pulumi.set(__self__, "size_gigabytes", size_gigabytes)
        if snapshot_id is not None:
            pulumi.set(__self__, "snapshot_id", snapshot_id)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def region(self) -> pulumi.Input['Ext4PropertiesRegion']:
        """
        The slug identifier for the region where the resource will initially be  available.
        """
        return pulumi.get(self, "region")

    @region.setter
    def region(self, value: pulumi.Input['Ext4PropertiesRegion']):
        pulumi.set(self, "region", value)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> Optional[pulumi.Input[str]]:
        """
        A time value given in ISO8601 combined date and time format that represents when the block storage volume was created.
        """
        return pulumi.get(self, "created_at")

    @created_at.setter
    def created_at(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "created_at", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        An optional free-form text field to describe a block storage volume.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="dropletIds")
    def droplet_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[int]]]]:
        """
        An array containing the IDs of the Droplets the volume is attached to. Note that at this time, a volume can only be attached to a single Droplet.
        """
        return pulumi.get(self, "droplet_ids")

    @droplet_ids.setter
    def droplet_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[int]]]]):
        pulumi.set(self, "droplet_ids", value)

    @property
    @pulumi.getter(name="filesystemLabel")
    def filesystem_label(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "filesystem_label")

    @filesystem_label.setter
    def filesystem_label(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "filesystem_label", value)

    @property
    @pulumi.getter(name="filesystemType")
    def filesystem_type(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the filesystem type to be used on the volume. When provided, the volume will automatically be formatted to the specified filesystem type. Currently, the available options are `ext4` and `xfs`. Pre-formatted volumes are automatically mounted when attached to Ubuntu, Debian, Fedora, Fedora Atomic, and CentOS Droplets created on or after April 26, 2018. Attaching pre-formatted volumes to other Droplets is not recommended.
        """
        return pulumi.get(self, "filesystem_type")

    @filesystem_type.setter
    def filesystem_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "filesystem_type", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        A human-readable name for the block storage volume. Must be lowercase and be composed only of numbers, letters and "-", up to a limit of 64 characters. The name must begin with a letter.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="sizeGigabytes")
    def size_gigabytes(self) -> Optional[pulumi.Input[int]]:
        """
        The size of the block storage volume in GiB (1024^3). This field does not apply  when creating a volume from a snapshot.
        """
        return pulumi.get(self, "size_gigabytes")

    @size_gigabytes.setter
    def size_gigabytes(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "size_gigabytes", value)

    @property
    @pulumi.getter(name="snapshotId")
    def snapshot_id(self) -> Optional[pulumi.Input[str]]:
        """
        The unique identifier for the volume snapshot from which to create the volume.
        """
        return pulumi.get(self, "snapshot_id")

    @snapshot_id.setter
    def snapshot_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "snapshot_id", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A flat array of tag names as strings to be applied to the resource. Tag names may be for either existing or new tags.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


class Ext4(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 created_at: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 droplet_ids: Optional[pulumi.Input[Sequence[pulumi.Input[int]]]] = None,
                 filesystem_label: Optional[pulumi.Input[str]] = None,
                 filesystem_type: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input['Ext4PropertiesRegion']] = None,
                 size_gigabytes: Optional[pulumi.Input[int]] = None,
                 snapshot_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Create a Ext4 resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] created_at: A time value given in ISO8601 combined date and time format that represents when the block storage volume was created.
        :param pulumi.Input[str] description: An optional free-form text field to describe a block storage volume.
        :param pulumi.Input[Sequence[pulumi.Input[int]]] droplet_ids: An array containing the IDs of the Droplets the volume is attached to. Note that at this time, a volume can only be attached to a single Droplet.
        :param pulumi.Input[str] filesystem_type: The name of the filesystem type to be used on the volume. When provided, the volume will automatically be formatted to the specified filesystem type. Currently, the available options are `ext4` and `xfs`. Pre-formatted volumes are automatically mounted when attached to Ubuntu, Debian, Fedora, Fedora Atomic, and CentOS Droplets created on or after April 26, 2018. Attaching pre-formatted volumes to other Droplets is not recommended.
        :param pulumi.Input[str] name: A human-readable name for the block storage volume. Must be lowercase and be composed only of numbers, letters and "-", up to a limit of 64 characters. The name must begin with a letter.
        :param pulumi.Input['Ext4PropertiesRegion'] region: The slug identifier for the region where the resource will initially be  available.
        :param pulumi.Input[int] size_gigabytes: The size of the block storage volume in GiB (1024^3). This field does not apply  when creating a volume from a snapshot.
        :param pulumi.Input[str] snapshot_id: The unique identifier for the volume snapshot from which to create the volume.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tags: A flat array of tag names as strings to be applied to the resource. Tag names may be for either existing or new tags.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Ext4Args,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Create a Ext4 resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param Ext4Args args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(Ext4Args, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 created_at: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 droplet_ids: Optional[pulumi.Input[Sequence[pulumi.Input[int]]]] = None,
                 filesystem_label: Optional[pulumi.Input[str]] = None,
                 filesystem_type: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input['Ext4PropertiesRegion']] = None,
                 size_gigabytes: Optional[pulumi.Input[int]] = None,
                 snapshot_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = Ext4Args.__new__(Ext4Args)

            __props__.__dict__["created_at"] = created_at
            __props__.__dict__["description"] = description
            __props__.__dict__["droplet_ids"] = droplet_ids
            __props__.__dict__["filesystem_label"] = filesystem_label
            __props__.__dict__["filesystem_type"] = filesystem_type
            __props__.__dict__["name"] = name
            if region is None and not opts.urn:
                raise TypeError("Missing required property 'region'")
            __props__.__dict__["region"] = region
            __props__.__dict__["size_gigabytes"] = size_gigabytes
            __props__.__dict__["snapshot_id"] = snapshot_id
            __props__.__dict__["tags"] = tags
            __props__.__dict__["volume"] = None
        super(Ext4, __self__).__init__(
            'digitalocean-native:volumes/v2:Ext4',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Ext4':
        """
        Get an existing Ext4 resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = Ext4Args.__new__(Ext4Args)

        __props__.__dict__["created_at"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["droplet_ids"] = None
        __props__.__dict__["filesystem_label"] = None
        __props__.__dict__["filesystem_type"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["region"] = None
        __props__.__dict__["size_gigabytes"] = None
        __props__.__dict__["snapshot_id"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["volume"] = None
        return Ext4(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> pulumi.Output[Optional[str]]:
        """
        A time value given in ISO8601 combined date and time format that represents when the block storage volume was created.
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        An optional free-form text field to describe a block storage volume.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="dropletIds")
    def droplet_ids(self) -> pulumi.Output[Optional[Sequence[int]]]:
        """
        An array containing the IDs of the Droplets the volume is attached to. Note that at this time, a volume can only be attached to a single Droplet.
        """
        return pulumi.get(self, "droplet_ids")

    @property
    @pulumi.getter(name="filesystemLabel")
    def filesystem_label(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "filesystem_label")

    @property
    @pulumi.getter(name="filesystemType")
    def filesystem_type(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the filesystem type to be used on the volume. When provided, the volume will automatically be formatted to the specified filesystem type. Currently, the available options are `ext4` and `xfs`. Pre-formatted volumes are automatically mounted when attached to Ubuntu, Debian, Fedora, Fedora Atomic, and CentOS Droplets created on or after April 26, 2018. Attaching pre-formatted volumes to other Droplets is not recommended.
        """
        return pulumi.get(self, "filesystem_type")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[Optional[str]]:
        """
        A human-readable name for the block storage volume. Must be lowercase and be composed only of numbers, letters and "-", up to a limit of 64 characters. The name must begin with a letter.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def region(self) -> pulumi.Output[Optional['Ext4PropertiesRegion']]:
        """
        The slug identifier for the region where the resource will initially be  available.
        """
        return pulumi.get(self, "region")

    @property
    @pulumi.getter(name="sizeGigabytes")
    def size_gigabytes(self) -> pulumi.Output[Optional[int]]:
        """
        The size of the block storage volume in GiB (1024^3). This field does not apply  when creating a volume from a snapshot.
        """
        return pulumi.get(self, "size_gigabytes")

    @property
    @pulumi.getter(name="snapshotId")
    def snapshot_id(self) -> pulumi.Output[Optional[str]]:
        """
        The unique identifier for the volume snapshot from which to create the volume.
        """
        return pulumi.get(self, "snapshot_id")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        A flat array of tag names as strings to be applied to the resource. Tag names may be for either existing or new tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def volume(self) -> pulumi.Output[Optional['outputs.VolumeFull']]:
        return pulumi.get(self, "volume")

