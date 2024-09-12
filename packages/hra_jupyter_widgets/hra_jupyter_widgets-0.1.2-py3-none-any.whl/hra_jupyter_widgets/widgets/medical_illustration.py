from traitlets import Dict, Unicode

from ._base import HraBaseWidget
from ._traits import Attribute, Event

_DEFAULT_ILLUSTRATIONS = "https://cdn.humanatlas.io/digital-objects/graph/2d-ftu-illustrations/latest/assets/2d-ftu-illustrations.jsonld"


class MedicalIllustration(HraBaseWidget):
    _tag_name = "hra-medical-illustration"
    _scripts = ["https://cdn.humanatlas.io/ui/medical-illustration/wc.js"]
    _styles = ["https://cdn.humanatlas.io/ui/medical-illustration/styles.css"]

    selected_illustration = Attribute(Unicode() | Dict(), required=True, help="")
    illustrations = Attribute(Unicode(_DEFAULT_ILLUSTRATIONS) | Dict(), help="")
    highlight = Attribute(Unicode(None, allow_none=True) | Dict(), help="")

    on_cell_click = Event()
    on_cell_hover = Event()
