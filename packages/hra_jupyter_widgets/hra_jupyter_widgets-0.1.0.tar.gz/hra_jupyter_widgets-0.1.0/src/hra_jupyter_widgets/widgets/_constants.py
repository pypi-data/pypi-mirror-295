class HraTraitType:
    Attribute = "attribute"
    Event = "event"


class ModelKey:
    TagName = "_tag_name"
    Scripts = "_scripts"
    Styles = "_styles"
    MaxHeight = "_max_height"
    Attributes = "_attributes"
    Events = "_events"


class AttributeBindingKey:
    AttributeName = "attribute_name"
    ModelKey = "model_key"


class EventBindingKey:
    EventName = "event_name"
    Properties = "properties"
