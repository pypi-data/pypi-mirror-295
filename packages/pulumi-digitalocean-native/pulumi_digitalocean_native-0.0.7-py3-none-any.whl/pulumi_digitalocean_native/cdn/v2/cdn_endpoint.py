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

__all__ = ['CdnEndpointArgs', 'CdnEndpoint']

@pulumi.input_type
class CdnEndpointArgs:
    def __init__(__self__, *,
                 origin: pulumi.Input[str],
                 certificate_id: Optional[pulumi.Input[str]] = None,
                 custom_domain: Optional[pulumi.Input[str]] = None,
                 ttl: Optional[pulumi.Input['Ttl']] = None):
        """
        The set of arguments for constructing a CdnEndpoint resource.
        :param pulumi.Input[str] origin: The fully qualified domain name (FQDN) for the origin server which provides the content for the CDN. This is currently restricted to a Space.
        :param pulumi.Input[str] certificate_id: The ID of a DigitalOcean managed TLS certificate used for SSL when a custom subdomain is provided.
        :param pulumi.Input[str] custom_domain: The fully qualified domain name (FQDN) of the custom subdomain used with the CDN endpoint.
        :param pulumi.Input['Ttl'] ttl: The amount of time the content is cached by the CDN's edge servers in seconds. TTL must be one of 60, 600, 3600, 86400, or 604800. Defaults to 3600 (one hour) when excluded.
        """
        pulumi.set(__self__, "origin", origin)
        if certificate_id is not None:
            pulumi.set(__self__, "certificate_id", certificate_id)
        if custom_domain is not None:
            pulumi.set(__self__, "custom_domain", custom_domain)
        if ttl is None:
            ttl = 3600
        if ttl is not None:
            pulumi.set(__self__, "ttl", ttl)

    @property
    @pulumi.getter
    def origin(self) -> pulumi.Input[str]:
        """
        The fully qualified domain name (FQDN) for the origin server which provides the content for the CDN. This is currently restricted to a Space.
        """
        return pulumi.get(self, "origin")

    @origin.setter
    def origin(self, value: pulumi.Input[str]):
        pulumi.set(self, "origin", value)

    @property
    @pulumi.getter(name="certificateId")
    def certificate_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of a DigitalOcean managed TLS certificate used for SSL when a custom subdomain is provided.
        """
        return pulumi.get(self, "certificate_id")

    @certificate_id.setter
    def certificate_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "certificate_id", value)

    @property
    @pulumi.getter(name="customDomain")
    def custom_domain(self) -> Optional[pulumi.Input[str]]:
        """
        The fully qualified domain name (FQDN) of the custom subdomain used with the CDN endpoint.
        """
        return pulumi.get(self, "custom_domain")

    @custom_domain.setter
    def custom_domain(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "custom_domain", value)

    @property
    @pulumi.getter
    def ttl(self) -> Optional[pulumi.Input['Ttl']]:
        """
        The amount of time the content is cached by the CDN's edge servers in seconds. TTL must be one of 60, 600, 3600, 86400, or 604800. Defaults to 3600 (one hour) when excluded.
        """
        return pulumi.get(self, "ttl")

    @ttl.setter
    def ttl(self, value: Optional[pulumi.Input['Ttl']]):
        pulumi.set(self, "ttl", value)


class CdnEndpoint(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 certificate_id: Optional[pulumi.Input[str]] = None,
                 custom_domain: Optional[pulumi.Input[str]] = None,
                 origin: Optional[pulumi.Input[str]] = None,
                 ttl: Optional[pulumi.Input['Ttl']] = None,
                 __props__=None):
        """
        Create a CdnEndpoint resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] certificate_id: The ID of a DigitalOcean managed TLS certificate used for SSL when a custom subdomain is provided.
        :param pulumi.Input[str] custom_domain: The fully qualified domain name (FQDN) of the custom subdomain used with the CDN endpoint.
        :param pulumi.Input[str] origin: The fully qualified domain name (FQDN) for the origin server which provides the content for the CDN. This is currently restricted to a Space.
        :param pulumi.Input['Ttl'] ttl: The amount of time the content is cached by the CDN's edge servers in seconds. TTL must be one of 60, 600, 3600, 86400, or 604800. Defaults to 3600 (one hour) when excluded.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: CdnEndpointArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Create a CdnEndpoint resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param CdnEndpointArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(CdnEndpointArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 certificate_id: Optional[pulumi.Input[str]] = None,
                 custom_domain: Optional[pulumi.Input[str]] = None,
                 origin: Optional[pulumi.Input[str]] = None,
                 ttl: Optional[pulumi.Input['Ttl']] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = CdnEndpointArgs.__new__(CdnEndpointArgs)

            __props__.__dict__["certificate_id"] = certificate_id
            __props__.__dict__["custom_domain"] = custom_domain
            if origin is None and not opts.urn:
                raise TypeError("Missing required property 'origin'")
            __props__.__dict__["origin"] = origin
            if ttl is None:
                ttl = 3600
            __props__.__dict__["ttl"] = ttl
            __props__.__dict__["created_at"] = None
            __props__.__dict__["endpoint"] = None
        super(CdnEndpoint, __self__).__init__(
            'digitalocean-native:cdn/v2:CdnEndpoint',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'CdnEndpoint':
        """
        Get an existing CdnEndpoint resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = CdnEndpointArgs.__new__(CdnEndpointArgs)

        __props__.__dict__["certificate_id"] = None
        __props__.__dict__["created_at"] = None
        __props__.__dict__["custom_domain"] = None
        __props__.__dict__["endpoint"] = None
        __props__.__dict__["origin"] = None
        __props__.__dict__["ttl"] = None
        return CdnEndpoint(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="certificateId")
    def certificate_id(self) -> pulumi.Output[Optional[str]]:
        """
        The ID of a DigitalOcean managed TLS certificate used for SSL when a custom subdomain is provided.
        """
        return pulumi.get(self, "certificate_id")

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> pulumi.Output[Optional[str]]:
        """
        A time value given in ISO8601 combined date and time format that represents when the CDN endpoint was created.
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter(name="customDomain")
    def custom_domain(self) -> pulumi.Output[Optional[str]]:
        """
        The fully qualified domain name (FQDN) of the custom subdomain used with the CDN endpoint.
        """
        return pulumi.get(self, "custom_domain")

    @property
    @pulumi.getter
    def endpoint(self) -> pulumi.Output[Optional['outputs.CdnEndpoint']]:
        return pulumi.get(self, "endpoint")

    @property
    @pulumi.getter
    def origin(self) -> pulumi.Output[str]:
        """
        The fully qualified domain name (FQDN) for the origin server which provides the content for the CDN. This is currently restricted to a Space.
        """
        return pulumi.get(self, "origin")

    @property
    @pulumi.getter
    def ttl(self) -> pulumi.Output[Optional['Ttl']]:
        """
        The amount of time the content is cached by the CDN's edge servers in seconds. TTL must be one of 60, 600, 3600, 86400, or 604800. Defaults to 3600 (one hour) when excluded.
        """
        return pulumi.get(self, "ttl")

