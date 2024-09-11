import asyncio
import json
import time
import traceback

from pydantic import BaseModel

from gravybox.betterstack import collect_logger
from gravybox.exceptions import GravyboxException, DataUnavailable
from gravybox.protocol import LinkRequest

logger = collect_logger()


def upstream_api_call(upstream_provider):
    """
    wrapper for all upstream api calls
    handles errors, task cancellations, metrics, and logging
    """

    def decorator(function):
        async def wrapper(*args, link_request: LinkRequest = None, **kwargs):
            if link_request is None:
                raise ValueError("please pass the original link request when making a call to an upstream api")
            call_args = [arg for arg in args]
            call_kwargs = [f"{key}={value}" for key, value in kwargs.items()]
            log_extras = {
                "upstream_provider": upstream_provider,
                "upstream_call_type": function.__name__,
                "upstream_call_arguments": json.dumps(call_args + call_kwargs),
                "trace_id": link_request.trace_id
            }
            logger.info("( ) calling upstream api", extra=log_extras)
            start_time = time.time()
            try:
                result: BaseModel = await function(*args, log_extras=log_extras, **kwargs)
                log_extras["elapsed_time"] = time.time() - start_time
                log_extras["result"] = result.model_dump_json()
                logger.info("(*) calling upstream api succeeded", extra=log_extras)
                return result
            except asyncio.CancelledError:
                log_extras["elapsed_time"] = time.time() - start_time
                logger.info("(*) calling upstream api cancelled, exiting gracefully", extra=log_extras)
                raise
            except DataUnavailable:
                log_extras["elapsed_time"] = time.time() - start_time
                logger.warning("(!) upstream api could not find requested data", extra=log_extras)
                return None
            except Exception as error:
                if isinstance(error, GravyboxException):
                    log_extras |= error.log_extras
                log_extras["error_str"] = str(error)
                log_extras["traceback"] = traceback.format_exc()
                log_extras["elapsed_time"] = time.time() - start_time
                logger.error("(!) upstream api failed with unhandled exception", extra=log_extras)
                return None

        return wrapper

    return decorator
