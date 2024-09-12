import asyncio
import secrets
from typing import Any

from lueur.make_id import make_id
from lueur.models import Discovery, Meta
from lueur.platform.k8s.deployment import (
    expand_links as deployment_expand_links,
)
from lueur.platform.k8s.deployment import explore_deployment
from lueur.platform.k8s.gateway import expand_links as gateway_expand_links
from lueur.platform.k8s.gateway import explore_gateway
from lueur.platform.k8s.ingress import explore_ingress
from lueur.platform.k8s.network_policy import explore_network_policy
from lueur.platform.k8s.node import expand_links as node_expand_links
from lueur.platform.k8s.node import explore_node
from lueur.platform.k8s.pod import explore_pod
from lueur.platform.k8s.replicaset import (
    expand_links as replicaset_expand_links,
)
from lueur.platform.k8s.replicaset import explore_replicaset
from lueur.platform.k8s.service import explore_service

__all__ = ["explore", "expand_links"]


async def explore() -> Discovery:
    resources = []
    tasks: list[asyncio.Task] = []

    async with asyncio.TaskGroup() as tg:
        tasks.append(tg.create_task(explore_node()))
        tasks.append(tg.create_task(explore_pod()))
        tasks.append(tg.create_task(explore_replicaset()))
        tasks.append(tg.create_task(explore_deployment()))
        tasks.append(tg.create_task(explore_ingress()))
        tasks.append(tg.create_task(explore_service()))
        tasks.append(tg.create_task(explore_network_policy()))
        tasks.append(tg.create_task(explore_gateway()))

    for task in tasks:
        result = task.result()
        if result is None:
            continue
        resources.extend(result)

    name = secrets.token_hex(8)

    return Discovery(
        id=make_id(name),
        resources=resources,
        meta=Meta(name=name, display="Kubernetes", kind="k8s", category=None),
    )


def expand_links(d: Discovery, serialized: dict[str, Any]) -> None:
    deployment_expand_links(d, serialized)
    gateway_expand_links(d, serialized)
    node_expand_links(d, serialized)
    replicaset_expand_links(d, serialized)
