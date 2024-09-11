import traceback
import uuid
import logging
from typing import Optional, Generic, TypeVar, Union, ParamSpec, Callable
from functools import update_wrapper


from pydantic import BaseModel

ResponseType = TypeVar("ResponseType")

R = TypeVar("R")
T = TypeVar("T")
P = ParamSpec("P")
F = TypeVar("F")


class APIError(BaseModel):
    """定义错误信息结构"""
    error_code: Union[int, str]
    message: str


class APIResponse(BaseModel, Generic[ResponseType]):
    """API响应结构"""
    data: Optional[ResponseType]
    error: Optional[APIError] = None
    traceId: Optional[str] = None
    success: bool


def with_exception_handling(f: Callable[P, R]) -> Callable[P, APIResponse[R]]:
    """Marks a callback as wanting to receive the current context object as first argument."""

    def wrapper(*args: P.args, **kwargs: P.kwargs) -> APIResponse[R]:
        trace_id = str(uuid.uuid4())
        try:
            return APIResponse[R](data=f(*args, **kwargs))
        except Exception as e:
            logging.getLogger().error(f"TraceId: {trace_id}\n{traceback.format_exc()}")
            return APIResponse[R](data=None, error=APIError(error_code=500, message=str(e) or "Internal Server Error"),
                                  traceId=trace_id)

    return update_wrapper(wrapper, f)
