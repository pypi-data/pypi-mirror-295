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

__all__ = ['ImagesCustomArgs', 'ImagesCustom']

@pulumi.input_type
class ImagesCustomArgs:
    def __init__(__self__, *,
                 description: Optional[pulumi.Input[str]] = None,
                 distribution: Optional[pulumi.Input['ImageUpdateDistribution']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input['ImagesCustomPropertiesRegion']] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 url: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a ImagesCustom resource.
        :param pulumi.Input[str] description: An optional free-form text field to describe an image.
        :param pulumi.Input['ImageUpdateDistribution'] distribution: The name of a custom image's distribution. Currently, the valid values are  `Arch Linux`, `CentOS`, `CoreOS`, `Debian`, `Fedora`, `Fedora Atomic`,  `FreeBSD`, `Gentoo`, `openSUSE`, `RancherOS`, `Rocky Linux`, `Ubuntu`, and `Unknown`.  Any other value will be accepted but ignored, and `Unknown` will be used in its place.
        :param pulumi.Input[str] name: The display name that has been given to an image.  This is what is shown in the control panel and is generally a descriptive title for the image in question.
        :param pulumi.Input['ImagesCustomPropertiesRegion'] region: The slug identifier for the region where the resource will initially be  available.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tags: A flat array of tag names as strings to be applied to the resource. Tag names may be for either existing or new tags.
        :param pulumi.Input[str] url: A URL from which the custom Linux virtual machine image may be retrieved.  The image it points to must be in the raw, qcow2, vhdx, vdi, or vmdk format.  It may be compressed using gzip or bzip2 and must be smaller than 100 GB after being decompressed.
        """
        if description is not None:
            pulumi.set(__self__, "description", description)
        if distribution is not None:
            pulumi.set(__self__, "distribution", distribution)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if region is not None:
            pulumi.set(__self__, "region", region)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if url is not None:
            pulumi.set(__self__, "url", url)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        An optional free-form text field to describe an image.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def distribution(self) -> Optional[pulumi.Input['ImageUpdateDistribution']]:
        """
        The name of a custom image's distribution. Currently, the valid values are  `Arch Linux`, `CentOS`, `CoreOS`, `Debian`, `Fedora`, `Fedora Atomic`,  `FreeBSD`, `Gentoo`, `openSUSE`, `RancherOS`, `Rocky Linux`, `Ubuntu`, and `Unknown`.  Any other value will be accepted but ignored, and `Unknown` will be used in its place.
        """
        return pulumi.get(self, "distribution")

    @distribution.setter
    def distribution(self, value: Optional[pulumi.Input['ImageUpdateDistribution']]):
        pulumi.set(self, "distribution", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The display name that has been given to an image.  This is what is shown in the control panel and is generally a descriptive title for the image in question.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def region(self) -> Optional[pulumi.Input['ImagesCustomPropertiesRegion']]:
        """
        The slug identifier for the region where the resource will initially be  available.
        """
        return pulumi.get(self, "region")

    @region.setter
    def region(self, value: Optional[pulumi.Input['ImagesCustomPropertiesRegion']]):
        pulumi.set(self, "region", value)

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

    @property
    @pulumi.getter
    def url(self) -> Optional[pulumi.Input[str]]:
        """
        A URL from which the custom Linux virtual machine image may be retrieved.  The image it points to must be in the raw, qcow2, vhdx, vdi, or vmdk format.  It may be compressed using gzip or bzip2 and must be smaller than 100 GB after being decompressed.
        """
        return pulumi.get(self, "url")

    @url.setter
    def url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "url", value)


class ImagesCustom(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 distribution: Optional[pulumi.Input['ImageUpdateDistribution']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input['ImagesCustomPropertiesRegion']] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 url: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Create a ImagesCustom resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: An optional free-form text field to describe an image.
        :param pulumi.Input['ImageUpdateDistribution'] distribution: The name of a custom image's distribution. Currently, the valid values are  `Arch Linux`, `CentOS`, `CoreOS`, `Debian`, `Fedora`, `Fedora Atomic`,  `FreeBSD`, `Gentoo`, `openSUSE`, `RancherOS`, `Rocky Linux`, `Ubuntu`, and `Unknown`.  Any other value will be accepted but ignored, and `Unknown` will be used in its place.
        :param pulumi.Input[str] name: The display name that has been given to an image.  This is what is shown in the control panel and is generally a descriptive title for the image in question.
        :param pulumi.Input['ImagesCustomPropertiesRegion'] region: The slug identifier for the region where the resource will initially be  available.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tags: A flat array of tag names as strings to be applied to the resource. Tag names may be for either existing or new tags.
        :param pulumi.Input[str] url: A URL from which the custom Linux virtual machine image may be retrieved.  The image it points to must be in the raw, qcow2, vhdx, vdi, or vmdk format.  It may be compressed using gzip or bzip2 and must be smaller than 100 GB after being decompressed.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[ImagesCustomArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Create a ImagesCustom resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param ImagesCustomArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ImagesCustomArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 distribution: Optional[pulumi.Input['ImageUpdateDistribution']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input['ImagesCustomPropertiesRegion']] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 url: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ImagesCustomArgs.__new__(ImagesCustomArgs)

            __props__.__dict__["description"] = description
            __props__.__dict__["distribution"] = distribution
            __props__.__dict__["name"] = name
            __props__.__dict__["region"] = region
            __props__.__dict__["tags"] = tags
            __props__.__dict__["url"] = url
            __props__.__dict__["image"] = None
        super(ImagesCustom, __self__).__init__(
            'digitalocean-native:images/v2:ImagesCustom',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ImagesCustom':
        """
        Get an existing ImagesCustom resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ImagesCustomArgs.__new__(ImagesCustomArgs)

        __props__.__dict__["description"] = None
        __props__.__dict__["distribution"] = None
        __props__.__dict__["image"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["region"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["url"] = None
        return ImagesCustom(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        An optional free-form text field to describe an image.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def distribution(self) -> pulumi.Output[Optional['ImageUpdateDistribution']]:
        """
        The name of a custom image's distribution. Currently, the valid values are  `Arch Linux`, `CentOS`, `CoreOS`, `Debian`, `Fedora`, `Fedora Atomic`,  `FreeBSD`, `Gentoo`, `openSUSE`, `RancherOS`, `Rocky Linux`, `Ubuntu`, and `Unknown`.  Any other value will be accepted but ignored, and `Unknown` will be used in its place.
        """
        return pulumi.get(self, "distribution")

    @property
    @pulumi.getter
    def image(self) -> pulumi.Output[Optional['outputs.Image']]:
        return pulumi.get(self, "image")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The display name that has been given to an image.  This is what is shown in the control panel and is generally a descriptive title for the image in question.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def region(self) -> pulumi.Output['ImagesCustomPropertiesRegion']:
        """
        The slug identifier for the region where the resource will initially be  available.
        """
        return pulumi.get(self, "region")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        A flat array of tag names as strings to be applied to the resource. Tag names may be for either existing or new tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def url(self) -> pulumi.Output[str]:
        """
        A URL from which the custom Linux virtual machine image may be retrieved.  The image it points to must be in the raw, qcow2, vhdx, vdi, or vmdk format.  It may be compressed using gzip or bzip2 and must be smaller than 100 GB after being decompressed.
        """
        return pulumi.get(self, "url")

