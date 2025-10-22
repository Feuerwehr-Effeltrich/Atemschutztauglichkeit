from openpyxl import load_workbook
from datetime import datetime
from dataclasses import dataclass
from typing import cast

@dataclass
class Person:
    name: str
    untersuchung: datetime
    unterweisung: datetime
    anlage: datetime
    agtUebung: datetime

def parse(xlsx: str) -> list[Person]:
    wb = load_workbook(xlsx)
    ws = wb.active
    if not ws:
        print("Empty xlsx sheet")
        return []

    people = []

    for row in ws.iter_rows(min_row=5, max_col=12):
        _, status, _, name, vorname, untersuchung, \
            unterweisung, anlage, agtUebung, _, _, _ = (c.value for c in row)

        if status != "Aktiv":
            continue

        people.append(Person(
            f"{vorname} {name}",
            cast(datetime, untersuchung),
            cast(datetime, unterweisung),
            cast(datetime, anlage),
            cast(datetime, agtUebung)
        ))

    return people
