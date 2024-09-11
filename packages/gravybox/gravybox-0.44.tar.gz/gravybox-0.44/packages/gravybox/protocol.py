from pydantic import BaseModel


class LinkRequest(BaseModel):
    trace_id: str


class LinkResponse(BaseModel):
    success: bool
    error: str = ""
