# mypy: disable-error-code="func-returns-value"
import asyncio
import logging
from typing import Any

from google.oauth2._service_account_async import Credentials

from lueur.make_id import make_id
from lueur.models import Discovery, Meta
from lueur.platform.gcp.address import explore_addresses
from lueur.platform.gcp.cloudrun import expand_links as cloudrun_links
from lueur.platform.gcp.cloudrun import explore_cloudrun
from lueur.platform.gcp.connector import explore_connector
from lueur.platform.gcp.firewall import explore_firewalls
from lueur.platform.gcp.forwardingrule import explore_forwardingrules
from lueur.platform.gcp.gke import expand_links as gke_expand_links
from lueur.platform.gcp.gke import explore_gke
from lueur.platform.gcp.healthchecks import explore_health_checks
from lueur.platform.gcp.lb import expand_links as lb_expand_links
from lueur.platform.gcp.lb import explore_lb
from lueur.platform.gcp.monitoring import expand_links as mon_expand_links
from lueur.platform.gcp.monitoring import explore_monitoring
from lueur.platform.gcp.securities import explore_securities
from lueur.platform.gcp.sql import expand_links as sql_expand_links
from lueur.platform.gcp.sql import explore_sql
from lueur.platform.gcp.targetproxy import explore_target_proxies
from lueur.platform.gcp.vpc import expand_links as vpc_expand_links
from lueur.platform.gcp.vpc import explore_vpc

__all__ = ["explore", "expand_links"]
logger = logging.getLogger("lueur.lib")


async def explore(
    project: str, location: str | None = None, creds: Credentials | None = None
) -> Discovery:
    resources = []
    tasks: list[asyncio.Task] = []

    async with asyncio.TaskGroup() as tg:
        if location:
            tasks.append(
                tg.create_task(
                    explore_addresses(project, location, creds),
                    name="explore_addresses",
                )
            )
            tasks.append(
                tg.create_task(
                    explore_gke(project, location, creds), name="explore_gke"
                )
            )
            tasks.append(
                tg.create_task(
                    explore_cloudrun(project, location, creds),
                    name="explore_cloudrun",
                )
            )
            tasks.append(
                tg.create_task(
                    explore_lb(project, location, creds), name="explore_lb"
                )
            )
            tasks.append(
                tg.create_task(
                    explore_connector(project, location, creds),
                    name="explore_connector",
                )
            )
            tasks.append(
                tg.create_task(
                    explore_securities(project, location, creds),
                    name="explore_securities",
                )
            )
            tasks.append(
                tg.create_task(
                    explore_firewalls(project, location, creds),
                    name="explore_firewalls",
                )
            )
            tasks.append(
                tg.create_task(
                    explore_forwardingrules(project, location, creds),
                    name="explore_forwardingrules",
                )
            )
            tasks.append(
                tg.create_task(
                    explore_health_checks(project, location, creds),
                    name="explore_health_checks",
                )
            )
            tasks.append(
                tg.create_task(
                    explore_target_proxies(project, location, creds),
                    name="explore_target_proxies",
                )
            )
        else:
            tasks.append(
                tg.create_task(
                    explore_addresses(project, None, creds),
                    name="explore_addresses",
                )
            )
            tasks.append(
                tg.create_task(
                    explore_sql(project, creds), name="explore_global_sql"
                )
            )
            tasks.append(
                tg.create_task(
                    explore_lb(project, None, creds), name="explore_global_lb"
                )
            )
            tasks.append(
                tg.create_task(
                    explore_vpc(project, creds), name="explore_global_vpc"
                )
            )
            tasks.append(
                tg.create_task(
                    explore_monitoring(project, creds),
                    name="explore_global_monitoring",
                )
            )
            tasks.append(
                tg.create_task(
                    explore_securities(project, None, creds),
                    name="explore_global_securities",
                )
            )
            tasks.append(
                tg.create_task(
                    explore_firewalls(project, None, creds),
                    name="explore_firewalls",
                )
            )
            tasks.append(
                tg.create_task(
                    explore_health_checks(project, None, creds),
                    name="explore_health_checks",
                )
            )
            tasks.append(
                tg.create_task(
                    explore_target_proxies(project, None, creds),
                    name="explore_target_proxies",
                )
            )

        [t.add_done_callback(task_done) for t in tasks]

    for task in tasks:
        result = task.result()
        if result is None:
            continue
        resources.extend(result)

    name = f"{project}-{location}"

    return Discovery(
        id=make_id(name),
        resources=resources,
        meta=Meta(name=name, display=name, kind="gcp", category=None),
    )


def expand_links(d: Discovery, serialized: dict[str, Any]) -> None:
    cloudrun_links(d, serialized)
    vpc_expand_links(d, serialized)
    sql_expand_links(d, serialized)
    gke_expand_links(d, serialized)
    lb_expand_links(d, serialized)
    mon_expand_links(d, serialized)


###############################################################################
# Private functions
###############################################################################
def task_done(task: asyncio.Task) -> None:
    task.remove_done_callback(task_done)

    if task.cancelled():
        logger.warning(f"Task '{task.get_name()}' cancelled")
        return None

    x = task.exception()
    if x:
        logger.error(f"{x=}")
        return None
