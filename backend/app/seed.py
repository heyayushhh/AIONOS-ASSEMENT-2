from app.database import SessionLocal
from app.models import User, Ticket, KnowledgeArticle, EmployeeRequest
from app.data.veridian_kb import VERIDIAN_KNOWLEDGE_BASE
from app.data.veridian_seed_data import VERIDIAN_EMPLOYEES, VERIDIAN_REQUESTS, VERIDIAN_TICKETS


def seed_if_empty():
    db = SessionLocal()
    try:
        # Check if Knowledge Base is already seeded
        if db.query(KnowledgeArticle).count() == 0:
            kb_records = [
                KnowledgeArticle(
                    kb_id=item["kb_id"],
                    title=item["title"],
                    category=item["category"],
                    content=item["content"],
                    summary=item["summary"],
                    requires_approval=item.get("requires_approval", False),
                    approval_authority=item.get("approval_authority"),
                )
                for item in VERIDIAN_KNOWLEDGE_BASE
            ]
            db.add_all(kb_records)

        # Check if Employees are seeded
        if db.query(User).count() == 0:
            user_records = [
                User(
                    name=emp["name"],
                    email=emp["email"],
                    role=emp["role"],
                    employment_type=emp["employment_type"],
                    department=emp["department"],
                )
                for emp in VERIDIAN_EMPLOYEES
            ]
            db.add_all(user_records)

        # Check if Employee Requests (REQ-01..15) are seeded
        if db.query(EmployeeRequest).count() == 0:
            req_records = [
                EmployeeRequest(
                    req_id=req["req_id"],
                    employee_name=req["employee_name"],
                    employee_email=req["employee_email"],
                    date_opened=req["date_opened"],
                    request_text=req["request_text"],
                    initial_action=req["initial_action"],
                    status=req["status"],
                    resolution_guidance=req["resolution_guidance"],
                    escalation_target=req["escalation_target"],
                )
                for req in VERIDIAN_REQUESTS
            ]
            db.add_all(req_records)

        # Check if Ticket Queue (TK-1042..1051) is seeded
        if db.query(Ticket).count() == 0:
            ticket_records = [
                Ticket(
                    ticket_id=t["ticket_id"],
                    employee_name=t["employee_name"],
                    issue_summary=t["issue_summary"],
                    status=t["status"],
                    is_active=t["is_active"],
                    category=t.get("category"),
                    priority=t.get("priority", "MEDIUM"),
                    resolution_notes=t.get("resolution_notes"),
                )
                for t in VERIDIAN_TICKETS
            ]
            db.add_all(ticket_records)

        db.commit()
    finally:
        db.close()
