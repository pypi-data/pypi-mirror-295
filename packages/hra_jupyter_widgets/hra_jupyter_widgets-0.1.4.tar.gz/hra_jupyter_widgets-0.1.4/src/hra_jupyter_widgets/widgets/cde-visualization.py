from traitlets import Bool, Dict, List, Unicode

from ._base import HraBaseWidget
from ._stylesheets import Font, Material
from ._traits import Attribute


class Cde(HraBaseWidget):
    _tag_name = "cde-visualization"
    _scripts = ["https://cdn.humanatlas.io/ui/cde-visualization-wc/wc.js"]
    _styles = ["https://cdn.humanatlas.io/ui/cde-visualization-wc/styles.css"]
    # _max_height = "1000px"

    # _base_href = Attribute(Unicode(_DEFAULT_BASE_HREF, read_only=True))
    # _home_url = Attribute(Unicode("", read_only=True))
    # # TODO: _logo_tooltip - Maybe set to empty string
    # _login_disabled = Attribute(Bool(True, read_only=True))

    # data_sources = Attribute(List(Unicode(), default_value=_DEFAULT_DATA_SOURCES))
    # selected_organs = Attribute(List(Unicode()))
    # token = Attribute(Unicode(None, allow_none=True))
    # remote_api_endpoint = Attribute(Unicode(_DEFAULT_REMOTE_API_ENDPOINT))
    # theme = Attribute(Unicode(_DEFAULT_THEME))
    # header = Attribute(Bool(False))
    # filter = Attribute(Dict(default_value=None, allow_none=True))  # TODO improve type
