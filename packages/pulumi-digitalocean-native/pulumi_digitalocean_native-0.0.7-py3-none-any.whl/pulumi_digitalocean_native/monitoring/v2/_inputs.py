# coding=utf-8
# *** WARNING: this file was generated by pulumigen. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from ._enums import *

__all__ = [
    'AlertsArgs',
    'SlackDetailsArgs',
]

@pulumi.input_type
class AlertsArgs:
    def __init__(__self__, *,
                 email: pulumi.Input[Sequence[pulumi.Input[str]]],
                 slack: pulumi.Input[Sequence[pulumi.Input['SlackDetailsArgs']]]):
        """
        :param pulumi.Input[Sequence[pulumi.Input[str]]] email: An email to notify on an alert trigger.
        :param pulumi.Input[Sequence[pulumi.Input['SlackDetailsArgs']]] slack: Slack integration details.
        """
        pulumi.set(__self__, "email", email)
        pulumi.set(__self__, "slack", slack)

    @property
    @pulumi.getter
    def email(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        An email to notify on an alert trigger.
        """
        return pulumi.get(self, "email")

    @email.setter
    def email(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "email", value)

    @property
    @pulumi.getter
    def slack(self) -> pulumi.Input[Sequence[pulumi.Input['SlackDetailsArgs']]]:
        """
        Slack integration details.
        """
        return pulumi.get(self, "slack")

    @slack.setter
    def slack(self, value: pulumi.Input[Sequence[pulumi.Input['SlackDetailsArgs']]]):
        pulumi.set(self, "slack", value)


@pulumi.input_type
class SlackDetailsArgs:
    def __init__(__self__, *,
                 channel: pulumi.Input[str],
                 url: pulumi.Input[str]):
        """
        :param pulumi.Input[str] channel: Slack channel to notify of an alert trigger.
        :param pulumi.Input[str] url: Slack Webhook URL.
        """
        pulumi.set(__self__, "channel", channel)
        pulumi.set(__self__, "url", url)

    @property
    @pulumi.getter
    def channel(self) -> pulumi.Input[str]:
        """
        Slack channel to notify of an alert trigger.
        """
        return pulumi.get(self, "channel")

    @channel.setter
    def channel(self, value: pulumi.Input[str]):
        pulumi.set(self, "channel", value)

    @property
    @pulumi.getter
    def url(self) -> pulumi.Input[str]:
        """
        Slack Webhook URL.
        """
        return pulumi.get(self, "url")

    @url.setter
    def url(self, value: pulumi.Input[str]):
        pulumi.set(self, "url", value)


