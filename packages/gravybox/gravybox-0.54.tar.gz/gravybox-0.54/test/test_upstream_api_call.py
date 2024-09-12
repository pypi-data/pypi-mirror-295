from asyncio import create_task, sleep, CancelledError

import pytest

from gravybox.protocol import LinkRequest
from test.testkit import sleeping_coroutine, TestTaskResult, failing_coroutine


@pytest.mark.asyncio
async def test_upstream_api_call_requires_link_request():
    with pytest.raises(ValueError, match="please pass the original link request when making a call to an upstream api"):
        await sleeping_coroutine(1, "test", 23, True)


@pytest.mark.asyncio
async def test_upstream_api_call_success():
    link_request = LinkRequest(trace_id="link_endpoint")
    result = await sleeping_coroutine(1, "test", 23, field_three=True, link_request=link_request)
    assert result == TestTaskResult(field_one="test", field_two=23, field_three=True)


@pytest.mark.asyncio
async def test_upstream_api_call_failure():
    link_request = LinkRequest(trace_id="endpoint_failure")
    result = await failing_coroutine(1, "test", 23, field_three=True, link_request=link_request)
    assert result is None


@pytest.mark.asyncio
async def test_upstream_api_call_cancelled():
    link_request = LinkRequest(trace_id="endpoint_cancel")
    task = create_task(sleeping_coroutine(999, "test", 23, field_three=True, link_request=link_request))
    await sleep(1)
    task.cancel()
    await sleep(1)
    with pytest.raises(CancelledError):
        await task.result()
