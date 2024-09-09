from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.chat_bot_ui_state_config import ChatBotUiStateConfig


T = TypeVar("T", bound="ChatBotUiState")


@_attrs_define
class ChatBotUiState:
    """
    Attributes:
        agent (Union[None, Unset, str]):
        layout (Union[None, Unset, str]):
        theme (Union[None, Unset, str]):
        thread_id (Union[None, Unset, str]):
        config (Union[Unset, ChatBotUiStateConfig]):
        id (Union[Unset, str]):
        user_id (Union[Unset, str]):
    """

    agent: Union[None, Unset, str] = UNSET
    layout: Union[None, Unset, str] = UNSET
    theme: Union[None, Unset, str] = UNSET
    thread_id: Union[None, Unset, str] = UNSET
    config: Union[Unset, "ChatBotUiStateConfig"] = UNSET
    id: Union[Unset, str] = UNSET
    user_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        agent: Union[None, Unset, str]
        if isinstance(self.agent, Unset):
            agent = UNSET
        else:
            agent = self.agent

        layout: Union[None, Unset, str]
        if isinstance(self.layout, Unset):
            layout = UNSET
        else:
            layout = self.layout

        theme: Union[None, Unset, str]
        if isinstance(self.theme, Unset):
            theme = UNSET
        else:
            theme = self.theme

        thread_id: Union[None, Unset, str]
        if isinstance(self.thread_id, Unset):
            thread_id = UNSET
        else:
            thread_id = self.thread_id

        config: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.config, Unset):
            config = self.config.to_dict()

        id = self.id

        user_id = self.user_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if agent is not UNSET:
            field_dict["agent"] = agent
        if layout is not UNSET:
            field_dict["layout"] = layout
        if theme is not UNSET:
            field_dict["theme"] = theme
        if thread_id is not UNSET:
            field_dict["threadId"] = thread_id
        if config is not UNSET:
            field_dict["config"] = config
        if id is not UNSET:
            field_dict["id"] = id
        if user_id is not UNSET:
            field_dict["user_id"] = user_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.chat_bot_ui_state_config import ChatBotUiStateConfig

        d = src_dict.copy()

        def _parse_agent(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        agent = _parse_agent(d.pop("agent", UNSET))

        def _parse_layout(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        layout = _parse_layout(d.pop("layout", UNSET))

        def _parse_theme(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        theme = _parse_theme(d.pop("theme", UNSET))

        def _parse_thread_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        thread_id = _parse_thread_id(d.pop("threadId", UNSET))

        _config = d.pop("config", UNSET)
        config: Union[Unset, ChatBotUiStateConfig]
        if isinstance(_config, Unset):
            config = UNSET
        else:
            config = ChatBotUiStateConfig.from_dict(_config)

        id = d.pop("id", UNSET)

        user_id = d.pop("user_id", UNSET)

        chat_bot_ui_state = cls(
            agent=agent,
            layout=layout,
            theme=theme,
            thread_id=thread_id,
            config=config,
            id=id,
            user_id=user_id,
        )

        chat_bot_ui_state.additional_properties = d
        return chat_bot_ui_state

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
