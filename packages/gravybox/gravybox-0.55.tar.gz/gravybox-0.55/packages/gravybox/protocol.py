from pydantic import BaseModel


class GravyboxRequest(BaseModel):
    trace_id: str


class GravyboxResponse(BaseModel):
    success: bool
    error: str = ""
    content: dict | None = None


class LinkRequest(GravyboxRequest):
    pass


class LinkResponse(GravyboxResponse):
    pass
