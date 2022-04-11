from __future__ import annotations
from protobuf.compiled_pb2 import *  # noqa
from functools import wraps
from typing import Callable, Optional, Type
from rich import print

from google.protobuf import json_format, message
MessageType = Optional[Type[message.Message]]


def wrapper_with_args(func):
    def param(*args, **kwargs):
        def wrapper(f):
            return func(*args, **kwargs, fn=f)
        return wrapper
    return param


@wrapper_with_args
def proto_wrap(req_class: MessageType, resp_class: MessageType, fn: Callable = None):  # type: ignore
    @wraps(fn)
    async def pwrapper(req, resp, *args, **kwargs):
        url_params = {k: v for k, v in kwargs.items()}
        preq = None
        if req_class is not None:
            # ifdef serialized connection enabled
            # preq = req_class()
            # preq.ParseFromString(await req.content)
            # else
            preq = json_format.ParseDict(await req.media(), req_class(), ignore_unknown_fields=True)
            # endif
        kwargs['preq'] = preq

        presp = None
        if resp_class is not None:
            presp = resp_class()
        kwargs['presp'] = presp

        print(f'req: [cyan]{fn.__name__}[/], {url_params=}, {preq=}')
        result = await fn(req, resp, *args, **kwargs)
        if presp is not None:
            # ifdef serialized connection enabled
            # resp.content = presp.SerializeToString()
            # else
            pdict = json_format.MessageToDict(presp, including_default_value_fields=True)
            print(f'presp: {presp=} => {pdict=}')
            if resp.media is None:
                resp.media = pdict
            else:
                resp.media.update(pdict)
            # endif
        return result

    @wraps(fn)
    async def try_pwrapper(*args, **kwargs):
        try:
            return await pwrapper(*args, **kwargs)
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise e
    return try_pwrapper
