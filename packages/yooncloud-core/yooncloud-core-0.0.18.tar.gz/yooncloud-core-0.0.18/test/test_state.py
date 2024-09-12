import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import json
import pytest
import logging
logging.basicConfig(level=logging.INFO)
from yooncloud_core.state import State
from yooncloud_core.strategy import handle_strategy


strategy = {
    "data": {
        "tick": {
            "type": "koreatickchart",
            "date": "2019-02-11",
            "symbols": ["057030", "005930", "075130"],
            "transforms": [
                    {
                    "type": "timecut",
                    "interval": "3 seconds",
                    "aggs": {
                        "bar": {
                            "type": "bar",
                            "price_field": "price",
                            "volume_field": "volume",
                        },
                        "bull_ratio": {
                            "type": "script",
                            "script": ["return sum(a.volume for a in bucket if a.isBull==True) / sum(a.volume for a in bucket)"]
                        }
                    }
                }
            ]
        },
    },
    "indicator": {
        "volume_norm_dev": {
            "type": "moving_normalized_deviation",
            "receive": "tick",
            "field": "volume",
            "window": 20,
        },
        "volume_moving_sum": {
            "type": "moving_sum",
            "receive": "tick",
            "field": "volume",
            "window": 20,
        },
        "volume_moving_sum_moving_average": {
            "type": "moving_average",
            "receive": "volume_moving_sum",
            "window": 20,
        },
        "max_volume": {
            "type": "max",
            "receive": "tick",
            "field": "volume"
        }
    },
    "signal": {
        "enter": {
            "receive": ["volume_norm_dev"],
            "conditions": [
                {
                    "field": "volume_norm_dev",
                    "gte": 4.0,
                }
            ]
        }
    }
}

@pytest.fixture(scope="module")
def test_state():
    state = State()
    State.set_option(output=["signal", "indicator"])
    signals = [a for a in handle_strategy(strategy)]
    signals_len = len([a for a in signals if a.symbol=="057030"])

    """
    state.indicator = {
        "volume_norm_dev": {
            "005930": [...],
            "0057030": [...],
            "075130": [...],
        },
        "volume_moving_sum": {
            "005930": [...],
            ...
        },
        ...
    }
    state.output = {
        "signal.005930": [...],
        "signal.057030": [...],
        "signal.075130": [...],
        "indicator.005930": [...],
        ...
    }
    """
    assert all(a in state["indicator"] for a in ['volume_norm_dev', 'volume_moving_sum', 'volume_moving_sum_moving_average', 'max_volume'])
    assert all(a in state["indicator"]["volume_norm_dev"] for a in ["005930", "057030", "075130"])
    assert all(a in state["output"] for a in ["signal.005930", "signal.057030", "signal.075130", "indicator.005930", "indicator.057030", "indicator.075130"])
    # state 에 기록된 것과 실제 리턴된 결과물이 동일해야한다
    assert signals_len == 84
    assert len(state["output"]["signal.057030"]) == signals_len
    assert len(state["output"]["indicator.057030"]) == 5471 # test_strategy.py 의 test_indicator 에서의 값 5452 보다 19가 큰데 왜냐하면 max_volume 항목이 추가됬기 때문에 첫틱부터 즉시 indicator 가 배출되기 때문이다. moving_fn 을 사용하는 다른 indicator 의 큐가 꽉찰때까지 기다리면서 None을 배출하지 않는다.
    return state


def test_state_json(test_state):
    dumps = State.json()
    loads = json.loads(dumps)
    assert len(loads["output"]["signal.057030"]) == len(test_state["output"]["signal.057030"])
    assert len(loads["output"]["indicator.057030"]) == 5471