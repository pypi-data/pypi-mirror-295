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
    'ForwardingRuleArgs',
    'HealthCheckArgs',
    'LbFirewallArgs',
    'StickySessionsArgs',
]

@pulumi.input_type
class ForwardingRuleArgs:
    def __init__(__self__, *,
                 entry_port: pulumi.Input[int],
                 entry_protocol: pulumi.Input['ForwardingRuleEntryProtocol'],
                 target_port: pulumi.Input[int],
                 target_protocol: pulumi.Input['ForwardingRuleTargetProtocol'],
                 certificate_id: Optional[pulumi.Input[str]] = None,
                 tls_passthrough: Optional[pulumi.Input[bool]] = None):
        """
        An object specifying a forwarding rule for a load balancer.
        :param pulumi.Input[int] entry_port: An integer representing the port on which the load balancer instance will listen.
        :param pulumi.Input['ForwardingRuleEntryProtocol'] entry_protocol: The protocol used for traffic to the load balancer. The possible values are: `http`, `https`, `http2`, `http3`, `tcp`, or `udp`. If you set the  `entry_protocol` to `udp`, the `target_protocol` must be set to `udp`.  When using UDP, the load balancer requires that you set up a health  check with a port that uses TCP, HTTP, or HTTPS to work properly.
        :param pulumi.Input[int] target_port: An integer representing the port on the backend Droplets to which the load balancer will send traffic.
        :param pulumi.Input['ForwardingRuleTargetProtocol'] target_protocol: The protocol used for traffic from the load balancer to the backend Droplets. The possible values are: `http`, `https`, `http2`, `tcp`, or `udp`. If you set the `target_protocol` to `udp`, the `entry_protocol` must be set to  `udp`. When using UDP, the load balancer requires that you set up a health  check with a port that uses TCP, HTTP, or HTTPS to work properly.
        :param pulumi.Input[str] certificate_id: The ID of the TLS certificate used for SSL termination if enabled.
        :param pulumi.Input[bool] tls_passthrough: A boolean value indicating whether SSL encrypted traffic will be passed through to the backend Droplets.
        """
        pulumi.set(__self__, "entry_port", entry_port)
        pulumi.set(__self__, "entry_protocol", entry_protocol)
        pulumi.set(__self__, "target_port", target_port)
        pulumi.set(__self__, "target_protocol", target_protocol)
        if certificate_id is not None:
            pulumi.set(__self__, "certificate_id", certificate_id)
        if tls_passthrough is not None:
            pulumi.set(__self__, "tls_passthrough", tls_passthrough)

    @property
    @pulumi.getter(name="entryPort")
    def entry_port(self) -> pulumi.Input[int]:
        """
        An integer representing the port on which the load balancer instance will listen.
        """
        return pulumi.get(self, "entry_port")

    @entry_port.setter
    def entry_port(self, value: pulumi.Input[int]):
        pulumi.set(self, "entry_port", value)

    @property
    @pulumi.getter(name="entryProtocol")
    def entry_protocol(self) -> pulumi.Input['ForwardingRuleEntryProtocol']:
        """
        The protocol used for traffic to the load balancer. The possible values are: `http`, `https`, `http2`, `http3`, `tcp`, or `udp`. If you set the  `entry_protocol` to `udp`, the `target_protocol` must be set to `udp`.  When using UDP, the load balancer requires that you set up a health  check with a port that uses TCP, HTTP, or HTTPS to work properly.
        """
        return pulumi.get(self, "entry_protocol")

    @entry_protocol.setter
    def entry_protocol(self, value: pulumi.Input['ForwardingRuleEntryProtocol']):
        pulumi.set(self, "entry_protocol", value)

    @property
    @pulumi.getter(name="targetPort")
    def target_port(self) -> pulumi.Input[int]:
        """
        An integer representing the port on the backend Droplets to which the load balancer will send traffic.
        """
        return pulumi.get(self, "target_port")

    @target_port.setter
    def target_port(self, value: pulumi.Input[int]):
        pulumi.set(self, "target_port", value)

    @property
    @pulumi.getter(name="targetProtocol")
    def target_protocol(self) -> pulumi.Input['ForwardingRuleTargetProtocol']:
        """
        The protocol used for traffic from the load balancer to the backend Droplets. The possible values are: `http`, `https`, `http2`, `tcp`, or `udp`. If you set the `target_protocol` to `udp`, the `entry_protocol` must be set to  `udp`. When using UDP, the load balancer requires that you set up a health  check with a port that uses TCP, HTTP, or HTTPS to work properly.
        """
        return pulumi.get(self, "target_protocol")

    @target_protocol.setter
    def target_protocol(self, value: pulumi.Input['ForwardingRuleTargetProtocol']):
        pulumi.set(self, "target_protocol", value)

    @property
    @pulumi.getter(name="certificateId")
    def certificate_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the TLS certificate used for SSL termination if enabled.
        """
        return pulumi.get(self, "certificate_id")

    @certificate_id.setter
    def certificate_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "certificate_id", value)

    @property
    @pulumi.getter(name="tlsPassthrough")
    def tls_passthrough(self) -> Optional[pulumi.Input[bool]]:
        """
        A boolean value indicating whether SSL encrypted traffic will be passed through to the backend Droplets.
        """
        return pulumi.get(self, "tls_passthrough")

    @tls_passthrough.setter
    def tls_passthrough(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "tls_passthrough", value)


@pulumi.input_type
class HealthCheckArgs:
    def __init__(__self__, *,
                 check_interval_seconds: Optional[pulumi.Input[int]] = None,
                 healthy_threshold: Optional[pulumi.Input[int]] = None,
                 path: Optional[pulumi.Input[str]] = None,
                 port: Optional[pulumi.Input[int]] = None,
                 protocol: Optional[pulumi.Input['HealthCheckProtocol']] = None,
                 response_timeout_seconds: Optional[pulumi.Input[int]] = None,
                 unhealthy_threshold: Optional[pulumi.Input[int]] = None):
        """
        An object specifying health check settings for the load balancer.
        :param pulumi.Input[int] check_interval_seconds: The number of seconds between between two consecutive health checks.
        :param pulumi.Input[int] healthy_threshold: The number of times a health check must pass for a backend Droplet to be marked "healthy" and be re-added to the pool.
        :param pulumi.Input[str] path: The path on the backend Droplets to which the load balancer instance will send a request.
        :param pulumi.Input[int] port: An integer representing the port on the backend Droplets on which the health check will attempt a connection.
        :param pulumi.Input['HealthCheckProtocol'] protocol: The protocol used for health checks sent to the backend Droplets. The possible values are `http`, `https`, or `tcp`.
        :param pulumi.Input[int] response_timeout_seconds: The number of seconds the load balancer instance will wait for a response until marking a health check as failed.
        :param pulumi.Input[int] unhealthy_threshold: The number of times a health check must fail for a backend Droplet to be marked "unhealthy" and be removed from the pool.
        """
        if check_interval_seconds is None:
            check_interval_seconds = 10
        if check_interval_seconds is not None:
            pulumi.set(__self__, "check_interval_seconds", check_interval_seconds)
        if healthy_threshold is None:
            healthy_threshold = 3
        if healthy_threshold is not None:
            pulumi.set(__self__, "healthy_threshold", healthy_threshold)
        if path is None:
            path = '/'
        if path is not None:
            pulumi.set(__self__, "path", path)
        if port is None:
            port = 80
        if port is not None:
            pulumi.set(__self__, "port", port)
        if protocol is None:
            protocol = 'http'
        if protocol is not None:
            pulumi.set(__self__, "protocol", protocol)
        if response_timeout_seconds is None:
            response_timeout_seconds = 5
        if response_timeout_seconds is not None:
            pulumi.set(__self__, "response_timeout_seconds", response_timeout_seconds)
        if unhealthy_threshold is None:
            unhealthy_threshold = 5
        if unhealthy_threshold is not None:
            pulumi.set(__self__, "unhealthy_threshold", unhealthy_threshold)

    @property
    @pulumi.getter(name="checkIntervalSeconds")
    def check_interval_seconds(self) -> Optional[pulumi.Input[int]]:
        """
        The number of seconds between between two consecutive health checks.
        """
        return pulumi.get(self, "check_interval_seconds")

    @check_interval_seconds.setter
    def check_interval_seconds(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "check_interval_seconds", value)

    @property
    @pulumi.getter(name="healthyThreshold")
    def healthy_threshold(self) -> Optional[pulumi.Input[int]]:
        """
        The number of times a health check must pass for a backend Droplet to be marked "healthy" and be re-added to the pool.
        """
        return pulumi.get(self, "healthy_threshold")

    @healthy_threshold.setter
    def healthy_threshold(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "healthy_threshold", value)

    @property
    @pulumi.getter
    def path(self) -> Optional[pulumi.Input[str]]:
        """
        The path on the backend Droplets to which the load balancer instance will send a request.
        """
        return pulumi.get(self, "path")

    @path.setter
    def path(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "path", value)

    @property
    @pulumi.getter
    def port(self) -> Optional[pulumi.Input[int]]:
        """
        An integer representing the port on the backend Droplets on which the health check will attempt a connection.
        """
        return pulumi.get(self, "port")

    @port.setter
    def port(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "port", value)

    @property
    @pulumi.getter
    def protocol(self) -> Optional[pulumi.Input['HealthCheckProtocol']]:
        """
        The protocol used for health checks sent to the backend Droplets. The possible values are `http`, `https`, or `tcp`.
        """
        return pulumi.get(self, "protocol")

    @protocol.setter
    def protocol(self, value: Optional[pulumi.Input['HealthCheckProtocol']]):
        pulumi.set(self, "protocol", value)

    @property
    @pulumi.getter(name="responseTimeoutSeconds")
    def response_timeout_seconds(self) -> Optional[pulumi.Input[int]]:
        """
        The number of seconds the load balancer instance will wait for a response until marking a health check as failed.
        """
        return pulumi.get(self, "response_timeout_seconds")

    @response_timeout_seconds.setter
    def response_timeout_seconds(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "response_timeout_seconds", value)

    @property
    @pulumi.getter(name="unhealthyThreshold")
    def unhealthy_threshold(self) -> Optional[pulumi.Input[int]]:
        """
        The number of times a health check must fail for a backend Droplet to be marked "unhealthy" and be removed from the pool.
        """
        return pulumi.get(self, "unhealthy_threshold")

    @unhealthy_threshold.setter
    def unhealthy_threshold(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "unhealthy_threshold", value)


@pulumi.input_type
class LbFirewallArgs:
    def __init__(__self__, *,
                 allow: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 deny: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        An object specifying allow and deny rules to control traffic to the load balancer.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] allow: the rules for allowing traffic to the load balancer (in the form 'ip:1.2.3.4' or 'cidr:1.2.0.0/16')
        :param pulumi.Input[Sequence[pulumi.Input[str]]] deny: the rules for denying traffic to the load balancer (in the form 'ip:1.2.3.4' or 'cidr:1.2.0.0/16')
        """
        if allow is not None:
            pulumi.set(__self__, "allow", allow)
        if deny is not None:
            pulumi.set(__self__, "deny", deny)

    @property
    @pulumi.getter
    def allow(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        the rules for allowing traffic to the load balancer (in the form 'ip:1.2.3.4' or 'cidr:1.2.0.0/16')
        """
        return pulumi.get(self, "allow")

    @allow.setter
    def allow(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "allow", value)

    @property
    @pulumi.getter
    def deny(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        the rules for denying traffic to the load balancer (in the form 'ip:1.2.3.4' or 'cidr:1.2.0.0/16')
        """
        return pulumi.get(self, "deny")

    @deny.setter
    def deny(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "deny", value)


@pulumi.input_type
class StickySessionsArgs:
    def __init__(__self__, *,
                 cookie_name: Optional[pulumi.Input[str]] = None,
                 cookie_ttl_seconds: Optional[pulumi.Input[int]] = None,
                 type: Optional[pulumi.Input['StickySessionsType']] = None):
        """
        An object specifying sticky sessions settings for the load balancer.
        :param pulumi.Input[str] cookie_name: The name of the cookie sent to the client. This attribute is only returned when using `cookies` for the sticky sessions type.
        :param pulumi.Input[int] cookie_ttl_seconds: The number of seconds until the cookie set by the load balancer expires. This attribute is only returned when using `cookies` for the sticky sessions type.
        :param pulumi.Input['StickySessionsType'] type: An attribute indicating how and if requests from a client will be persistently served by the same backend Droplet. The possible values are `cookies` or `none`.
        """
        if cookie_name is not None:
            pulumi.set(__self__, "cookie_name", cookie_name)
        if cookie_ttl_seconds is not None:
            pulumi.set(__self__, "cookie_ttl_seconds", cookie_ttl_seconds)
        if type is None:
            type = 'none'
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="cookieName")
    def cookie_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the cookie sent to the client. This attribute is only returned when using `cookies` for the sticky sessions type.
        """
        return pulumi.get(self, "cookie_name")

    @cookie_name.setter
    def cookie_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cookie_name", value)

    @property
    @pulumi.getter(name="cookieTtlSeconds")
    def cookie_ttl_seconds(self) -> Optional[pulumi.Input[int]]:
        """
        The number of seconds until the cookie set by the load balancer expires. This attribute is only returned when using `cookies` for the sticky sessions type.
        """
        return pulumi.get(self, "cookie_ttl_seconds")

    @cookie_ttl_seconds.setter
    def cookie_ttl_seconds(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "cookie_ttl_seconds", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input['StickySessionsType']]:
        """
        An attribute indicating how and if requests from a client will be persistently served by the same backend Droplet. The possible values are `cookies` or `none`.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input['StickySessionsType']]):
        pulumi.set(self, "type", value)


