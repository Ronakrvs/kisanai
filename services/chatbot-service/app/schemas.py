from pydantic import BaseModel
from typing import Literal


class ChatRequest(BaseModel):
    message: str
    language: Literal["hi", "en"] = "hi"


class ChatResponse(BaseModel):
    answer: str
    language: str
