# coding=utf-8
# *** WARNING: this file was generated by pulumigen. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = ['LoadBalancersDropletArgs', 'LoadBalancersDroplet']

@pulumi.input_type
class LoadBalancersDropletArgs:
    def __init__(__self__, *,
                 droplet_ids: pulumi.Input[Sequence[pulumi.Input[int]]],
                 lb_id: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a LoadBalancersDroplet resource.
        :param pulumi.Input[Sequence[pulumi.Input[int]]] droplet_ids: An array containing the IDs of the Droplets assigned to the load balancer.
        :param pulumi.Input[str] lb_id: A unique identifier for a load balancer.
        """
        pulumi.set(__self__, "droplet_ids", droplet_ids)
        if lb_id is not None:
            pulumi.set(__self__, "lb_id", lb_id)

    @property
    @pulumi.getter(name="dropletIds")
    def droplet_ids(self) -> pulumi.Input[Sequence[pulumi.Input[int]]]:
        """
        An array containing the IDs of the Droplets assigned to the load balancer.
        """
        return pulumi.get(self, "droplet_ids")

    @droplet_ids.setter
    def droplet_ids(self, value: pulumi.Input[Sequence[pulumi.Input[int]]]):
        pulumi.set(self, "droplet_ids", value)

    @property
    @pulumi.getter(name="lbId")
    def lb_id(self) -> Optional[pulumi.Input[str]]:
        """
        A unique identifier for a load balancer.
        """
        return pulumi.get(self, "lb_id")

    @lb_id.setter
    def lb_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "lb_id", value)


class LoadBalancersDroplet(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 droplet_ids: Optional[pulumi.Input[Sequence[pulumi.Input[int]]]] = None,
                 lb_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Create a LoadBalancersDroplet resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[int]]] droplet_ids: An array containing the IDs of the Droplets assigned to the load balancer.
        :param pulumi.Input[str] lb_id: A unique identifier for a load balancer.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: LoadBalancersDropletArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Create a LoadBalancersDroplet resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param LoadBalancersDropletArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(LoadBalancersDropletArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 droplet_ids: Optional[pulumi.Input[Sequence[pulumi.Input[int]]]] = None,
                 lb_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = LoadBalancersDropletArgs.__new__(LoadBalancersDropletArgs)

            if droplet_ids is None and not opts.urn:
                raise TypeError("Missing required property 'droplet_ids'")
            __props__.__dict__["droplet_ids"] = droplet_ids
            __props__.__dict__["lb_id"] = lb_id
        super(LoadBalancersDroplet, __self__).__init__(
            'digitalocean-native:load_balancers/v2:LoadBalancersDroplet',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'LoadBalancersDroplet':
        """
        Get an existing LoadBalancersDroplet resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = LoadBalancersDropletArgs.__new__(LoadBalancersDropletArgs)

        __props__.__dict__["droplet_ids"] = None
        return LoadBalancersDroplet(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="dropletIds")
    def droplet_ids(self) -> pulumi.Output[Sequence[int]]:
        """
        An array containing the IDs of the Droplets assigned to the load balancer.
        """
        return pulumi.get(self, "droplet_ids")

