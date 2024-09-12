import boto3
import pydash as _
from typing import Union, List
from datetime import date
from pydantic import BaseModel, field_validator
from .base import Base
from .s3 import S3


s3 = boto3.client("s3")

class Input(BaseModel):
    date: date
    symbols: Union[str, List[str]]

    @field_validator("date")
    @classmethod
    def validate_date(cls, v:date):
        # koreatickchart 데이터는 2018-06-01 부터 2019-02-11 까지다
        assert v.toordinal() >= date.fromisoformat("2018-06-01").toordinal(), "date' must be equal or greater than 2018-06-01"
        assert v.toordinal() <= date.fromisoformat("2019-02-12").toordinal(), "date' must be equal or less than 2019-02-11"
        return v


class Koreatickchart(Base):
    schema = {
        "stockcode": "string",
        "timestamp": "datetime",
        "price": "int",
        "volume": "int",
        "isBull": "boolean",
        "sortKey": "int",
    }
    def __init__(
            # daychart 와는 다르게 tickchart 는 columns 옵션을 안받는다
            self,
            date:str,
            symbols="all",
            *args,
            **kwargs,
        ):
        self.input = Input(date=date, symbols=symbols)
        super().__init__(schema=self.schema, symbol_field="stockcode", timeseries_axis_field="timestamp", *args, **kwargs)


    def gen(self):
        yield from S3(bucket="yooncloud-data", key=f"koreatickchart/{self.input.date}.jsonl", sql=self._sql())


    def _sql(self):
        sql = f"SELECT * FROM s3object s "
        if self.input.symbols == "all":
            pass
        else:
            symbols_clause = [f"s.stockcode='{a}'" for a in self.input.symbols]
            symbols_clause = " OR ".join(symbols_clause)
            symbols_clause = f"WHERE {symbols_clause}"
            sql += symbols_clause
        return sql
    