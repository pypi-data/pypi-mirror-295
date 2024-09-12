import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import time
import logging
logging.basicConfig(level=logging.INFO)
from datetime import date, datetime
from yooncloud_core.data import S3, Athena, Koreadaychart, Koreatickchart


def test_s3():
    daychart = [a for a in S3(bucket="yooncloud-data", key="koreadaychart/timestamp=2024-01-02/2024-01-02.csv.gz")]
    assert len(daychart) == 2786
    assert daychart[0]["name"] == "삼성전자" and daychart[0]["volume"] == "17142847"
    assert daychart[-1]["name"]=="디에스앤엘" and daychart[-1]["volume"] == "12658080"


def test_athena():
    sql = "select * from koreadaychart where timestamp >= '2024-01-02' and timestamp <= '2024-01-05' ORDER BY timestamp"
    daychart = [a for a in Athena(sql=sql)]
    assert len(daychart)==11141

    daychart = [a for a in daychart if a["name"]=="삼성전자"]
    assert daychart[0]["date"] == "2024-01-02" and daychart[0]["volume"] == "17142847"
    assert daychart[1]["date"] == "2024-01-03" and daychart[1]["volume"] == "21753644"
    assert daychart[2]["date"] == "2024-01-04" and daychart[2]["volume"] == "15324439"
    assert daychart[3]["date"] == "2024-01-05" and daychart[3]["volume"] == "11304316"


def test_koreadaychart():
    start = "2024-01-02"
    end = "2024-01-05"
    daychart = [a for a in Koreadaychart(start_date=start, end_date=end)]
    assert len(daychart)==11141
    
    daychart = [a for a in daychart if a.name=="SK하이닉스"]
    tzinfo = daychart[0].timestamp.tzinfo
    assert daychart[0].date == datetime(2024, 1, 2, tzinfo=tzinfo) and daychart[0].volume == 2147458
    assert daychart[1].date == datetime(2024, 1, 3, tzinfo=tzinfo) and daychart[1].volume == 3257820
    assert daychart[2].date == datetime(2024, 1, 4, tzinfo=tzinfo) and daychart[2].volume == 2661970
    assert daychart[3].date == datetime(2024, 1, 5, tzinfo=tzinfo) and daychart[3].volume == 1846781


def test_koreatickchart():
    date = "2019-02-11"
    start_time = time.time()
    tickchart = [a for a in Koreatickchart(date=date)]
    # 대충 5~6분정도 걸림
    logging.info(f"it tooks {round(time.time() - start_time)} secs")
    assert len(tickchart)==5924192
    

def test_koreadaychart_symbols_columns():
    kwargs = {
        "start_date": "2024-01-02",
        "end_date": "2024-01-05",
        "symbols": ["005930", "057030"],
        "columns": ["stockcode", "name", "date", "volume"]
    }
    daychart = [a for a in Koreadaychart(**kwargs)]
    # check 'symbols' option
    assert len(daychart)==8
    # check 'columns' option
    assert not hasattr(daychart[0], "open") and not hasattr(daychart[0], "close")
 

def test_koreatickchart_symbols_columns():
    date = "2019-02-11"
    start_time = time.time()
    tickchart = [a for a in Koreatickchart(date=date, symbols=["005930", "057030"])]
    # 일부만 긁어오는거라 별로 안걸림
    logging.info(f"it tooks {round(time.time() - start_time)} secs")
    # check 'symbols' option
    assert len(tickchart)==82784


def test_data_transform():
    my_filter = {
        "type": "filter",
        "script": [
            "return row.stockcode=='005930'",
        ]
    }
    my_map = {
        "type": "map",
        "script": [
            "row.홀짝 = '짝' if row.volume % 2 == 0 else '홀'",
            "return row",
        ]
    }
    my_tap = {
        "type": "tap",
        "script": [
            "rows.append({'message': 'This is last tick!'})",
            "return rows",
        ]
    }  
    transforms = [
        my_filter,
        my_map,
        my_tap,
    ]
    daychart = [a for a in Koreadaychart(start_date="2024-01-02", end_date="2024-01-05", transforms=transforms)]

    assert all(a.stockcode=='005930' for a in daychart[:-1])
    assert all("홀짝" in a.model_dump() for a in daychart[:-1])
    assert list(daychart[-1].keys()) == ["message"]


def test_koreatickchart_timecut():
    transforms = [
        {
            "type": "timecut",
            "interval": "30 min",
            "aggs": {
                "min_volume": {
                    "type": "min",
                    "field": "volume"
                },
                "max_volume": {
                    "type": "max",
                    "field": "volume"
                },
                "sum_volume": {
                    "type": "sum",
                    "field": "volume"
                },
                "my_bar": {
                    "type": "bar",
                    "price_field": "price",
                    "volume_field": "volume",
                },
            }
        }
    ]
    daychart = [a for a in Koreadaychart(start_date="2019-02-11", end_date="2019-02-11", symbols=["057030"])]
    bars = [a for a in Koreatickchart(date="2019-02-11", transforms=transforms, symbols=["057030"])]

    assert len(bars)==13 # 09시 부터 15:20 까지 30분 간격으로 13번 만들어지는 bar
    assert sum(a.volume for a in bars) != daychart[0].volume # tickchart 에는 장전 시간외 거래틱이 포함되지 않기 때문에 일봉 데이터와 값이 다르다
    assert max(a.high for a in bars) == daychart[0].high
    assert min(a.low for a in bars) == daychart[0].low


def test_koreadaychart_timecut():
    transforms = [
        {
            "type": "timecut",
            "interval": "7days",
            "aggs": {
                "open": {
                    "type": "script",
                    "script": ["return bucket[0].open"]
                },
                "high": {
                    "type": "max",
                    "field": "high"
                },
                "low": {
                    "type": "min",
                    "field": "low"
                },
                "close": {
                    "type": "script",
                    "script": ["return bucket[-1].close"]
                },
                "volume": {
                    "type": "sum",
                    "field": "volume"
                },
            }
        }
    ]
    daychart = [a for a in Koreadaychart(start_date="2024-01-02" , end_date="2024-03-31", symbols=["005930"])]
    weekchart = [a for a in Koreadaychart(start_date="2024-01-02" , transforms=transforms, end_date="2024-03-31", symbols=["005930"])]

    assert len(weekchart)==13
    assert max(a.high for a in daychart[:4]) == weekchart[0].high # 첫주: 2024-01-02 ~ 2024-01-05 (4일간)
    assert min(a.low for a in daychart[:4]) == weekchart[0].low
    assert daychart[0].open == weekchart[0].open
    assert daychart[-1].close == weekchart[-1].close
    assert sum(a.volume for a in daychart[:4]) == weekchart[0].volume