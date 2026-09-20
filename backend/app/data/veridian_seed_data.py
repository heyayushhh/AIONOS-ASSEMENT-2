"""
Veridian Corp Official Seed Dataset (REQ-01 to REQ-15, Ticket Queue TK-1042 to TK-1051, Users)
Grounded strictly in Assessment 2 PDF specification for the week of September 21–25, 2026.
"""

VERIDIAN_EMPLOYEES = [
    {"name": "Aditi Sharma", "email": "aditi.sharma@veridian-corp.example", "role": "employee", "employment_type": "full_time", "department": "Engineering"},
    {"name": "Vikram Chawla", "email": "vikram.chawla@veridian-corp.example", "role": "employee", "employment_type": "full_time", "department": "Sales"},
    {"name": "Karan Mehta", "email": "karan.mehta@veridian-corp.example", "role": "employee", "employment_type": "full_time", "department": "Marketing"},
    {"name": "Ritu Bhatia", "email": "ritu.bhatia@veridian-corp.example", "role": "employee", "employment_type": "full_time", "department": "Data Analytics"},
    {"name": "Sanjay Oberoi", "email": "sanjay.oberoi@veridian-corp.example", "role": "employee", "employment_type": "full_time", "department": "Operations"},
    {"name": "Meera Iyer", "email": "meera.iyer@veridian-corp.example", "role": "employee", "employment_type": "full_time", "department": "Human Resources"},
    {"name": "Farhan Ali", "email": "farhan.ali@veridian-corp.example", "role": "employee", "employment_type": "full_time", "department": "Design"},
    {"name": "Ananya Reddy", "email": "ananya.reddy@veridian-corp.example", "role": "employee", "employment_type": "full_time", "department": "Product"},
    {"name": "Rohit Desai", "email": "rohit.desai@veridian-corp.example", "role": "employee", "employment_type": "full_time", "department": "Legal"},
    {"name": "Kavya Pillai", "email": "kavya.pillai@veridian-corp.example", "role": "employee", "employment_type": "full_time", "department": "Finance"},
    {"name": "Nikhil Bansal", "email": "nikhil.bansal@veridian-corp.example", "role": "employee", "employment_type": "full_time", "department": "Engineering"},
    {"name": "Sneha Kulkarni", "email": "sneha.kulkarni@veridian-corp.example", "role": "employee", "employment_type": "full_time", "department": "Accounting"},
    {"name": "Aman Gupta", "email": "aman.gupta@veridian-corp.example", "role": "employee", "employment_type": "full_time", "department": "Customer Support"},
    {"name": "Tanya Chopra", "email": "tanya.chopra@veridian-corp.example", "role": "employee", "employment_type": "full_time", "department": "Growth"},
    {"name": "Rahul Menon", "email": "rahul.menon@veridian-corp.example", "role": "employee", "employment_type": "full_time", "department": "General"},
    {"name": "IT Helpdesk Admin", "email": "helpdesk-admin@veridian-corp.example", "role": "admin", "employment_type": "full_time", "department": "IT Operations"},
]

VERIDIAN_REQUESTS = [
    {
        "req_id": "REQ-01",
        "employee_name": "Aditi Sharma",
        "employee_email": "aditi.sharma@veridian-corp.example",
        "date_opened": "Mon 21 Sep",
        "request_text": "My laptop won’t turn on at all, it’s completely dead, had it about 3.5 years now.",
        "initial_action": "Not started",
        "status": "OPEN",
        "resolution_guidance": (
            "Laptop is completely dead (verified hardware failure) and 3.5 years old. "
            "Under KB-03, it is eligible for replacement (>3 years / failure), requiring at least 2 weeks advance notice. "
            "Under Asset Management Policy (4-year refresh cycle), replacement at 3.5 years is early and requires Finance sign-off in addition to IT approval."
        ),
        "escalation_target": "Finance & IT",
    },
    {
        "req_id": "REQ-02",
        "employee_name": "Vikram Chawla",
        "employee_email": "vikram.chawla@veridian-corp.example",
        "date_opened": "Mon 21 Sep",
        "request_text": "Can I get Wi-Fi access for a guest visiting our office tomorrow?",
        "initial_action": "Not started",
        "status": "RESOLVED",
        "resolution_guidance": (
            "Under KB-07, guest Wi-Fi credentials are valid for 24 hours and can be generated directly by any employee "
            "at the front-desk kiosk. No IT ticket or administrative approval is required."
        ),
        "escalation_target": "None",
    },
    {
        "req_id": "REQ-03",
        "employee_name": "Karan Mehta",
        "employee_email": "karan.mehta@veridian-corp.example",
        "date_opened": "Mon 21 Sep",
        "request_text": "I’m locked out of my account, tried my password 6 times.",
        "initial_action": "In progress — reset queued",
        "status": "IN_PROGRESS",
        "resolution_guidance": (
            "Under KB-01, employees can normally reset passwords via self-service portal. However, after 5 failed attempts "
            "(Karan attempted 6 times), the account is locked out and IT must unlock it manually. No managerial approval is required."
        ),
        "escalation_target": "IT Support L1/L2",
    },
    {
        "req_id": "REQ-04",
        "employee_name": "Ritu Bhatia",
        "employee_email": "ritu.bhatia@veridian-corp.example",
        "date_opened": "Tue 22 Sep",
        "request_text": "Need approval to install a data-analysis tool that’s not in the software catalog.",
        "initial_action": "Waiting on Security review",
        "status": "IN_PROGRESS",
        "resolution_guidance": (
            "Under KB-04, non-catalog software cannot be self-installed and strictly requires an IT Security review, "
            "which takes 3–5 business days. The request has been routed to IT Security for assessment."
        ),
        "escalation_target": "IT Security",
    },
    {
        "req_id": "REQ-05",
        "employee_name": "Sanjay Oberoi",
        "employee_email": "sanjay.oberoi@veridian-corp.example",
        "date_opened": "Tue 22 Sep",
        "request_text": "My VPN stopped working this morning, says credentials expired.",
        "initial_action": "Not started",
        "status": "OPEN",
        "resolution_guidance": (
            "Under KB-02, VPN credentials for full-time employees expire every 90 days and must be renewed by the employee "
            "via the self-service access portal. Full-time employees do not require manager re-approval for renewal."
        ),
        "escalation_target": "None",
    },
    {
        "req_id": "REQ-06",
        "employee_name": "Meera Iyer",
        "employee_email": "meera.iyer@veridian-corp.example",
        "date_opened": "Tue 22 Sep",
        "request_text": "Printer on the 3rd floor keeps showing “paper jam” even though there’s no jam.",
        "initial_action": "Investigating — technician assigned",
        "status": "IN_PROGRESS",
        "resolution_guidance": (
            "Under KB-05, troubleshooting steps are: 1) Check printer queue, 2) Restart the print spooler service. "
            "Since the false jam persists, an on-site technician is assigned and an IT ticket logged with the printer asset tag."
        ),
        "escalation_target": "IT Field Support",
    },
    {
        "req_id": "REQ-07",
        "employee_name": "Farhan Ali",
        "employee_email": "farhan.ali@veridian-corp.example",
        "date_opened": "Wed 23 Sep",
        "request_text": "I’ve started working from home 4 days a week, how do I get a monitor?",
        "initial_action": "Not started",
        "status": "OPEN",
        "resolution_guidance": (
            "Under KB-10, working remotely > 3 days/week qualifies Farhan (4 days) for a one-time home office equipment allowance (chair, monitor). "
            "Process requires Manager sign-off followed by Finance processing. IT only coordinates shipping once approved."
        ),
        "escalation_target": "Manager & Finance",
    },
    {
        "req_id": "REQ-08",
        "employee_name": "Ananya Reddy",
        "employee_email": "ananya.reddy@veridian-corp.example",
        "date_opened": "Wed 23 Sep",
        "request_text": "I think I got a phishing email asking for my login — forwarding it to a few teammates to check.",
        "initial_action": "Escalated to Security (auto-flagged)",
        "status": "IN_PROGRESS",
        "resolution_guidance": (
            "CRITICAL SECURITY ALERT (KB-09): Any suspected phishing email must be reported immediately to security@veridian-corp.example "
            "and MUST NOT be forwarded to other employees. Teammates must be advised to delete the forwarded copy immediately."
        ),
        "escalation_target": "IT Security (Incident Response)",
    },
    {
        "req_id": "REQ-09",
        "employee_name": "Rohit Desai",
        "employee_email": "rohit.desai@veridian-corp.example",
        "date_opened": "Wed 23 Sep",
        "request_text": "My mailbox is full and I can’t send emails.",
        "initial_action": "Not started",
        "status": "OPEN",
        "resolution_guidance": (
            "Under KB-06, default quota is 25GB. Rohit should first archive old emails. If an increase is required, "
            "it requires Manager approval and is strictly capped at 50GB."
        ),
        "escalation_target": "Manager (if quota increase needed)",
    },
    {
        "req_id": "REQ-10",
        "employee_name": "Kavya Pillai",
        "employee_email": "kavya.pillai@veridian-corp.example",
        "date_opened": "Wed 23 Sep",
        "request_text": "Can someone give me admin access to the finance reporting server? Need it urgently for month-end.",
        "initial_action": "Not started",
        "status": "OPEN",
        "resolution_guidance": (
            "Administrative server access requires formal business justification, Security review, and Manager sign-off. "
            "(Precedent: TK-1050 was rejected when no business justification was provided). IT cannot grant ad-hoc admin access."
        ),
        "escalation_target": "IT Security & Department Manager",
    },
    {
        "req_id": "REQ-11",
        "employee_name": "Nikhil Bansal",
        "employee_email": "nikhil.bansal@veridian-corp.example",
        "date_opened": "Thu 24 Sep",
        "request_text": "New contractor joining my team next week, they’ll need VPN access.",
        "initial_action": "Not started",
        "status": "OPEN",
        "resolution_guidance": (
            "Under KB-02, unlike full-time employees who receive VPN automatically, contractors require manager approval "
            "submitted via the official access request form. Credentials will be valid for 90 days."
        ),
        "escalation_target": "Manager Approval Form",
    },
    {
        "req_id": "REQ-12",
        "employee_name": "Sneha Kulkarni",
        "employee_email": "sneha.kulkarni@veridian-corp.example",
        "date_opened": "Thu 24 Sep",
        "request_text": "I can’t log into the expense tool, keeps saying invalid credentials.",
        "initial_action": "Waiting on employee response (asked for a screenshot, no reply yet)",
        "status": "IN_PROGRESS",
        "resolution_guidance": (
            "Under KB-08, initial access/provisioning is granted by Finance. IT can only troubleshoot login/technical issues "
            "once an account exists. IT is waiting on employee screenshot/details to verify account provisioning."
        ),
        "escalation_target": "Finance (if unprovisioned) / IT L1 (if login bug)",
    },
    {
        "req_id": "REQ-13",
        "employee_name": "Aman Gupta",
        "employee_email": "aman.gupta@veridian-corp.example",
        "date_opened": "Thu 24 Sep",
        "request_text": "Laptop screen is flickering on and off, had it 2 years, might just need a fix not a replacement.",
        "initial_action": "Not started",
        "status": "OPEN",
        "resolution_guidance": (
            "Under KB-03 and Asset Management Policy, a 2-year-old laptop has not reached the 3-year IT replacement threshold or 4-year refresh cycle. "
            "First course of action is an IT hardware diagnostic and repair ticket. Replacement is only considered for verified irreparable failure and requires Finance sign-off."
        ),
        "escalation_target": "IT Hardware Support",
    },
    {
        "req_id": "REQ-14",
        "employee_name": "Tanya Chopra",
        "employee_email": "tanya.chopra@veridian-corp.example",
        "date_opened": "Fri 25 Sep",
        "request_text": "Requesting approval to install a browser extension for productivity tracking.",
        "initial_action": "Not started",
        "status": "OPEN",
        "resolution_guidance": (
            "Under KB-04, browser extensions not in the approved software catalog are classified as non-catalog software "
            "and require IT Security review (3–5 business days SLA) before installation."
        ),
        "escalation_target": "IT Security",
    },
    {
        "req_id": "REQ-15",
        "employee_name": "Rahul Menon",
        "employee_email": "rahul.menon@veridian-corp.example",
        "date_opened": "Fri 25 Sep",
        "request_text": "hey can you help, its not working",
        "initial_action": "Not started",
        "status": "WAITING_INFO",
        "resolution_guidance": (
            "Vague request with no specifics. Agent must acknowledge and prompt Rahul for specific details: "
            "device/hardware type, application name, exact error message, and recent actions."
        ),
        "escalation_target": "None (Awaiting Requester Details)",
    },
]

VERIDIAN_TICKETS = [
    {
        "ticket_id": "TK-1042",
        "employee_name": "R. Verma",
        "issue_summary": "VPN credential expired",
        "status": "Resolved (closed)",
        "is_active": False,
        "category": "VPN",
        "priority": "LOW",
        "resolution_notes": "User guided to self-service portal to renew 90-day credentials (KB-02). Ticket closed.",
    },
    {
        "ticket_id": "TK-1043",
        "employee_name": "S. Iyer",
        "issue_summary": "Laptop replacement (3.2 yrs old)",
        "status": "Approved — pending fulfillment (active)",
        "is_active": True,
        "category": "Hardware",
        "priority": "MEDIUM",
        "resolution_notes": "Eligible (>3 years per KB-03). Finance sign-off obtained per Asset Management Policy. Awaiting hardware shipment.",
    },
    {
        "ticket_id": "TK-1044",
        "employee_name": "A. Khan",
        "issue_summary": "Non-catalog software request",
        "status": "Pending Security review (active)",
        "is_active": True,
        "category": "Software",
        "priority": "MEDIUM",
        "resolution_notes": "Submitted for IT Security review under KB-04 (3-5 business days SLA).",
    },
    {
        "ticket_id": "TK-1045",
        "employee_name": "P. Joshi",
        "issue_summary": "Mailbox quota increase",
        "status": "Approved at 35GB (closed)",
        "is_active": False,
        "category": "Email",
        "priority": "LOW",
        "resolution_notes": "Manager approval received; quota increased to 35GB (within 50GB cap per KB-06). Ticket closed.",
    },
    {
        "ticket_id": "TK-1046",
        "employee_name": "M. Das",
        "issue_summary": "Printer paper jam, floor 2",
        "status": "Resolved (closed)",
        "is_active": False,
        "category": "Printer",
        "priority": "LOW",
        "resolution_notes": "Spooler restarted and physical jam cleared on floor 2 printer (KB-05). Ticket closed.",
    },
    {
        "ticket_id": "TK-1047",
        "employee_name": "K. Singh",
        "issue_summary": "Home office equipment request",
        "status": "Pending Finance (active)",
        "is_active": True,
        "category": "Equipment",
        "priority": "MEDIUM",
        "resolution_notes": "Manager approved >3 days remote eligibility. Currently pending Finance processing under KB-10.",
    },
    {
        "ticket_id": "TK-1048",
        "employee_name": "T. Rao",
        "issue_summary": "Phishing email reported",
        "status": "Escalated to Security — under investigation (active)",
        "is_active": True,
        "category": "Security",
        "priority": "CRITICAL",
        "resolution_notes": "Reported to security@veridian-corp.example per KB-09. Security team analyzing email headers and blocking malicious sender.",
    },
    {
        "ticket_id": "TK-1049",
        "employee_name": "V. Nambiar",
        "issue_summary": "Password reset",
        "status": "Resolved (closed)",
        "is_active": False,
        "category": "Access",
        "priority": "LOW",
        "resolution_notes": "User assisted with self-service portal reset (KB-01). Ticket closed.",
    },
    {
        "ticket_id": "TK-1050",
        "employee_name": "J. Fernandes",
        "issue_summary": "Admin access request",
        "status": "Rejected — no business justification provided (closed)",
        "is_active": False,
        "category": "Access",
        "priority": "MEDIUM",
        "resolution_notes": "Admin access request rejected due to absence of business justification and security sign-off. Ticket closed.",
    },
    {
        "ticket_id": "TK-1051",
        "employee_name": "L. Menon",
        "issue_summary": "Guest Wi-Fi issued",
        "status": "Resolved (closed)",
        "is_active": False,
        "category": "Network",
        "priority": "LOW",
        "resolution_notes": "24-hour pass generated via front-desk kiosk (KB-07). Ticket closed.",
    },
]
