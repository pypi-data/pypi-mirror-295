import pytest

from gravybox.betterstack import collect_logger
from gravybox.exceptions import DataUnavailable
from gravybox.protocol import LinkRequest
from gravybox.upstream_centrifuge import UpstreamCentrifuge
from test.testkit import sleeping_coroutine, TestTaskResult, none_result_coroutine, failing_coroutine

logger = collect_logger()


@pytest.mark.asyncio
async def test_upstream_centrifuge_single_task():
    link_request = LinkRequest(trace_id="centrifuge")
    tasks = [
        sleeping_coroutine(1, "test", 23, field_three=True, link_request=link_request)
    ]
    centrifuge = UpstreamCentrifuge(tasks, TestTaskResult)
    result = await centrifuge.activate()
    assert result == TestTaskResult(field_one="test", field_two=23, field_three=True)


@pytest.mark.asyncio
async def test_upstream_centrifuge_two_task():
    link_request = LinkRequest(trace_id="double_centrifuge")
    tasks = [
        sleeping_coroutine(1, "test", 23, field_three=True, link_request=link_request),
        sleeping_coroutine(999, "sleepy", 333, field_three=False, link_request=link_request)
    ]
    centrifuge = UpstreamCentrifuge(tasks, TestTaskResult)
    result = await centrifuge.activate()
    assert result == TestTaskResult(field_one="test", field_two=23, field_three=True)


@pytest.mark.asyncio
async def test_upstream_centrifuge_failing_task():
    link_request = LinkRequest(trace_id="failing_centrifuge")
    tasks = [
        sleeping_coroutine(5, "test", 23, field_three=True, link_request=link_request),
        failing_coroutine(1, "failure", 333, field_three=False, link_request=link_request)
    ]
    centrifuge = UpstreamCentrifuge(tasks, TestTaskResult)
    result = await centrifuge.activate()
    assert result == TestTaskResult(field_one="test", field_two=23, field_three=True)


@pytest.mark.asyncio
async def test_upstream_centrifuge_none_result_task():
    link_request = LinkRequest(trace_id="failing_centrifuge")
    tasks = [
        sleeping_coroutine(5, "test", 23, field_three=True, link_request=link_request),
        none_result_coroutine(2, None, None, field_three=False, link_request=link_request)
    ]
    centrifuge = UpstreamCentrifuge(tasks, TestTaskResult)
    result = await centrifuge.activate()
    assert result == TestTaskResult(field_one="test", field_two=23, field_three=True)


@pytest.mark.asyncio
async def test_upstream_centrifuge_total_failure():
    link_request = LinkRequest(trace_id="total_failure")
    tasks = [
        failing_coroutine(2, "failure", 333, field_three=False, link_request=link_request),
        failing_coroutine(1, "failure", 333, field_three=False, link_request=link_request)
    ]
    centrifuge = UpstreamCentrifuge(tasks, TestTaskResult)
    with pytest.raises(DataUnavailable):
        await centrifuge.activate()


@pytest.mark.asyncio
async def test_upstream_centrifuge_merge_two_results():
    link_request = LinkRequest(trace_id="centrifuge_merge")
    tasks = [
        sleeping_coroutine(1, None, 23, field_three=True, link_request=link_request),
        sleeping_coroutine(3, "test", None, field_three=True, link_request=link_request),
    ]
    centrifuge = UpstreamCentrifuge(tasks, TestTaskResult)
    result = await centrifuge.activate()
    assert result == TestTaskResult(field_one="test", field_two=23, field_three=True)


@pytest.mark.asyncio
async def test_upstream_centrifuge_merge_overwrite():
    link_request = LinkRequest(trace_id="merge_overwrite")
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
    link_request = LinkRequest(trace_id="centrifuge_chaos")
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
