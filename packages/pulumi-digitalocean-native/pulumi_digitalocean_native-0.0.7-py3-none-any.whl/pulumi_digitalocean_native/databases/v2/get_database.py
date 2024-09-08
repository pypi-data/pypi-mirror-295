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

__all__ = [
    'GetDatabaseProperties',
    'AwaitableGetDatabaseProperties',
    'get_database',
    'get_database_output',
]

@pulumi.output_type
class GetDatabaseProperties:
    def __init__(__self__, db=None):
        if db and not isinstance(db, dict):
            raise TypeError("Expected argument 'db' to be a dict")
        pulumi.set(__self__, "db", db)

    @property
    @pulumi.getter
    def db(self) -> 'outputs.Database':
        return pulumi.get(self, "db")


class AwaitableGetDatabaseProperties(GetDatabaseProperties):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDatabaseProperties(
            db=self.db)


def get_database(database_cluster_uuid: Optional[str] = None,
                 database_name: Optional[str] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDatabaseProperties:
    """
    Use this data source to access information about an existing resource.

    :param str database_cluster_uuid: A unique identifier for a database cluster.
    :param str database_name: The name of the database.
    """
    __args__ = dict()
    __args__['databaseClusterUuid'] = database_cluster_uuid
    __args__['databaseName'] = database_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('digitalocean-native:databases/v2:getDatabase', __args__, opts=opts, typ=GetDatabaseProperties).value

    return AwaitableGetDatabaseProperties(
        db=pulumi.get(__ret__, 'db'))


@_utilities.lift_output_func(get_database)
def get_database_output(database_cluster_uuid: Optional[pulumi.Input[str]] = None,
                        database_name: Optional[pulumi.Input[str]] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetDatabaseProperties]:
    """
    Use this data source to access information about an existing resource.

    :param str database_cluster_uuid: A unique identifier for a database cluster.
    :param str database_name: The name of the database.
    """
    ...
