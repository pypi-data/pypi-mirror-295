from __future__ import annotations

import collections.abc as abc
import typing as t

import traitlets as tr

from ._constants import AttributeBindingKey, EventBindingKey, HraTraitType
from ._utils import get_trait_attribute_name, get_trait_event_name

G = t.TypeVar("G")
S = t.TypeVar("S")


class Attribute(tr.TraitType[G, S]):
    def __new__(
        cls: type[Attribute[G, S]],
        trait: tr.TraitType[G, S],
        *,
        attribute_name: str | None = None,
        required=False,
        help: str | None = None,
    ) -> tr.TraitType[G, S]:
        trait.metadata["type"] = HraTraitType.Attribute
        trait.metadata["required"] = required
        trait.metadata["sync"] = True

        if attribute_name:
            trait.metadata[AttributeBindingKey.AttributeName] = attribute_name

        if help is not None:
            trait.help = help
            trait.__doc__ = help
            trait.metadata["help"] = help

        return trait

    def __instancecheck__(self, instance: t.Any) -> bool:
        return (
            isinstance(instance, tr.TraitType)
            and instance.metadata.get("type") == HraTraitType.Attribute
        )


EventHandler = abc.Callable[[t.Any], None]


class EventRegistry(t.Protocol):
    def __call__(self, handler: EventHandler, remove=False) -> None: ...


@t.runtime_checkable
class _EventWidget(t.Protocol):
    def register_event_handler(
        self, event: str, handler: EventHandler, remove=False
    ) -> None: ...


class Event(tr.TraitType[EventRegistry, EventRegistry]):
    def __init__(
        self,
        *,
        event_name: str | None = None,
        properties: list[str] | None = None,
        help: str | None = None,
    ) -> None:
        super().__init__(allow_none=True, read_only=True, help=help)
        self.metadata["type"] = HraTraitType.Event

        if event_name:
            self.metadata[EventBindingKey.EventName] = event_name

        if properties is not None:
            self.metadata[EventBindingKey.Properties] = properties

    def default(self, obj: t.Any = None) -> EventRegistry | None:
        if not isinstance(obj, _EventWidget):
            raise TypeError("Event must be a property of a HraBaseWidget subclass")

        def register(handler: EventHandler, remove=False) -> None:
            event_name = get_trait_event_name(self)
            obj.register_event_handler(event_name, handler, remove)

        return register


class _Bindings(tr.List[dict[str, t.Any]]):
    def default(self, obj: t.Any = None) -> tr.List[dict[str, t.Any]]:
        if not isinstance(obj, tr.HasTraits):
            return []

        traits = self._select_traits(obj)
        return [self._create_binding(key, trait) for key, trait in traits.items()]

    def _select_traits(self, _obj: tr.HasTraits) -> dict[str, tr.TraitType]: ...

    def _create_binding(self, _key: str, _trait: tr.TraitType) -> dict[str, t.Any]: ...


class ModelAttributes(_Bindings):
    def __init__(self, **kwargs) -> None:
        super().__init__(
            tr.Dict(
                per_key_traits={
                    AttributeBindingKey.AttributeName: tr.Unicode(),
                    AttributeBindingKey.ModelKey: tr.Unicode(),
                }
            ),
            **kwargs,
        )

    def _select_traits(self, obj: tr.HasTraits) -> dict[str, tr.TraitType]:
        return obj.traits(type=HraTraitType.Attribute)

    def _create_binding(self, key: str, trait: tr.TraitType) -> dict[str, t.Any]:
        return {
            AttributeBindingKey.AttributeName: get_trait_attribute_name(trait, key),
            AttributeBindingKey.ModelKey: key,
        }


class ModelEvents(_Bindings):
    def __init__(self, **kwargs) -> None:
        super().__init__(
            tr.Dict(
                per_key_traits={
                    EventBindingKey.EventName: tr.Unicode(),
                    EventBindingKey.Properties: tr.List(
                        trait=tr.Unicode(),
                        default_value=None,
                        allow_none=True,
                    ),
                }
            ),
            **kwargs,
        )

    def _select_traits(self, obj: tr.HasTraits) -> dict[str, tr.TraitType]:
        return obj.traits(type=HraTraitType.Event)

    def _create_binding(self, key: str, trait: tr.TraitType) -> dict[str, t.Any]:
        return {
            EventBindingKey.EventName: get_trait_event_name(trait, key),
            EventBindingKey.Properties: trait.metadata.get(EventBindingKey.Properties),
        }
