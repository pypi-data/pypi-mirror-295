# coding=utf-8
# *** WARNING: this file was generated by pulumigen. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'ResourcesItemPropertiesResourceType',
]


class ResourcesItemPropertiesResourceType(str, Enum):
    """
    The type of the resource.
    """
    DROPLET = "droplet"
    IMAGE = "image"
    VOLUME = "volume"
    VOLUME_SNAPSHOT = "volume_snapshot"
