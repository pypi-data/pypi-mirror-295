# coding=utf-8
# *** WARNING: this file was generated by pulumigen. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload, Awaitable
from .. import _utilities
from . import outputs
from ._enums import *

__all__ = [
    'Project',
    'AwaitableProject',
    'get_project',
    'get_project_output',
]

@pulumi.output_type
class Project:
    """
    A project is a collection of environments
    """
    def __init__(__self__, created_at=None, environment_ids=None, id=None, name=None, owner=None, updated_at=None):
        if created_at and not isinstance(created_at, str):
            raise TypeError("Expected argument 'created_at' to be a str")
        pulumi.set(__self__, "created_at", created_at)
        if environment_ids and not isinstance(environment_ids, list):
            raise TypeError("Expected argument 'environment_ids' to be a list")
        pulumi.set(__self__, "environment_ids", environment_ids)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if owner and not isinstance(owner, dict):
            raise TypeError("Expected argument 'owner' to be a dict")
        pulumi.set(__self__, "owner", owner)
        if updated_at and not isinstance(updated_at, str):
            raise TypeError("Expected argument 'updated_at' to be a str")
        pulumi.set(__self__, "updated_at", updated_at)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> str:
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter(name="environmentIds")
    def environment_ids(self) -> Sequence[str]:
        """
        The environments associated with the project
        """
        return pulumi.get(self, "environment_ids")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The ID of the project
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the project
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def owner(self) -> 'outputs.Owner':
        return pulumi.get(self, "owner")

    @property
    @pulumi.getter(name="updatedAt")
    def updated_at(self) -> str:
        return pulumi.get(self, "updated_at")


class AwaitableProject(Project):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return Project(
            created_at=self.created_at,
            environment_ids=self.environment_ids,
            id=self.id,
            name=self.name,
            owner=self.owner,
            updated_at=self.updated_at)


def get_project(project_id: Optional[str] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableProject:
    """
    Use this data source to access information about an existing resource.
    """
    __args__ = dict()
    __args__['projectId'] = project_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('render:projects:getProject', __args__, opts=opts, typ=Project).value

    return AwaitableProject(
        created_at=pulumi.get(__ret__, 'created_at'),
        environment_ids=pulumi.get(__ret__, 'environment_ids'),
        id=pulumi.get(__ret__, 'id'),
        name=pulumi.get(__ret__, 'name'),
        owner=pulumi.get(__ret__, 'owner'),
        updated_at=pulumi.get(__ret__, 'updated_at'))


@_utilities.lift_output_func(get_project)
def get_project_output(project_id: Optional[pulumi.Input[str]] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[Project]:
    """
    Use this data source to access information about an existing resource.
    """
    ...
