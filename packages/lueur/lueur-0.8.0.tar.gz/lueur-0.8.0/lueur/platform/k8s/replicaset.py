# mypy: disable-error-code="call-arg"
from typing import Any

import msgspec
from kubernetes import client

from lueur.links import add_link
from lueur.make_id import make_id
from lueur.models import Discovery, K8SMeta, Link, Resource
from lueur.platform.k8s.client import AsyncClient, Client
from lueur.rules import iter_resource

__all__ = ["explore_replicaset"]


async def explore_replicaset() -> list[Resource]:
    resources = []

    async with Client(client.AppsV1Api) as c:
        rs = await explore_replicasets(c)
        resources.extend(rs)

    return resources


###############################################################################
# Private functions
###############################################################################
async def explore_replicasets(c: AsyncClient) -> list[Resource]:
    response = await c.execute("list_replica_set_for_all_namespaces")

    pods = msgspec.json.decode(response.data)

    results = []
    for rs in pods["items"]:
        meta = rs["metadata"]
        results.append(
            Resource(
                id=make_id(meta["uid"]),
                meta=K8SMeta(
                    name=meta["name"],
                    display=meta["name"],
                    kind="replicaset",
                    platform="k8s",
                    ns=meta["namespace"],
                    category="compute",
                ),
                struct=rs,
            )
        )

    return results


def expand_links(d: Discovery, serialized: dict[str, Any]) -> None:
    for rs in iter_resource(
        serialized,
        "$.resources[?@.meta.kind=='replicaset' && @.meta.platform=='k8s'].meta.name",  # noqa: E501
    ):
        r_id = rs.parent.parent.obj["id"]  # type: ignore
        name = rs.value

        p = f"$.resources[?@.meta.kind=='pod'].struct.metadata.ownerReferences[?@.kind=='ReplicaSet' && @.name=='{name}']"  # noqa E501
        for pod in iter_resource(serialized, p):
            add_link(
                d,
                r_id,
                Link(
                    direction="out",
                    kind="pod",
                    path=pod.path,
                    pointer=str(pod.pointer()),
                ),
            )
