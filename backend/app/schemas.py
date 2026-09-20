from typing import List, Optional, Any
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class Citation(BaseModel):
    kb_id: Optional[str] = None
    title: str
    chunk_id: Optional[str] = None


class ChatRequest(BaseModel):
    user_id: Optional[int] = 1
    user_name: Optional[str] = None
    question: str


class ChatResponse(BaseModel):
    answer: str
    citations: List[Citation] = []
    policy_decision: Optional[str] = None
    escalated_to: Optional[str] = None
    tool_calls: Optional[List[Any]] = None
    latency_ms: Optional[int] = None


class TicketOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    ticket_id: str
    employee_name: str
    issue_summary: str
    status: str
    is_active: bool
    category: Optional[str] = None
    priority: str
    resolution_notes: Optional[str] = None
    created_at: Optional[datetime] = None


class EmployeeRequestOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    req_id: str
    employee_name: str
    employee_email: str
    date_opened: str
    request_text: str
    initial_action: str
    status: str
    resolution_guidance: Optional[str] = None
    escalation_target: Optional[str] = None


class KnowledgeArticleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    kb_id: str
    title: str
    category: str
    content: str
    summary: str
    requires_approval: bool
    approval_authority: Optional[str] = None


class ScenarioPreset(BaseModel):
    req_id: str
    employee_name: str
    title: str
    prompt: str
    expected_rule: str
    policy_ref: str


class LogOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: Optional[int]
    question: str
    answer: str
    sources_json: Optional[str]
    tool_calls_json: Optional[str]
    latency_ms: Optional[int]
    created_at: Optional[datetime]
