from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.event_type_update_schemas_additional_property import EventTypeUpdateSchemasAdditionalProperty


T = TypeVar("T", bound="EventTypeUpdateSchemas")


@attr.s(auto_attribs=True)
class EventTypeUpdateSchemas:
    """The schema for the event type for a specific version as a JSON schema.

    Example:
        {'1': {'description': 'An invoice was paid by a user', 'properties': {'invoiceId': {'description': 'The invoice
            id', 'type': 'string'}, 'userId': {'description': 'The user id', 'type': 'string'}}, 'required': ['invoiceId',
            'userId'], 'title': 'Invoice Paid Event', 'type': 'object'}}

    """

    additional_properties: Dict[str, "EventTypeUpdateSchemasAdditionalProperty"] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        pass

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.event_type_update_schemas_additional_property import EventTypeUpdateSchemasAdditionalProperty

        d = src_dict.copy()
        event_type_update_schemas = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = EventTypeUpdateSchemasAdditionalProperty.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        event_type_update_schemas.additional_properties = additional_properties
        return event_type_update_schemas

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "EventTypeUpdateSchemasAdditionalProperty":
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: "EventTypeUpdateSchemasAdditionalProperty") -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
