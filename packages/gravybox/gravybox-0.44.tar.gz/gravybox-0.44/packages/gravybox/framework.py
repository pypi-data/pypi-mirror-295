import asyncio
import time
import traceback
from asyncio import create_task, as_completed
from typing import Type, List, Coroutine

from pydantic import BaseModel
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, Response

from gravybox.betterstack import collect_logger
from gravybox.exceptions import GravyboxException
from gravybox.protocol import LinkRequest

logger = collect_logger()


class LinkEndpoint(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request, call_next):
        log_extras = {}
        try:
            link_request = await request.json()
            log_extras["trace_id"] = link_request["trace_id"]
        except Exception as error:
            log_extras["error_str"] = str(error)
            log_extras["traceback"] = traceback.format_exc()
            logger.error("(!) link failed to parse request", extra=log_extras)
            return JSONResponse(status_code=400, content={
                "success": False,
                "error": "request does not contain valid json, or is missing trace_id",
                "content": None
            })

        logger.info("( ) link request", extra=log_extras)
        start_time = time.time()
        try:
            response: Response = await call_next(request)
            log_extras["elapsed_time"] = time.time() - start_time
            logger.info("(*) link response", extra=log_extras)
            return response
        except Exception as error:
            if isinstance(error, GravyboxException):
                log_extras |= error.log_extras
            log_extras["error_str"] = str(error)
            log_extras["traceback"] = traceback.format_exc()
            log_extras["elapsed_time"] = time.time() - start_time
            logger.error("(!) link failed with unhandled exception", extra=log_extras)
            return JSONResponse(status_code=500, content={
                "success": False,
                "error": "server encountered unhandled exception",
                "content": None
            })


def upstream_api_call(upstream_provider):
    def decorator(function):
        async def wrapper(*args, link_request: LinkRequest = None, **kwargs):
            if link_request is None:
                raise ValueError("please pass the original link request when making a call to an upstream api")
            call_args = [arg for arg in args]
            call_kwargs = [f"{key}={value}" for key, value in kwargs.items()]
            log_extras = {
                "upstream_provider": upstream_provider,
                "upstream_call_type": function.__name__,
                "upstream_call_arguments": call_args + call_kwargs,
                "trace_id": link_request.trace_id
            }
            logger.info("( ) calling upstream api", extra=log_extras)
            start_time = time.time()
            try:
                result: BaseModel = await function(*args, log_extras=log_extras, **kwargs)
                log_extras["elapsed_time"] = time.time() - start_time
                log_extras["result"] = result.model_dump()
                logger.info("(*) calling upstream api succeeded", extra=log_extras)
                return result
            except asyncio.CancelledError:
                logger.info("(*) calling upstream api cancelled, exiting gracefully", extra=log_extras)
                raise
            except Exception as error:
                if isinstance(error, GravyboxException):
                    log_extras |= error.log_extras
                log_extras["error_str"] = str(error)
                log_extras["traceback"] = traceback.format_exc()
                log_extras["elapsed_time"] = time.time() - start_time
                logger.warning("(!) calling upstream api failed", extra=log_extras)
                return None

        return wrapper

    return decorator


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
        if value is not None:
            return True
    return False


class UpstreamCentrifuge:
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
        return self.result_model.model_validate(final_result)
