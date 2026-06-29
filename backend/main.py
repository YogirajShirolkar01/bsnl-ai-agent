from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class IssueRequest(BaseModel):
    description: str


@app.get("/")
def home():
    return {"message": "BSNL AI Agent backend is running"}


def _classify_issue(description: str):
    lowered = description.lower()

    if not description.strip():
        return {
            "message": "Please enter a problem description",
            "description": "",
            "category": "Unknown",
            "priority": "Low",
            "assigned_to": "No team"
        }

    severity_keywords = ["down", "not working", "outage", "fail", "broken", "cut", "dead"]

    rules = [
        {
            "category": "Network",
            "keywords": ["internet", "network", "router", "wifi", "broadband", "vpn", "lan", "connectivity"],
            "assigned_to": "Network Team",
        },
        {
            "category": "Fiber",
            "keywords": ["fiber", "optical", "olt", "ont", "ftth", "optic", "line cut"],
            "assigned_to": "Fiber Team",
        },
        {
            "category": "Mobile",
            "keywords": ["mobile", "tower", "signal", "sms", "voice call", "cellular", "sim"],
            "assigned_to": "Mobile Team",
        },
        {
            "category": "Landline",
            "keywords": ["landline", "telephone", "phone line", "pstn"],
            "assigned_to": "Landline Team",
        },
        {
            "category": "Billing",
            "keywords": ["bill", "payment", "recharge", "invoice", "credit", "balance"],
            "assigned_to": "Billing Team",
        },
        {
            "category": "Customer Care",
            "keywords": ["complaint", "service request", "customer care", "grievance"],
            "assigned_to": "Customer Care Team",
        },
    ]

    for rule in rules:
        if any(keyword in lowered for keyword in rule["keywords"]):
            priority = "High" if any(word in lowered for word in severity_keywords) else "Medium"
            return {
                "message": f"Issue received and routed to {rule['assigned_to']}",
                "description": description,
                "category": rule["category"],
                "priority": priority,
                "assigned_to": rule["assigned_to"],
            }

    return {
        "message": "Issue not defined or invalid issue",
        "description": description,
        "category": "Invalid",
        "priority": "Low",
        "assigned_to": "No team",
    }


@app.post("/report-issue")
def report_issue(request: IssueRequest):
    return _classify_issue(request.description)
