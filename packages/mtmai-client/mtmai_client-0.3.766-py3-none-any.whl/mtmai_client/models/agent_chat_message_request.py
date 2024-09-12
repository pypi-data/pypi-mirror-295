from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AgentChatMessageRequest")


@_attrs_define
class AgentChatMessageRequest:
    """
    Attributes:
        chat_id (str):
        skip (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.
    """

    chat_id: str
    skip: Union[Unset, int] = 0
    limit: Union[Unset, int] = 100
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        chat_id = self.chat_id

        skip = self.skip

        limit = self.limit

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "chat_id": chat_id,
            }
        )
        if skip is not UNSET:
            field_dict["skip"] = skip
        if limit is not UNSET:
            field_dict["limit"] = limit

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        chat_id = d.pop("chat_id")

        skip = d.pop("skip", UNSET)

        limit = d.pop("limit", UNSET)

        agent_chat_message_request = cls(
            chat_id=chat_id,
            skip=skip,
            limit=limit,
        )

        agent_chat_message_request.additional_properties = d
        return agent_chat_message_request

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
