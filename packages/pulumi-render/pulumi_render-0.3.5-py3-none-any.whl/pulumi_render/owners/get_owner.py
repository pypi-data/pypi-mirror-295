# coding=utf-8
# *** WARNING: this file was generated by pulumigen. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload, Awaitable
from .. import _utilities
from ._enums import *

__all__ = [
    'Owner',
    'AwaitableOwner',
    'get_owner',
    'get_owner_output',
]

@pulumi.output_type
class Owner:
    def __init__(__self__, email=None, id=None, name=None, two_factor_auth_enabled=None, type=None):
        if email and not isinstance(email, str):
            raise TypeError("Expected argument 'email' to be a str")
        pulumi.set(__self__, "email", email)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if two_factor_auth_enabled and not isinstance(two_factor_auth_enabled, bool):
            raise TypeError("Expected argument 'two_factor_auth_enabled' to be a bool")
        pulumi.set(__self__, "two_factor_auth_enabled", two_factor_auth_enabled)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def email(self) -> str:
        return pulumi.get(self, "email")

    @property
    @pulumi.getter
    def id(self) -> str:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="twoFactorAuthEnabled")
    def two_factor_auth_enabled(self) -> Optional[bool]:
        """
        Whether two-factor authentication is enabled for the owner. Only present for user owners.
        """
        return pulumi.get(self, "two_factor_auth_enabled")

    @property
    @pulumi.getter
    def type(self) -> 'OwnerType':
        return pulumi.get(self, "type")


class AwaitableOwner(Owner):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return Owner(
            email=self.email,
            id=self.id,
            name=self.name,
            two_factor_auth_enabled=self.two_factor_auth_enabled,
            type=self.type)


def get_owner(owner_id: Optional[str] = None,
              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableOwner:
    """
    Use this data source to access information about an existing resource.

    :param str owner_id: The ID of the user or team
    """
    __args__ = dict()
    __args__['ownerId'] = owner_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('render:owners:getOwner', __args__, opts=opts, typ=Owner).value

    return AwaitableOwner(
        email=pulumi.get(__ret__, 'email'),
        id=pulumi.get(__ret__, 'id'),
        name=pulumi.get(__ret__, 'name'),
        two_factor_auth_enabled=pulumi.get(__ret__, 'two_factor_auth_enabled'),
        type=pulumi.get(__ret__, 'type'))


@_utilities.lift_output_func(get_owner)
def get_owner_output(owner_id: Optional[pulumi.Input[str]] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[Owner]:
    """
    Use this data source to access information about an existing resource.

    :param str owner_id: The ID of the user or team
    """
    ...
