import json
import time
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.schemas import (
    ChatRequest, ChatResponse, TicketOut, EmployeeRequestOut,
    KnowledgeArticleOut, ScenarioPreset, LogOut
)
from app.database import get_db
from app.models import ChatLog, Ticket, EmployeeRequest, KnowledgeArticle
from app.services.gemini_agent import gemini_agent
from app.services.veridian_policy_engine import policy_engine
from app.metrics import build_metrics

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok", "service": "Veridian Corp IT Internal Service Agent"}


@router.post("/api/chat", response_model=ChatResponse)
@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest, db: Session = Depends(get_db)):
    start = time.time()
    result = gemini_agent.process_chat(req.question, req.user_name)
    latency_ms = int((time.time() - start) * 1000)

    # Persist chat log
    log = ChatLog(
        user_id=req.user_id,
        employee_name=req.user_name,
        question=req.question,
        answer=result.get("answer", ""),
        sources_json=json.dumps(result.get("citations", [])),
        tool_calls_json=json.dumps(result.get("tool_calls", [])),
        escalated_to=result.get("escalated_to"),
        latency_ms=latency_ms,
    )
    db.add(log)
    db.commit()

    return ChatResponse(
        answer=result.get("answer", ""),
        citations=result.get("citations", []),
        policy_decision=result.get("policy_decision"),
        escalated_to=result.get("escalated_to"),
        tool_calls=result.get("tool_calls"),
        latency_ms=latency_ms,
    )


@router.get("/api/tickets", response_model=List[TicketOut])
@router.get("/tickets", response_model=List[TicketOut])
def list_tickets(active_only: Optional[bool] = None, db: Session = Depends(get_db)):
    query = db.query(Ticket)
    if active_only is not None:
        query = query.filter(Ticket.is_active == active_only)
    return query.order_by(Ticket.ticket_id.asc()).all()


@router.get("/api/tickets/{ticket_id}", response_model=TicketOut)
def get_ticket(ticket_id: str, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.ticket_id.ilike(ticket_id.strip())).first()
    if not ticket:
        raise HTTPException(status_code=404, detail=f"Ticket {ticket_id} not found")
    return ticket


@router.get("/api/requests", response_model=List[EmployeeRequestOut])
def list_requests(db: Session = Depends(get_db)):
    return db.query(EmployeeRequest).order_by(EmployeeRequest.req_id.asc()).all()


@router.get("/api/requests/{req_id}", response_model=EmployeeRequestOut)
def get_request(req_id: str, db: Session = Depends(get_db)):
    req = db.query(EmployeeRequest).filter(EmployeeRequest.req_id.ilike(req_id.strip())).first()
    if not req:
        raise HTTPException(status_code=404, detail=f"Request {req_id} not found")
    return req


@router.get("/api/kb", response_model=List[KnowledgeArticleOut])
def list_kb(db: Session = Depends(get_db)):
    return db.query(KnowledgeArticle).order_by(KnowledgeArticle.kb_id.asc()).all()


@router.get("/api/kb/{kb_id}", response_model=KnowledgeArticleOut)
def get_kb(kb_id: str, db: Session = Depends(get_db)):
    kb = db.query(KnowledgeArticle).filter(KnowledgeArticle.kb_id.ilike(kb_id.strip())).first()
    if not kb:
        raise HTTPException(status_code=404, detail=f"Knowledge article {kb_id} not found")
    return kb


@router.get("/api/scenarios", response_model=List[ScenarioPreset])
def list_scenarios():
    scenarios = [
        {
            "req_id": "REQ-01",
            "employee_name": "Aditi Sharma",
            "title": "Aditi: Dead Laptop (~3.5 yrs old)",
            "prompt": "REQ-01: Aditi Sharma - My laptop won't turn on at all, it's completely dead, had it about 3.5 years now.",
            "expected_rule": "Eligible (>3 yrs/failure per KB-03), but requires 2-week notice and Finance sign-off under Asset Management Policy (4-yr refresh cycle).",
            "policy_ref": "KB-03, ASSET-01",
        },
        {
            "req_id": "REQ-02",
            "employee_name": "Vikram Chawla",
            "title": "Vikram: Guest Wi-Fi for Visitor",
            "prompt": "REQ-02: Vikram Chawla - Can I get Wi-Fi access for a guest visiting our office tomorrow?",
            "expected_rule": "Self-service 24-hour pass generated at front-desk kiosk. No IT ticket or approval required.",
            "policy_ref": "KB-07",
        },
        {
            "req_id": "REQ-03",
            "employee_name": "Karan Mehta",
            "title": "Karan: Account Lockout (6 attempts)",
            "prompt": "REQ-03: Karan Mehta - I'm locked out of my account, tried my password 6 times.",
            "expected_rule": "Account locked (>5 attempts per KB-01). IT must unlock manually. No manager approval required.",
            "policy_ref": "KB-01",
        },
        {
            "req_id": "REQ-04",
            "employee_name": "Ritu Bhatia",
            "title": "Ritu: Non-Catalog Software Request",
            "prompt": "REQ-04: Ritu Bhatia - Need approval to install a data-analysis tool that's not in the software catalog.",
            "expected_rule": "Non-catalog software requires IT Security review (3–5 business days SLA per KB-04).",
            "policy_ref": "KB-04",
        },
        {
            "req_id": "REQ-05",
            "employee_name": "Sanjay Oberoi",
            "title": "Sanjay: Expired VPN Credentials",
            "prompt": "REQ-05: Sanjay Oberoi - My VPN stopped working this morning, says credentials expired.",
            "expected_rule": "90-day credential expiration per KB-02. Full-time employees self-renew in employee portal.",
            "policy_ref": "KB-02",
        },
        {
            "req_id": "REQ-06",
            "employee_name": "Meera Iyer",
            "title": "Meera: Printer False Paper Jam",
            "prompt": "REQ-06: Meera Iyer - Printer on the 3rd floor keeps showing 'paper jam' even though there's no jam.",
            "expected_rule": "Check queue & restart print spooler. If unresolved, log ticket with printer asset tag (KB-05).",
            "policy_ref": "KB-05",
        },
        {
            "req_id": "REQ-07",
            "employee_name": "Farhan Ali",
            "title": "Farhan: WFH 4 Days & Monitor Allowance",
            "prompt": "REQ-07: Farhan Ali - I've started working from home 4 days a week, how do I get a monitor?",
            "expected_rule": "Eligible (>3 days remote per KB-10). Requires Manager sign-off + Finance processing before IT shipping.",
            "policy_ref": "KB-10",
        },
        {
            "req_id": "REQ-08",
            "employee_name": "Ananya Reddy",
            "title": "Ananya: Phishing Email & Forwarding",
            "prompt": "REQ-08: Ananya Reddy - I think I got a phishing email asking for my login — forwarding it to a few teammates to check.",
            "expected_rule": "Security Alert (KB-09): Stop forwarding immediately! Report to security@veridian-corp.example.",
            "policy_ref": "KB-09",
        },
        {
            "req_id": "REQ-09",
            "employee_name": "Rohit Desai",
            "title": "Rohit: Full Mailbox Quota",
            "prompt": "REQ-09: Rohit Desai - My mailbox is full and I can't send emails.",
            "expected_rule": "Default 25GB quota (archive old mail). Quota increase requires Manager approval, capped at 50GB (KB-06).",
            "policy_ref": "KB-06",
        },
        {
            "req_id": "REQ-10",
            "employee_name": "Kavya Pillai",
            "title": "Kavya: Urgent Admin Server Access",
            "prompt": "REQ-10: Kavya Pillai - Can someone give me admin access to the finance reporting server? Need it urgently for month-end.",
            "expected_rule": "Admin access requires formal business justification & Security approval (TK-1050 precedent).",
            "policy_ref": "TK-1050, Policy",
        },
        {
            "req_id": "REQ-11",
            "employee_name": "Nikhil Bansal",
            "title": "Nikhil: Contractor VPN Access",
            "prompt": "REQ-11: Nikhil Bansal - New contractor joining my team next week, they'll need VPN access.",
            "expected_rule": "Contractors require Manager approval submitted via Access Request Form (KB-02).",
            "policy_ref": "KB-02",
        },
        {
            "req_id": "REQ-12",
            "employee_name": "Sneha Kulkarni",
            "title": "Sneha: Expense Tool Login Issue",
            "prompt": "REQ-12: Sneha Kulkarni - I can't log into the expense tool, keeps saying invalid credentials.",
            "expected_rule": "Finance grants initial tool access; IT provides technical support for existing accounts (KB-08).",
            "policy_ref": "KB-08",
        },
        {
            "req_id": "REQ-13",
            "employee_name": "Aman Gupta",
            "title": "Aman: Laptop Flickering (2 yrs old)",
            "prompt": "REQ-13: Aman Gupta - Laptop screen is flickering on and off, had it 2 years, might just need a fix not a replacement.",
            "expected_rule": "2 yrs old (under 3-yr refresh cycle per KB-03 / ASSET-01). Route for hardware repair/diagnostic ticket.",
            "policy_ref": "KB-03, ASSET-01",
        },
        {
            "req_id": "REQ-14",
            "employee_name": "Tanya Chopra",
            "title": "Tanya: Browser Extension Request",
            "prompt": "REQ-14: Tanya Chopra - Requesting approval to install a browser extension for productivity tracking.",
            "expected_rule": "Non-catalog extension requires IT Security review (3–5 business days SLA per KB-04).",
            "policy_ref": "KB-04",
        },
        {
            "req_id": "REQ-15",
            "employee_name": "Rahul Menon",
            "title": "Rahul: Vague 'not working' Query",
            "prompt": "REQ-15: Rahul Menon - hey can you help, its not working",
            "expected_rule": "Agent requests specific clarification on device, application, and error symptoms.",
            "policy_ref": "Clarification",
        },
    ]
    return scenarios


@router.get("/api/metrics")
@router.get("/metrics")
def metrics(db: Session = Depends(get_db)):
    return build_metrics(db)


@router.get("/api/audit/{log_id}", response_model=LogOut)
def audit_log(log_id: int, db: Session = Depends(get_db)):
    log = db.query(ChatLog).filter(ChatLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    return log
