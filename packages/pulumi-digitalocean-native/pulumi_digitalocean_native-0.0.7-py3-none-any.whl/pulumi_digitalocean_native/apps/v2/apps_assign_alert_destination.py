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
from ._inputs import *

__all__ = ['AppsAssignAlertDestinationArgs', 'AppsAssignAlertDestination']

@pulumi.input_type
class AppsAssignAlertDestinationArgs:
    def __init__(__self__, *,
                 alert_id: Optional[pulumi.Input[str]] = None,
                 app_id: Optional[pulumi.Input[str]] = None,
                 emails: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 slack_webhooks: Optional[pulumi.Input[Sequence[pulumi.Input['AppAlertSlackWebhookArgs']]]] = None):
        """
        The set of arguments for constructing a AppsAssignAlertDestination resource.
        :param pulumi.Input[str] alert_id: The alert ID
        :param pulumi.Input[str] app_id: The app ID
        """
        if alert_id is not None:
            pulumi.set(__self__, "alert_id", alert_id)
        if app_id is not None:
            pulumi.set(__self__, "app_id", app_id)
        if emails is not None:
            pulumi.set(__self__, "emails", emails)
        if slack_webhooks is not None:
            pulumi.set(__self__, "slack_webhooks", slack_webhooks)

    @property
    @pulumi.getter(name="alertId")
    def alert_id(self) -> Optional[pulumi.Input[str]]:
        """
        The alert ID
        """
        return pulumi.get(self, "alert_id")

    @alert_id.setter
    def alert_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "alert_id", value)

    @property
    @pulumi.getter(name="appId")
    def app_id(self) -> Optional[pulumi.Input[str]]:
        """
        The app ID
        """
        return pulumi.get(self, "app_id")

    @app_id.setter
    def app_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "app_id", value)

    @property
    @pulumi.getter
    def emails(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "emails")

    @emails.setter
    def emails(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "emails", value)

    @property
    @pulumi.getter(name="slackWebhooks")
    def slack_webhooks(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['AppAlertSlackWebhookArgs']]]]:
        return pulumi.get(self, "slack_webhooks")

    @slack_webhooks.setter
    def slack_webhooks(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['AppAlertSlackWebhookArgs']]]]):
        pulumi.set(self, "slack_webhooks", value)


class AppsAssignAlertDestination(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 alert_id: Optional[pulumi.Input[str]] = None,
                 app_id: Optional[pulumi.Input[str]] = None,
                 emails: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 slack_webhooks: Optional[pulumi.Input[Sequence[pulumi.Input[Union['AppAlertSlackWebhookArgs', 'AppAlertSlackWebhookArgsDict']]]]] = None,
                 __props__=None):
        """
        Create a AppsAssignAlertDestination resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] alert_id: The alert ID
        :param pulumi.Input[str] app_id: The app ID
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[AppsAssignAlertDestinationArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Create a AppsAssignAlertDestination resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param AppsAssignAlertDestinationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AppsAssignAlertDestinationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 alert_id: Optional[pulumi.Input[str]] = None,
                 app_id: Optional[pulumi.Input[str]] = None,
                 emails: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 slack_webhooks: Optional[pulumi.Input[Sequence[pulumi.Input[Union['AppAlertSlackWebhookArgs', 'AppAlertSlackWebhookArgsDict']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AppsAssignAlertDestinationArgs.__new__(AppsAssignAlertDestinationArgs)

            __props__.__dict__["alert_id"] = alert_id
            __props__.__dict__["app_id"] = app_id
            __props__.__dict__["emails"] = emails
            __props__.__dict__["slack_webhooks"] = slack_webhooks
            __props__.__dict__["alert"] = None
        super(AppsAssignAlertDestination, __self__).__init__(
            'digitalocean-native:apps/v2:AppsAssignAlertDestination',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'AppsAssignAlertDestination':
        """
        Get an existing AppsAssignAlertDestination resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = AppsAssignAlertDestinationArgs.__new__(AppsAssignAlertDestinationArgs)

        __props__.__dict__["alert"] = None
        __props__.__dict__["emails"] = None
        __props__.__dict__["slack_webhooks"] = None
        return AppsAssignAlertDestination(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def alert(self) -> pulumi.Output[Optional['outputs.AppAlert']]:
        return pulumi.get(self, "alert")

    @property
    @pulumi.getter
    def emails(self) -> pulumi.Output[Optional[Sequence[str]]]:
        return pulumi.get(self, "emails")

    @property
    @pulumi.getter(name="slackWebhooks")
    def slack_webhooks(self) -> pulumi.Output[Optional[Sequence['outputs.AppAlertSlackWebhook']]]:
        return pulumi.get(self, "slack_webhooks")

