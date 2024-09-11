from dataclasses import dataclass, field, asdict
from typing import Dict, List, Tuple, Union, Type
from uuid import UUID
from enum import Enum
import json



class Status(Enum):
    PASS = 1
    WARNING = 2
    ERROR = 3


class ResultType(Enum):
    INTEGER = int
    FLOAT = float
    TEXT = str


@dataclass
class ColumnMetadata:
    id: int
    unit: str
    type: ResultType


@dataclass
class Result:
    value: Union[int, float, str]
    status: Status


class ResultTableMeta(type):
    def __new__(cls, name, bases, dct):
        cls_instance = super().__new__(cls, name, bases, dct)
        meta = dct.get('Meta')

        if meta:
            cls_instance.table_name = meta.table_name
            cls_instance.columns_map = {col_name: ColumnMetadata(id=col_id, unit=unit, type=result_type)
                                        for col_name, (col_id, unit, result_type) in meta.Columns.items()}
            cls_instance.rows_map = {row_name: row_id
                                     for row_name, row_id in meta.Rows.items()}
        return cls_instance


class Row:
    def __init__(self, columns_map: Dict[str, ColumnMetadata]):
        self.columns_map = columns_map
        self.data: Dict[str, Result] = {}

    def __getitem__(self, column_name: str) -> Result:
        return self.data[column_name]

    def __setitem__(self, column_name: str, result: Result):
        if column_name not in self.columns_map:
            raise ValueError(f"Column name '{column_name}' not found in columns_map.")
        column_metadata = self.columns_map[column_name]
        if not isinstance(result.value, column_metadata.type.value):
            raise ValueError(f"Value {result.value} for column '{column_name}' is not of type {column_metadata.type.name}")
        self.data[column_name] = result


@dataclass
class BaseResultTable(metaclass=ResultTableMeta):
    results: Dict[str, Row] = field(default_factory=dict)

    def as_dict(self) -> dict:
        results_list = []
        for row_name, row in self.results.items():
            row_id = self.rows_map.get(row_name)
            for column_name, result in row.data.items():
                column_metadata = self.columns_map.get(column_name)
                results_list.append({
                    "column_id": column_metadata.id,
                    "row_id": row_id,
                    "result": result.value,
                    "status": result.status.value
                })

        meta_info = {
            "table_name": self.table_name,
            "columns": {name: {"id": meta.id, "unit": meta.unit, "type": meta.type.name} for name, meta in self.columns_map.items()},
            "rows": self.rows_map
        }
        return {
            "meta": meta_info,
            "results": results_list
        }

    def to_json(self) -> str:
        dict_result = self.as_dict()
        return json.dumps(dict_result, default=str)

    def __getitem__(self, row_name: str) -> Row:
        if row_name not in self.rows_map:
            raise ValueError(f"Row name '{row_name}' not found in rows_map.")
        if row_name not in self.results:
            self.results[row_name] = Row(self.columns_map)
        return self.results[row_name]


# Example of a specific result table with its own metadata
class LatencyResultTable(BaseResultTable):
    class Meta:
        table_name = "latency_percentile_write"
        Columns = {
            "latency": (1, "ms", ResultType.FLOAT),
            "op_rate": (2, "ops", ResultType.INTEGER)
        }
        Rows = {
            "mean": 1,
            "p99": 2
        }


# Client code example
if __name__ == "__main__":
    class LatencyResultTable(BaseResultTable):
        class Meta:
            table_name = "latency_percentile_write"
            Columns = {
                "latency": (1, "ms", ResultType.FLOAT),
                "op_rate": (2, "ops", ResultType.INTEGER)
            }
            Rows = {
                "mean": 1,
                "p99": 2
            }

    result_table = LatencyResultTable()

    result_table["mean"]["latency"] = Result(value=1.1, status=Status.WARNING)
    result_table["mean"]["op_rate"] = Result(value=59988, status=Status.ERROR)
    result_table["p99"]["latency"] = Result(value=2.7, status=Status.PASS)
    result_table["p99"]["op_rate"] = Result(value=59988, status=Status.WARNING)

    from argus.client.sct.client import ArgusSCTClient

    run_id = UUID("24e09748-bba4-47fd-a615-bf7ea2c425eb")
    client = ArgusSCTClient(run_id, auth_token="UO+2GXL9XqSgcVJijWk5WnbPXPit5ot5nfkLAHAr7SaqROfSCWycabpp/wxyY8+I", base_url="http://localhost:5000")
    client.submit_results(result_table)