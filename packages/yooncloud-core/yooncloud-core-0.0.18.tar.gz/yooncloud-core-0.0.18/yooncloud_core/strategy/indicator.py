import pydash as _
from collections import defaultdict, deque
from pydantic import create_model
from ..state import State


model = create_model("indicator", __config__={"extra": "allow"})

@State.output("indicator", division_property_paths=["symbol"])
def handle_indicator(indicator):
    listener = defaultdict(lambda: defaultdict(list))
    def make_callback(symbol, name, schema):
        schema["state_id"] = f"indicator.{name}.{symbol}"
        coro = instatantiate_indicator(schema)
        def func(datum, ret):
            if coro_ret := coro.send(datum):
                setattr(ret, name, coro_ret)
                for cb in listener[symbol][name]:
                    cb(coro_ret, ret)        
        return func

    def register(symbol):
        for name, schema in indicator.items():
            schema = schema.copy()
            receive = _.pop(schema, "receive")
            callback = make_callback(symbol, name, schema)
            listener[symbol][receive].append(callback)

    ret = model()
    while True:
        datum = yield ret if len(ret.model_dump()) > 2 else None
        ret = model(**{"symbol": datum.symbol, "timestamp": datum.timestamp})
        if datum.symbol not in listener:
            register(datum.symbol)
        for cb in listener[datum.symbol][datum._name]:
            cb(datum, ret)


def instatantiate_indicator(schema):
    indicator_type = _.pop(schema, "type")
    coro = {
        "max": max_,
        "min": min_,
        "moving_fn": moving_fn,
        "moving_sum": moving_sum,
        "moving_average": moving_average,
        "moving_normalized_deviation": moving_normalized_deviation,
        "bollinger_band": bollinger_band,
        "serial_diff": serial_diff,
    }[indicator_type](**schema)
    next(coro)
    return coro


#####################
###   indicator   ###
#####################

import numpy # do not delete this line

def max_(state_id:str, field=None):
    # indicator 에는 데이터(pydantic 인스턴스) 뿐아니라 다른 indicator 의 값(int, str 등 기본 타입)도 올수 있기 때문에 field 인수는 있을수도 없을수도 있다.
    ref, new_value = State.ref(float("-inf"), _id=state_id), float("-inf")
    while True:
        new_value = yield max(ref.value, new_value)
        new_value = getattr(new_value, field) if field else new_value
        ref.value = max(ref.value, new_value)


def min_(state_id:str, field=None):
    value, new_value = float("inf"), float("inf")
    while True:
        new_value = yield min(value, new_value)
        new_value = getattr(new_value, field) if field else new_value
        value = min(value, new_value)
    

def moving_fn(window:int, script:list[str], state_id:str):
    calculator = make_function_with_script(script)
    q = State.deque(state_id, maxlen=window)
    while True:
        datum = yield round(calculator(q), 2) if len(q)==q.maxlen else None
        q.append(datum)


def moving_sum(window:int, field:str=None, **kwargs):
    script = [f"return sum(a{'.' + field if field else ''} for a in values)"]
    yield from moving_fn(window=window, script=script, **kwargs)


def moving_average(window:int, field:str=None, **kwargs):
    script = [f"return numpy.mean([a{'.' + field if field else ''} for a in values])"]
    yield from moving_fn(window=window, script=script, **kwargs)


def moving_normalized_deviation(window:int, field:str=None, **kwargs):
    script = [
        f"stddev = numpy.std([a{'.' + field if field else ''} for a in values])",
        f"avg = numpy.mean([a{'.' + field if field else ''} for a in values])",
        f"return abs(values[-1]{'.' + field if field else ''} - avg) / stddev"
    ]
    yield from moving_fn(window=window, script=script, **kwargs)


def bollinger_band(sigma:int, window:int, field:str, **kwargs):
    script = [
        f"stddev = numpy.std([a{'.' + field if field else ''} for a in values])",
        f"lower_band, upper_band = values[-1] - {sigma} * stddev, values[-1] + {sigma} * stddev",
        "return [lower_band, upper_band]"
    ]
    yield from moving_fn(window=window, script=script, **kwargs)


def serial_diff(lag:int, **kwargs):
    # elasticsearch 의 동작을 그대로 모방하기 위해 window 값을 1 더크게 준다.
    window = lag + 1
    script = ["return values[-1] - values[0]"]
    return moving_fn(window=window, script=script, **kwargs)


def make_function_with_script(script:list[str], args="values"):
    exec(f"def func({args}):\n\t" + "\n\t".join(script))
    return locals()["func"]