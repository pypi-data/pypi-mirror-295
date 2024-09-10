from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CommonFormField")


@_attrs_define
class CommonFormField:
    """
    Attributes:
        name (str):
        label (Union[None, Unset, str]):
        type (Union[None, Unset, str]):
        required (Union[None, Unset, bool]):
        default (Union[None, Unset, str]):
        description (Union[None, Unset, str]):
        options (Union[List[str], None, Unset]):
        placeholder (Union[None, Unset, str]):
    """

    name: str
    label: Union[None, Unset, str] = UNSET
    type: Union[None, Unset, str] = UNSET
    required: Union[None, Unset, bool] = UNSET
    default: Union[None, Unset, str] = UNSET
    description: Union[None, Unset, str] = UNSET
    options: Union[List[str], None, Unset] = UNSET
    placeholder: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        label: Union[None, Unset, str]
        if isinstance(self.label, Unset):
            label = UNSET
        else:
            label = self.label

        type: Union[None, Unset, str]
        if isinstance(self.type, Unset):
            type = UNSET
        else:
            type = self.type

        required: Union[None, Unset, bool]
        if isinstance(self.required, Unset):
            required = UNSET
        else:
            required = self.required

        default: Union[None, Unset, str]
        if isinstance(self.default, Unset):
            default = UNSET
        else:
            default = self.default

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        options: Union[List[str], None, Unset]
        if isinstance(self.options, Unset):
            options = UNSET
        elif isinstance(self.options, list):
            options = self.options

        else:
            options = self.options

        placeholder: Union[None, Unset, str]
        if isinstance(self.placeholder, Unset):
            placeholder = UNSET
        else:
            placeholder = self.placeholder

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if label is not UNSET:
            field_dict["label"] = label
        if type is not UNSET:
            field_dict["type"] = type
        if required is not UNSET:
            field_dict["required"] = required
        if default is not UNSET:
            field_dict["default"] = default
        if description is not UNSET:
            field_dict["description"] = description
        if options is not UNSET:
            field_dict["options"] = options
        if placeholder is not UNSET:
            field_dict["placeholder"] = placeholder

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        def _parse_label(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        label = _parse_label(d.pop("label", UNSET))

        def _parse_type(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        type = _parse_type(d.pop("type", UNSET))

        def _parse_required(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        required = _parse_required(d.pop("required", UNSET))

        def _parse_default(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        default = _parse_default(d.pop("default", UNSET))

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_options(data: object) -> Union[List[str], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                options_type_0 = cast(List[str], data)

                return options_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List[str], None, Unset], data)

        options = _parse_options(d.pop("options", UNSET))

        def _parse_placeholder(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        placeholder = _parse_placeholder(d.pop("placeholder", UNSET))

        common_form_field = cls(
            name=name,
            label=label,
            type=type,
            required=required,
            default=default,
            description=description,
            options=options,
            placeholder=placeholder,
        )

        common_form_field.additional_properties = d
        return common_form_field

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
