import dataclasses
import os
from csv import DictWriter
from typing import List, Any

from practice_interval.interval_lib import Interval

@dataclasses.dataclass
class NewtonRecord:
    function: str
    derivative: str
    primary_interval: Interval
    precision: Any
    roots: str


class CSVWriter:
    def __init__(self, path: str):
        self.path = path
        self.header = [
            "#function",
            "function",
            "derivative",
            "primary_interval",
            "roots"
        ]

    def save(self, journal: List[NewtonRecord]):
        with open(self.path, mode="w") as f:
            f = DictWriter(f, fieldnames=self.header)
            f.writeheader()
            for idx, rec in enumerate(journal):
                print(rec.roots)
                f.writerow({
                    "#function": idx + 1,
                    "function": rec.function,
                    "derivative": rec.derivative,
                    "primary_interval": rec.primary_interval,
                    "roots": rec.roots
                })
