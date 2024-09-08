# coding=utf-8
# *** WARNING: this file was generated by pulumigen. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from . import _utilities
import typing
# Export this package's modules as members:
from .provider import *

# Make subpackages available:
if typing.TYPE_CHECKING:
    import pulumi_render.blueprints as __blueprints
    blueprints = __blueprints
    import pulumi_render.config as __config
    config = __config
    import pulumi_render.cron_jobs as __cron_jobs
    cron_jobs = __cron_jobs
    import pulumi_render.disks as __disks
    disks = __disks
    import pulumi_render.env_groups as __env_groups
    env_groups = __env_groups
    import pulumi_render.environments as __environments
    environments = __environments
    import pulumi_render.metrics as __metrics
    metrics = __metrics
    import pulumi_render.notification_settings as __notification_settings
    notification_settings = __notification_settings
    import pulumi_render.owners as __owners
    owners = __owners
    import pulumi_render.postgres as __postgres
    postgres = __postgres
    import pulumi_render.projects as __projects
    projects = __projects
    import pulumi_render.redis as __redis
    redis = __redis
    import pulumi_render.registrycredentials as __registrycredentials
    registrycredentials = __registrycredentials
    import pulumi_render.services as __services
    services = __services
else:
    blueprints = _utilities.lazy_import('pulumi_render.blueprints')
    config = _utilities.lazy_import('pulumi_render.config')
    cron_jobs = _utilities.lazy_import('pulumi_render.cron_jobs')
    disks = _utilities.lazy_import('pulumi_render.disks')
    env_groups = _utilities.lazy_import('pulumi_render.env_groups')
    environments = _utilities.lazy_import('pulumi_render.environments')
    metrics = _utilities.lazy_import('pulumi_render.metrics')
    notification_settings = _utilities.lazy_import('pulumi_render.notification_settings')
    owners = _utilities.lazy_import('pulumi_render.owners')
    postgres = _utilities.lazy_import('pulumi_render.postgres')
    projects = _utilities.lazy_import('pulumi_render.projects')
    redis = _utilities.lazy_import('pulumi_render.redis')
    registrycredentials = _utilities.lazy_import('pulumi_render.registrycredentials')
    services = _utilities.lazy_import('pulumi_render.services')

_utilities.register(
    resource_modules="""
[
 {
  "pkg": "render",
  "mod": "cron-jobs",
  "fqn": "pulumi_render.cron_jobs",
  "classes": {
   "render:cron-jobs:RunCronJob": "RunCronJob"
  }
 },
 {
  "pkg": "render",
  "mod": "disks",
  "fqn": "pulumi_render.disks",
  "classes": {
   "render:disks:Disk": "Disk",
   "render:disks:RestoreSnapshot": "RestoreSnapshot"
  }
 },
 {
  "pkg": "render",
  "mod": "env-groups",
  "fqn": "pulumi_render.env_groups",
  "classes": {
   "render:env-groups:EnvGroup": "EnvGroup",
   "render:env-groups:LinkServiceToEnvGroup": "LinkServiceToEnvGroup"
  }
 },
 {
  "pkg": "render",
  "mod": "environments",
  "fqn": "pulumi_render.environments",
  "classes": {
   "render:environments:Environment": "Environment",
   "render:environments:ResourcesToEnvironment": "ResourcesToEnvironment"
  }
 },
 {
  "pkg": "render",
  "mod": "postgres",
  "fqn": "pulumi_render.postgres",
  "classes": {
   "render:postgres:FailoverPostgres": "FailoverPostgres",
   "render:postgres:Postgres": "Postgres",
   "render:postgres:PostgresBackup": "PostgresBackup",
   "render:postgres:RecoverPostgres": "RecoverPostgres",
   "render:postgres:RestartPostgres": "RestartPostgres",
   "render:postgres:ResumePostgres": "ResumePostgres",
   "render:postgres:SuspendPostgres": "SuspendPostgres"
  }
 },
 {
  "pkg": "render",
  "mod": "projects",
  "fqn": "pulumi_render.projects",
  "classes": {
   "render:projects:Project": "Project"
  }
 },
 {
  "pkg": "render",
  "mod": "redis",
  "fqn": "pulumi_render.redis",
  "classes": {
   "render:redis:Redis": "Redis"
  }
 },
 {
  "pkg": "render",
  "mod": "registrycredentials",
  "fqn": "pulumi_render.registrycredentials",
  "classes": {
   "render:registrycredentials:RegistryCredential": "RegistryCredential"
  }
 },
 {
  "pkg": "render",
  "mod": "services",
  "fqn": "pulumi_render.services",
  "classes": {
   "render:services:AutoscaleService": "AutoscaleService",
   "render:services:BackgroundWorker": "BackgroundWorker",
   "render:services:CancelDeploy": "CancelDeploy",
   "render:services:CancelJob": "CancelJob",
   "render:services:CronJob": "CronJob",
   "render:services:CustomDomain": "CustomDomain",
   "render:services:Deploy": "Deploy",
   "render:services:EnvVarsForService": "EnvVarsForService",
   "render:services:Header": "Header",
   "render:services:Job": "Job",
   "render:services:PreviewService": "PreviewService",
   "render:services:PrivateService": "PrivateService",
   "render:services:RefreshCustomDomain": "RefreshCustomDomain",
   "render:services:RestartService": "RestartService",
   "render:services:RollbackDeploy": "RollbackDeploy",
   "render:services:Route": "Route",
   "render:services:ScaleService": "ScaleService",
   "render:services:SecretFilesForService": "SecretFilesForService",
   "render:services:StaticSite": "StaticSite",
   "render:services:SuspendService": "SuspendService",
   "render:services:WebService": "WebService"
  }
 }
]
""",
    resource_packages="""
[
 {
  "pkg": "render",
  "token": "pulumi:providers:render",
  "fqn": "pulumi_render",
  "class": "Provider"
 }
]
"""
)
