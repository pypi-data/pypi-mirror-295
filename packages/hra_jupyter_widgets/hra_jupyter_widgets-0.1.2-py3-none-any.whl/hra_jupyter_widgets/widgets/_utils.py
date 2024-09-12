from __future__ import annotations

import traitlets as tr

from ._constants import AttributeBindingKey, EventBindingKey


def _snake_to_kebab_case(name: str) -> str:
    return name.replace("_", "-")


def get_trait_attribute_name(trait: tr.TraitType, key: str | None = None) -> str:
    if AttributeBindingKey.AttributeName in trait.metadata:
        return trait.metadata[AttributeBindingKey.AttributeName]
    if key is None:
        key = trait.name or ""
    return _snake_to_kebab_case(key).removeprefix('-')


def get_trait_event_name(trait: tr.TraitType, key: str | None = None) -> str:
    if EventBindingKey.EventName in trait.metadata:
        return trait.metadata[EventBindingKey.EventName]
    if key is None:
        key = trait.name or ""
    return _snake_to_kebab_case(key).removeprefix("on-")
