import pytest
from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from starlette.testclient import TestClient

from gravybox.endpoints import LinkEndpoint
from gravybox.exceptions import DataUnavailable
from gravybox.protocol import LinkRequest, LinkResponse

app = FastAPI()
app.add_middleware(LinkEndpoint)

router = APIRouter(prefix="/test")


class TestModel(BaseModel):
    value_one_plus_one: int
    opposite_of_value_two: bool


class TestRequest(LinkRequest):
    value_one: int
    value_two: bool


class TestResponse(LinkResponse):
    content: TestModel | None


@router.post("/success")
async def success_endpoint(link_request: TestRequest) -> TestResponse:
    result = TestModel(
        value_one_plus_one=link_request.value_one + 1,
        opposite_of_value_two=not link_request.value_two
    )
    return TestResponse(success=True, content=result)


@router.post("/failure")
async def failing_endpoint(link_request: TestRequest) -> TestResponse:
    raise RuntimeError("failing endpoint failed as expected")


@router.post("/data_unavailable")
async def data_unavailable_endpoint(link_request: TestRequest) -> TestResponse:
    raise DataUnavailable()


app.include_router(router)


@pytest.mark.asyncio
async def test_link_endpoint_no_payload():
    with TestClient(app) as client:
        response = client.post("/test/success")
        assert response.status_code == 400
        test_response = TestResponse.model_validate(response.json())
        assert test_response.success is False
        assert test_response.error == "request does not contain valid json, or is missing a trace_id"
        assert test_response.content is None


@pytest.mark.asyncio
async def test_link_endpoint_no_trace_id():
    with TestClient(app) as client:
        test_request = {
            "value_one": 3,
            "value_two": False
        }
        response = client.post("/test/success", json=test_request)
        assert response.status_code == 400
        test_response = TestResponse.model_validate(response.json())
        assert test_response.success is False
        assert test_response.error == "request does not contain valid json, or is missing a trace_id"
        assert test_response.content is None


@pytest.mark.asyncio
async def test_link_endpoint_malformed_payload():
    with TestClient(app) as client:
        test_request = {
            "trace_id": "malformed_payload",
            "value_one": 3
        }
        response = client.post("/test/success", json=test_request)
        assert response.status_code == 422


@pytest.mark.asyncio
async def test_link_endpoint_success():
    with TestClient(app) as client:
        test_request = TestRequest(trace_id="success", value_one=3, value_two=False)
        response = client.post("/test/success", json=test_request.model_dump())
        assert response.status_code == 200
        test_response = TestResponse.model_validate(response.json())
        assert test_response.success is True
        assert test_response.error == ""
        assert test_response.content.value_one_plus_one == 4
        assert test_response.content.opposite_of_value_two is True


@pytest.mark.asyncio
async def test_link_endpoint_failure():
    with TestClient(app) as client:
        test_request = TestRequest(trace_id="failure", value_one=3, value_two=False)
        response = client.post("/test/failure", json=test_request.model_dump())
        assert response.status_code == 500
        test_response = TestResponse.model_validate(response.json())
        assert test_response.success is False
        assert test_response.error == "server encountered unhandled exception"
        assert test_response.content is None


@pytest.mark.asyncio
async def test_link_endpoint_data_unavailable():
    with TestClient(app) as client:
        test_request = TestRequest(trace_id="data unavailable", value_one=3, value_two=False)
        response = client.post("/test/data_unavailable", json=test_request.model_dump())
        assert response.status_code == 500
        test_response = TestResponse.model_validate(response.json())
        assert test_response.success is False
        assert test_response.error == "data unavailable"
        assert test_response.content is None
