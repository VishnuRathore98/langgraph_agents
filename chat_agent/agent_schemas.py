from pydantic import BaseModel, Field


class ChatSession(BaseModel):
    role: str = Field(description="The role of the user")
    content: str = Field(
        description="The message, question, or response provided by the role."
    )


class ChatSchema(BaseModel):
    session_id: str = Field(description="The session id to uniqly identify a session.")
    session_content: list[ChatSession] = Field(
        description="The actual content of the session."
    )
