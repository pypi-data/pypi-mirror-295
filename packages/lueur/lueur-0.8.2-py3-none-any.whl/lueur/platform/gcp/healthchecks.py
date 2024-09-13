# mypy: disable-error-code="union-attr"
import msgspec
from google.oauth2._service_account_async import Credentials

from lueur.make_id import make_id
from lueur.models import GCPMeta, Resource
from lueur.platform.gcp.client import AuthorizedSession, Client

__all__ = ["explore_health_checks"]


async def explore_health_checks(
    project: str, location: str | None = None, creds: Credentials | None = None
) -> list[Resource]:
    resources = []

    async with Client("https://compute.googleapis.com", creds) as c:
        if location:
            hc = await explore_regional_healthchecks(c, project, location)
            resources.extend(hc)
        else:
            hc = await explore_global_healthchecks(c, project)
            resources.extend(hc)

    return resources


###############################################################################
# Private functions
###############################################################################
async def explore_global_healthchecks(
    c: AuthorizedSession, project: str
) -> list[Resource]:
    response = await c.get(
        f"/compute/v1/projects/{project}/global/healthChecks"
    )

    firewalls = msgspec.json.decode(response.content)

    results = []
    for hc in firewalls.get("items", []):
        self_link = hc["selfLink"]
        name = hc["name"]
        display = name

        results.append(
            Resource(
                id=make_id(hc["id"]),
                meta=GCPMeta(
                    name=name,
                    display=display,
                    kind="global-healthchecks",
                    project=project,
                    self_link=self_link,
                    platform="gcp",
                    category="observability",
                ),
                struct=hc,
            )
        )

    return results


async def explore_regional_healthchecks(
    c: AuthorizedSession, project: str, location: str
) -> list[Resource]:
    response = await c.get(
        f"/compute/v1/projects/{project}/regions/{location}/healthChecks"
    )

    firewalls = msgspec.json.decode(response.content)

    results = []
    for hc in firewalls.get("items", []):
        self_link = hc["selfLink"]
        name = hc["name"]
        display = name

        results.append(
            Resource(
                id=make_id(hc["id"]),
                meta=GCPMeta(
                    name=name,
                    display=display,
                    kind="regional-healthchecks",
                    project=project,
                    self_link=self_link,
                    region=location,
                    platform="gcp",
                    category="observability",
                ),
                struct=hc,
            )
        )

    return results
