import asyncio
from asyncio import sleep, create_task, CancelledError

import pytest
from pydantic import BaseModel

from gravybox.betterstack import collect_logger
from gravybox.exceptions import DataUnavailable
from gravybox.framework import upstream_api_call, UpstreamCentrifuge
from gravybox.protocol import GravyboxRequest

logger = collect_logger()


class TestRequest(GravyboxRequest):
    pass


class TestTaskResult(BaseModel):
    field_one: str | None = None
    field_two: int | None = None
    field_three: bool | None = None


@upstream_api_call("testkit")
async def sleeping_coroutine(sleep_time: int,
                             field_one: str,
                             field_two: int,
                             field_three: bool = False,
                             log_extras: dict = None):
    logger.info("sleeping coroutine started sleeping", extra=log_extras)
    await asyncio.sleep(sleep_time)
    logger.info("sleeping coroutine finished sleeping", extra=log_extras)
    result = TestTaskResult(field_one=field_one, field_two=field_two, field_three=field_three)
    return result


@upstream_api_call("testkit")
async def failing_coroutine(sleep_time: int,
                            field_one: str,
                            field_two: int,
                            field_three: bool = False,
                            log_extras: dict = None):
    logger.info("failing coroutine started sleeping", extra=log_extras)
    await asyncio.sleep(sleep_time)
    logger.info("failing coroutine finished sleeping", extra=log_extras)
    raise RuntimeError("failing task failed as expected")


@upstream_api_call("testkit")
async def none_result_coroutine(sleep_time: int,
                                field_one: str,
                                field_two: int,
                                field_three: bool = False,
                                log_extras: dict = None):
    logger.info("none result coroutine started sleeping", extra=log_extras)
    await asyncio.sleep(sleep_time)
    logger.info("none result coroutine finished sleeping", extra=log_extras)
    return None


@pytest.mark.asyncio
async def test_link_endpoint_requires_link_request():
    with pytest.raises(ValueError, match="please pass the original link request when making a call to an upstream api"):
        await sleeping_coroutine(1, "test", 23, True)


@pytest.mark.asyncio
async def test_link_endpoint():
    link_request = TestRequest(trace_id="link_endpoint")
    result = await sleeping_coroutine(1, "test", 23, field_three=True, link_request=link_request)
    assert result == TestTaskResult(field_one="test", field_two=23, field_three=True)


@pytest.mark.asyncio
async def test_link_endpoint_failure():
    link_request = TestRequest(trace_id="endpoint_failure")
    result = await failing_coroutine(1, "test", 23, field_three=True, link_request=link_request)
    assert result is None


@pytest.mark.asyncio
async def test_link_endpoint_cancelled():
    link_request = TestRequest(trace_id="endpoint_cancel")
    task = create_task(sleeping_coroutine(999, "test", 23, field_three=True, link_request=link_request))
    await sleep(1)
    task.cancel()
    await sleep(1)
    with pytest.raises(CancelledError):
        await task.result()


@pytest.mark.asyncio
async def test_upstream_centrifuge_single_task():
    link_request = TestRequest(trace_id="centrifuge")
    tasks = [
        sleeping_coroutine(1, "test", 23, field_three=True, link_request=link_request)
    ]
    centrifuge = UpstreamCentrifuge(tasks, TestTaskResult)
    result = await centrifuge.activate()
    assert result == TestTaskResult(field_one="test", field_two=23, field_three=True)


@pytest.mark.asyncio
async def test_upstream_centrifuge_two_task():
    link_request = TestRequest(trace_id="double_centrifuge")
    tasks = [
        sleeping_coroutine(1, "test", 23, field_three=True, link_request=link_request),
        sleeping_coroutine(999, "sleepy", 333, field_three=False, link_request=link_request)
    ]
    centrifuge = UpstreamCentrifuge(tasks, TestTaskResult)
    result = await centrifuge.activate()
    assert result == TestTaskResult(field_one="test", field_two=23, field_three=True)


@pytest.mark.asyncio
async def test_upstream_centrifuge_failing_task():
    link_request = TestRequest(trace_id="failing_centrifuge")
    tasks = [
        sleeping_coroutine(5, "test", 23, field_three=True, link_request=link_request),
        failing_coroutine(1, "failure", 333, field_three=False, link_request=link_request)
    ]
    centrifuge = UpstreamCentrifuge(tasks, TestTaskResult)
    result = await centrifuge.activate()
    assert result == TestTaskResult(field_one="test", field_two=23, field_three=True)


@pytest.mark.asyncio
async def test_upstream_centrifuge_none_result_task():
    link_request = TestRequest(trace_id="failing_centrifuge")
    tasks = [
        sleeping_coroutine(5, "test", 23, field_three=True, link_request=link_request),
        none_result_coroutine(2, None, None, field_three=False, link_request=link_request)
    ]
    centrifuge = UpstreamCentrifuge(tasks, TestTaskResult)
    result = await centrifuge.activate()
    assert result == TestTaskResult(field_one="test", field_two=23, field_three=True)


@pytest.mark.asyncio
async def test_upstream_centrifuge_total_failure():
    link_request = TestRequest(trace_id="total_failure")
    tasks = [
        failing_coroutine(2, "failure", 333, field_three=False, link_request=link_request),
        failing_coroutine(1, "failure", 333, field_three=False, link_request=link_request)
    ]
    centrifuge = UpstreamCentrifuge(tasks, TestTaskResult)
    with pytest.raises(DataUnavailable):
        await centrifuge.activate()


@pytest.mark.asyncio
async def test_upstream_centrifuge_merge_two_results():
    link_request = TestRequest(trace_id="centrifuge_merge")
    tasks = [
        sleeping_coroutine(1, None, 23, field_three=True, link_request=link_request),
        sleeping_coroutine(3, "test", None, field_three=True, link_request=link_request),
    ]
    centrifuge = UpstreamCentrifuge(tasks, TestTaskResult)
    result = await centrifuge.activate()
    assert result == TestTaskResult(field_one="test", field_two=23, field_three=True)


@pytest.mark.asyncio
async def test_upstream_centrifuge_merge_overwrite():
    link_request = TestRequest(trace_id="merge_overwrite")
    tasks = [
        sleeping_coroutine(1, None, None, field_three=True, link_request=link_request),
        sleeping_coroutine(3, "test", None, field_three=True, link_request=link_request),
        sleeping_coroutine(5, "late_precedence", 15, field_three=False, link_request=link_request),
    ]
    centrifuge = UpstreamCentrifuge(tasks, TestTaskResult)
    result = await centrifuge.activate()
    assert result == TestTaskResult(field_one="late_precedence", field_two=15, field_three=False)


@pytest.mark.asyncio
async def test_upstream_centrifuge_chaos():
    link_request = TestRequest(trace_id="centrifuge_chaos")
    tasks = [
        sleeping_coroutine(99, None, None, field_three=True, link_request=link_request),
        failing_coroutine(33, "failure", 333, field_three=False, link_request=link_request),
        sleeping_coroutine(1, None, None, field_three=True, link_request=link_request),
        none_result_coroutine(3, None, None, field_three=False, link_request=link_request),
        failing_coroutine(1, "failure", 333, field_three=False, link_request=link_request),
        sleeping_coroutine(3, "test", None, field_three=True, link_request=link_request),
        none_result_coroutine(2, None, None, field_three=False, link_request=link_request),
        failing_coroutine(2, "failure", 333, field_three=False, link_request=link_request),
        sleeping_coroutine(5, "late_precedence", 15, field_three=False, link_request=link_request),
        sleeping_coroutine(19, "something_else", 25, field_three=False, link_request=link_request)
    ]
    centrifuge = UpstreamCentrifuge(tasks, TestTaskResult)
    result = await centrifuge.activate()
    assert result == TestTaskResult(field_one="late_precedence", field_two=15, field_three=False)
