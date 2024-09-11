from traitlets import Enum, List, Unicode

from ._base import HraBaseWidget
from ._stylesheets import Font, Material
from ._traits import Attribute, Event

_DEFAULT_BASE_HREF = "https://cdn.humanatlas.io/ui/ccf-organ-info/"
_DEFAULT_DATA_SOURCES = ["https://purl.humanatlas.io/collection/ds-graphs"]
_DEFAULT_REMOTE_API_ENDPOINT = "https://apps.humanatlas.io/api"


class EuiOrganInformation(HraBaseWidget):
    _tag_name = "ccf-organ-info"
    _scripts = ["https://cdn.humanatlas.io/ui/ccf-organ-info/wc.js"]
    _styles = [
        Font.Inter,
        Material.Icons,
        "https://cdn.humanatlas.io/ui/ccf-organ-info/styles.css",
    ]

    _base_href = Attribute(Unicode(_DEFAULT_BASE_HREF))

    # organ_iri = Attribute(Unicode("http://purl.obolibrary.org/obo/UBERON_0002113"))
    organ_iri = Attribute(Unicode(), required=True)
    sex = Attribute(Enum(["Female", "Male"], default_value=None, allow_none=True))
    side = Attribute(Enum(["Left", "Right"], default_value=None, allow_none=True))
    data_sources = Attribute(List(Unicode(), default_value=_DEFAULT_DATA_SOURCES))
    highlight_providers = Attribute(List(Unicode(), default_value=[]))
    token = Attribute(Unicode(None, allow_none=True))
    remote_api_endpoint = Attribute(Unicode(_DEFAULT_REMOTE_API_ENDPOINT))
    donor_label = Attribute(Unicode(None, allow_none=True))
    rui_url = Attribute(Unicode(None, allow_none=True))
    eui_url = Attribute(Unicode(None, allow_none=True))
    asctb_url = Attribute(Unicode(None, allow_none=True))
    hra_portal_url = Attribute(Unicode(None, allow_none=True))
    online_course_url = Attribute(Unicode(None, allow_none=True))
    paper_url = Attribute(Unicode(None, allow_none=True))

    on_sex_change = Event(event_name="sexChange")
    on_side_change = Event(event_name="sideChange")
    on_node_click = Event(event_name="nodeClicked")
