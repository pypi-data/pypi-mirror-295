from enum import Enum


class AgentViewType(str, Enum):
    POPUP = "popup"
    SIDEBAR = "sidebar"

    def __str__(self) -> str:
        return str(self.value)
