import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
import logging
import pandas as pd
logging.basicConfig(level=logging.INFO)
from yooncloud_core.strategy import handle_data, handle_indicator, handle_signal, handle_strategy


def test_data_timestamp_order():
    data_input = {
        "test_daychart": {
            "type": "koreadaychart",
            "start_date": "2019-02-07",
            "end_date": "2019-02-13",
            "symbols": ["005930", "057030"]
        },
        "test_tickchart": {
            "type": "koreatickchart",
            "date": "2019-02-11",
            "symbols": ["003080"]
        },
    }
    gen = handle_data(data_input)
    data = [a for a in gen]
    # daychart 의 경우 7,8,11,12,13일 총 5일간, 종목은 2개니까 10개의 데이터가 발생했고 tickchart 의 경우 '003080' 종목은 2019-02-11 이날 총 91개 틱데이터가 발생했다. 합산하면 101개.
    assert len(data)==101
    # 시계열 순서로 잘 배출되는지 된다면 첫 6개의 데이터는 7,8,11일 총 3일간의 daychart 여야 한다. 그 이후 91개의 tickchart 가 오고 그 다음 12,13일 총 2일간의 daychart 4개가 다시 와야한다.
    assert all(a._name == "test_daychart" for a in data[:6])
    assert all(a._name == "test_tickchart" for a in data[6:6+91])
    assert all(a._name == "test_daychart" for a in data[-4:])


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
def test_data():
    tickchart = [a for a in handle_data(strategy['data'])]
    assert len([a for a in tickchart if a.symbol=="057030"]) == 5471
    assert len([a for a in tickchart if a.symbol=="075130"]) == 1207
    assert len([a for a in tickchart if a.symbol=="005930"]) == 7489
    yield tickchart


@pytest.fixture(scope="module")
def test_indicator(test_data):
    indicator_coro = handle_indicator(strategy["indicator"])
    next(indicator_coro)
    indicator = [indicator_coro.send(a) for a in test_data]
    assert all(a is None for a in indicator[:19]) # 위의 스키마에 따르면 20번째 틱 부터 indicator 가 발생한다. 19번째 까지는 None

    indicator = [a for a in indicator if a != None]
    assert len([a for a in indicator if a.symbol=="057030"]) == 5452 # tick 갯수에서 -19 된 값
    assert len([a for a in indicator if a.symbol=="075130"]) == 1188
    assert len([a for a in indicator if a.symbol=="005930"]) == 7470
    indicator = [a for a in indicator if a.symbol=="057030"]
    yield indicator


@pytest.fixture(scope="module")
def test_signal(test_indicator):
    signal_coro = handle_signal(strategy["signal"])
    next(signal_coro)
    signal = [signal_coro.send(a) for a in test_indicator]
    assert len(signal) == 5452 # indicator 갯수와 동일
    signal = [a for a in signal if a]
    assert len(signal) == 84
    assert len([a for a in signal if a.enter==False]) == len([a for a in signal if a.enter==True])
    yield signal


def test_draw(test_data, test_indicator, test_signal):
    # 차트 그리기
    tickchart_df = pd.DataFrame(a.model_dump() for a in test_data if a.symbol=="057030")
    indicator_df = pd.DataFrame(a.model_dump() for a in test_indicator if a and a.symbol=="057030")
    signal_df = pd.DataFrame(a.model_dump() for a in test_signal if a.symbol=="057030" and a.enter==True) 

    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03)
    # candle stick
    candlestick = go.Candlestick(x=tickchart_df['timestamp'], open=tickchart_df['open'], high=tickchart_df['high'], low=tickchart_df['low'], close=tickchart_df['close'], yaxis="y1", name="candlestick")
    fig.add_trace(candlestick, row=1, col=1)
    # 보조 차트 - volume moving sum
    volume_moving_sum = go.Line(x=indicator_df["timestamp"], y=indicator_df["volume_moving_sum"], yaxis="y2", name="volume_moving_sum")
    fig.add_trace(volume_moving_sum, row=2, col=1)
    # 보조 차트 - volume moving sum moving average (filled line chart)
    volume_moving_sum_moving_average = go.Scatter(x=indicator_df["timestamp"], y=indicator_df["volume_moving_sum_moving_average"], yaxis="y2", fill="tozeroy", name="volume_moving_sum_moving_average")
    fig.add_trace(volume_moving_sum_moving_average, row=2, col=1)
    # 진입(enter) 시그널
    enter_df = pd.merge(tickchart_df[["timestamp", "low"]], signal_df, on='timestamp', how='inner')
    enter_df["marker"] = enter_df["low"] * enter_df["enter"] - 10
    enter = go.Scatter(x=enter_df["timestamp"], y=enter_df["marker"], yaxis="y1", mode="markers", marker=dict(symbol="arrow-up", color="purple", size=10), name="enter signal")
    fig.add_trace(enter, row=1, col=1)

    fig.update_layout(xaxis_rangeslider_visible=False, yaxis=dict(domain=[0, 0.80]), yaxis2=dict(domain=[0.81, 1]))
    fig.show()


def test_strategy():
    signals = [a for a in handle_strategy(strategy)]
    assert len([a for a in signals if a.symbol=="057030"]) == 84
    assert len([a for a in signals if a.symbol=="005930"]) == 238
    assert len([a for a in signals if a.symbol=="075130"]) == 26