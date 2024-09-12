from __future__ import annotations

import collections
import pathlib
import typing as t

import anywidget
import ipywidgets
import traitlets as tr

from ._constants import HraTraitType, ModelKey
from ._traits import EventHandler, ModelAttributes, ModelEvents


class HraBaseWidget(anywidget.AnyWidget):
    _esm = pathlib.Path(__file__).resolve().parent.parent / "static" / "hra_app.js"

    _max_height = None
    _attributes = ModelAttributes().tag(sync=True)
    _events = ModelEvents().tag(sync=True)
    _event_dispatchers = tr.Instance(
        collections.defaultdict,
        (ipywidgets.CallbackDispatcher,),
    )

    def __init__(self, *args, **kwargs) -> None:
        self.add_traits(**self._create_model_traits())
        self.on_msg(self._handle_event)
        self._ensure_required_attributes(kwargs)
        super().__init__(*args, **kwargs)

    def register_event_handler(
        self, event: str, handler: EventHandler, remove=False
    ) -> None:
        self._event_dispatchers[event].register_callback(handler, remove)

    def _create_model_traits(self) -> dict[str, tr.TraitType]:
        keys = [ModelKey.TagName, ModelKey.Scripts, ModelKey.Styles, ModelKey.MaxHeight]
        to_trait = lambda key: tr.Any(getattr(self, key)).tag(sync=True)
        return {key: to_trait(key) for key in keys}

    def _ensure_required_attributes(self, kwargs: dict[str, t.Any]) -> None:
        required = self.trait_names(type=HraTraitType.Attribute, required=True)
        missing = [name for name in required if name not in kwargs]
        if missing:
            raise AttributeError(f"Missing required arguments: {missing}")

    def _handle_event(self, _widget: t.Any, content: t.Any, _buffers: t.Any) -> None:
        if isinstance(content, dict) and "event" in content:
            self._event_dispatchers[content["event"]](content.get("data"))
