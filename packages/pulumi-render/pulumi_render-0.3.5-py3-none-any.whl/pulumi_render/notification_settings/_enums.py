# coding=utf-8
# *** WARNING: this file was generated by pulumigen. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'GetOwnerNotificationSettingPropertiesNotificationsToSend',
    'GetServiceNotificationOverridePropertiesNotificationsToSend',
    'GetServiceNotificationOverridePropertiesPreviewNotificationsEnabled',
    'NotificationOverrideWithCursorOverridePropertiesNotificationsToSend',
    'NotificationOverrideWithCursorOverridePropertiesPreviewNotificationsEnabled',
]


class GetOwnerNotificationSettingPropertiesNotificationsToSend(str, Enum):
    NONE = "none"
    FAILURE = "failure"
    ALL = "all"


class GetServiceNotificationOverridePropertiesNotificationsToSend(str, Enum):
    DEFAULT = "default"
    NONE = "none"
    FAILURE = "failure"
    ALL = "all"


class GetServiceNotificationOverridePropertiesPreviewNotificationsEnabled(str, Enum):
    DEFAULT = "default"
    FALSE = "false"
    TRUE = "true"


class NotificationOverrideWithCursorOverridePropertiesNotificationsToSend(str, Enum):
    DEFAULT = "default"
    NONE = "none"
    FAILURE = "failure"
    ALL = "all"


class NotificationOverrideWithCursorOverridePropertiesPreviewNotificationsEnabled(str, Enum):
    DEFAULT = "default"
    FALSE = "false"
    TRUE = "true"
