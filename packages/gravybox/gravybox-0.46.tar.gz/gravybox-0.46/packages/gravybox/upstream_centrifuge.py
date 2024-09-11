from asyncio import create_task, as_completed
from typing import List, Coroutine, Type

from pydantic import BaseModel

from gravybox.exceptions import DataUnavailable


def merge_dicts_and_trim_nones(first: dict, second: dict):
    trimmed_first = {key: value for key, value in first.items() if value is not None}
    trimmed_second = {key: value for key, value in second.items() if value is not None}
    result = trimmed_first | trimmed_second
    return result


def all_fields_populated(instance: BaseModel):
    for key, value in instance.model_dump().items():
        if value is None:
            return False
    return True


def no_fields_populated(instance: BaseModel):
    for key, value in instance.model_dump().items():
        if value is None:
            return True
    return False


class UpstreamCentrifuge:
    """
    calls upstream apis simultaneously
    expects each upstream call to return an instance of result_model, raise an exception, or return None
    """

    def __init__(self, upstream_calls: List[Coroutine], result_model: Type[BaseModel]):
        self.tasks = [create_task(upstream_call) for upstream_call in upstream_calls]
        self.result_model = result_model

    async def activate(self):
        final_result = self.result_model()
        for upstream_call_wrapper in as_completed(self.tasks):
            upstream_result = await upstream_call_wrapper
            if upstream_result is not None:
                final_result_dict = merge_dicts_and_trim_nones(final_result.model_dump(), upstream_result.model_dump())
                final_result = self.result_model.model_validate(final_result_dict)
                if all_fields_populated(final_result):
                    break
        for task in self.tasks:
            if not task.done():
                task.cancel()
        if no_fields_populated(final_result):
            raise DataUnavailable()
        return self.result_model.model_validate(final_result)
