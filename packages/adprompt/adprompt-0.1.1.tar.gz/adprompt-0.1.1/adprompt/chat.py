from openai.types.chat import ChatCompletion
from pydantic import BaseModel


class ChatResponse(BaseModel):
    result: dict = None
    content: str = None
    completion: ChatCompletion = None
    error_message: str = None
