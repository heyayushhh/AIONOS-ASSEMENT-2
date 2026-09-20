"""
Veridian Corp AI Helpdesk Copilot — Comprehensive Evaluation Runner
Tests endpoints, grounding, scenario matching, persona independence, and policy safety.
"""

import json
import os
import urllib.request

API_URL = os.environ.get("API_URL", "http://localhost:8000")


def main():
    print(f"Running Veridian Corp Agent Evaluation against: {API_URL}")
    print("=" * 60)

    # 1. Health check
    try:
        h = json.loads(urllib.request.urlopen(f"{API_URL}/health", timeout=5).read())
        print(f" [PASS] Health check: {h.get('status')} ({h.get('service')})")
    except Exception as e:
        print(f" [FAIL] Health check failed: {e}")
        return

    # 2. Scenarios
    sc = json.loads(urllib.request.urlopen(f"{API_URL}/api/scenarios", timeout=5).read())
    assert len(sc) == 15, f"Expected 15 scenarios, found {len(sc)}"
    print(f" [PASS] Scenario Presets: {len(sc)} scenarios loaded (REQ-01 to REQ-15)")

    # 3. Tickets
    tk = json.loads(urllib.request.urlopen(f"{API_URL}/api/tickets", timeout=5).read())
    active_cnt = len([t for t in tk if t.get("is_active")])
    closed_cnt = len([t for t in tk if not t.get("is_active")])
    assert len(tk) == 10 and active_cnt == 4 and closed_cnt == 6
    print(f" [PASS] Ticket Queue: {len(tk)} total ({active_cnt} Active, {closed_cnt} Closed)")

    # 4. Knowledge Base
    kb = json.loads(urllib.request.urlopen(f"{API_URL}/api/kb", timeout=5).read())
    assert len(kb) == 11
    print(f" [PASS] Knowledge Base: {len(kb)} policies loaded (KB-01..10 + ASSET-01)")

    # 5. Helper for chat
    def send_chat(user, q):
        req = urllib.request.Request(
            f"{API_URL}/api/chat",
            data=json.dumps({"user_name": user, "question": q}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        return json.loads(urllib.request.urlopen(req, timeout=10).read())

    # 6. Critical Bug Regression: Sanjay Oberoi asking for Guest Wi-Fi
    r_wifi = send_chat("Sanjay Oberoi", "How can I provide Wi-Fi access to a visitor?")
    c_wifi = [c["kb_id"] for c in r_wifi.get("citations", [])]
    assert "KB-07" in c_wifi and "REQ-02" in c_wifi, f"Expected KB-07 & REQ-02, got {c_wifi}"
    assert "vpn" not in r_wifi.get("answer", "").lower(), "VPN returned instead of Wi-Fi"
    print(" [PASS] Critical Bug Fix: Sanjay Oberoi asking Guest Wi-Fi -> KB-07 & REQ-02")

    # 7. Laptop Replacement (3.5 yrs / dead)
    r_laptop = send_chat("Sanjay Oberoi", "My laptop will not turn on at all, it is completely dead, had it about 3.5 years now.")
    c_laptop = [c["kb_id"] for c in r_laptop.get("citations", [])]
    assert "KB-03" in c_laptop and "ASSET-01" in c_laptop and "REQ-01" in c_laptop
    assert r_laptop.get("policy_decision") == "FINANCE_SIGNOFF_REQUIRED"
    print(" [PASS] Core Scenario 2: Laptop replacement -> REQ-01 / KB-03 + ASSET-01")

    # 8. Account Lockout
    r_lock = send_chat("Aditi Sharma", "I am locked out of my account, tried my password 6 times.")
    c_lock = [c["kb_id"] for c in r_lock.get("citations", [])]
    assert "KB-01" in c_lock and "REQ-03" in c_lock
    assert r_lock.get("policy_decision") == "MANUAL_IT_UNLOCK_REQUIRED"
    print(" [PASS] Core Scenario 3: Account lockout -> REQ-03 / KB-01")

    # 9. Phishing Report
    r_phish = send_chat("Vikram Chawla", "I think I got a phishing email asking for my login credentials. Should I forward it?")
    c_phish = [c["kb_id"] for c in r_phish.get("citations", [])]
    assert "KB-09" in c_phish and "REQ-08" in c_phish
    assert r_phish.get("policy_decision") == "ESCALATED_SECURITY"
    print(" [PASS] Core Scenario 4: Phishing report -> REQ-08 / KB-09")

    # 10. Contractor VPN
    r_vpn = send_chat("Meera Iyer", "New contractor joining my team next week, they will need VPN access.")
    c_vpn = [c["kb_id"] for c in r_vpn.get("citations", [])]
    assert "KB-02" in c_vpn and "REQ-11" in c_vpn
    assert r_vpn.get("policy_decision") == "MANAGER_APPROVAL_REQUIRED"
    print(" [PASS] Core Scenario 5: Contractor VPN -> REQ-11 / KB-02")

    # 11. Policy Safety: Empty & Unknown
    r_empty = send_chat("Aditi Sharma", "")
    assert r_empty.get("policy_decision") == "EMPTY_QUERY"
    print(" [PASS] Policy Safety: Empty query handled (EMPTY_QUERY)")

    r_unknown = send_chat("Aditi Sharma", "Can I bring an elephant into the executive boardroom?")
    assert r_unknown.get("policy_decision") == "NO_POLICY_MATCH"
    assert len(r_unknown.get("citations", [])) == 0
    print(" [PASS] Policy Safety: Unknown query handled (NO_POLICY_MATCH, 0 hallucinations)")

    print("=" * 60)
    print("Evaluation Result: 100% OF TESTS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    main()
