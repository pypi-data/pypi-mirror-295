import pydash as _
from pydantic import create_model
from collections import defaultdict
from ..state import State


model = create_model("signal", __config__={"extra": "allow"})

@State.output("signal", division_property_paths=["symbol"])
def handle_signal(signal_schema):
    """
    symbol 별로 시그널 coroutine 을 생성후 유지

    signals = {
        "005930": {
            "my-signal-1": <coroutine>,
            "my-signal-2": <coroutine>
        },
        "057030": {
            ...
        }
    }
    """
    receive = {signal_name : _.pop(schema, "receive") for signal_name, schema in signal_schema.items()}
    signals = defaultdict(dict)
    def register(symbol):
        for k,v in signal_schema.items():
            signal_coro = instatantiate_signal(v)
            next(signal_coro)
            signals[symbol][k] = signal_coro
        
    ret = model()
    while True:
        datum = yield ret if len(ret.model_dump()) > 2 else None
        ret = model(**{"symbol": datum.symbol, "timestamp": datum.timestamp})
        if datum.symbol not in signals:
            register(datum.symbol)
        for signal_name, coro in signals[datum.symbol].items():
            if any(hasattr(datum, a) for a in receive[signal_name]):
                coro_ret = coro.send(datum)
                if coro_ret is not None:
                    setattr(ret, signal_name, coro_ret)


def instatantiate_signal(signal):
    condition_coros = [instatantiate_condition(a) for a in  signal["conditions"]]
    ret = False
    last = ret
    while True:
        datum = yield ret
        # True 에서 False, False 에서 True 로 바뀔때만 배출. 그외는 None
        ret = all(a.send(datum) for a in condition_coros)
        if ret == last:
            ret = None
        else:
            last = ret


######################
###   conditions   ###
######################

def instatantiate_condition(condition):
    field = condition.get("field")
    if value := condition.get("eq"):
        coro = eq(field, value)
    elif value := condition.get("gt"):
        coro = gt(field, value)
    elif value := condition.get("gte"):
        coro = gte(field, value)
    elif value := condition.get("lt"):
        coro = lt(field, value)
    elif value := condition.get("lte"):
        coro = lte(field, value)
    elif script := condition.get("script"):
        coro = script(script)
    next(coro)
    return coro


def script(script:list[str]):
    func = make_function_with_script(script)
    ret = None
    while True:
        datum = yield ret
        ret = func(datum)


def eq(field:str, value):
    s = [f"return indicator.{field} == {value}"]
    yield from script(script=s)


def gt(field:str, value):
    s = [f"return indicator.{field} > {value}"]
    yield from script(script=s)


def gte(field:str, value):
    s = [f"return indicator.{field} >= {value}"]
    yield from script(script=s)


def lt(field:str, value):
    s = [f"return indicator.{field} < {value}"]
    yield from script(script=s)


def lte(field:str, value):
    s = [f"return indicator.{field} <= {value}"]
    yield from script(script=s)


def make_function_with_script(script:list[str], args="indicator"):
    exec(f"def func({args}):\n\t" + "\n\t".join(script))
    return locals()["func"]