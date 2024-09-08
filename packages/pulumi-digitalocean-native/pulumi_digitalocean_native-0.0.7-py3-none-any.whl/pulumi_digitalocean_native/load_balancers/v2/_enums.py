# coding=utf-8
# *** WARNING: this file was generated by pulumigen. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'ForwardingRuleEntryProtocol',
    'ForwardingRuleTargetProtocol',
    'HealthCheckProtocol',
    'LoadBalancerBaseAlgorithm',
    'LoadBalancerBaseSize',
    'LoadBalancerBaseStatus',
    'LoadBalancerPropertiesRegionEnum',
    'StickySessionsType',
]


class ForwardingRuleEntryProtocol(str, Enum):
    """
    The protocol used for traffic to the load balancer. The possible values are: `http`, `https`, `http2`, `http3`, `tcp`, or `udp`. If you set the  `entry_protocol` to `udp`, the `target_protocol` must be set to `udp`.  When using UDP, the load balancer requires that you set up a health  check with a port that uses TCP, HTTP, or HTTPS to work properly.
    """
    HTTP = "http"
    HTTPS = "https"
    HTTP2 = "http2"
    HTTP3 = "http3"
    TCP = "tcp"
    UDP = "udp"


class ForwardingRuleTargetProtocol(str, Enum):
    """
    The protocol used for traffic from the load balancer to the backend Droplets. The possible values are: `http`, `https`, `http2`, `tcp`, or `udp`. If you set the `target_protocol` to `udp`, the `entry_protocol` must be set to  `udp`. When using UDP, the load balancer requires that you set up a health  check with a port that uses TCP, HTTP, or HTTPS to work properly.
    """
    HTTP = "http"
    HTTPS = "https"
    HTTP2 = "http2"
    TCP = "tcp"
    UDP = "udp"


class HealthCheckProtocol(str, Enum):
    """
    The protocol used for health checks sent to the backend Droplets. The possible values are `http`, `https`, or `tcp`.
    """
    HTTP = "http"
    HTTPS = "https"
    TCP = "tcp"


class LoadBalancerBaseAlgorithm(str, Enum):
    """
    This field has been deprecated. You can no longer specify an algorithm for load balancers.
    """
    ROUND_ROBIN = "round_robin"
    LEAST_CONNECTIONS = "least_connections"


class LoadBalancerBaseSize(str, Enum):
    """
    This field has been replaced by the `size_unit` field for all regions except in AMS2, NYC2, and SFO1. Each available load balancer size now equates to the load balancer having a set number of nodes.
    * `lb-small` = 1 node
    * `lb-medium` = 3 nodes
    * `lb-large` = 6 nodes

    You can resize load balancers after creation up to once per hour. You cannot resize a load balancer within the first hour of its creation.
    """
    LB_SMALL = "lb-small"
    LB_MEDIUM = "lb-medium"
    LB_LARGE = "lb-large"


class LoadBalancerBaseStatus(str, Enum):
    """
    A status string indicating the current state of the load balancer. This can be `new`, `active`, or `errored`.
    """
    NEW = "new"
    ACTIVE = "active"
    ERRORED = "errored"


class LoadBalancerPropertiesRegionEnum(str, Enum):
    """
    The slug identifier for the region where the resource will initially be  available.
    """
    AMS1 = "ams1"
    AMS2 = "ams2"
    AMS3 = "ams3"
    BLR1 = "blr1"
    FRA1 = "fra1"
    LON1 = "lon1"
    NYC1 = "nyc1"
    NYC2 = "nyc2"
    NYC3 = "nyc3"
    SFO1 = "sfo1"
    SFO2 = "sfo2"
    SFO3 = "sfo3"
    SGP1 = "sgp1"
    TOR1 = "tor1"


class StickySessionsType(str, Enum):
    """
    An attribute indicating how and if requests from a client will be persistently served by the same backend Droplet. The possible values are `cookies` or `none`.
    """
    COOKIES = "cookies"
    NONE = "none"
