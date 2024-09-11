from pydantic import BaseModel

from galileo_core.schemas.shared.message_role import MessageRole


class Message(BaseModel):
    content: str
    role: str = MessageRole.user

    @property
    def message(self) -> str:
        role = self.role.value if isinstance(self.role, MessageRole) else self.role
        return f"{role}: {self.content}"
