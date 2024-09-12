# mypy: disable-error-code="call-arg,index"
from typing import Any

import msgspec
from kubernetes import client

from lueur.links import add_link
from lueur.make_id import make_id
from lueur.models import Discovery, K8SMeta, Link, Resource
from lueur.platform.k8s.client import AsyncClient, Client
from lueur.rules import iter_resource

__all__ = ["explore_gateway"]


async def explore_gateway() -> list[Resource]:
    resources = []

    async with Client(client.CoreV1Api) as c:
        namespaces = await list_all_namespaces(c)

    async with Client(client.CustomObjectsApi) as c:
        for ns in namespaces:
            gateways = await explore_namespaced_gateways(c, ns, "v1")
            resources.extend(gateways)

            gateways = await explore_namespaced_gateways(c, ns, "v1beta1")
            resources.extend(gateways)

            gateways = await explore_namespaced_http_routes(c, ns, "v1")
            resources.extend(gateways)

            gateways = await explore_namespaced_http_routes(c, ns, "v1beta1")
            resources.extend(gateways)

    return resources


###############################################################################
# Private functions
###############################################################################
async def list_all_namespaces(c: AsyncClient) -> list[str]:
    response = await c.execute("list_namespace")

    namespaces = msgspec.json.decode(response.data)

    return [ns["metadata"]["name"] for ns in namespaces["items"]]


async def explore_namespaced_gateways(
    c: AsyncClient, ns: str, api_version: str = "v1"
) -> list[Resource]:
    response = await c.execute(
        "list_namespaced_custom_object",
        group="gateway.networking.k8s.io",
        version=api_version,
        plural="gateways",
        namespace=ns,
    )

    if response.status != 200:
        return []

    gateways = msgspec.json.decode(response.data)

    results = []
    for gw in gateways["items"]:
        meta = gw["metadata"]
        spec = gw["spec"]

        results.append(
            Resource(
                id=make_id(meta["uid"]),
                meta=K8SMeta(
                    name=f"{spec['gatewayClassName']}/{meta['name']}",
                    display=meta["name"],
                    kind="gateway",
                    platform="k8s",
                    ns=meta["namespace"],
                    category="loadbalancer",
                ),
                struct=gw,
            )
        )

    return results


async def explore_namespaced_http_routes(
    c: AsyncClient, ns: str, api_version: str = "v1"
) -> list[Resource]:
    response = await c.execute(
        "list_namespaced_custom_object",
        group="gateway.networking.k8s.io",
        version=api_version,
        plural="HTTPRoutes",
        namespace=ns,
    )

    if response.status != 200:
        return []

    routes = msgspec.json.decode(response.data)

    results = []
    for route in routes["items"]:
        meta = route["metadata"]

        results.append(
            Resource(
                id=make_id(meta["uid"]),
                meta=K8SMeta(
                    name=f"{meta['namespace']}/{meta['name']}",
                    display=meta["name"],
                    kind="httproute",
                    platform="k8s",
                    ns=meta["namespace"],
                    category="loadbalancer",
                ),
                struct=route,
            )
        )

    return results


def expand_links(d: Discovery, serialized: dict[str, Any]) -> None:
    for annotation in iter_resource(
        serialized,
        "$.resources[?@.meta.kind=='gateway'].struct.metadata.annotations['networking.gke.io/backend-services']",  # noqa E501
    ):
        r_id = annotation.parent.parent.parent.parent.obj["id"]  # type: ignore
        name = annotation.value.rsplit("/", 1)[-1]  # type: ignore

        p = f"$.resources[?@.meta.kind=='service' && @.struct.cloudRun.serviceName=='{name}']"  # noqa E501
        for svc in iter_resource(serialized, p):
            add_link(
                d,
                r_id,
                Link(
                    direction="out",
                    kind="service",
                    path=svc.path,
                    pointer=str(svc.pointer()),
                ),
            )

            svc_name = svc.obj["meta"]["name"]  # type: ignore

            p = f"$.resources[?@.meta.kind=='slo' && match(@.meta.name, '{svc_name}/serviceLevelObjectives/.*')]"  # noqa E501
            for slo in iter_resource(serialized, p):
                add_link(
                    d,
                    r_id,
                    Link(
                        direction="out",
                        kind="slo",
                        path=slo.path,
                        pointer=str(slo.pointer()),
                    ),
                )

    for urlmap in iter_resource(
        serialized,
        "$.resources[?@.meta.kind=='gateway'].struct.metadata.annotations['networking.gke.io/url-maps']",  # noqa E501
    ):
        r_id = urlmap.parent.parent.parent.parent.obj["id"]  # type: ignore
        name = urlmap.value.rsplit("/", 1)[-1]  # type: ignore

        p = f"$.resources[?@.meta.kind=='global-urlmap' && @.meta.name=='{name}']"  # noqa E501
        for urlmap in iter_resource(serialized, p):
            add_link(
                d,
                r_id,
                Link(
                    direction="out",
                    kind="global-urlmap",
                    path=urlmap.path,
                    pointer=str(urlmap.pointer()),
                ),
            )
