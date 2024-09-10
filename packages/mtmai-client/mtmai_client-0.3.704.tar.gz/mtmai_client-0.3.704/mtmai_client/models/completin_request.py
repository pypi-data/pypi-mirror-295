from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.completin_request_task_type_0 import CompletinRequestTaskType0


T = TypeVar("T", bound="CompletinRequest")


@_attrs_define
class CompletinRequest:
    """
    Attributes:
        prompt (str):
        thread_id (Union[None, Unset, str]):
        chat_id (Union[None, Unset, str]):
        option (Union[None, Unset, str]):
        task (Union['CompletinRequestTaskType0', None, Unset]):
    """

    prompt: str
    thread_id: Union[None, Unset, str] = UNSET
    chat_id: Union[None, Unset, str] = UNSET
    option: Union[None, Unset, str] = UNSET
    task: Union["CompletinRequestTaskType0", None, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.completin_request_task_type_0 import CompletinRequestTaskType0

        prompt = self.prompt

        thread_id: Union[None, Unset, str]
        if isinstance(self.thread_id, Unset):
            thread_id = UNSET
        else:
            thread_id = self.thread_id

        chat_id: Union[None, Unset, str]
        if isinstance(self.chat_id, Unset):
            chat_id = UNSET
        else:
            chat_id = self.chat_id

        option: Union[None, Unset, str]
        if isinstance(self.option, Unset):
            option = UNSET
        else:
            option = self.option

        task: Union[Dict[str, Any], None, Unset]
        if isinstance(self.task, Unset):
            task = UNSET
        elif isinstance(self.task, CompletinRequestTaskType0):
            task = self.task.to_dict()
        else:
            task = self.task

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "prompt": prompt,
            }
        )
        if thread_id is not UNSET:
            field_dict["thread_id"] = thread_id
        if chat_id is not UNSET:
            field_dict["chat_id"] = chat_id
        if option is not UNSET:
            field_dict["option"] = option
        if task is not UNSET:
            field_dict["task"] = task

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.completin_request_task_type_0 import CompletinRequestTaskType0

        d = src_dict.copy()
        prompt = d.pop("prompt")

        def _parse_thread_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        thread_id = _parse_thread_id(d.pop("thread_id", UNSET))

        def _parse_chat_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        chat_id = _parse_chat_id(d.pop("chat_id", UNSET))

        def _parse_option(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        option = _parse_option(d.pop("option", UNSET))

        def _parse_task(data: object) -> Union["CompletinRequestTaskType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                task_type_0 = CompletinRequestTaskType0.from_dict(data)

                return task_type_0
            except:  # noqa: E722
                pass
            return cast(Union["CompletinRequestTaskType0", None, Unset], data)

        task = _parse_task(d.pop("task", UNSET))

        completin_request = cls(
            prompt=prompt,
            thread_id=thread_id,
            chat_id=chat_id,
            option=option,
            task=task,
        )

        completin_request.additional_properties = d
        return completin_request

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
