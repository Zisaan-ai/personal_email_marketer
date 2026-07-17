from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

from decision_engine import DecisionEngine
from explainable_ai import ExplainableAI
from workflow_executor import WorkflowExecutor

app = FastAPI(title="Cold Email Deliverability & Visual Builder API")

# Models for Request Bodies
class MetricsDelta(BaseModel):
    old_health: float
    new_health: float
    bounce_rate_delta: float
    reply_rate_delta: float
    complaint_rate_delta: float

class WorkflowEvent(BaseModel):
    workflow_dag: Dict[str, Any]
    current_node_id: str
    event_data: Dict[str, Any]

@app.get("/api/v1/mailboxes/{mailbox_id}/reputation")
async def get_reputation(mailbox_id: str):
    """
    Mock endpoint to fetch provider-specific reputation and AI explanation.
    In a real app, this queries the PostgreSQL database.
    """
    # Hardcoded mock response reflecting the architectural example
    return {
        "mailbox_id": mailbox_id,
        "overall_health": 88,
        "trust_score": 92,
        "risk_score": 12,
        "providers": [
            {
                "provider_name": "Gmail",
                "reputation_score": 91,
                "daily_limit": 155,
                "campaign_percent": 77,
                "warmup_percent": 23,
                "strategy": "Ramp-up"
            },
            {
                "provider_name": "Outlook",
                "reputation_score": 78,
                "daily_limit": 100,
                "campaign_percent": 60,
                "warmup_percent": 40,
                "strategy": "Stabilize"
            }
        ],
        "ai_explanation": {
            "summary": "Health dropped from 92 to 88 because Outlook Bounce Rate increased by 1.2%.",
            "recommendation": "Reduce Outlook campaign volume by 20%. Expected recovery: 3-5 days."
        }
    }

@app.post("/api/v1/decision/explain")
async def generate_explanation(data: MetricsDelta):
    """
    Generates NLG explanation based on metrics changes.
    """
    metrics_delta = {
        "bounce_rate": data.bounce_rate_delta,
        "reply_rate": data.reply_rate_delta,
        "complaint_rate": data.complaint_rate_delta
    }
    
    # Mocking strategy for the example
    strategy_result = {"strategy": "Recovery" if data.new_health < 70 else "Stabilize"}
    
    explanation = ExplainableAI.generate_explanation(
        data.old_health, data.new_health, "Outlook", metrics_delta, strategy_result
    )
    return explanation

@app.post("/api/v1/workflows/execute")
async def execute_workflow(data: WorkflowEvent):
    """
    Traverses the visual workflow DAG based on incoming events.
    """
    result = WorkflowExecutor.process_event(data.workflow_dag, data.current_node_id, data.event_data)
    return result

# To run: uvicorn main:app --reload
