from pydantic import BaseModel

from mmisp.api_schemas.events.add_edit_get_event_response import AddEditGetEventGalaxyClusterRelation
from mmisp.api_schemas.events.get_all_events_response import GetAllEventsGalaxyClusterGalaxy
from mmisp.api_schemas.galaxies import ExportGalaxyGalaxyElement, GetAllSearchGalaxiesAttributes
from mmisp.api_schemas.organisations import GetOrganisationResponse
from mmisp.api_schemas.organisations.organisation import Organisation


class GetGalaxyClusterResponse(BaseModel):
    id: str | None = None
    uuid: str | None = None
    collection_uuid: str
    type: str
    value: str
    tag_name: str
    description: str
    galaxy_id: str
    source: str
    authors: list[str]
    version: str
    distribution: str
    sharing_group_id: str
    org_id: str
    orgc_id: str
    default: bool
    locked: bool
    extends_uuid: str
    extends_version: str
    published: bool
    deleted: bool
    Galaxy: GetAllSearchGalaxiesAttributes
    GalaxyElement: list[ExportGalaxyGalaxyElement]
    Org: GetOrganisationResponse
    Orgc: GetOrganisationResponse


class ExportGalaxyClusterResponse(BaseModel):
    id: str
    uuid: str
    collection_uuid: str
    type: str
    value: str
    tag_name: str
    description: str
    galaxy_id: str
    source: str
    authors: list[str]
    version: str
    distribution: str
    sharing_group_id: str
    org_id: str
    orgc_id: str
    default: bool
    locked: bool
    extends_uuid: str
    extends_version: str
    published: bool
    deleted: bool
    GalaxyElement: list[ExportGalaxyGalaxyElement]
    Galaxy: GetAllEventsGalaxyClusterGalaxy
    GalaxyClusterRelation: list[AddEditGetEventGalaxyClusterRelation] = []
    Org: Organisation
    Orgc: Organisation
