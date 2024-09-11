from pydantic import BaseModel


class GravyboxRequest(BaseModel):
    trace_id: str


class LinkRequest(GravyboxRequest):
    pass


class GravyboxResponse(BaseModel):
    success: bool
    error: str = ""
    content: dict | None = None
