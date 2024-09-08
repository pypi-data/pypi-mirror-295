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
from ._inputs import *

__all__ = ['DatabasesConnectionPoolArgs', 'DatabasesConnectionPool']

@pulumi.input_type
class DatabasesConnectionPoolArgs:
    def __init__(__self__, *,
                 db: pulumi.Input[str],
                 mode: pulumi.Input[str],
                 size: pulumi.Input[int],
                 connection: Optional[pulumi.Input['ConnectionArgs']] = None,
                 database_cluster_uuid: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 private_connection: Optional[pulumi.Input['PrivateConnectionArgs']] = None,
                 user: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a DatabasesConnectionPool resource.
        :param pulumi.Input[str] db: The database for use with the connection pool.
        :param pulumi.Input[str] mode: The PGBouncer transaction mode for the connection pool. The allowed values are session, transaction, and statement.
        :param pulumi.Input[int] size: The desired size of the PGBouncer connection pool. The maximum allowed size is determined by the size of the cluster's primary node. 25 backend server connections are allowed for every 1GB of RAM. Three are reserved for maintenance. For example, a primary node with 1 GB of RAM allows for a maximum of 22 backend server connections while one with 4 GB would allow for 97. Note that these are shared across all connection pools in a cluster.
        :param pulumi.Input[str] database_cluster_uuid: A unique identifier for a database cluster.
        :param pulumi.Input[str] name: A unique name for the connection pool. Must be between 3 and 60 characters.
        :param pulumi.Input[str] user: The name of the user for use with the connection pool. When excluded, all sessions connect to the database as the inbound user.
        """
        pulumi.set(__self__, "db", db)
        pulumi.set(__self__, "mode", mode)
        pulumi.set(__self__, "size", size)
        if connection is not None:
            pulumi.set(__self__, "connection", connection)
        if database_cluster_uuid is not None:
            pulumi.set(__self__, "database_cluster_uuid", database_cluster_uuid)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if private_connection is not None:
            pulumi.set(__self__, "private_connection", private_connection)
        if user is not None:
            pulumi.set(__self__, "user", user)

    @property
    @pulumi.getter
    def db(self) -> pulumi.Input[str]:
        """
        The database for use with the connection pool.
        """
        return pulumi.get(self, "db")

    @db.setter
    def db(self, value: pulumi.Input[str]):
        pulumi.set(self, "db", value)

    @property
    @pulumi.getter
    def mode(self) -> pulumi.Input[str]:
        """
        The PGBouncer transaction mode for the connection pool. The allowed values are session, transaction, and statement.
        """
        return pulumi.get(self, "mode")

    @mode.setter
    def mode(self, value: pulumi.Input[str]):
        pulumi.set(self, "mode", value)

    @property
    @pulumi.getter
    def size(self) -> pulumi.Input[int]:
        """
        The desired size of the PGBouncer connection pool. The maximum allowed size is determined by the size of the cluster's primary node. 25 backend server connections are allowed for every 1GB of RAM. Three are reserved for maintenance. For example, a primary node with 1 GB of RAM allows for a maximum of 22 backend server connections while one with 4 GB would allow for 97. Note that these are shared across all connection pools in a cluster.
        """
        return pulumi.get(self, "size")

    @size.setter
    def size(self, value: pulumi.Input[int]):
        pulumi.set(self, "size", value)

    @property
    @pulumi.getter
    def connection(self) -> Optional[pulumi.Input['ConnectionArgs']]:
        return pulumi.get(self, "connection")

    @connection.setter
    def connection(self, value: Optional[pulumi.Input['ConnectionArgs']]):
        pulumi.set(self, "connection", value)

    @property
    @pulumi.getter(name="databaseClusterUuid")
    def database_cluster_uuid(self) -> Optional[pulumi.Input[str]]:
        """
        A unique identifier for a database cluster.
        """
        return pulumi.get(self, "database_cluster_uuid")

    @database_cluster_uuid.setter
    def database_cluster_uuid(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "database_cluster_uuid", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        A unique name for the connection pool. Must be between 3 and 60 characters.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="privateConnection")
    def private_connection(self) -> Optional[pulumi.Input['PrivateConnectionArgs']]:
        return pulumi.get(self, "private_connection")

    @private_connection.setter
    def private_connection(self, value: Optional[pulumi.Input['PrivateConnectionArgs']]):
        pulumi.set(self, "private_connection", value)

    @property
    @pulumi.getter
    def user(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the user for use with the connection pool. When excluded, all sessions connect to the database as the inbound user.
        """
        return pulumi.get(self, "user")

    @user.setter
    def user(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "user", value)


class DatabasesConnectionPool(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 connection: Optional[pulumi.Input[Union['ConnectionArgs', 'ConnectionArgsDict']]] = None,
                 database_cluster_uuid: Optional[pulumi.Input[str]] = None,
                 db: Optional[pulumi.Input[str]] = None,
                 mode: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 private_connection: Optional[pulumi.Input[Union['PrivateConnectionArgs', 'PrivateConnectionArgsDict']]] = None,
                 size: Optional[pulumi.Input[int]] = None,
                 user: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Create a DatabasesConnectionPool resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] database_cluster_uuid: A unique identifier for a database cluster.
        :param pulumi.Input[str] db: The database for use with the connection pool.
        :param pulumi.Input[str] mode: The PGBouncer transaction mode for the connection pool. The allowed values are session, transaction, and statement.
        :param pulumi.Input[str] name: A unique name for the connection pool. Must be between 3 and 60 characters.
        :param pulumi.Input[int] size: The desired size of the PGBouncer connection pool. The maximum allowed size is determined by the size of the cluster's primary node. 25 backend server connections are allowed for every 1GB of RAM. Three are reserved for maintenance. For example, a primary node with 1 GB of RAM allows for a maximum of 22 backend server connections while one with 4 GB would allow for 97. Note that these are shared across all connection pools in a cluster.
        :param pulumi.Input[str] user: The name of the user for use with the connection pool. When excluded, all sessions connect to the database as the inbound user.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DatabasesConnectionPoolArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Create a DatabasesConnectionPool resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param DatabasesConnectionPoolArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DatabasesConnectionPoolArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 connection: Optional[pulumi.Input[Union['ConnectionArgs', 'ConnectionArgsDict']]] = None,
                 database_cluster_uuid: Optional[pulumi.Input[str]] = None,
                 db: Optional[pulumi.Input[str]] = None,
                 mode: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 private_connection: Optional[pulumi.Input[Union['PrivateConnectionArgs', 'PrivateConnectionArgsDict']]] = None,
                 size: Optional[pulumi.Input[int]] = None,
                 user: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DatabasesConnectionPoolArgs.__new__(DatabasesConnectionPoolArgs)

            __props__.__dict__["connection"] = connection
            __props__.__dict__["database_cluster_uuid"] = database_cluster_uuid
            if db is None and not opts.urn:
                raise TypeError("Missing required property 'db'")
            __props__.__dict__["db"] = db
            if mode is None and not opts.urn:
                raise TypeError("Missing required property 'mode'")
            __props__.__dict__["mode"] = mode
            __props__.__dict__["name"] = name
            __props__.__dict__["private_connection"] = private_connection
            if size is None and not opts.urn:
                raise TypeError("Missing required property 'size'")
            __props__.__dict__["size"] = size
            __props__.__dict__["user"] = user
            __props__.__dict__["pool"] = None
        super(DatabasesConnectionPool, __self__).__init__(
            'digitalocean-native:databases/v2:DatabasesConnectionPool',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'DatabasesConnectionPool':
        """
        Get an existing DatabasesConnectionPool resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = DatabasesConnectionPoolArgs.__new__(DatabasesConnectionPoolArgs)

        __props__.__dict__["connection"] = None
        __props__.__dict__["db"] = None
        __props__.__dict__["mode"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["pool"] = None
        __props__.__dict__["private_connection"] = None
        __props__.__dict__["size"] = None
        __props__.__dict__["user"] = None
        return DatabasesConnectionPool(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def connection(self) -> pulumi.Output[Optional['outputs.Connection']]:
        return pulumi.get(self, "connection")

    @property
    @pulumi.getter
    def db(self) -> pulumi.Output[str]:
        """
        The database for use with the connection pool.
        """
        return pulumi.get(self, "db")

    @property
    @pulumi.getter
    def mode(self) -> pulumi.Output[str]:
        """
        The PGBouncer transaction mode for the connection pool. The allowed values are session, transaction, and statement.
        """
        return pulumi.get(self, "mode")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        A unique name for the connection pool. Must be between 3 and 60 characters.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def pool(self) -> pulumi.Output['outputs.ConnectionPool']:
        return pulumi.get(self, "pool")

    @property
    @pulumi.getter(name="privateConnection")
    def private_connection(self) -> pulumi.Output[Optional['outputs.PrivateConnection']]:
        return pulumi.get(self, "private_connection")

    @property
    @pulumi.getter
    def size(self) -> pulumi.Output[int]:
        """
        The desired size of the PGBouncer connection pool. The maximum allowed size is determined by the size of the cluster's primary node. 25 backend server connections are allowed for every 1GB of RAM. Three are reserved for maintenance. For example, a primary node with 1 GB of RAM allows for a maximum of 22 backend server connections while one with 4 GB would allow for 97. Note that these are shared across all connection pools in a cluster.
        """
        return pulumi.get(self, "size")

    @property
    @pulumi.getter
    def user(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the user for use with the connection pool. When excluded, all sessions connect to the database as the inbound user.
        """
        return pulumi.get(self, "user")

