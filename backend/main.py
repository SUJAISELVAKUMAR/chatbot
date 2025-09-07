<<<<<<< HEAD
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data
jobs = [
    {"id": 1, "title": "Software Engineer", "timeslots": ["10:00", "11:00", "14:00"]},
    {"id": 2, "title": "Frontend Developer", "timeslots": ["09:00", "13:00", "15:00"]},
    {"id": 3, "title": "Data Analyst", "timeslots": ["10:30", "12:30", "16:00"]},
]

# Track booked slots
booked_slots = []  # [{ "job_id": 1, "timeslot": "10:00", "candidate": "Alice" }]


=======
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Allow frontend to access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

jobs_data = [
    {"id": 1, "title": "Software Engineer", "timeslots": ["10:00", "11:00", "14:00"]},
    {"id": 2, "title": "Frontend Developer", "timeslots": ["09:00", "13:00", "15:00"]},
    {"id": 3, "title": "Data Analyst", "timeslots": ["10:30", "12:30", "16:00"]}
]

>>>>>>> ea46fc23ccbad6d64fff55771f15da52a696783b
class ScheduleRequest(BaseModel):
    job_id: int
    candidate_name: str
    timeslot: str

<<<<<<< HEAD

@app.get("/jobs")
def get_jobs():
    return jobs


@app.post("/schedule")
def schedule(req: ScheduleRequest):
    # Find job
    job = next((j for j in jobs if j["id"] == req.job_id), None)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Check if timeslot exists
    if req.timeslot not in job["timeslots"]:
        raise HTTPException(status_code=400, detail="Invalid timeslot")

    # Check if already booked
    already = next(
        (b for b in booked_slots if b["job_id"] == req.job_id and b["timeslot"] == req.timeslot),
        None,
    )
    if already:
        raise HTTPException(status_code=409, detail="Timeslot already booked.Please choose another slot.")

    # Book the slot
    booked_slots.append({"job_id": req.job_id, "timeslot": req.timeslot, "candidate": req.candidate_name})

    return {
        "message": f"Interview scheduled for {req.candidate_name} for '{job['title']}' at {req.timeslot}."
    }
=======
@app.get("/jobs")
def get_jobs():
    return jobs_data

@app.post("/schedule")
def schedule_interview(req: ScheduleRequest):
    job = next((j for j in jobs_data if j["id"] == req.job_id), None)
    if not job:
        return {"detail": "Job not found"}
    if req.timeslot not in job["timeslots"]:
        return {"detail": "Timeslot not available"}
    job["timeslots"].remove(req.timeslot)
    return {"message": f"Interview scheduled for {req.candidate_name} for '{job['title']}' at {req.timeslot}."}
>>>>>>> ea46fc23ccbad6d64fff55771f15da52a696783b
