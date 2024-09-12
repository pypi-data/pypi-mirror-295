from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.message_public import MessagePublic


T = TypeVar("T", bound="MessagePullResponseItem")


@_attrs_define
class MessagePullResponseItem:
    """
    Attributes:
        queue (str):
        messages (List['MessagePublic']):
    """

    queue: str
    messages: List["MessagePublic"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        queue = self.queue

        messages = []
        for messages_item_data in self.messages:
            messages_item = messages_item_data.to_dict()
            messages.append(messages_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "queue": queue,
                "messages": messages,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.message_public import MessagePublic

        d = src_dict.copy()
        queue = d.pop("queue")

        messages = []
        _messages = d.pop("messages")
        for messages_item_data in _messages:
            messages_item = MessagePublic.from_dict(messages_item_data)

            messages.append(messages_item)

        message_pull_response_item = cls(
            queue=queue,
            messages=messages,
        )

        message_pull_response_item.additional_properties = d
        return message_pull_response_item

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
