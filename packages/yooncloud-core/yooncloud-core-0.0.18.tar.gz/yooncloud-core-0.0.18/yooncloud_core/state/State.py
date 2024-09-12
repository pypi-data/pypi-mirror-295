import json
import pydash as _
import functools
from datetime import datetime
from pydantic import BaseModel
from collections import deque


class State:
    state = {}
    option = {
        "output": []
    }
    def __new__(cls):
        return cls.state

    @classmethod
    def set_option(cls, **kwargs):
        cls.option = {**cls.option, **kwargs}

    @classmethod
    def deque(cls, _id, *args, **kwargs):
        q = Deque(*args, **kwargs)
        _.set_(cls.state, _id, q)
        return q

    @classmethod
    def dict(cls, _id, *args, **kwargs):
        d = Dict(*args, **kwargs)
        _.set_(cls.state, _id, d)
        return d

    @classmethod
    def ref(cls, value, _id):
        r = Ref(value, _id)
        _.set_(cls.state, _id, value)
        return r

    @classmethod
    def json(cls):
        class Encoder(json.JSONEncoder):
            def default(self, o):
                if isinstance(o, deque):
                    return list(o)
                if isinstance(o, datetime):
                    return o.isoformat()
                if isinstance(o, BaseModel):
                    return o.model_dump()
                return super().default(o)
        return json.dumps(cls.state, cls=Encoder)

    @classmethod
    def output(cls, prefix, division_property_paths=[]):
        def get_id(datum):
            ret = prefix
            for a in division_property_paths:
                ret += f".{_.get(datum, a)}"
            return ret

        def add_output(datum):
            if datum==None:
                return
            _id = get_id(datum)
            if "output" not in cls.state:
                cls.state["output"] = {}
            if _id not in cls.state["output"]:
                cls.state["output"][_id] = list()
            cls.state["output"][_id].append(datum)

        def get_callbacks():
            callbacks = []
            if any(a.startswith(prefix) for a in cls.option["output"]):
                callbacks.append(add_output)
            return callbacks

        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                coro = func(*args, **kwargs)
                ret = next(coro)
                callbacks = get_callbacks()
                while True:
                    for a in callbacks:
                        a(ret)
                    datum = yield ret
                    try:
                        ret = coro.send(datum)
                    except StopIteration:
                        return
            return wrapper
        return decorator


#################
###   Types   ###
#################

class Deque(deque):
    def append(self, item):
        super().append(item)
        
            
class Dict(dict):
    def __setitem__(self, key, value) -> None:
        return super().__setitem__(key, value)


class Ref:
    def __init__(self, value, _id):
        self._v = value
        self._id = _id
    @property
    def value(self):
        return self._v
    @value.setter
    def value(self, value):
        self._v = value
        _.set_(State.state, self._id, value)