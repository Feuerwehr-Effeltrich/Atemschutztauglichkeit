from download import download
from parse import parse, Person
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import schedule

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

__xlsx = "Tauglichkeit.xlsx"
finding: list[Person]

@app.post("/update")
def update():
    global finding
    download(__xlsx)
    finding = parse(__xlsx)
update()
schedule.every().day.at("02:00").do(update)

@app.get("/api.json")
def api():
    return finding

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
