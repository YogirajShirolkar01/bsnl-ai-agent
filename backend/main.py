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
            "department": "Unknown",
            "priority": "Low",
            "assigned_to": "No team",
            "contact_number": "",
        }

    severity_keywords = ["down", "not working", "outage", "fail", "broken", "cut", "dead"]

    rules = [
        {
            "category": "Network",
            "department": "Network",
            "contact_number": "7262059405",
            "keywords": ["internet", "network", "router", "wifi", "broadband", "vpn", "lan", "connectivity"],
            "assigned_to": "Network Team",
        },
        {
            "category": "Fiber",
            "department": "Fiber",
            "contact_number": "9049104430",
            "keywords": ["fiber", "optical", "olt", "ont", "ftth", "optic", "line cut"],
            "assigned_to": "Fiber Team",
        },
        {
            "category": "Mobile",
            "department": "Mobile",
            "contact_number": "9968326836",
            "keywords": ["mobile", "tower", "signal", "sms", "voice call", "cellular", "sim", "call drop"],
            "assigned_to": "Mobile Team",
        },
        {
            "category": "Landline",
            "department": "Landline",
            "contact_number": "",
            "keywords": ["landline", "telephone", "phone line", "pstn", "drop"],
            "assigned_to": "Landline Team",
        },
        {
            "category": "Billing",
            "department": "Billing",
            "contact_number": "",
            "keywords": ["bill", "payment", "recharge", "invoice", "credit", "balance"],
            "assigned_to": "Billing Team",
        },
        {
            "category": "Customer Care",
            "department": "Customer Care",
            "contact_number": "",
            "keywords": ["complaint", "service request", "customer care", "grievance"],
            "assigned_to": "Customer Care Team",
        },
    ]

    for rule in rules:
        if any(keyword in lowered for keyword in rule["keywords"]):
            priority = "High" if any(word in lowered for word in severity_keywords) else "Medium"
            return {
                "message": f"Issue analyzed by Bhashni and routed to {rule['assigned_to']}",
                "description": description,
                "category": rule["category"],
                "department": rule["department"],
                "priority": priority,
                "assigned_to": rule["assigned_to"],
                "contact_number": rule["contact_number"],
            }

    return {
        "message": "Issue not defined or invalid issue",
        "description": description,
        "category": "Invalid",
        "department": "Unknown",
        "priority": "Low",
        "assigned_to": "No team",
        "contact_number": "",
    }


@app.post("/report-issue")
def report_issue(request: IssueRequest):
    return _classify_issue(request.description)
