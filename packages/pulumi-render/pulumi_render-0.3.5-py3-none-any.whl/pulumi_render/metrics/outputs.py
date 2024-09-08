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

__all__ = [
    'ListActiveConnectionsItemProperties',
    'ListActiveConnectionsItemPropertiesLabelsItemProperties',
    'ListActiveConnectionsItemPropertiesValuesItemProperties',
    'ListReplicationLagItemProperties',
    'ListReplicationLagItemPropertiesLabelsItemProperties',
    'ListReplicationLagItemPropertiesValuesItemProperties',
]

@pulumi.output_type
class ListActiveConnectionsItemProperties(dict):
    """
    A time series data point
    """
    def __init__(__self__, *,
                 labels: Sequence['outputs.ListActiveConnectionsItemPropertiesLabelsItemProperties'],
                 unit: str,
                 values: Sequence['outputs.ListActiveConnectionsItemPropertiesValuesItemProperties']):
        """
        A time series data point
        :param Sequence['ListActiveConnectionsItemPropertiesLabelsItemProperties'] labels: List of labels describing the time series
        :param Sequence['ListActiveConnectionsItemPropertiesValuesItemProperties'] values: The values of the time series
        """
        pulumi.set(__self__, "labels", labels)
        pulumi.set(__self__, "unit", unit)
        pulumi.set(__self__, "values", values)

    @property
    @pulumi.getter
    def labels(self) -> Sequence['outputs.ListActiveConnectionsItemPropertiesLabelsItemProperties']:
        """
        List of labels describing the time series
        """
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter
    def unit(self) -> str:
        return pulumi.get(self, "unit")

    @property
    @pulumi.getter
    def values(self) -> Sequence['outputs.ListActiveConnectionsItemPropertiesValuesItemProperties']:
        """
        The values of the time series
        """
        return pulumi.get(self, "values")


@pulumi.output_type
class ListActiveConnectionsItemPropertiesLabelsItemProperties(dict):
    """
    A time series datapoint label
    """
    def __init__(__self__, *,
                 field: str,
                 value: str):
        """
        A time series datapoint label
        """
        pulumi.set(__self__, "field", field)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def field(self) -> str:
        return pulumi.get(self, "field")

    @property
    @pulumi.getter
    def value(self) -> str:
        return pulumi.get(self, "value")


@pulumi.output_type
class ListActiveConnectionsItemPropertiesValuesItemProperties(dict):
    """
    A time series datapoint value
    """
    def __init__(__self__, *,
                 timestamp: str,
                 value: float):
        """
        A time series datapoint value
        """
        pulumi.set(__self__, "timestamp", timestamp)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def timestamp(self) -> str:
        return pulumi.get(self, "timestamp")

    @property
    @pulumi.getter
    def value(self) -> float:
        return pulumi.get(self, "value")


@pulumi.output_type
class ListReplicationLagItemProperties(dict):
    """
    A time series data point
    """
    def __init__(__self__, *,
                 labels: Sequence['outputs.ListReplicationLagItemPropertiesLabelsItemProperties'],
                 unit: str,
                 values: Sequence['outputs.ListReplicationLagItemPropertiesValuesItemProperties']):
        """
        A time series data point
        :param Sequence['ListReplicationLagItemPropertiesLabelsItemProperties'] labels: List of labels describing the time series
        :param Sequence['ListReplicationLagItemPropertiesValuesItemProperties'] values: The values of the time series
        """
        pulumi.set(__self__, "labels", labels)
        pulumi.set(__self__, "unit", unit)
        pulumi.set(__self__, "values", values)

    @property
    @pulumi.getter
    def labels(self) -> Sequence['outputs.ListReplicationLagItemPropertiesLabelsItemProperties']:
        """
        List of labels describing the time series
        """
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter
    def unit(self) -> str:
        return pulumi.get(self, "unit")

    @property
    @pulumi.getter
    def values(self) -> Sequence['outputs.ListReplicationLagItemPropertiesValuesItemProperties']:
        """
        The values of the time series
        """
        return pulumi.get(self, "values")


@pulumi.output_type
class ListReplicationLagItemPropertiesLabelsItemProperties(dict):
    """
    A time series datapoint label
    """
    def __init__(__self__, *,
                 field: str,
                 value: str):
        """
        A time series datapoint label
        """
        pulumi.set(__self__, "field", field)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def field(self) -> str:
        return pulumi.get(self, "field")

    @property
    @pulumi.getter
    def value(self) -> str:
        return pulumi.get(self, "value")


@pulumi.output_type
class ListReplicationLagItemPropertiesValuesItemProperties(dict):
    """
    A time series datapoint value
    """
    def __init__(__self__, *,
                 timestamp: str,
                 value: float):
        """
        A time series datapoint value
        """
        pulumi.set(__self__, "timestamp", timestamp)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def timestamp(self) -> str:
        return pulumi.get(self, "timestamp")

    @property
    @pulumi.getter
    def value(self) -> float:
        return pulumi.get(self, "value")


