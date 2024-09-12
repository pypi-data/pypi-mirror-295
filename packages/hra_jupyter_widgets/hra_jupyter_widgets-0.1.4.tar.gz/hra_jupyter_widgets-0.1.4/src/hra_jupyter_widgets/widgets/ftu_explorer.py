from traitlets import Dict, Unicode

from ._base import HraBaseWidget
from ._stylesheets import Font, Material
from ._traits import Attribute, Event

_DEFAULT_BASE_HREF = "https://cdn.humanatlas.io/ui/ftu-ui/"
_DEFAULT_SUMMARIES = "assets/TEMP/ftu-cell-summaries.jsonld"
_DEFAULT_DATASETS = "assets/TEMP/ftu-datasets.jsonld"


class FtuExplorer(HraBaseWidget):
    _tag_name = "hra-ftu-ui"
    _scripts = [
        "https://cdn.humanatlas.io/ui/ftu-ui/polyfills.js",
        "https://cdn.humanatlas.io/ui/ftu-ui/main.js",
    ]
    _styles = [
        Font.Inter,
        Material.Icons,
        Material.Symbols,
        "https://cdn.humanatlas.io/ui/ftu-ui/styles.css",
    ]

    _base_href = Attribute(Unicode(_DEFAULT_BASE_HREF, read_only=True))

    selected_illustration = Attribute(Unicode(None, allow_none=True) | Dict(), help="")
    illustrations = Attribute(Unicode(None, allow_none=True) | Dict(), help="")
    summaries = Attribute(Unicode(_DEFAULT_SUMMARIES) | Dict(), help="")
    datasets = Attribute(Unicode(_DEFAULT_DATASETS) | Dict(), help="")

    on_illustration_selected = Event()
    on_cell_click = Event()
    on_cell_hover = Event()
