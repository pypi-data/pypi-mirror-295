from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.event_type_from_open_api_schemas import EventTypeFromOpenApiSchemas


T = TypeVar("T", bound="EventTypeFromOpenApi")


@attr.s(auto_attribs=True)
class EventTypeFromOpenApi:
    """
    Attributes:
        deprecated (bool):
        description (str):
        name (str): The event type's name Example: user.signup.
        schemas (Union[Unset, None, EventTypeFromOpenApiSchemas]):  Example: {'description': 'An invoice was paid by a
            user', 'properties': {'invoiceId': {'description': 'The invoice id', 'type': 'string'}, 'userId':
            {'description': 'The user id', 'type': 'string'}}, 'required': ['invoiceId', 'userId'], 'title': 'Invoice Paid
            Event', 'type': 'object'}.
    """

    deprecated: bool
    description: str
    name: str
    schemas: Union[Unset, None, "EventTypeFromOpenApiSchemas"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        deprecated = self.deprecated
        description = self.description
        name = self.name
        schemas = self.schemas

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "deprecated": deprecated,
                "description": description,
                "name": name,
            }
        )
        if schemas is not UNSET:
            field_dict["schemas"] = schemas

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        deprecated = d.pop("deprecated")

        description = d.pop("description")

        name = d.pop("name")

        schemas = d.pop("schemas", UNSET)

        event_type_from_open_api = cls(
            deprecated=deprecated,
            description=description,
            name=name,
            schemas=schemas,
        )

        event_type_from_open_api.additional_properties = d
        return event_type_from_open_api

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
