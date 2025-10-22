from download import download
from parse import parse, Person, ParsedData
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import schedule
from datetime import datetime, timedelta
from dataclasses import dataclass
import copy
from typing import Optional

@dataclass
class PersonStatus:
    name: str
    vorname: str
    untersuchung: Optional[datetime]
    untersuchung_status: str
    unterweisung: Optional[datetime]
    unterweisung_status: str
    anlage: Optional[datetime]
    anlage_status: str
    agtUebung: Optional[datetime]
    agtUebung_status: str
    overall_status: str


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

__xlsx = "Tauglichkeit.xlsx"
finding: list[Person]
data_age: Optional[str] = None
last_update_timestamp: Optional[datetime] = None

@app.post("/update")
def update():
    global finding, data_age, last_update_timestamp
    download(__xlsx)
    parsed_data = parse(__xlsx)
    finding = parsed_data.people
    data_age = parsed_data.data_age
    last_update_timestamp = datetime.now()
update()
schedule.every().day.at("02:00").do(update)

def format_timedelta(td: timedelta) -> str:
    seconds = int(td.total_seconds())
    if seconds < 60:
        return f"{seconds} Sekunden"
    minutes = seconds // 60
    if minutes < 60:
        return f"{minutes} Minuten"
    hours = minutes // 60
    if hours < 24:
        return f"{hours} Stunden"
    days = hours // 24
    return f"{days} Tage"

def get_processed_data() -> list[PersonStatus]:
    people = copy.deepcopy(finding)

    # Add 15 days to each date
    for person in people:
        if person.untersuchung: person.untersuchung += timedelta(days=15)
        if person.unterweisung: person.unterweisung += timedelta(days=15)
        if person.anlage: person.anlage += timedelta(days=15)
        if person.agtUebung: person.agtUebung += timedelta(days=15)

    people_status: list[PersonStatus] = []
    today = datetime.now()

    for p in people:
        statuses = []

        # Untersuchung status
        if p.untersuchung:
            if p.untersuchung.year > today.year or (p.untersuchung.year == today.year and p.untersuchung.month >= today.month):
                untersuchung_status = "green"
            elif p.untersuchung.year == today.year and today.month - p.untersuchung.month <= 1:
                untersuchung_status = "yellow"
            else:
                untersuchung_status = "red"
        else:
            untersuchung_status = "red" # Missing date is critical
        statuses.append(untersuchung_status)

        # Unterweisung status
        if p.unterweisung:
            if p.unterweisung.year > today.year:
                unterweisung_status = "green"
            elif today.year == p.unterweisung.year:
                unterweisung_status = "yellow"
            else:
                unterweisung_status = "red"
        else:
            unterweisung_status = "red" # Missing date is critical
        statuses.append(unterweisung_status)

        # Belastungsübung (anlage) status
        if p.anlage:
            if p.anlage.year >= today.year:
                anlage_status = "green"
            elif today.year - p.anlage.year == 1:
                anlage_status = "yellow"
            else:
                anlage_status = "red"
        else:
            anlage_status = "red" # Missing date is critical
        statuses.append(anlage_status)

        # Übung/Einsatz (agtUebung) status
        if p.agtUebung:
            if p.agtUebung >= today:
                agtUebung_status = "green"
            elif (p.agtUebung + timedelta(days=180)).year >= today.year:
                agtUebung_status = "yellow"
            else:
                agtUebung_status = "red"
        else:
            agtUebung_status = "red" # Missing date is critical
        statuses.append(agtUebung_status)

        if "red" in statuses:
            overall_status = "red"
        elif "yellow" in statuses:
            overall_status = "yellow"
        else:
            overall_status = "green"

        people_status.append(PersonStatus(
            p.name,
            p.vorname,
            p.untersuchung,
            untersuchung_status,
            p.unterweisung,
            unterweisung_status,
            p.anlage,
            anlage_status,
            p.agtUebung,
            agtUebung_status,
            overall_status
        ))

    status_order = {"green": 0, "yellow": 1, "red": 2}
    people_status.sort(key=lambda x: (status_order[x.overall_status], x.name))

    return people_status

@app.get("/api.json")
def api():
    return {"people": get_processed_data(), "data_age": data_age, "last_update_timestamp": last_update_timestamp}

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    formatted_last_update = None
    if last_update_timestamp:
        time_diff = datetime.now() - last_update_timestamp
        formatted_last_update = f"zuletzt aktualisiert vor {format_timedelta(time_diff)}"

    return templates.TemplateResponse("index.html", {"request": request, "people": get_processed_data(), "data_age": data_age, "last_update_timestamp": formatted_last_update})
