import json
import time
import traceback

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, Response

from gravybox.betterstack import collect_logger
from gravybox.exceptions import DataUnavailable, GravyboxException
from gravybox.protocol import LinkResponse

logger = collect_logger()


class LinkEndpoint(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request, call_next):
        log_extras = {}
        try:
            payload = await request.json()
            log_extras["request_json"] = json.dumps(payload)
            log_extras["trace_id"] = payload["trace_id"]
        except Exception as error:
            log_extras["error_str"] = str(error)
            logger.error("(!) failed to parse request", extra=log_extras)
            return JSONResponse(
                status_code=400,
                content=LinkResponse(
                    success=False,
                    error="request does not contain valid json, or is missing a trace_id"
                ).model_dump()
            )
        logger.info("( ) link request", extra=log_extras)
        start_time = time.time()
        try:
            response: Response = await call_next(request)
            log_extras["elapsed_time"] = time.time() - start_time
            log_extras["status_code"] = response.status_code
            logger.info("(*) link response", extra=log_extras)
            return response
        except DataUnavailable:
            log_extras["elapsed_time"] = time.time() - start_time
            logger.warning("(!) link could not find requested data", extra=log_extras)
            return JSONResponse(
                status_code=500,
                content=LinkResponse(
                    success=False,
                    error="data unavailable"
                ).model_dump()
            )
        except Exception as error:
            if isinstance(error, GravyboxException):
                log_extras |= error.log_extras
            log_extras["error_str"] = str(error)
            log_extras["traceback"] = traceback.format_exc()
            log_extras["elapsed_time"] = time.time() - start_time
            logger.error("(!) link failed with unhandled exception", extra=log_extras)
            return JSONResponse(
                status_code=500,
                content=LinkResponse(
                    success=False,
                    error="server encountered unhandled exception"
                ).model_dump()
            )
