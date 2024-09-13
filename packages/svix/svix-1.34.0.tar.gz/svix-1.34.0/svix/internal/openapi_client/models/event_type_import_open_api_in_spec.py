from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.event_type_import_open_api_in_spec_additional_property import (
        EventTypeImportOpenApiInSpecAdditionalProperty,
    )


T = TypeVar("T", bound="EventTypeImportOpenApiInSpec")


@attr.s(auto_attribs=True)
class EventTypeImportOpenApiInSpec:
    """A pre-parsed JSON spec.

    Example:
        {'info': {'title': 'Webhook Example', 'version': '1.0.0'}, 'openapi': '3.1.0', 'webhooks': {'pet.new': {'post':
            {'requestBody': {'content': {'application/json': {'schema': {'properties': {'id': {'format': 'int64', 'type':
            'integer'}, 'name': {'type': 'string'}, 'tag': {'type': 'string'}}, 'required': ['id', 'name']}}},
            'description': 'Information about a new pet in the system'}, 'responses': {'200': {'description': 'Return a 200
            status to indicate that the data was received successfully'}}}}}}

    """

    additional_properties: Dict[str, "EventTypeImportOpenApiInSpecAdditionalProperty"] = attr.ib(
        init=False, factory=dict
    )

    def to_dict(self) -> Dict[str, Any]:
        pass

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.event_type_import_open_api_in_spec_additional_property import (
            EventTypeImportOpenApiInSpecAdditionalProperty,
        )

        d = src_dict.copy()
        event_type_import_open_api_in_spec = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = EventTypeImportOpenApiInSpecAdditionalProperty.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        event_type_import_open_api_in_spec.additional_properties = additional_properties
        return event_type_import_open_api_in_spec

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "EventTypeImportOpenApiInSpecAdditionalProperty":
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: "EventTypeImportOpenApiInSpecAdditionalProperty") -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
