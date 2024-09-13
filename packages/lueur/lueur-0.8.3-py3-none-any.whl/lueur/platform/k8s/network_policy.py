# mypy: disable-error-code="call-arg"
import msgspec
from kubernetes import client

from lueur.make_id import make_id
from lueur.models import K8SMeta, Resource
from lueur.platform.k8s.client import AsyncClient, Client

__all__ = ["explore_network_policy"]


async def explore_network_policy() -> list[Resource]:
    resources = []

    async with Client(client.NetworkingV1Api) as c:
        policies = await explore_network_policies(c)
        resources.extend(policies)

    return resources


###############################################################################
# Private functions
###############################################################################
async def explore_network_policies(c: AsyncClient) -> list[Resource]:
    response = await c.execute("list_network_policy_for_all_namespaces")

    policies = msgspec.json.decode(response.data)

    results = []
    for policy in policies["items"]:
        meta = policy["metadata"]
        results.append(
            Resource(
                id=make_id(meta["uid"]),
                meta=K8SMeta(
                    name=meta["name"],
                    display=meta["name"],
                    kind="network-policy",
                    platform="k8s",
                    namespace=meta.get("namespace"),
                    category="security",
                ),
                struct=policy,
            )
        )

    return results
