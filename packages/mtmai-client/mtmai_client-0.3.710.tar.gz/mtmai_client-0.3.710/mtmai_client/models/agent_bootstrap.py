from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.agent_view_type import AgentViewType
from ..types import UNSET, Unset

T = TypeVar("T", bound="AgentBootstrap")


@_attrs_define
class AgentBootstrap:
    """前端获取 agent 的配置
    前端全局agent 加载器会在所有页面加载时返回配置初始化agent UI

        Attributes:
            view_type (Union[AgentViewType, None, Unset]):  Default: AgentViewType.SIDEBAR.
            is_show_fab (Union[Unset, bool]):  Default: True.
    """

    view_type: Union[AgentViewType, None, Unset] = AgentViewType.SIDEBAR
    is_show_fab: Union[Unset, bool] = True
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        view_type: Union[None, Unset, str]
        if isinstance(self.view_type, Unset):
            view_type = UNSET
        elif isinstance(self.view_type, AgentViewType):
            view_type = self.view_type.value
        else:
            view_type = self.view_type

        is_show_fab = self.is_show_fab

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if view_type is not UNSET:
            field_dict["view_type"] = view_type
        if is_show_fab is not UNSET:
            field_dict["is_show_fab"] = is_show_fab

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_view_type(data: object) -> Union[AgentViewType, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                view_type_type_0 = AgentViewType(data)

                return view_type_type_0
            except:  # noqa: E722
                pass
            return cast(Union[AgentViewType, None, Unset], data)

        view_type = _parse_view_type(d.pop("view_type", UNSET))

        is_show_fab = d.pop("is_show_fab", UNSET)

        agent_bootstrap = cls(
            view_type=view_type,
            is_show_fab=is_show_fab,
        )

        agent_bootstrap.additional_properties = d
        return agent_bootstrap

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
