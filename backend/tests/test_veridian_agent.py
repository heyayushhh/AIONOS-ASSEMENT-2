import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.veridian_policy_engine import policy_engine
from app.database import engine, SessionLocal
from app.models import Base, Ticket, EmployeeRequest, KnowledgeArticle
from app.seed import seed_if_empty


# Initialize and seed database for testing
Base.metadata.create_all(bind=engine)
seed_if_empty()

client = TestClient(app)


# --- 1. Health & Scenario Presets ---
def test_health_endpoint():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


def test_scenario_presets_count():
    res = client.get("/api/scenarios")
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 15
    req_ids = [s["req_id"] for s in data]
    assert "REQ-01" in req_ids
    assert "REQ-15" in req_ids


# --- 2. Ticket Queue Verification (Active vs Closed) ---
def test_ticket_queue_ground_truth():
    res = client.get("/api/tickets")
    assert res.status_code == 200
    tickets = res.json()
    assert len(tickets) == 10

    ticket_dict = {t["ticket_id"]: t for t in tickets}

    # Verified Active tickets from PDF
    assert ticket_dict["TK-1043"]["is_active"] is True
    assert ticket_dict["TK-1044"]["is_active"] is True
    assert ticket_dict["TK-1047"]["is_active"] is True
    assert ticket_dict["TK-1048"]["is_active"] is True

    # Verified Closed tickets from PDF
    assert ticket_dict["TK-1042"]["is_active"] is False
    assert ticket_dict["TK-1045"]["is_active"] is False
    assert ticket_dict["TK-1046"]["is_active"] is False
    assert ticket_dict["TK-1049"]["is_active"] is False
    assert ticket_dict["TK-1050"]["is_active"] is False
    assert ticket_dict["TK-1051"]["is_active"] is False


def test_ticket_filter_active_and_closed():
    res_active = client.get("/api/tickets?active_only=true")
    assert res_active.status_code == 200
    active_tickets = res_active.json()
    assert len(active_tickets) == 4
    for t in active_tickets:
        assert t["is_active"] is True

    res_closed = client.get("/api/tickets?active_only=false")
    assert res_closed.status_code == 200
    closed_tickets = res_closed.json()
    assert len(closed_tickets) == 6
    for t in closed_tickets:
        assert t["is_active"] is False


# --- 3. Knowledge Base Endpoints ---
def test_knowledge_base_articles():
    res = client.get("/api/kb")
    assert res.status_code == 200
    kb_list = res.json()
    assert len(kb_list) == 11
    kb_ids = [k["kb_id"] for k in kb_list]
    for i in range(1, 11):
        assert f"KB-{i:02d}" in kb_ids
    assert "ASSET-01" in kb_ids


# --- 4. Policy Tests: Passwords & Lockout (KB-01) ---
def test_password_self_service():
    res = policy_engine.evaluate_request("How do I reset my password?")
    assert "self-service portal" in res["answer"].lower()
    assert res["citations"][0]["kb_id"] == "KB-01"


def test_password_lockout_karan_req03():
    res = policy_engine.evaluate_request("REQ-03: Karan Mehta - I’m locked out of my account, tried my password 6 times.")
    assert "locked" in res["answer"].lower()
    assert "manual" in res["answer"].lower() or "it support" in res["answer"].lower()
    assert res["citations"][0]["kb_id"] == "KB-01"


# --- 5. Policy Tests: VPN & Contractors (KB-02) ---
def test_contractor_vpn_nikhil_req11():
    res = policy_engine.evaluate_request("REQ-11: Nikhil Bansal - New contractor joining my team next week, they’ll need VPN access.")
    assert "contractor" in res["answer"].lower()
    assert "manager approval" in res["answer"].lower()
    assert res["citations"][0]["kb_id"] == "KB-02"


def test_vpn_expiry_sanjay_req05():
    res = policy_engine.evaluate_request("REQ-05: Sanjay Oberoi - My VPN stopped working this morning, says credentials expired.")
    assert "90 days" in res["answer"].lower() or "renew" in res["answer"].lower()
    assert res["citations"][0]["kb_id"] == "KB-02"


# --- 6. Policy Tests: Laptop Replacement & Asset Management (KB-03 & ASSET-01) ---
def test_laptop_replacement_aditi_req01():
    res = policy_engine.evaluate_request("REQ-01: Aditi Sharma - My laptop won’t turn on at all, it’s completely dead, had it about 3.5 years now.")
    assert "finance" in res["answer"].lower() or "asset management" in res["answer"].lower()
    assert any(c["kb_id"] == "KB-03" for c in res["citations"])


def test_laptop_diagnostic_aman_req13():
    res = policy_engine.evaluate_request("REQ-13: Aman Gupta - Laptop screen is flickering on and off, had it 2 years, might just need a fix not a replacement.")
    assert "repair" in res["answer"].lower() or "diagnostic" in res["answer"].lower()
    assert any(c["kb_id"] == "KB-03" for c in res["citations"])


# --- 7. Policy Tests: Non-Catalog Software & Extensions (KB-04) ---
def test_software_install_ritu_req04():
    res = policy_engine.evaluate_request("REQ-04: Ritu Bhatia - Need approval to install a data-analysis tool that’s not in the software catalog.")
    assert "security review" in res["answer"].lower()
    assert "3–5 business days" in res["answer"] or "3-5 business days" in res["answer"]
    assert res["citations"][0]["kb_id"] == "KB-04"


def test_browser_extension_tanya_req14():
    res = policy_engine.evaluate_request("REQ-14: Tanya Chopra - Requesting approval to install a browser extension for productivity tracking.")
    assert "security review" in res["answer"].lower() or "non-catalog" in res["answer"].lower()
    assert res["citations"][0]["kb_id"] == "KB-04"


# --- 8. Policy Tests: Printer Troubleshooting (KB-05) ---
def test_printer_troubleshooting_meera_req06():
    res = policy_engine.evaluate_request("REQ-06: Meera Iyer - Printer on the 3rd floor keeps showing “paper jam” even though there’s no jam.")
    assert "spooler" in res["answer"].lower() or "printer" in res["answer"].lower()
    assert res["citations"][0]["kb_id"] == "KB-05"


# --- 9. Policy Tests: Mailbox Quota (KB-06) ---
def test_mailbox_quota_rohit_req09():
    res = policy_engine.evaluate_request("REQ-09: Rohit Desai - My mailbox is full and I can’t send emails.")
    assert "25gb" in res["answer"].lower() or "50gb" in res["answer"].lower()
    assert "manager approval" in res["answer"].lower()
    assert res["citations"][0]["kb_id"] == "KB-06"


# --- 10. Policy Tests: Guest Wi-Fi (KB-07) ---
def test_guest_wifi_vikram_req02():
    res = policy_engine.evaluate_request("REQ-02: Vikram Chawla - Can I get Wi-Fi access for a guest visiting our office tomorrow?")
    assert "kiosk" in res["answer"].lower() or "24 hours" in res["answer"].lower()
    assert "no it ticket" in res["answer"].lower() or "no approval" in res["answer"].lower() or "front-desk" in res["answer"].lower()
    assert res["citations"][0]["kb_id"] == "KB-07"


# --- 11. Policy Tests: Expense Software (KB-08) ---
def test_expense_software_sneha_req12():
    res = policy_engine.evaluate_request("REQ-12: Sneha Kulkarni - I can’t log into the expense tool, keeps saying invalid credentials.")
    assert "finance" in res["answer"].lower()
    assert res["citations"][0]["kb_id"] == "KB-08"


# --- 12. Policy Tests: Security Incident & Phishing (KB-09) ---
def test_phishing_ananya_req08():
    res = policy_engine.evaluate_request("REQ-08: Ananya Reddy - I think I got a phishing email asking for my login — forwarding it to a few teammates to check.")
    assert "security@veridian-corp.example" in res["answer"].lower()
    assert "not forward" in res["answer"].lower() or "warning" in res["answer"].lower() or "delete" in res["answer"].lower()
    assert res["citations"][0]["kb_id"] == "KB-09"


# --- 13. Policy Tests: WFH Equipment Allowance (KB-10) ---
def test_wfh_equipment_farhan_req07():
    res = policy_engine.evaluate_request("REQ-07: Farhan Ali - I’ve started working from home 4 days a week, how do I get a monitor?")
    assert "3 days" in res["answer"].lower() or "finance" in res["answer"].lower() or "manager" in res["answer"].lower()
    assert res["citations"][0]["kb_id"] == "KB-10"


# --- 14. Policy Tests: Admin Server Access (REQ-10) ---
def test_admin_access_kavya_req10():
    res = policy_engine.evaluate_request("REQ-10: Kavya Pillai - Can someone give me admin access to the finance reporting server? Need it urgently for month-end.")
    assert "justification" in res["answer"].lower() or "security" in res["answer"].lower() or "approval" in res["answer"].lower()


# --- 15. Clarification on Vague Request (REQ-15) ---
def test_vague_request_rahul_req15():
    res = policy_engine.evaluate_request("REQ-15: Rahul Menon - hey can you help, its not working")
    assert res["policy_decision"] == "WAITING_INFO" or "clarification" in res["answer"].lower() or "specific" in res["answer"].lower() or "device" in res["answer"].lower()


# --- 16. Integration Chat Route Test ---
def test_api_chat_flow():
    payload = {"user_name": "Vikram Chawla", "question": "Can I get guest wifi for tomorrow?"}
    res = client.post("/api/chat", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "answer" in data
    assert len(data["citations"]) > 0
    assert any(c["kb_id"] == "KB-07" for c in data["citations"])


# --- 17. CRITICAL BUG FIX: Sanjay Oberoi asking for Visitor Wi-Fi ---
def test_scenario_bug_sanjay_asking_guest_wifi():
    """
    Direct regression test for critical bug:
    Requester Persona: Sanjay Oberoi
    User Message: 'How can I provide Wi-Fi access to a visitor?'
    Must NOT return REQ-05 / expired VPN credentials.
    Must return Guest Wi-Fi (REQ-02 / KB-07).
    """
    res = policy_engine.evaluate_request(
        "How can I provide Wi-Fi access to a visitor?",
        user_name="Sanjay Oberoi"
    )
    # Must NOT be REQ-05 / VPN credentials
    assert "vpn" not in res["answer"].lower()
    assert not any(c["kb_id"] == "REQ-05" for c in res["citations"])

    # Must be Guest Wi-Fi (KB-07 and REQ-02)
    assert "kiosk" in res["answer"].lower() or "24 hours" in res["answer"].lower()
    citation_ids = [c["kb_id"] for c in res["citations"]]
    assert "KB-07" in citation_ids
    assert "REQ-02" in citation_ids
    assert res["policy_decision"] == "SELF_SERVICE_KIOSK"
    assert res["escalated_to"] is None


# --- 18. Verification of 5 Core Demanded Scenarios with Switched Personas ---
def test_all_five_core_scenarios_with_different_personas():
    # 1. Guest Wi-Fi -> REQ-02 / KB-07 (with Sanjay Oberoi)
    r1 = policy_engine.evaluate_request("How can I provide Wi-Fi access to a visitor?", user_name="Sanjay Oberoi")
    c1 = [c["kb_id"] for c in r1["citations"]]
    assert "KB-07" in c1 and "REQ-02" in c1
    assert r1["policy_decision"] == "SELF_SERVICE_KIOSK"

    # 2. Laptop replacement -> REQ-01 / KB-03 + ASSET-01 (with Sanjay Oberoi)
    r2 = policy_engine.evaluate_request("My laptop won't turn on at all, it's completely dead, had it about 3.5 years now.", user_name="Sanjay Oberoi")
    c2 = [c["kb_id"] for c in r2["citations"]]
    assert "KB-03" in c2 and "ASSET-01" in c2 and "REQ-01" in c2
    assert r2["policy_decision"] == "FINANCE_SIGNOFF_REQUIRED"
    assert "Finance" in r2["escalated_to"]

    # 3. Account lockout -> REQ-03 / KB-01 (with Aditi Sharma)
    r3 = policy_engine.evaluate_request("I'm locked out of my account, tried my password 6 times.", user_name="Aditi Sharma")
    c3 = [c["kb_id"] for c in r3["citations"]]
    assert "KB-01" in c3 and "REQ-03" in c3
    assert r3["policy_decision"] == "MANUAL_IT_UNLOCK_REQUIRED"
    assert "IT Support" in r3["escalated_to"]

    # 4. Phishing report -> REQ-08 / KB-09 (with Vikram Chawla)
    r4 = policy_engine.evaluate_request("I think I got a phishing email asking for my login credentials. Should I forward it?", user_name="Vikram Chawla")
    c4 = [c["kb_id"] for c in r4["citations"]]
    assert "KB-09" in c4 and "REQ-08" in c4
    assert r4["policy_decision"] == "ESCALATED_SECURITY"
    assert "security@veridian-corp.example" in r4["escalated_to"]

    # 5. Contractor VPN -> REQ-11 / KB-02 (with Meera Iyer)
    r5 = policy_engine.evaluate_request("New contractor joining my team next week, they'll need VPN access.", user_name="Meera Iyer")
    c5 = [c["kb_id"] for c in r5["citations"]]
    assert "KB-02" in c5 and "REQ-11" in c5
    assert r5["policy_decision"] == "MANAGER_APPROVAL_REQUIRED"
    assert "Manager" in r5["escalated_to"]


# --- 19. Policy Safety: Empty & Unknown Query Handlers ---
def test_empty_query_handling():
    res = policy_engine.evaluate_request("", user_name="Aditi Sharma")
    assert res["policy_decision"] == "EMPTY_QUERY"
    assert "please enter" in res["answer"].lower() or "hello" in res["answer"].lower()


def test_unknown_query_handling():
    res = policy_engine.evaluate_request("Can I bring my exotic reptile to the executive boardroom?", user_name="Aditi Sharma")
    assert res["policy_decision"] == "NO_POLICY_MATCH"
    assert "could not locate an applicable veridian corp it policy" in res["answer"].lower()
    # Ensure agent does not invent policies or tickets
    assert len(res["citations"]) == 0
    assert res["escalated_to"] == "IT Support Helpdesk"


# --- 20. Full API Requester Switching via POST /api/chat ---
def test_api_requester_switching_san_jay_to_aditi():
    # Sanjay asks for Guest Wi-Fi
    p1 = {"user_name": "Sanjay Oberoi", "question": "How can I provide Wi-Fi access to a visitor?"}
    res1 = client.post("/api/chat", json=p1)
    assert res1.status_code == 200
    d1 = res1.json()
    assert any(c["kb_id"] == "KB-07" for c in d1["citations"])
    assert any(c["kb_id"] == "REQ-02" for c in d1["citations"])
    assert "vpn" not in d1["answer"].lower()

    # Aditi asks for Guest Wi-Fi (should also be Guest Wi-Fi, not Aditi's laptop REQ-01)
    p2 = {"user_name": "Aditi Sharma", "question": "How can I provide Wi-Fi access to a visitor?"}
    res2 = client.post("/api/chat", json=p2)
    assert res2.status_code == 200
    d2 = res2.json()
    assert any(c["kb_id"] == "KB-07" for c in d2["citations"])
    assert "laptop" not in d2["answer"].lower()

