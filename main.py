from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

API_KEY = "ak_2y086qo4refpcumkrpqbjmnv"

# IMPORTANT:
# Replace with your actual email address
EMAIL = "24f2004647@ds.study.iitm.ac.in"

app = FastAPI()


# Allow browser verification
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Event(BaseModel):
    user: str
    amount: float
    ts: int

class AnalyticsRequest(BaseModel):
    events: List[Event]

from typing import Optional

@app.post("/analytics")
async def analytics(
    data: AnalyticsRequest,
    x_api_key: Optional[str] = Header(
        default=None,
        alias="X-API-Key"
    )
):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )

    total_events = len(data.events)

    unique_users = len(
        {event.user for event in data.events}
    )

    revenue = sum(
        event.amount
        for event in data.events
        if event.amount > 0
    )

    positive_totals = {}

    for event in data.events:
        if event.amount > 0:
            positive_totals[event.user] = (
                positive_totals.get(event.user, 0)
                + event.amount
            )

    top_user = (
        max(positive_totals, key=positive_totals.get)
        if positive_totals
        else ""
    )

    return {
        "email": EMAIL,
        "total_events": total_events,
        "unique_users": unique_users,
        "revenue": revenue,
        "top_user": top_user
    }

@app.get("/")
def root():
    return {"status": "ok"}
