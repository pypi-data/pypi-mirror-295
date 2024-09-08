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

__all__ = [
    'CdnEndpoint',
    'MetaMeta',
    'PageLinks',
    'PageLinksPagesProperties',
]

@pulumi.output_type
class CdnEndpoint(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "certificateId":
            suggest = "certificate_id"
        elif key == "createdAt":
            suggest = "created_at"
        elif key == "customDomain":
            suggest = "custom_domain"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in CdnEndpoint. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        CdnEndpoint.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        CdnEndpoint.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 origin: str,
                 certificate_id: Optional[str] = None,
                 created_at: Optional[str] = None,
                 custom_domain: Optional[str] = None,
                 endpoint: Optional[str] = None,
                 id: Optional[str] = None,
                 ttl: Optional['CdnEndpointTtl'] = None):
        """
        :param str origin: The fully qualified domain name (FQDN) for the origin server which provides the content for the CDN. This is currently restricted to a Space.
        :param str certificate_id: The ID of a DigitalOcean managed TLS certificate used for SSL when a custom subdomain is provided.
        :param str created_at: A time value given in ISO8601 combined date and time format that represents when the CDN endpoint was created.
        :param str custom_domain: The fully qualified domain name (FQDN) of the custom subdomain used with the CDN endpoint.
        :param str endpoint: The fully qualified domain name (FQDN) from which the CDN-backed content is served.
        :param str id: A unique ID that can be used to identify and reference a CDN endpoint.
        :param 'CdnEndpointTtl' ttl: The amount of time the content is cached by the CDN's edge servers in seconds. TTL must be one of 60, 600, 3600, 86400, or 604800. Defaults to 3600 (one hour) when excluded.
        """
        pulumi.set(__self__, "origin", origin)
        if certificate_id is not None:
            pulumi.set(__self__, "certificate_id", certificate_id)
        if created_at is not None:
            pulumi.set(__self__, "created_at", created_at)
        if custom_domain is not None:
            pulumi.set(__self__, "custom_domain", custom_domain)
        if endpoint is not None:
            pulumi.set(__self__, "endpoint", endpoint)
        if id is not None:
            pulumi.set(__self__, "id", id)
        if ttl is None:
            ttl = 3600
        if ttl is not None:
            pulumi.set(__self__, "ttl", ttl)

    @property
    @pulumi.getter
    def origin(self) -> str:
        """
        The fully qualified domain name (FQDN) for the origin server which provides the content for the CDN. This is currently restricted to a Space.
        """
        return pulumi.get(self, "origin")

    @property
    @pulumi.getter(name="certificateId")
    def certificate_id(self) -> Optional[str]:
        """
        The ID of a DigitalOcean managed TLS certificate used for SSL when a custom subdomain is provided.
        """
        return pulumi.get(self, "certificate_id")

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> Optional[str]:
        """
        A time value given in ISO8601 combined date and time format that represents when the CDN endpoint was created.
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter(name="customDomain")
    def custom_domain(self) -> Optional[str]:
        """
        The fully qualified domain name (FQDN) of the custom subdomain used with the CDN endpoint.
        """
        return pulumi.get(self, "custom_domain")

    @property
    @pulumi.getter
    def endpoint(self) -> Optional[str]:
        """
        The fully qualified domain name (FQDN) from which the CDN-backed content is served.
        """
        return pulumi.get(self, "endpoint")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        A unique ID that can be used to identify and reference a CDN endpoint.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def ttl(self) -> Optional['CdnEndpointTtl']:
        """
        The amount of time the content is cached by the CDN's edge servers in seconds. TTL must be one of 60, 600, 3600, 86400, or 604800. Defaults to 3600 (one hour) when excluded.
        """
        return pulumi.get(self, "ttl")


@pulumi.output_type
class MetaMeta(dict):
    def __init__(__self__, *,
                 total: Optional[int] = None):
        """
        :param int total: Number of objects returned by the request.
        """
        if total is not None:
            pulumi.set(__self__, "total", total)

    @property
    @pulumi.getter
    def total(self) -> Optional[int]:
        """
        Number of objects returned by the request.
        """
        return pulumi.get(self, "total")


@pulumi.output_type
class PageLinks(dict):
    def __init__(__self__, *,
                 pages: Optional['outputs.PageLinksPagesProperties'] = None):
        if pages is not None:
            pulumi.set(__self__, "pages", pages)

    @property
    @pulumi.getter
    def pages(self) -> Optional['outputs.PageLinksPagesProperties']:
        return pulumi.get(self, "pages")


@pulumi.output_type
class PageLinksPagesProperties(dict):
    def __init__(__self__, *,
                 first: Optional[str] = None,
                 last: Optional[str] = None,
                 next: Optional[str] = None,
                 prev: Optional[str] = None):
        if first is not None:
            pulumi.set(__self__, "first", first)
        if last is not None:
            pulumi.set(__self__, "last", last)
        if next is not None:
            pulumi.set(__self__, "next", next)
        if prev is not None:
            pulumi.set(__self__, "prev", prev)

    @property
    @pulumi.getter
    def first(self) -> Optional[str]:
        return pulumi.get(self, "first")

    @property
    @pulumi.getter
    def last(self) -> Optional[str]:
        return pulumi.get(self, "last")

    @property
    @pulumi.getter
    def next(self) -> Optional[str]:
        return pulumi.get(self, "next")

    @property
    @pulumi.getter
    def prev(self) -> Optional[str]:
        return pulumi.get(self, "prev")


