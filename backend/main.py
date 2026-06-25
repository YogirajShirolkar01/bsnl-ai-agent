from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "BSNL AI Agent backend is running"}

@app.post("/report-issue")
def report_issue(data: dict):
    description = data.get("description", "")
    return {
        "message": "Issue received",
        "description": description,
        "category": "Network",
        "priority": "High",
        "assigned_to": "Network Team"
    }
