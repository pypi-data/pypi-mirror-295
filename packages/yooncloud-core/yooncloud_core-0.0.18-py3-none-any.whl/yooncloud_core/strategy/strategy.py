from .data import handle_data
from .indicator import handle_indicator
from .signal import handle_signal


def handle_strategy(strategy):
    def started_gen(data_gen):
        # 아래 while 문이 돌아가기 위해선 data_gen 이 started 된 상태여야한다. 그러기 위해서 next(data_gen) 을 실행하면 뽑혀나온 첫번째 데이터는 어떻게 처리할 방법이 없다. 이를위해 next() 를 한번 견딜수 있게끔 감싸주는 함수
        yield
        yield from data_gen
    gens = [
        started_gen(handle_data(strategy["data"])),
        handle_indicator(strategy["indicator"]),
        handle_signal(strategy["signal"])
    ]
    for gen in gens:
        next(gen)

    datum = None
    while True:
        ret = None
        for i, gen in enumerate(gens):
            try:
                datum = gen.send(datum)
            except StopIteration:
                return
            if datum is None:
                break
            if i == len(gens)-1:
                ret = datum
        if ret:
            yield ret