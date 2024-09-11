import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.message_public_message import MessagePublicMessage


T = TypeVar("T", bound="MessagePublic")


@_attrs_define
class MessagePublic:
    """
    Attributes:
        msg_id (int):
        read_ct (int):
        enqueued_at (datetime.datetime):
        vt (datetime.datetime):
        message (MessagePublicMessage):
    """

    msg_id: int
    read_ct: int
    enqueued_at: datetime.datetime
    vt: datetime.datetime
    message: "MessagePublicMessage"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        msg_id = self.msg_id

        read_ct = self.read_ct

        enqueued_at = self.enqueued_at.isoformat()

        vt = self.vt.isoformat()

        message = self.message.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "msg_id": msg_id,
                "read_ct": read_ct,
                "enqueued_at": enqueued_at,
                "vt": vt,
                "message": message,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.message_public_message import MessagePublicMessage

        d = src_dict.copy()
        msg_id = d.pop("msg_id")

        read_ct = d.pop("read_ct")

        enqueued_at = isoparse(d.pop("enqueued_at"))

        vt = isoparse(d.pop("vt"))

        message = MessagePublicMessage.from_dict(d.pop("message"))

        message_public = cls(
            msg_id=msg_id,
            read_ct=read_ct,
            enqueued_at=enqueued_at,
            vt=vt,
            message=message,
        )

        message_public.additional_properties = d
        return message_public

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
