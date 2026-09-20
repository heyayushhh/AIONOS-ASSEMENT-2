# Veridian Corp IT Internal Service Agent — Architecture

## 1. System Architecture

```
┌────────────────────────────────────────────────────────┐
│                   React 18 + Vite UI                   │
│   - Agent Chat & 15 Scenario Quick Runners (REQ-01..15) │
│   - Ticket Queue Viewer (TK-1042..TK-1051)             │
│   - Knowledge Base & Policy Explorer (KB-01..KB-10)    │
│   - Execution & Latency Metrics Monitor                │
└───────────────────────────┬────────────────────────────┘
                            │ REST / JSON (FastAPI)
                            ▼
┌────────────────────────────────────────────────────────┐
│                   FastAPI Backend                      │
│   - Routes: /api/chat, /api/tickets, /api/requests,    │
│             /api/kb, /api/scenarios, /api/metrics      │
└─────────────┬───────────────────────────┬──────────────┘
              │                           │
              ▼                           ▼
┌───────────────────────────┐ ┌──────────────────────────┐
│     Gemini AI Agent       │ │  Veridian Policy Engine  │
│ - Strict KB Grounding     │ │ - Deterministic Rules    │
│ - Tool Call Execution     │ │ - Offline 100% Fallback  │
└───────────────────────────┘ └──────────────────────────┘
              │                           │
              └─────────────┬─────────────┘
                            ▼
┌────────────────────────────────────────────────────────┐
│                 SQLAlchemy ORM Layer                   │
│   - KnowledgeArticle (KB-01..10, ASSET-01)             │
│   - EmployeeRequest (REQ-01..15)                       │
│   - Ticket (TK-1042..1051 with Active/Closed flags)    │
│   - User & ChatLog Models                              │
└───────────────────────────┬────────────────────────────┘
                            ▼
┌────────────────────────────────────────────────────────┐
│             SQLite / PostgreSQL Database               │
└────────────────────────────────────────────────────────┘
```

## 2. Decision Logic & Policy Resolution

1. **Password Lockout vs Self-Service (KB-01)**:
   * Self-service reset at any time.
   * Lockout strictly occurs after $\ge 5$ failed attempts $\rightarrow$ IT manual unlock queued.
2. **VPN Access (KB-02)**:
   * Full-time employees: Automatic access; 90-day credentials renewal via self-service.
   * Contractors: Manager approval required via Access Request Form.
3. **Laptop Replacement (KB-03 & ASSET-01)**:
   * Age $\ge 4$ years: Standard refresh cycle.
   * Age $\ge 3$ years or Hardware Failure: Eligible under KB-03, but requires Finance sign-off under Asset Management Policy.
   * Age $< 3$ years without verified failure: Route for Hardware Repair / Diagnostic.
4. **Software Installations (KB-04)**:
   * Standard Catalog: Self-installed.
   * Non-catalog tools & extensions: Escalated to IT Security review (3–5 business days SLA).
5. **Printer Troubleshooting (KB-05)**:
   * Spooler restart & queue check $\rightarrow$ if unresolved, ticket logged with printer asset tag.
6. **Mailbox Quota (KB-06)**:
   * Default 25GB $\rightarrow$ increases require Manager approval, capped at 50GB.
7. **Guest Wi-Fi (KB-07)**:
   * Front-desk kiosk 24-hour pass generation (no IT ticket required).
8. **Expense Management (KB-08)**:
   * Provisioning handled by Finance $\rightarrow$ IT handles technical/login issues for existing accounts.
9. **Security Incident (KB-09)**:
   * Report to `security@veridian-corp.example` immediately $\rightarrow$ DO NOT FORWARD to colleagues.
10. **WFH Equipment (KB-10)**:
    * Remote $> 3$ days/week $\rightarrow$ Manager sign-off + Finance processing $\rightarrow$ IT coordinates shipment.
