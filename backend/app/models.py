from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    role = Column(String, nullable=False, default="employee")  # employee, it_agent, admin, contractor
    department = Column(String, nullable=True)
    employment_type = Column(String, nullable=False, default="full_time")  # full_time, contractor


class KnowledgeArticle(Base):
    __tablename__ = "knowledge_articles"
    id = Column(Integer, primary_key=True, index=True)
    kb_id = Column(String, unique=True, nullable=False, index=True)  # KB-01, KB-02, ..., KB-10, ASSET-01
    title = Column(String, nullable=False)
    category = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    summary = Column(Text, nullable=False)
    requires_approval = Column(Boolean, default=False)
    approval_authority = Column(String, nullable=True)  # IT, Security, Finance, Manager, None
    created_at = Column(DateTime, server_default=func.now())


class EmployeeRequest(Base):
    __tablename__ = "employee_requests"
    id = Column(Integer, primary_key=True, index=True)
    req_id = Column(String, unique=True, nullable=False, index=True)  # REQ-01..REQ-15
    employee_name = Column(String, nullable=False)
    employee_email = Column(String, nullable=False)
    date_opened = Column(String, nullable=False)
    request_text = Column(Text, nullable=False)
    initial_action = Column(String, nullable=False)
    status = Column(String, nullable=False, default="OPEN")  # OPEN, IN_PROGRESS, ESCALATED, RESOLVED, WAITING_INFO
    resolution_guidance = Column(Text, nullable=True)
    escalation_target = Column(String, nullable=True)  # Security, Finance, Manager, IT_L2, None


class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(String, unique=True, nullable=False, index=True)  # TK-1042..TK-1051
    employee_name = Column(String, nullable=False)
    issue_summary = Column(String, nullable=False)
    status = Column(String, nullable=False)  # Status text from PDF e.g. "Resolved (closed)", "Pending Security review (active)"
    is_active = Column(Boolean, nullable=False, default=True)
    category = Column(String, nullable=True)
    priority = Column(String, nullable=False, default="MEDIUM")  # LOW, MEDIUM, HIGH, CRITICAL
    description = Column(Text, nullable=True)
    resolution_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())


class ChatLog(Base):
    __tablename__ = "chat_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    employee_name = Column(String, nullable=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    sources_json = Column(Text, nullable=True)
    tool_calls_json = Column(Text, nullable=True)
    escalated_to = Column(String, nullable=True)
    latency_ms = Column(Integer, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
