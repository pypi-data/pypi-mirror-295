# coding=utf-8
# *** WARNING: this file was generated by pulumigen. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['RestartPostgresArgs', 'RestartPostgres']

@pulumi.input_type
class RestartPostgresArgs:
    def __init__(__self__, *,
                 postgres_id: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a RestartPostgres resource.
        """
        if postgres_id is not None:
            pulumi.set(__self__, "postgres_id", postgres_id)

    @property
    @pulumi.getter(name="postgresId")
    def postgres_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "postgres_id")

    @postgres_id.setter
    def postgres_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "postgres_id", value)


class RestartPostgres(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 postgres_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Create a RestartPostgres resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[RestartPostgresArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Create a RestartPostgres resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param RestartPostgresArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(RestartPostgresArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 postgres_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = RestartPostgresArgs.__new__(RestartPostgresArgs)

            __props__.__dict__["postgres_id"] = postgres_id
        super(RestartPostgres, __self__).__init__(
            'render:postgres:RestartPostgres',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'RestartPostgres':
        """
        Get an existing RestartPostgres resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = RestartPostgresArgs.__new__(RestartPostgresArgs)

        return RestartPostgres(resource_name, opts=opts, __props__=__props__)

