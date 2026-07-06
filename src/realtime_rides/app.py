from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from realtime_rides.eventhub_client import publish_ride_event
from realtime_rides.ride_generator import generate_ride_event
from realtime_rides.settings import load_eventhub_settings

app = FastAPI(title="Realtime Rides Event Simulator")
templates = Jinja2Templates(directory="templates")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/book")
def book_ride(request: Request):
    ride_event = generate_ride_event()
    publish_ride_event(ride_event, load_eventhub_settings())
    return templates.TemplateResponse(
        "confirmation.html",
        {"request": request, "confirmation_number": ride_event["confirmation_number"]},
    )

