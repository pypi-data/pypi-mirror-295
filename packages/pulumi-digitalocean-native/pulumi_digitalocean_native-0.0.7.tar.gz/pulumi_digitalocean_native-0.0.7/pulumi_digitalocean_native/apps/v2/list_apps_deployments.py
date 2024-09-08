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
    'AppsDeploymentsResponse',
    'AwaitableAppsDeploymentsResponse',
    'list_apps_deployments',
    'list_apps_deployments_output',
]

@pulumi.output_type
class AppsDeploymentsResponse:
    def __init__(__self__, deployments=None, links=None, meta=None):
        if deployments and not isinstance(deployments, list):
            raise TypeError("Expected argument 'deployments' to be a list")
        pulumi.set(__self__, "deployments", deployments)
        if links and not isinstance(links, dict):
            raise TypeError("Expected argument 'links' to be a dict")
        pulumi.set(__self__, "links", links)
        if meta and not isinstance(meta, dict):
            raise TypeError("Expected argument 'meta' to be a dict")
        pulumi.set(__self__, "meta", meta)

    @property
    @pulumi.getter
    def deployments(self) -> Optional[Sequence['outputs.AppsDeployment']]:
        return pulumi.get(self, "deployments")

    @property
    @pulumi.getter
    def links(self) -> Optional['outputs.PageLinks']:
        return pulumi.get(self, "links")

    @property
    @pulumi.getter
    def meta(self) -> 'outputs.MetaMeta':
        return pulumi.get(self, "meta")


class AwaitableAppsDeploymentsResponse(AppsDeploymentsResponse):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return AppsDeploymentsResponse(
            deployments=self.deployments,
            links=self.links,
            meta=self.meta)


def list_apps_deployments(app_id: Optional[str] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableAppsDeploymentsResponse:
    """
    Use this data source to access information about an existing resource.

    :param str app_id: The app ID
    """
    __args__ = dict()
    __args__['appId'] = app_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('digitalocean-native:apps/v2:listAppsDeployments', __args__, opts=opts, typ=AppsDeploymentsResponse).value

    return AwaitableAppsDeploymentsResponse(
        deployments=pulumi.get(__ret__, 'deployments'),
        links=pulumi.get(__ret__, 'links'),
        meta=pulumi.get(__ret__, 'meta'))


@_utilities.lift_output_func(list_apps_deployments)
def list_apps_deployments_output(app_id: Optional[pulumi.Input[str]] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[AppsDeploymentsResponse]:
    """
    Use this data source to access information about an existing resource.

    :param str app_id: The app ID
    """
    ...
