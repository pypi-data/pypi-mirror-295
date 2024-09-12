import pandas as pd
from pydash import _
from typing import Optional, Generator
from datetime import datetime
from pydantic import BaseModel, create_model
from datetimerange import DateTimeRange



class Base:
    def __init__(self, name="", schema=None, symbol_field=None, timeseries_axis_field="", transforms=[]):
        self.name = name
        self.timeseries_axis_field = timeseries_axis_field

        gen = self.gen()
        def add_field(row):
            # _name
            row["_name"] = name
            # timestamp
            if timeseries_axis_field:
                row["timestamp"] = row[timeseries_axis_field]
            # symbol
            if symbol_field:
                row["symbol"] = row[symbol_field]
            return row
        gen = map(add_field, gen)
        # apply pydantic model
        if schema:
            model = self.create_model(schema, name)
            gen = map(lambda a: model(**a), gen)
        # transform
        gen = self._transform(gen, transforms)
        if type(gen) == list:
            gen = iter(gen)
        self._gen = gen
        

    def __iter__(self):
        return self


    def __next__(self):
        return next(self._gen)


    def _transform(self, gen, transforms):
        for t in transforms:
            match t["type"]:
                case "map":
                    func = make_function_with_script(t["script"])
                    gen = map(func, gen)
                case "filter":
                    func = make_function_with_script(t["script"])
                    gen = filter(func, gen)
                case "tap":
                    func = make_function_with_script(t["script"], args="rows")
                    gen = [a for a in gen]
                    gen = func(gen)
                case "timecut":
                    t.pop("type")
                    gen = self._timecut(**t, gen=gen)
                    pass
                case "unit_cut":
                    pass
                case "moving_function":
                    pass
        return gen

    
    def create_model(self, schema:Optional[dict], name:str) -> BaseModel:
        types = {
            "string": str,
            "int": int,
            "integer": int,
            "float": float,
            "date": datetime,
            "datetime": datetime,
            "bool": bool,
            "boolean": bool,
        }
        kwargs = {k: (types[v], None) for k,v in schema.items()}
        kwargs["timestamp"] = (datetime, ...)
        return create_model(name, **kwargs, __config__={"extra": "allow"})


    def gen(self):
        raise NotImplementedError()
    

    def _timecut(self, interval:int, aggs:dict, gen:Generator):
        def get_dtrange_coro():
            first_datum = yield
            timestamp = first_datum.timestamp
            timedelta = pd.to_timedelta(interval)
            # init start, timedelta, end
            start = datetime.fromisoformat(timestamp.date().isoformat()).replace(tzinfo=timestamp.tzinfo)
            if timedelta.days > 0:
                # interval 이 1일간 이상일경우 (보통 일봉데이터를 주봉데이터로 변환하기 위해 '7 days' 등이 값으로 들어온 경우) 주(week)의 월요일부터 시작하여 주단위로 계산할수 있게끔 start 를 변환. 그 외는 그날 00시 부터 시작하게끔 변환 
                start -= pd.Timedelta(days=start.weekday())
            end = datetime.fromisoformat("2099-01-01").replace(tzinfo=start.tzinfo)
            while True:
                yield DateTimeRange(start, end).range(timedelta)
        dtrange_coro = get_dtrange_coro()
        next(dtrange_coro)

        bucket_coros = {}
        aggregation_funcs = {}
        def init_by_each_symbol(symbol, dtrange):
            # init bucket coro
            if symbol not in bucket_coros:
                coro = timecut_bucket_coro(dtrange)
                bucket_coros[symbol] = coro
                next(coro)
            # init aggregation funcs
            if symbol not in aggregation_funcs:
                aggregation_funcs[symbol] = timecut_aggregation(aggs, self.name, symbol)
        
        while True:
            try:
                datum = next(gen)
                dtrange = dtrange_coro.send(datum)
                init_by_each_symbol(datum.symbol, dtrange)
            except StopIteration as e:
                # gen 에서 모든 데이터를 뽑아내서 고갈되었을때
                for symbol, coro in bucket_coros.items():
                    try:
                        coro.send("flush")
                    except StopIteration as e:
                        bucket, timestamp = e.value
                        ret = aggregation_funcs[symbol](bucket)
                        ret.timestamp = timestamp
                        yield ret
                break
            else:
                bucket, timestamp = bucket_coros[datum.symbol].send(datum)
                if bucket:
                    ret = aggregation_funcs[datum.symbol](bucket)
                    ret.timestamp = timestamp - pd.to_timedelta(interval)
                    yield ret
                
                
def timecut_bucket_coro(dtrange:DateTimeRange):
    datum = yield
    bucket = [datum]
    ret = None
    timestamp = None
    for cut in dtrange:
        if cut <= datum.timestamp:
            continue
        while True:
            datum = yield ret, timestamp
            if datum=="flush":
                return bucket, timestamp
            if datum.timestamp < cut:
                bucket.append(datum)
                ret = None
            else:
                ret = bucket.copy() if bucket else None
                bucket.clear()
                bucket.append(datum)
                timestamp = cut
                break
            

def timecut_aggregation(aggs:dict, name:str, symbol:str):
    model_root = create_model(name, __config__={"extra": "allow"})
    script_func = {}

    def func(bucket:list):
        ret = {}
        for agg_name, agg in aggs.items():
            match agg["type"]:
                case "sum":
                    ret[agg_name] = sum(a.volume for a in bucket)
                case "min":
                    ret[agg_name] = min(getattr(a, agg["field"]) for a in bucket)
                case "max":
                    ret[agg_name] = max(getattr(a, agg["field"]) for a in bucket)
                case "bar":
                    ret["open"] = getattr(bucket[0], agg["price_field"])
                    ret["high"] = max(getattr(datum, agg["price_field"]) for datum in bucket)
                    ret["low"] = min(getattr(datum, agg["price_field"]) for datum in bucket)
                    ret["close"] = getattr(bucket[-1], agg["price_field"])
                    ret["volume"] = sum(getattr(datum, agg["volume_field"]) for datum in bucket)
                case "script":
                    if agg_name not in script_func:
                        script_func[agg_name] = make_function_with_script(agg["script"], args="bucket")
                    ret[agg_name] = script_func[agg_name](bucket)

        ret["_name"] = name
        ret["symbol"] = symbol
        return model_root(**ret)
    return func


def make_function_with_script(script: list[str], args="row"):
    exec(f"def func({args}):\n\t" + "\n\t".join(script))
    return locals()["func"]