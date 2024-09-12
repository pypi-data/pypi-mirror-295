import heapq
import datetime
import pydash as _
from ..data import S3, Athena, Koreadaychart, Koreatickchart
from ..state import State


@State.output("data", division_property_paths=["_name", "symbol"])
def handle_data(data):
    q = []
    for k,v in data.items():
        gen = instantiate_data(name=k, kwargs=v)
        push(q, gen)

    while q:
        yield pop(q)


def instantiate_data(name, kwargs):
    # get data type
    data_type = _.pop(kwargs, "type")
    gen = {
        "s3": S3,
        "athena": Athena,
        "koreadaychart": Koreadaychart,
        "koreatickchart": Koreatickchart,
    }[data_type](name=name, **kwargs)
    return gen

    
def pop(q):
    __, datum, gen = heapq.heappop(q)
    push(q, gen)
    return datum


def push(q, gen):
    try:
        datum = next(gen)
    except StopIteration:
        return
    # 시간순정렬을 위한 timestamp (시계열 데이터가 아닌경우 값을 아주 빠른 날짜로 줘서 최우선적으로 배출), datum, generator 3가지 순서의 튜플
    timestamp = datum.timestamp if hasattr(datum, "timestamp") else datetime.datetime(1,1,1)
    heapq.heappush(q, (timestamp, datum, gen))