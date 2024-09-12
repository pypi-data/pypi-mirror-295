from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.chat_messages_item_artifacts_item import ChatMessagesItemArtifactsItem
    from ..models.chat_messages_item_props import ChatMessagesItemProps


T = TypeVar("T", bound="ChatMessagesItem")


@_attrs_define
class ChatMessagesItem:
    """
    Attributes:
        id (str):
        role (Union[Unset, str]):
        content (Union[Unset, str]):
        component (Union[Unset, str]):
        props (Union[Unset, ChatMessagesItemProps]):
        artifacts (Union[Unset, List['ChatMessagesItemArtifactsItem']]):
    """

    id: str
    role: Union[Unset, str] = UNSET
    content: Union[Unset, str] = UNSET
    component: Union[Unset, str] = UNSET
    props: Union[Unset, "ChatMessagesItemProps"] = UNSET
    artifacts: Union[Unset, List["ChatMessagesItemArtifactsItem"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        role = self.role

        content = self.content

        component = self.component

        props: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.props, Unset):
            props = self.props.to_dict()

        artifacts: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.artifacts, Unset):
            artifacts = []
            for artifacts_item_data in self.artifacts:
                artifacts_item = artifacts_item_data.to_dict()
                artifacts.append(artifacts_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
            }
        )
        if role is not UNSET:
            field_dict["role"] = role
        if content is not UNSET:
            field_dict["content"] = content
        if component is not UNSET:
            field_dict["component"] = component
        if props is not UNSET:
            field_dict["props"] = props
        if artifacts is not UNSET:
            field_dict["artifacts"] = artifacts

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.chat_messages_item_artifacts_item import ChatMessagesItemArtifactsItem
        from ..models.chat_messages_item_props import ChatMessagesItemProps

        d = src_dict.copy()
        id = d.pop("id")

        role = d.pop("role", UNSET)

        content = d.pop("content", UNSET)

        component = d.pop("component", UNSET)

        _props = d.pop("props", UNSET)
        props: Union[Unset, ChatMessagesItemProps]
        if isinstance(_props, Unset):
            props = UNSET
        else:
            props = ChatMessagesItemProps.from_dict(_props)

        artifacts = []
        _artifacts = d.pop("artifacts", UNSET)
        for artifacts_item_data in _artifacts or []:
            artifacts_item = ChatMessagesItemArtifactsItem.from_dict(artifacts_item_data)

            artifacts.append(artifacts_item)

        chat_messages_item = cls(
            id=id,
            role=role,
            content=content,
            component=component,
            props=props,
            artifacts=artifacts,
        )

        chat_messages_item.additional_properties = d
        return chat_messages_item

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
