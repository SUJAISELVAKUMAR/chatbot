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

class ScheduleRequest(BaseModel):
    job_id: int
    candidate_name: str
    timeslot: str

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
