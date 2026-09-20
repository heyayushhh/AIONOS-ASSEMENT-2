# 🛡️ Veridian Corp — Enterprise IT Support Copilot
### **Internal Service Agent Prototype • AIONOS Assignment 2**
*Ground Truth Operational Window: Monday, 21 September 2026 – Friday, 25 September 2026*

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI%20v0.110+-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/Frontend-React%2018%20%2B%20Vite-61DAFB.svg?logo=react&logoColor=black)](https://reactjs.org/)
[![SQLite](https://img.shields.io/badge/Database-SQLite%20(Auto--Seeded)-003B57.svg?logo=sqlite&logoColor=white)](https://sqlite.org)
[![Pytest](https://img.shields.io/badge/Tests-27%2F27%20Passed%20(100%25)-brightgreen.svg?logo=pytest&logoColor=white)](https://pytest.org)
[![Gemini](https://img.shields.io/badge/AI%20Engine-Google%20Gemini%20%2B%20Deterministic%20Core-blue.svg?logo=google&logoColor=white)](https://ai.google.dev)
[![License](https://img.shields.io/badge/License-Veridian%20Corp%20Internal-orange.svg)]()

---

## 📖 Table of Contents
1. [Executive Summary: Why Veridian Corp Needs This Agent](#-executive-summary-why-veridian-corp-needs-this-agent)
2. [High-Level Architecture & Core Flow](#-high-level-architecture--core-flow)
3. [The Source of Truth: Policies & Asset Governance](#-the-source-of-truth-policies--asset-governance)
4. [The 15 Employee Support Scenarios (REQ-01 to REQ-15)](#-the-15-employee-support-scenarios-req-01-to-req-15)
5. [The Active Ticket Queue & Historical Precedents (TK-1042 to TK-1051)](#-the-active-ticket-queue--historical-precedents-tk-1042-to-tk-1051)
6. [Dual-Engine Intelligence & Offline Fallback](#-dual-engine-intelligence--offline-fallback)
7. [Enterprise Security & Policy Guardrails](#-enterprise-security--policy-guardrails)
8. [Interactive Frontend Console Experience](#-interactive-frontend-console-experience)
9. [Quick Start & One-Command Local Execution](#-quick-start--one-command-local-execution)
10. [REST API Documentation](#-rest-api-documentation)
11. [Automated Testing & Validation](#-automated-testing--validation)
12. [Known Limitations & Production Roadmap](#-known-limitations--production-roadmap)

---

## 🌟 Executive Summary: Why Veridian Corp Needs This Agent

### The Operational Challenge (September 21–25, 2026)
During the operational week of September 21–25, 2026, **Veridian Corp** faced an acute surge in IT support requests across 15 employees and an active backlog of 10 ticketing records. The IT Operations team was strained by two opposing pressures:
1. **High-Frequency Self-Service Drain**: Trivial requests like 24-hour guest Wi-Fi passes, 90-day VPN credential renewals, and standard self-service password resets were generating avoidable Level-1 tickets, slowing response times for genuine technical emergencies.
2. **High-Risk Governance & Security Gaps**: Critical organizational risks required strict compliance with multi-departmental rules:
   * **Security Threat Containment**: Employee Ananya Reddy forwarded a live phishing email to teammates, risking widespread malware infection without immediate intervention.
   * **Policy Conflict & Asset Governance**: Aditi Sharma requested a replacement for a 3.5-year-old laptop. While hardware failure qualifies under IT policy **KB-03** (3-year threshold), the corporate **Asset Management Policy** mandates a 4-year lifecycle, strictly requiring **Finance sign-off** before fulfillment.
   * **Unauthorized Privilege Escalation**: Employee Kavya Pillai requested urgent administrative access to financial reporting servers for month-end without business justification — violating the precedent set by rejected ticket **TK-1050**.

### The Solution: An Autonomous, Policy-Grounded Service Agent
The **Veridian Corp IT Internal Service Agent** solves these challenges by combining conversational natural-language understanding with a **zero-hallucination deterministic policy engine**:
* ⚡ **Instant Zero-Touch Resolution**: Immediately directs users to self-service portals and front-desk kiosks without opening wasteful tickets.
* 🛡️ **Cross-Policy Governance**: Automatically cross-references IT knowledge base rules with corporate Finance and Asset Management policies to enforce mandatory management and finance approvals.
* 🚨 **Immediate Security Containment**: Automatically warns employees to stop forwarding phishing emails, instructs recipients to delete malicious messages unread, and escalates to `security@veridian-corp.example`.
* ⚖️ **Historical Precedent Awareness**: Uses the 10 prior ticketing records (TK-1042..1051) as binding precedent to reject unjustified admin access requests and track active fulfillment workflows.
* 🔌 **Zero External Dependency Guarantee**: Fully operates **100% offline** on local SQLite without needing external cloud LLMs, while seamlessly utilizing Google Gemini when an optional API key is supplied.

---

## 🏛️ High-Level Architecture & Core Flow

```
                                ┌─────────────────────────────────────────────────────────┐
                                │             React 18 + Vite Copilot UI                  │
                                │   • 15 Official Demo Scenarios (REQ-01 to REQ-15)       │
                                │   • Live Ticket Queue with Active/Closed Filters        │
                                │   • Knowledge Base & Policy Inspector Modal             │
                                │   • Real-Time Operations & Grounding Latency Metrics    │
                                └────────────────────────────┬────────────────────────────┘
                                                             │ HTTP / JSON REST APIs
                                                             ▼
                                ┌─────────────────────────────────────────────────────────┐
                                │                  FastAPI Application                    │
                                │   • Endpoints: /api/chat, /api/scenarios, /api/tickets  │
                                │   • Structured Tool Execution & Escalation Engine       │
                                │   • Input Sanitization & Empty/Vague Query Detection    │
                                └─────────────┬─────────────────────────────┬─────────────┘
                                              │                             │
                     ┌────────────────────────▼────┐          ┌─────────────▼───────────────────────┐
                     │   Optional: Google Gemini   │          │   Deterministic Veridian Policy     │
                     │   Generative AI (Flash 1.5) │          │   Reasoning Engine (100% Offline)   │
                     │  • Natural Conversation     │          │  • Strict PDF Grounding (KB-01..10) │
                     │  • Strict System Directives │          │  • Zero Hallucinations              │
                     │  • Graceful Fallback Engine │          │  • Sub-15ms Execution Latency       │
                     └─────────────────────────────┘          └─────────────────────────────────────┘
                                              │                             │
                                              └──────────────┬──────────────┘
                                                             ▼
                                ┌─────────────────────────────────────────────────────────┐
                                │            SQLite Database (helpdesk.db)                │
                                │   • Auto-seeded on first run via SQLAlchemy models       │
                                │   • 11 Official Policies (KB-01..10 + ASSET-01)         │
                                │   • 15 Official Employee Requests (REQ-01..15)          │
                                │   • 10 Official Ticket Queue Records (TK-1042..1051)    │
                                │   • Real-Time Audit Logs & Metrics Tracking             │
                                └─────────────────────────────────────────────────────────┘
```

---

## 📚 The Source of Truth: Policies & Asset Governance

The agent is grounded strictly in the **Assessment 2 Data Pack** for Veridian Corp (September 21–25, 2026). It never fabricates policies or creates synthetic exceptions.

| Policy ID | Title | Core Rule & Guidance | Approval Authority |
| :--- | :--- | :--- | :--- |
| **KB-01** | **Password Reset Policy** | Employees can reset passwords via self-service portal anytime. Accounts lock after **5 failed attempts**, requiring manual IT unlock. | **No approval required** (Manual IT unlock upon lockout) |
| **KB-02** | **VPN Access Policy** | Full-time employees receive automatic VPN access. Contractors strictly require **manager approval** via the Access Request Form. Credentials expire every 90 days (self-renewed). | **Manager approval** (for contractors only) |
| **KB-03** | **Laptop Replacement Policy** | Laptops are eligible for replacement after **3 years of service**, or earlier in verified hardware failure. Requests require at least **2 weeks advance notice**. | **IT & Finance** (Cross-referenced with ASSET-01) |
| **KB-04** | **Software Installation Requests** | Approved catalog software can be self-installed. Non-catalog software and browser extensions require **IT Security review** (takes **3–5 business days** SLA). | **IT Security** |
| **KB-05** | **Printer Troubleshooting** | Step 1: Check print queue. Step 2: Restart local print spooler service. If false jams or issues persist, log ticket with **printer asset tag**. | **IT Field Support** |
| **KB-06** | **Email Mailbox Quota** | Default quota is **25GB** (users must archive old mail). Quota increases require **manager approval** and are strictly **capped at 50GB**. | **Manager approval** (Hard cap at 50GB) |
| **KB-07** | **Guest Wi-Fi Access** | Credentials valid for **24 hours**. Generated directly by any employee at the **front-desk kiosk**. **No IT ticket or approval required**. | **Self-service kiosk** |
| **KB-08** | **Expense Software Access** | Initial account provisioning is granted by **Finance**, not IT. IT only assists with login and credential troubleshooting after account exists. | **Finance** (Provisioning) / **IT** (Login issues) |
| **KB-09** | **Security Incident Reporting** | Suspected phishing, malware, or unauthorized access must be reported immediately to **`security@veridian-corp.example`**. **MUST NEVER BE FORWARDED**. | **IT Security Incident Response** |
| **KB-10** | **Work-From-Home Equipment** | Remote work **> 3 days/week** qualifies for one-time home office allowance (chair, monitor). Requires **manager sign-off** and **Finance processing** before IT ships. | **Manager & Finance** |
| **ASSET-01** | **Asset Management Policy** | All company hardware follows a standard **4-year refresh cycle**. Early replacement outside this cycle strictly requires **Finance sign-off** in addition to IT approval. | **Finance & IT Assets** |

---

## 📋 The 15 Employee Support Scenarios (REQ-01 to REQ-15)

Every employee request from the official Data Pack is fully modeled, seeded, and verified:

| ID | Requester Persona | Department | Date | Problem Statement | Official Agent Resolution & Action |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **REQ-01** | Aditi Sharma | Engineering | Mon 21 Sep | Dead laptop (~3.5 yrs old), won't turn on. | Eligible (>3 yrs / failure per KB-03), requires 2 weeks notice. Because it is under 4 years, **Finance sign-off** is required under Asset Management Policy. |
| **REQ-02** | Vikram Chawla | Sales | Mon 21 Sep | Guest Wi-Fi access for visitor tomorrow. | Directs to front-desk kiosk for instant 24-hour pass (KB-07). No ticket needed. |
| **REQ-03** | Karan Mehta | Marketing | Mon 21 Sep | Account locked out after 6 tries. | Self-service disabled (>5 attempts per KB-01). Manual IT unlock queued; no manager approval needed. |
| **REQ-04** | Ritu Bhatia | Data Analytics | Tue 22 Sep | Non-catalog data analysis tool approval. | Non-catalog software requires IT Security review (3–5 business days SLA per KB-04). |
| **REQ-05** | Sanjay Oberoi | Operations | Tue 22 Sep | Expired VPN credentials. | 90-day expiration policy (KB-02). Full-time employees self-renew via portal; no manager re-approval needed. |
| **REQ-06** | Meera Iyer | HR | Tue 22 Sep | Printer 3rd floor false paper jam. | Step 1: clear queue and restart spooler. If unresolved, log ticket with printer asset tag (KB-05). |
| **REQ-07** | Farhan Ali | Design | Wed 23 Sep | WFH 4 days/week, requesting monitor. | Eligible (>3 days remote per KB-10). Escalates for Manager sign-off + Finance processing before IT shipping. |
| **REQ-08** | Ananya Reddy | Product | Wed 23 Sep | Phishing email received, forwarded to team. | **CRITICAL SECURITY ALERT (KB-09)**: Stop forwarding! Inform teammates to delete unread. Auto-escalated to `security@veridian-corp.example`. |
| **REQ-09** | Rohit Desai | Legal | Wed 23 Sep | Mailbox full, cannot send emails. | Default 25GB quota (archive old mail). Quota increases require Manager approval, strictly capped at 50GB (KB-06). |
| **REQ-10** | Kavya Pillai | Finance | Wed 23 Sep | Urgent admin access to finance server. | Privileged access requires formal business justification & Security approval (citing rejected precedent TK-1050). |
| **REQ-11** | Nikhil Bansal | Engineering | Thu 24 Sep | Contractor joining team, needs VPN. | Contractors require Manager approval submitted via official Access Request Form (KB-02). |
| **REQ-12** | Sneha Kulkarni | Accounting | Thu 24 Sep | Expense tool invalid credentials. | Finance provisions accounts; IT provides login troubleshooting once account exists (KB-08). |
| **REQ-13** | Aman Gupta | Support | Thu 24 Sep | Screen flickering (2 yrs old), might need fix. | Within 4-year lifecycle (KB-03 / ASSET-01). Routed for hardware diagnostic/repair ticket rather than replacement. |
| **REQ-14** | Tanya Chopra | Growth | Fri 25 Sep | Productivity browser extension request. | Non-catalog extensions require IT Security review (3–5 business days SLA, KB-04). |
| **REQ-15** | Rahul Menon | General | Fri 25 Sep | *"hey can you help, its not working"* | Vague query: Agent politely requests device name, software, exact error symptoms, and timing. |

---

## 🎫 The Active Ticket Queue & Historical Precedents (TK-1042 to TK-1051)

The system maintains the exact state of Veridian Corp's ticketing queue to support consistent decision-making and operational tracking:

| Ticket ID | Requester | Issue Summary | Status | State | How the Agent Uses This Record |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **TK-1042** | R. Verma | VPN credential expired | Resolved (closed) | Closed | Resolution precedent for REQ-05 (self-service renewal). |
| **TK-1043** | S. Iyer | Laptop replacement (3.2 yrs old) | Approved — pending fulfillment (active) | **ACTIVE** | Active fulfillment queue item tracking hardware delivery. |
| **TK-1044** | A. Khan | Non-catalog software request | Pending Security review (active) | **ACTIVE** | Demonstrates active 3–5 day Security review SLA queue. |
| **TK-1045** | P. Joshi | Mailbox quota increase | Approved at 35GB (closed) | Closed | Precedent showing quota increases under 50GB cap are granted with approval. |
| **TK-1046** | M. Das | Printer paper jam, floor 2 | Resolved (closed) | Closed | Precedent showing technician dispatch after spooler restart fails. |
| **TK-1047** | K. Singh | Home office equipment request | Pending Finance (active) | **ACTIVE** | Active ticket in Finance processing queue for WFH equipment. |
| **TK-1048** | T. Rao | Phishing email reported | Escalated to Security (active) | **ACTIVE** | Open security incident case under active investigation. |
| **TK-1049** | V. Nambiar | Password reset | Resolved (closed) | Closed | Precedent for manual IT unlock after lockout threshold. |
| **TK-1050** | J. Fernandes | Admin access request | Rejected — no business justification provided (closed) | Closed | **Binding Governance Precedent**: Cited when rejecting unauthorized admin access (REQ-10). |
| **TK-1051** | L. Menon | Guest Wi-Fi issued | Resolved (closed) | Closed | Precedent for front-desk kiosk self-service pass issuance. |

---

## 🧠 Dual-Engine Intelligence & Offline Fallback

The agent is architected to guarantee **100% operational continuity**:

```
                              [Incoming User Message]
                                         │
                         Is GEMINI_API_KEY Configured?
                                    /        \
                                  YES         NO
                                  /             \
                   Call Google Gemini API        Directly Execute Veridian
                   (Grounded 1.5 Flash)           Policy Reasoning Engine
                            │                              │
                     Did API Succeed?                      │
                        /        \                         │
                      YES         NO (Timeout/Error)       │
                      /             \                      │
            Return Natural Response  Fallback to Engine ───┘
```

1. **Deterministic Policy Core (Always Available)**:
   * 100% grounded in `KB-01` to `KB-10` and `ASSET-01`.
   * Zero hallucination guarantee: uncataloged queries return safe clarification without inventing policies or fake tickets.
   * Execution latency: **< 15 milliseconds**.
2. **Google Gemini Generative Layer (Optional)**:
   * When `GEMINI_API_KEY` is provided, enhances conversational tone and linguistic nuance while strictly constrained by system directives.
   * Structured citations and policy decisions are cross-verified by the policy engine.
   * If the API call fails or experiences network timeout, the application seamlessly falls back to the deterministic core without interrupting the user.

---

## 🔒 Enterprise Security & Policy Guardrails

* 🚫 **No Invented Policies or Citations**: If an employee asks an uncataloged question (*"Can I bring an elephant into the boardroom?"*), the agent returns `NO_POLICY_MATCH` with 0 fake citations and routes to IT Support.
* 🚫 **No Fake Physical Actions**: The agent never claims physical delivery or replacement is complete. Tickets are routed for fulfillment or diagnostic prep.
* 🚫 **No Unauthorized Approval Bypasses**: The agent enforces mandatory human sign-offs:
  * **Finance Sign-off** for laptops replaced prior to the 4-year asset cycle.
  * **Manager Approval** for contractor VPNs and mailbox quota increases.
  * **IT Security Sign-off** for non-catalog software and administrative server access.
* 🚨 **Phishing Propagation Blocker**: Instantly issues an urgent security directive forbidding the forwarding of phishing emails to colleagues.
* ❓ **Clarification on Ambiguity**: Prompts for required missing information whenever vague requests (*"it's not working"*) are submitted.

---

## 💻 Interactive Frontend Console Experience

The React 18 frontend (`http://localhost:5173`) delivers a modern, dark-themed enterprise copilot:

1. **Executive Command Bar**: Displays agent status, active simulated requester persona, and grounded policy validation.
2. **Left-Rail Scenario Runner (15 REQs)**: Instant, one-click execution of all 15 official demo requests with category filter chips (`Hardware`, `Network`, `Security`, `Access`, `Facilities`).
3. **Conversational Stage**: Rich markdown rendering, policy citation pills, and prominent Human Escalation cards (color-coded for Security, Finance, and Management).
4. **Live Ticket Queue Explorer**: Interactive table of TK-1042..1051 with instant toggles for Active vs. Closed cases.
5. **Knowledge Base Explorer**: Full searchable catalog of KB-01..10 and ASSET-01.
6. **Policy Inspector Modal**: Clicking any citation badge opens the official policy text, governing authority, and SLA constraints.
7. **Real-Time Operations & Metrics**: Displays live ticket queue breakdowns, audit log counters, and agent response latency.

---

## 🚀 Quick Start & One-Command Local Execution

### 1. Prerequisites
* **Python**: 3.10+ (tested on Python 3.10, 3.11, 3.12, 3.14)
* **Node.js**: v18+ and npm
* **Operating System**: Windows, macOS, or Linux

### 2. Clone the Repository
```bash
git clone https://github.com/heyayushhh/AIONOS-ASSEMENT-2.git
cd AIONOS-ASSEMENT-2
```

### 3. Start Backend (Terminal 1)
```bash
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```
* Backend starts at: `http://localhost:8000`
* Interactive API Docs: `http://localhost:8000/docs`
* Health Check: `http://localhost:8000/health`
* *Note: SQLite database `helpdesk.db` is auto-created and auto-seeded on first run.*

### 4. Start Frontend (Terminal 2)
```bash
cd frontend
npm install
npm run dev
```
* Open your browser at: `http://localhost:5173`

---

## 📡 REST API Documentation

| Method | Endpoint | Description | Sample Request Payload |
| :--- | :--- | :--- | :--- |
| `GET` | `/health` | Service health status | *None* |
| `POST` | `/api/chat` | Main conversational IT copilot endpoint | `{"user_name": "Sanjay Oberoi", "question": "How can I provide Wi-Fi access to a visitor?"}` |
| `GET` | `/api/scenarios` | Returns all 15 official demo presets | *None* |
| `GET` | `/api/tickets` | Returns tickets (`?active_only=true` supported) | *None* |
| `GET` | `/api/requests` | Returns all 15 employee requests with guidance | *None* |
| `GET` | `/api/kb` | Returns all 11 knowledge base articles | *None* |
| `GET` | `/api/metrics` | Returns operations & queue status breakdown | *None* |

---

## 🧪 Automated Testing & Validation

### Run Backend Unit & Integration Tests (27 Tests)
```bash
python -m pytest backend/tests/test_veridian_agent.py -v
```
**Test Results**: **27 Passed, 0 Failed (100% Success)** in 0.59s.
* Verified ticket active/closed partition (4 active, 6 closed).
* Verified all 15 demo scenarios (REQ-01 to REQ-15).
* Verified requester persona switching independence.
* Verified policy safety: empty query (`EMPTY_QUERY`) and unknown query (`NO_POLICY_MATCH`).

### Run End-to-End Live API Evaluation
```bash
python eval/run_eval.py
```
**Evaluation Results**: **10/10 Checks Passed (100% Accuracy)** against live server.

### Validate Frontend Production Build
```bash
npm --prefix frontend run build
```
**Build Result**: Built in **2.33s** with zero errors (`2056 modules transformed`).

---

## ⚠️ Known Limitations & Production Roadmap

1. **Simulated Live Directory**: In the current prototype, user authentication is simulated via the Requester Persona dropdown rather than an active enterprise Single Sign-On (SSO / Okta / Azure AD) provider.
2. **Database Defaults**: Default setup uses local SQLite for instant portability. Production deployments should configure PostgreSQL via `DATABASE_URL`.
3. **Optional External LLM Rate Limits**: When using an active `GEMINI_API_KEY`, external API rate limits and network latency depend on Google Gemini cloud endpoints; however, the local deterministic engine provides zero-latency instant response as a fallback.

---

**Veridian Corp IT Operations** • Built with ❤️ for **AIONOS Assignment 2**
