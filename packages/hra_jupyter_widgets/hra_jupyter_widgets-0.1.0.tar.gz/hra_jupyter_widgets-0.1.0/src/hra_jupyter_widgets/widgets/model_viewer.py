import pathlib
import typing as t

import anywidget
from traitlets import Bytes, Unicode

STATIC_DIR = pathlib.Path(__file__).resolve().parent.parent / "static"


class ModelViewer(anywidget.AnyWidget):
    """Provides Google's model viewer as a jupyter widget.

    Inputs:
        width (string): Width of the viewer (must be valid css, ex: 500px)
        height (string): Height of the viewer (must be valid css, ex: 500px)
        url (string): The URL to the 3D model (only glTF and GLB models are supported)
        data (bytes): In memory data of the 3D model

    Raises:
        AttributeError: If neither a url or raw data is provided when the viewer is created

    See:
        https://github.com/google/model-viewer/tree/master
    """

    _esm = STATIC_DIR / "model_viewer.js"
    _css = STATIC_DIR / "model_viewer.css"

    width = Unicode(
        None, allow_none=True, help="Width of the model viewer (default 500px)"
    ).tag(sync=True)
    height = Unicode(
        None, allow_none=True, help="Height of the model viewer (default 500px)"
    ).tag(sync=True)

    url = Unicode(None, allow_none=True, help="Url to the 3D model").tag(sync=True)
    data = Bytes(None, allow_none=True, help="In memory 3D model").tag(sync=True)

    def __init__(
        self,
        *args: t.Any,
        url: str | None = None,
        data: bytes | None = None,
        **kwargs: t.Any,
    ) -> None:
        if url is None and data is None:
            raise AttributeError("Must provide either 'url' or 'data'")
        super().__init__(*args, url=url, data=data, **kwargs)
