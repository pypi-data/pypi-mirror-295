# coding=utf-8
# *** WARNING: this file was generated by pulumigen. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._enums import *
from ._inputs import *

__all__ = ['RedisArgs', 'Redis']

@pulumi.input_type
class RedisArgs:
    def __init__(__self__, *,
                 owner_id: pulumi.Input[str],
                 plan: pulumi.Input['Plan'],
                 environment_id: Optional[pulumi.Input[str]] = None,
                 ip_allow_list: Optional[pulumi.Input[Sequence[pulumi.Input['CidrBlockAndDescriptionArgs']]]] = None,
                 maxmemory_policy: Optional[pulumi.Input['MaxmemoryPolicy']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Redis resource.
        :param pulumi.Input[str] owner_id: The ID of the owner of the Redis instance
        :param pulumi.Input['MaxmemoryPolicy'] maxmemory_policy: The eviction policy for the Redis instance
        :param pulumi.Input[str] name: The name of the Redis instance
        :param pulumi.Input[str] region: The region where the Redis instance is located
        """
        pulumi.set(__self__, "owner_id", owner_id)
        pulumi.set(__self__, "plan", plan)
        if environment_id is not None:
            pulumi.set(__self__, "environment_id", environment_id)
        if ip_allow_list is not None:
            pulumi.set(__self__, "ip_allow_list", ip_allow_list)
        if maxmemory_policy is not None:
            pulumi.set(__self__, "maxmemory_policy", maxmemory_policy)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if region is not None:
            pulumi.set(__self__, "region", region)

    @property
    @pulumi.getter(name="ownerId")
    def owner_id(self) -> pulumi.Input[str]:
        """
        The ID of the owner of the Redis instance
        """
        return pulumi.get(self, "owner_id")

    @owner_id.setter
    def owner_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "owner_id", value)

    @property
    @pulumi.getter
    def plan(self) -> pulumi.Input['Plan']:
        return pulumi.get(self, "plan")

    @plan.setter
    def plan(self, value: pulumi.Input['Plan']):
        pulumi.set(self, "plan", value)

    @property
    @pulumi.getter(name="environmentId")
    def environment_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "environment_id")

    @environment_id.setter
    def environment_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "environment_id", value)

    @property
    @pulumi.getter(name="ipAllowList")
    def ip_allow_list(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['CidrBlockAndDescriptionArgs']]]]:
        return pulumi.get(self, "ip_allow_list")

    @ip_allow_list.setter
    def ip_allow_list(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['CidrBlockAndDescriptionArgs']]]]):
        pulumi.set(self, "ip_allow_list", value)

    @property
    @pulumi.getter(name="maxmemoryPolicy")
    def maxmemory_policy(self) -> Optional[pulumi.Input['MaxmemoryPolicy']]:
        """
        The eviction policy for the Redis instance
        """
        return pulumi.get(self, "maxmemory_policy")

    @maxmemory_policy.setter
    def maxmemory_policy(self, value: Optional[pulumi.Input['MaxmemoryPolicy']]):
        pulumi.set(self, "maxmemory_policy", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Redis instance
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def region(self) -> Optional[pulumi.Input[str]]:
        """
        The region where the Redis instance is located
        """
        return pulumi.get(self, "region")

    @region.setter
    def region(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "region", value)


class Redis(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 environment_id: Optional[pulumi.Input[str]] = None,
                 ip_allow_list: Optional[pulumi.Input[Sequence[pulumi.Input[Union['CidrBlockAndDescriptionArgs', 'CidrBlockAndDescriptionArgsDict']]]]] = None,
                 maxmemory_policy: Optional[pulumi.Input['MaxmemoryPolicy']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 owner_id: Optional[pulumi.Input[str]] = None,
                 plan: Optional[pulumi.Input['Plan']] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Input type for creating a Redis instance

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input['MaxmemoryPolicy'] maxmemory_policy: The eviction policy for the Redis instance
        :param pulumi.Input[str] name: The name of the Redis instance
        :param pulumi.Input[str] owner_id: The ID of the owner of the Redis instance
        :param pulumi.Input[str] region: The region where the Redis instance is located
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: RedisArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Input type for creating a Redis instance

        :param str resource_name: The name of the resource.
        :param RedisArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(RedisArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 environment_id: Optional[pulumi.Input[str]] = None,
                 ip_allow_list: Optional[pulumi.Input[Sequence[pulumi.Input[Union['CidrBlockAndDescriptionArgs', 'CidrBlockAndDescriptionArgsDict']]]]] = None,
                 maxmemory_policy: Optional[pulumi.Input['MaxmemoryPolicy']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 owner_id: Optional[pulumi.Input[str]] = None,
                 plan: Optional[pulumi.Input['Plan']] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = RedisArgs.__new__(RedisArgs)

            __props__.__dict__["environment_id"] = environment_id
            __props__.__dict__["ip_allow_list"] = ip_allow_list
            __props__.__dict__["maxmemory_policy"] = maxmemory_policy
            __props__.__dict__["name"] = name
            if owner_id is None and not opts.urn:
                raise TypeError("Missing required property 'owner_id'")
            __props__.__dict__["owner_id"] = owner_id
            if plan is None and not opts.urn:
                raise TypeError("Missing required property 'plan'")
            __props__.__dict__["plan"] = plan
            __props__.__dict__["region"] = region
            __props__.__dict__["created_at"] = None
            __props__.__dict__["maintenance"] = None
            __props__.__dict__["options"] = None
            __props__.__dict__["owner"] = None
            __props__.__dict__["status"] = None
            __props__.__dict__["updated_at"] = None
            __props__.__dict__["version"] = None
        super(Redis, __self__).__init__(
            'render:redis:Redis',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Redis':
        """
        Get an existing Redis resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = RedisArgs.__new__(RedisArgs)

        __props__.__dict__["created_at"] = None
        __props__.__dict__["environment_id"] = None
        __props__.__dict__["ip_allow_list"] = None
        __props__.__dict__["maintenance"] = None
        __props__.__dict__["maxmemory_policy"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["options"] = None
        __props__.__dict__["owner"] = None
        __props__.__dict__["owner_id"] = None
        __props__.__dict__["plan"] = None
        __props__.__dict__["region"] = None
        __props__.__dict__["status"] = None
        __props__.__dict__["updated_at"] = None
        __props__.__dict__["version"] = None
        return Redis(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> pulumi.Output[str]:
        """
        The creation time of the Redis instance
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter(name="environmentId")
    def environment_id(self) -> pulumi.Output[Optional[str]]:
        """
        The ID of the environment the Redis instance is associated with
        """
        return pulumi.get(self, "environment_id")

    @property
    @pulumi.getter(name="ipAllowList")
    def ip_allow_list(self) -> pulumi.Output[Sequence['outputs.CidrBlockAndDescription']]:
        """
        The IP allow list for the Redis instance
        """
        return pulumi.get(self, "ip_allow_list")

    @property
    @pulumi.getter
    def maintenance(self) -> pulumi.Output[Optional['outputs.MaintenanceProperties']]:
        return pulumi.get(self, "maintenance")

    @property
    @pulumi.getter(name="maxmemoryPolicy")
    def maxmemory_policy(self) -> pulumi.Output[Optional['MaxmemoryPolicy']]:
        """
        The eviction policy for the Redis instance
        """
        return pulumi.get(self, "maxmemory_policy")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the Redis instance
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def options(self) -> pulumi.Output['outputs.RedisOptions']:
        """
        Options for a Redis instance
        """
        return pulumi.get(self, "options")

    @property
    @pulumi.getter
    def owner(self) -> pulumi.Output['outputs.Owner']:
        return pulumi.get(self, "owner")

    @property
    @pulumi.getter(name="ownerId")
    def owner_id(self) -> pulumi.Output[str]:
        """
        The ID of the owner of the Redis instance
        """
        return pulumi.get(self, "owner_id")

    @property
    @pulumi.getter
    def plan(self) -> pulumi.Output['Plan']:
        return pulumi.get(self, "plan")

    @property
    @pulumi.getter
    def region(self) -> pulumi.Output['Region']:
        """
        Defaults to "oregon"
        """
        return pulumi.get(self, "region")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output['Status']:
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="updatedAt")
    def updated_at(self) -> pulumi.Output[str]:
        """
        The last updated time of the Redis instance
        """
        return pulumi.get(self, "updated_at")

    @property
    @pulumi.getter
    def version(self) -> pulumi.Output[str]:
        """
        The version of Redis
        """
        return pulumi.get(self, "version")

