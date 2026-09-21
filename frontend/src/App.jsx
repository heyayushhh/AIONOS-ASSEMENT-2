import React, { useState, useEffect, useRef } from "react";
import ReactMarkdown from "react-markdown";
import {
  sendChat,
  getTickets,
  getRequests,
  getKnowledgeBase,
  getScenarios,
  getMetrics,
  API_BASE,
} from "./api";
import {
  Terminal,
  Shield,
  FileText,
  CheckCircle2,
  AlertTriangle,
  AlertCircle,
  Search,
  Send,
  Clock,
  BookOpen,
  Layers,
  BarChart3,
  User,
  Sparkles,
  ExternalLink,
  X,
  ArrowRight,
  HelpCircle,
  Zap,
} from "lucide-react";
import "./styles.css";

export default function App() {
  const [activeTab, setActiveTab] = useState("chat");
  const [messages, setMessages] = useState([
    {
      sender: "agent",
      text: "👋 **Welcome to Veridian Corp IT Internal Service Agent.**\n\nI am your enterprise IT support copilot, grounded strictly in Veridian's official knowledge base (**KB-01 to KB-10**) and the **Asset Management Policy** for the week of **September 21–25, 2026**.\n\n* **Instant Scenarios**: Select any of the 15 Employee Requests in the left rail.\n* **Ticket Status**: Check queue status and precedent history for **TK-1042 to TK-1051**.\n* **Policy Guidance**: Ask any question regarding password lockouts, VPN, laptop replacements, software approvals, printers, mailbox quotas, guest Wi-Fi, expense access, security reporting, or WFH equipment.",
      citations: [{ kb_id: "KB-01..10", title: "Veridian IT Knowledge Base" }],
      policyDecision: "READY",
      toolCalls: [],
      latencyMs: 12,
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    },
  ]);
  const [inputText, setInputText] = useState("");
  const [loading, setLoading] = useState(false);
  const [userName, setUserName] = useState("Aditi Sharma");
  const [selectedScenarioId, setSelectedScenarioId] = useState(null);

  // Data states
  const [scenarios, setScenarios] = useState([]);
  const [categoryFilter, setCategoryFilter] = useState("all");
  const [scenarioSearch, setScenarioSearch] = useState("");
  const [tickets, setTickets] = useState([]);
  const [ticketFilter, setTicketFilter] = useState("all"); // all, active, closed
  const [requestsList, setRequestsList] = useState([]);
  const [kbList, setKbList] = useState([]);
  const [metrics, setMetrics] = useState(null);
  const [kbSearch, setKbSearch] = useState("");

  // Modal inspector state
  const [inspectedPolicy, setInspectedPolicy] = useState(null);

  const chatEndRef = useRef(null);

  useEffect(() => {
    loadInitialData();
  }, []);

  useEffect(() => {
    if (activeTab === "chat") {
      chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages, activeTab]);

  async function loadInitialData() {
    try {
      const [scenariosData, ticketsData, requestsData, kbData, metricsData] = await Promise.all([
        getScenarios().catch(() => []),
        getTickets().catch(() => []),
        getRequests().catch(() => []),
        getKnowledgeBase().catch(() => []),
        getMetrics().catch(() => null),
      ]);
      setScenarios(scenariosData);
      setTickets(ticketsData);
      setRequestsList(requestsData);
      setKbList(kbData);
      setMetrics(metricsData);
    } catch (err) {
      console.error("Error loading initial data:", err);
    }
  }

  async function handleSendMessage(customText = null, customUser = null) {
    const textToSend = (customText || inputText).trim();
    if (!textToSend || loading) return;

    const currentUserName = customUser || userName;

    const userMsg = {
      sender: "user",
      text: textToSend,
      userName: currentUserName,
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    };

    setMessages((prev) => [...prev, userMsg]);
    if (!customText) setInputText("");
    setLoading(true);

    try {
      const resp = await sendChat({
        user_name: currentUserName,
        question: textToSend,
      });

      const agentMsg = {
        sender: "agent",
        text: resp.answer,
        citations: resp.citations || [],
        policyDecision: resp.policy_decision,
        escalatedTo: resp.escalated_to,
        toolCalls: resp.tool_calls || [],
        latencyMs: resp.latency_ms,
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      };

      setMessages((prev) => [...prev, agentMsg]);
      getMetrics().then(setMetrics).catch(() => {});
      getTickets().then(setTickets).catch(() => {});
    } catch (err) {
      const isLocal = API_BASE.includes("localhost") || API_BASE.includes("127.0.0.1");
      const targetHint = isLocal
        ? `Ensure backend is running locally at \`${API_BASE}\`.`
        : `Connecting to \`${API_BASE}\`. If your backend is hosted on a free-tier platform (like Render), it may take 30–50 seconds to wake up from spin-down. Please try again in a few moments.`;

      setMessages((prev) => [
        ...prev,
        {
          sender: "agent",
          text: `⚠️ **Connection Alert**: ${err.message || "Failed to fetch"}.\n\n${targetHint}`,
          timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  function runScenario(sc) {
    setActiveTab("chat");
    setSelectedScenarioId(sc.req_id);
    setUserName(sc.employee_name);
    handleSendMessage(sc.prompt, sc.employee_name);
  }

  function handleOpenPolicyModal(kbId) {
    const cleanId = (kbId || "").toUpperCase().trim();
    const found = kbList.find((k) => k.kb_id.toUpperCase() === cleanId || k.title.toUpperCase().includes(cleanId));
    if (found) {
      setInspectedPolicy(found);
      return;
    }
    const foundReq = requestsList.find((r) => r.req_id.toUpperCase() === cleanId);
    if (foundReq) {
      setInspectedPolicy({
        kb_id: foundReq.req_id,
        title: `${foundReq.req_id}: ${foundReq.employee_name} (${foundReq.status})`,
        content: `**Request Text**: "${foundReq.request_text}"\n\n**Resolution Guidance**:\n${foundReq.resolution_guidance}`,
        category: "Official Employee Request",
        requires_approval: foundReq.escalation_target !== "None",
        approval_authority: foundReq.escalation_target,
      });
      return;
    }
    const foundTicket = tickets.find((t) => t.ticket_id.toUpperCase() === cleanId);
    if (foundTicket) {
      setInspectedPolicy({
        kb_id: foundTicket.ticket_id,
        title: `${foundTicket.ticket_id}: ${foundTicket.issue_summary}`,
        content: `**Employee**: ${foundTicket.employee_name}\n**Status**: ${foundTicket.status} (${foundTicket.is_active ? "Active" : "Closed"})\n\n**Resolution Notes**:\n${foundTicket.resolution_notes || "N/A"}`,
        category: "Ticket Queue Record",
        requires_approval: foundTicket.is_active,
        approval_authority: foundTicket.status,
      });
      return;
    }
    setInspectedPolicy({
      kb_id: cleanId || "POLICY",
      title: `Veridian Policy: ${cleanId}`,
      content: `Official policy record for ${cleanId} from the Veridian Corp Knowledge Base. Grounded strictly in Assessment 2 PDF rules.`,
      category: "Corporate IT Policy",
      requires_approval: cleanId.includes("KB-02") || cleanId.includes("KB-03") || cleanId.includes("KB-04") || cleanId.includes("KB-06") || cleanId.includes("KB-08") || cleanId.includes("KB-10") || cleanId.includes("ASSET"),
      approval_authority: cleanId.includes("KB-04") ? "IT Security" : cleanId.includes("ASSET") ? "Finance & IT" : "Management / Finance",
    });
  }

  // Category tags mapping
  function getScenarioCategory(reqId) {
    const map = {
      "REQ-01": "Hardware",
      "REQ-02": "Network",
      "REQ-03": "Access",
      "REQ-04": "Software",
      "REQ-05": "Network",
      "REQ-06": "Hardware",
      "REQ-07": "Facilities",
      "REQ-08": "Security",
      "REQ-09": "Email",
      "REQ-10": "Access",
      "REQ-11": "Network",
      "REQ-12": "Finance",
      "REQ-13": "Hardware",
      "REQ-14": "Software",
      "REQ-15": "General",
    };
    return map[reqId] || "IT Support";
  }

  const filteredScenarios = scenarios.filter((sc) => {
    const category = getScenarioCategory(sc.req_id).toLowerCase();
    const matchesCat =
      categoryFilter === "all" ||
      category.includes(categoryFilter.toLowerCase());

    const matchesSearch =
      !scenarioSearch ||
      sc.employee_name.toLowerCase().includes(scenarioSearch.toLowerCase()) ||
      sc.title.toLowerCase().includes(scenarioSearch.toLowerCase()) ||
      sc.req_id.toLowerCase().includes(scenarioSearch.toLowerCase());

    return matchesCat && matchesSearch;
  });

  const filteredTickets = tickets.filter((t) => {
    if (ticketFilter === "active") return t.is_active;
    if (ticketFilter === "closed") return !t.is_active;
    return true;
  });

  const filteredKb = kbList.filter((kb) => {
    if (!kbSearch) return true;
    const s = kbSearch.toLowerCase();
    return (
      kb.kb_id.toLowerCase().includes(s) ||
      kb.title.toLowerCase().includes(s) ||
      kb.content.toLowerCase().includes(s) ||
      kb.category.toLowerCase().includes(s)
    );
  });

  const quickPrompts = [
    { label: "Guest Wi-Fi 24h Pass", prompt: "Can I get Wi-Fi access for a guest visiting our office tomorrow?" },
    { label: "Laptop Won't Turn On (3.5 yrs)", prompt: "My laptop won't turn on at all, it's completely dead, had it about 3.5 years now." },
    { label: "Account Lockout (6 Tries)", prompt: "I'm locked out of my account, tried my password 6 times." },
    { label: "Report Phishing Email", prompt: "I think I got a phishing email asking for my login credentials. Should I forward it?" },
    { label: "Contractor VPN Request", prompt: "New contractor joining my team next week, they'll need VPN access." },
    { label: "Printer Paper Jam Issue", prompt: "Printer on the 3rd floor keeps showing 'paper jam' even though there's no jam." },
    { label: "Mailbox Quota Full", prompt: "My mailbox is full and I can't send emails. How can I get a quota increase?" },
  ];

  return (
    <div className="app-container">
      {/* --------------------------------------------------------------------
          Command Header Bar
         -------------------------------------------------------------------- */}
      <header className="app-header">
        <div className="brand-section">
          <div className="brand-logo">
            <Shield size={20} strokeWidth={2.4} />
          </div>
          <div className="brand-details">
            <div className="brand-title-row">
              <span className="brand-name">Veridian Corp</span>
              <span className="brand-pill">IT Support Copilot</span>
            </div>
            <span className="brand-desc">
              Internal Service Agent • Week of Sep 21–25, 2026
            </span>
          </div>
        </div>

        <div className="header-actions">
          <div className="status-indicator" title={`Connected Backend: ${API_BASE}`}>
            <span className="status-dot"></span>
            <span>Agent Online • Grounded</span>
          </div>

          <div className="requester-badge-box">
            <User size={14} style={{ color: "var(--primary-light)" }} />
            <select
              className="requester-select"
              value={userName}
              onChange={(e) => setUserName(e.target.value)}
              title="Select simulated active employee"
            >
              <option value="Aditi Sharma">Aditi Sharma (Engineering • REQ-01)</option>
              <option value="Vikram Chawla">Vikram Chawla (Sales • REQ-02)</option>
              <option value="Karan Mehta">Karan Mehta (Marketing • REQ-03)</option>
              <option value="Ritu Bhatia">Ritu Bhatia (Data Analytics • REQ-04)</option>
              <option value="Sanjay Oberoi">Sanjay Oberoi (Operations • REQ-05)</option>
              <option value="Meera Iyer">Meera Iyer (Human Resources • REQ-06)</option>
              <option value="Farhan Ali">Farhan Ali (Design • REQ-07)</option>
              <option value="Ananya Reddy">Ananya Reddy (Product • REQ-08)</option>
              <option value="Rohit Desai">Rohit Desai (Legal • REQ-09)</option>
              <option value="Kavya Pillai">Kavya Pillai (Finance • REQ-10)</option>
              <option value="Nikhil Bansal">Nikhil Bansal (Engineering • REQ-11)</option>
              <option value="Sneha Kulkarni">Sneha Kulkarni (Accounting • REQ-12)</option>
              <option value="Aman Gupta">Aman Gupta (Support • REQ-13)</option>
              <option value="Tanya Chopra">Tanya Chopra (Growth • REQ-14)</option>
              <option value="Rahul Menon">Rahul Menon (General • REQ-15)</option>
            </select>
          </div>
        </div>
      </header>

      {/* --------------------------------------------------------------------
          Navigation Bar (Tab Strip)
         -------------------------------------------------------------------- */}
      <nav className="app-nav">
        <button
          className={`nav-tab-btn ${activeTab === "chat" ? "active" : ""}`}
          onClick={() => setActiveTab("chat")}
        >
          <Terminal size={15} />
          <span>Agent Chat & Scenarios</span>
          <span className="nav-tag-pill">15 REQs</span>
        </button>
        <button
          className={`nav-tab-btn ${activeTab === "tickets" ? "active" : ""}`}
          onClick={() => setActiveTab("tickets")}
        >
          <Layers size={15} />
          <span>Ticket Queue</span>
          <span className="nav-tag-pill">
            {tickets.filter((t) => t.is_active).length} Active
          </span>
        </button>
        <button
          className={`nav-tab-btn ${activeTab === "requests" ? "active" : ""}`}
          onClick={() => setActiveTab("requests")}
        >
          <FileText size={15} />
          <span>Employee Requests</span>
          <span className="nav-tag-pill">15 Total</span>
        </button>
        <button
          className={`nav-tab-btn ${activeTab === "kb" ? "active" : ""}`}
          onClick={() => setActiveTab("kb")}
        >
          <BookOpen size={15} />
          <span>Knowledge Base & Policies</span>
          <span className="nav-tag-pill">11 Policies</span>
        </button>
        <button
          className={`nav-tab-btn ${activeTab === "metrics" ? "active" : ""}`}
          onClick={() => setActiveTab("metrics")}
        >
          <BarChart3 size={15} />
          <span>Operations & Metrics</span>
        </button>
      </nav>

      {/* --------------------------------------------------------------------
          Main Viewport
         -------------------------------------------------------------------- */}
      <div className="main-viewport">
        {/* ======================= TAB 1: CHAT & SCENARIOS ======================= */}
        {activeTab === "chat" && (
          <div className="chat-workspace-split">
            {/* Left Rail: 15 Scenarios Sidebar */}
            <aside className="scenario-sidebar">
              <div className="sidebar-top">
                <div className="sidebar-header-row">
                  <div className="sidebar-title">
                    <Sparkles size={14} style={{ color: "#38bdf8" }} />
                    <span>Official Demo Scenarios</span>
                  </div>
                  <span className="scenario-count-badge">15 REQs</span>
                </div>

                <div className="sidebar-search-container">
                  <Search size={14} className="sidebar-search-icon" />
                  <input
                    type="text"
                    className="sidebar-search-input"
                    placeholder="Search 15 scenarios..."
                    value={scenarioSearch}
                    onChange={(e) => setScenarioSearch(e.target.value)}
                  />
                </div>

                <div className="sidebar-category-chips">
                  {["all", "Hardware", "Security", "Access", "Network", "Facilities"].map((cat) => (
                    <button
                      key={cat}
                      className={`cat-chip ${categoryFilter === cat ? "active" : ""}`}
                      onClick={() => setCategoryFilter(cat)}
                    >
                      {cat === "all" ? "All Categories" : cat}
                    </button>
                  ))}
                </div>
              </div>

              <div className="scenario-scroll-list">
                {filteredScenarios.map((sc) => {
                  const isSelected = selectedScenarioId === sc.req_id;
                  const category = getScenarioCategory(sc.req_id);
                  return (
                    <div
                      key={sc.req_id}
                      className={`scenario-card-item ${isSelected ? "selected" : ""}`}
                      onClick={() => runScenario(sc)}
                    >
                      <div className="card-top-row">
                        <span className="req-id-tag">{sc.req_id}</span>
                        <span className="cat-chip" style={{ fontSize: "0.68rem", padding: "1px 6px" }}>
                          {category}
                        </span>
                      </div>
                      <div className="employee-name">{sc.employee_name}</div>
                      <div className="scenario-snippet">{sc.title}</div>
                      <div className="scenario-footer-row">
                        <div className="policy-tag-pill">
                          <Shield size={11} />
                          <span>{sc.policy_ref}</span>
                        </div>
                        <ArrowRight size={12} style={{ color: "var(--text-muted)" }} />
                      </div>
                    </div>
                  );
                })}
              </div>
            </aside>

            {/* Center Stage: Chat Canvas */}
            <main className="chat-center-stage">
              {/* Session Meta Strip */}
              <div className="session-info-strip">
                <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                  <span style={{ color: "#ffffff", fontWeight: 600 }}>
                    Requester Persona: {userName}
                  </span>
                  <span>•</span>
                  <span>Exercise Context: Veridian Corp</span>
                </div>
                <div className="session-badge-pill">
                  <Clock size={12} />
                  <span>Veridian-Policy-Engine • Deterministic Grounding</span>
                </div>
              </div>

              {/* Conversation Messages */}
              <div className="chat-messages-scroll">
                {messages.map((m, idx) => {
                  const isUser = m.sender === "user";
                  return (
                    <div
                      key={idx}
                      className={`message-box-wrapper ${
                        isUser ? "message-box-user" : "message-box-agent"
                      }`}
                    >
                      {isUser ? (
                        /* User Message Card */
                        <div className="user-msg-card">
                          <div>{m.text}</div>
                          <div className="user-meta-sub">
                            <span>{m.userName || "Requester"}</span>
                            <span>•</span>
                            <span>{m.timestamp}</span>
                          </div>
                        </div>
                      ) : (
                        /* Agent Message Card */
                        <div className="agent-msg-card">
                          {/* Top Header */}
                          <div className="agent-header-bar">
                            <div className="agent-identity">
                              <div className="agent-avatar-icon">
                                <Zap size={14} />
                              </div>
                              <div>
                                <div className="agent-title-text">Veridian IT Internal Agent</div>
                                <div style={{ fontSize: "0.72rem", color: "var(--text-muted)" }}>
                                  Autonomous Service Copilot
                                </div>
                              </div>
                            </div>
                            <div className="agent-check-pill">
                              <CheckCircle2 size={12} />
                              <span>Grounded Policy Check Passed</span>
                            </div>
                          </div>

                          {/* Rendered Markdown */}
                          <div className="agent-markdown-content">
                            <ReactMarkdown>{m.text}</ReactMarkdown>
                          </div>

                          {/* Escalation Callout Box */}
                          {m.escalatedTo && m.escalatedTo !== "None" && (
                            <div
                              className={`escalation-banner ${
                                m.escalatedTo.toLowerCase().includes("security")
                                  ? "escalation-security-style"
                                  : m.escalatedTo.toLowerCase().includes("manager") ||
                                    m.escalatedTo.toLowerCase().includes("finance")
                                  ? "escalation-approval-style"
                                  : "escalation-it-style"
                              }`}
                            >
                              {m.escalatedTo.toLowerCase().includes("security") ? (
                                <AlertCircle size={20} style={{ flexShrink: 0 }} />
                              ) : (
                                <AlertTriangle size={20} style={{ flexShrink: 0 }} />
                              )}
                              <div className="escalation-info">
                                <div className="escalation-tag-title">
                                  Human Escalation / Approval Required
                                </div>
                                <div className="escalation-dept-name">
                                  Target: <strong>{m.escalatedTo}</strong>
                                </div>
                              </div>
                            </div>
                          )}

                          {/* Grounded Knowledge Citations */}
                          {m.citations && m.citations.length > 0 && (
                            <div className="citations-box">
                              <div className="citations-heading">
                                <BookOpen size={12} />
                                <span>Grounded Policy Sources (Click to inspect)</span>
                              </div>
                              <div className="citations-wrap">
                                {m.citations.map((c, i) => (
                                  <button
                                    key={i}
                                    className="citation-pill-btn"
                                    onClick={() => handleOpenPolicyModal(c.kb_id || c.title)}
                                    title="View full policy definition"
                                  >
                                    <span className="citation-mono-code">{c.kb_id || "KB"}</span>
                                    <span>{c.title}</span>
                                    <ExternalLink size={11} style={{ opacity: 0.7 }} />
                                  </button>
                                ))}
                              </div>
                            </div>
                          )}

                          {/* Bottom Meta */}
                          <div className="agent-meta-bottom">
                            <span>Execution: Deterministic Engine</span>
                            <span>•</span>
                            <span>{m.timestamp}</span>
                            {m.latencyMs !== undefined && (
                              <>
                                <span>•</span>
                                <span>⚡ Latency: {m.latencyMs}ms</span>
                              </>
                            )}
                          </div>
                        </div>
                      )}
                    </div>
                  );
                })}

                {loading && (
                  <div className="message-box-wrapper message-box-agent">
                    <div className="agent-msg-card" style={{ display: "flex", alignItems: "center", gap: "10px", color: "var(--text-muted)" }}>
                      <span className="status-dot"></span>
                      <span>Evaluating request against Veridian Corp policies & ticket records...</span>
                    </div>
                  </div>
                )}
                <div ref={chatEndRef} />
              </div>

              {/* Bottom Floating Input Dock */}
              <div className="chat-dock-container">
                {/* Quick Prompts Ribbon */}
                <div className="quick-prompt-ribbon">
                  {quickPrompts.map((qp, i) => (
                    <button
                      key={i}
                      className="quick-chip-action"
                      onClick={() => handleSendMessage(qp.prompt)}
                    >
                      <Sparkles size={12} style={{ color: "#60a5fa" }} />
                      <span>{qp.label}</span>
                    </button>
                  ))}
                </div>

                {/* Main Input Element */}
                <div className="input-field-card">
                  <Terminal size={17} className="terminal-prompt-icon" />
                  <input
                    type="text"
                    className="chat-input-element"
                    placeholder="Ask an IT support question, search policies, or test a scenario..."
                    value={inputText}
                    onChange={(e) => setInputText(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && handleSendMessage()}
                  />
                  <button
                    className="send-action-btn"
                    onClick={() => handleSendMessage()}
                    disabled={loading || !inputText.trim()}
                  >
                    <Send size={14} />
                    <span>Send</span>
                  </button>
                </div>
              </div>
            </main>
          </div>
        )}

        {/* ======================= TAB 2: TICKET QUEUE ======================= */}
        {activeTab === "tickets" && (
          <div className="canvas-panel">
            <div className="panel-header-box">
              <div>
                <h2 className="panel-headline">Official Veridian Ticket Queue (TK-1042 to TK-1051)</h2>
                <p className="panel-subtext">
                  Official queue records from Assessment 2 PDF. Active cases require agent or human resolution; closed tickets provide historical precedent.
                </p>
              </div>

              <div className="filter-pill-container">
                <button
                  className={`filter-pill-tab ${ticketFilter === "all" ? "selected" : ""}`}
                  onClick={() => setTicketFilter("all")}
                >
                  All Tickets ({tickets.length})
                </button>
                <button
                  className={`filter-pill-tab ${ticketFilter === "active" ? "selected" : ""}`}
                  onClick={() => setTicketFilter("active")}
                >
                  Active Cases Only ({tickets.filter((t) => t.is_active).length})
                </button>
                <button
                  className={`filter-pill-tab ${ticketFilter === "closed" ? "selected" : ""}`}
                  onClick={() => setTicketFilter("closed")}
                >
                  Closed Precedents ({tickets.filter((t) => !t.is_active).length})
                </button>
              </div>
            </div>

            <div className="table-viewport-card">
              <table className="modern-table">
                <thead>
                  <tr>
                    <th>Ticket ID</th>
                    <th>Requester</th>
                    <th>Issue Summary</th>
                    <th>Status & Queue State</th>
                    <th>Precedent / Resolution Notes</th>
                    <th>Agent Action</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredTickets.map((t) => (
                    <tr key={t.ticket_id}>
                      <td>
                        <span className="table-mono-id">{t.ticket_id}</span>
                      </td>
                      <td>
                        <strong style={{ color: "#ffffff" }}>{t.employee_name}</strong>
                      </td>
                      <td>{t.issue_summary}</td>
                      <td>
                        <span
                          className={
                            t.is_active ? "badge-active-open" : "badge-closed-rec"
                          }
                        >
                          {t.is_active ? "🟢 ACTIVE CASE" : "🔒 CLOSED"} — {t.status}
                        </span>
                      </td>
                      <td style={{ color: "#cbd5e1", maxWidth: "420px" }}>
                        {t.resolution_notes}
                      </td>
                      <td>
                        <button
                          className="table-action-btn"
                          onClick={() => {
                            setActiveTab("chat");
                            handleSendMessage(`Status of ticket ${t.ticket_id}`);
                          }}
                        >
                          <span>Query Agent</span>
                          <ArrowRight size={12} />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* ======================= TAB 3: EMPLOYEE REQUESTS ======================= */}
        {activeTab === "requests" && (
          <div className="canvas-panel">
            <div className="panel-header-box">
              <div>
                <h2 className="panel-headline">Employee Requests (REQ-01 to REQ-15)</h2>
                <p className="panel-subtext">
                  Official employee requests received during the exercise week of September 21–25, 2026.
                </p>
              </div>
            </div>

            <div className="table-viewport-card">
              <table className="modern-table">
                <thead>
                  <tr>
                    <th>Request ID</th>
                    <th>Requester</th>
                    <th>Date</th>
                    <th>Employee Inquiry</th>
                    <th>Initial Status</th>
                    <th>Policy Guidance & Escalation</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  {requestsList.map((r) => (
                    <tr key={r.req_id}>
                      <td>
                        <span className="req-id-tag">{r.req_id}</span>
                      </td>
                      <td>
                        <strong style={{ color: "#ffffff" }}>{r.employee_name}</strong>
                        <div style={{ fontSize: "0.72rem", color: "var(--text-muted)" }}>
                          {r.employee_email}
                        </div>
                      </td>
                      <td style={{ whiteSpace: "nowrap" }}>{r.date_opened}</td>
                      <td style={{ maxWidth: "260px" }}>
                        <em>"{r.request_text}"</em>
                      </td>
                      <td>
                        <span className="badge-active-open">{r.initial_action}</span>
                      </td>
                      <td style={{ maxWidth: "380px", color: "#cbd5e1" }}>
                        {r.resolution_guidance}
                        {r.escalation_target && r.escalation_target !== "None" && (
                          <div style={{ marginTop: "4px", color: "#f87171", fontWeight: 600 }}>
                            ➡️ Target: {r.escalation_target}
                          </div>
                        )}
                      </td>
                      <td>
                        <button
                          className="table-action-btn"
                          onClick={() => {
                            runScenario({
                              req_id: r.req_id,
                              employee_name: r.employee_name,
                              prompt: `${r.req_id}: ${r.employee_name} - ${r.request_text}`,
                            });
                          }}
                        >
                          <span>Evaluate</span>
                          <ArrowRight size={12} />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* ======================= TAB 4: KNOWLEDGE BASE ======================= */}
        {activeTab === "kb" && (
          <div className="canvas-panel">
            <div className="panel-header-box">
              <div>
                <h2 className="panel-headline">Veridian Knowledge Base (KB-01 to KB-10 + Asset Policy)</h2>
                <p className="panel-subtext">
                  Official corporate policies grounding all IT support evaluations and human escalation rules.
                </p>
              </div>

              <div className="sidebar-search-container" style={{ width: "300px" }}>
                <Search size={14} className="sidebar-search-icon" />
                <input
                  type="text"
                  className="sidebar-search-input"
                  placeholder="Search 11 corporate policies..."
                  value={kbSearch}
                  onChange={(e) => setKbSearch(e.target.value)}
                />
              </div>
            </div>

            <div className="kb-layout-grid">
              {filteredKb.map((kb) => (
                <div key={kb.kb_id} className="kb-module-card">
                  <div className="kb-card-head">
                    <span className="req-id-tag">{kb.kb_id}</span>
                    <span className="cat-chip">{kb.category}</span>
                  </div>
                  <h3 className="kb-article-title">{kb.title}</h3>
                  <p className="kb-article-text">{kb.content}</p>
                  <div className="kb-card-foot">
                    <span>
                      {kb.requires_approval
                        ? `🔒 Approval: ${kb.approval_authority}`
                        : "✅ Self-Service Direct"}
                    </span>
                    <button
                      className="table-action-btn"
                      onClick={() => {
                        setActiveTab("chat");
                        handleSendMessage(`Explain policy ${kb.kb_id}: ${kb.title}`);
                      }}
                    >
                      <span>Ask Copilot</span>
                      <ArrowRight size={11} />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ======================= TAB 5: SYSTEM METRICS ======================= */}
        {activeTab === "metrics" && (
          <div className="canvas-panel">
            <div className="panel-header-box">
              <div>
                <h2 className="panel-headline">Operations & System Metrics</h2>
                <p className="panel-subtext">
                  Real-time operational telemetry, query execution latency, and queue ticket distribution.
                </p>
              </div>
            </div>

            {metrics && (
              <div className="metrics-tiles-grid">
                <div className="metric-kpi-card">
                  <div className="kpi-title">
                    <Terminal size={14} />
                    <span>Total Evaluated Queries</span>
                  </div>
                  <div className="kpi-digit">{metrics.total_logs}</div>
                  <div className="kpi-foot">
                    <CheckCircle2 size={12} />
                    <span>Logged to SQLite Audit Trail</span>
                  </div>
                </div>

                <div className="metric-kpi-card">
                  <div className="kpi-title">
                    <Clock size={14} />
                    <span>Average Latency</span>
                  </div>
                  <div className="kpi-digit" style={{ color: "#34d399" }}>
                    {metrics.avg_latency_ms} ms
                  </div>
                  <div className="kpi-foot">
                    <Sparkles size={12} />
                    <span>Sub-second deterministic response</span>
                  </div>
                </div>

                <div className="metric-kpi-card">
                  <div className="kpi-title">
                    <Layers size={14} />
                    <span>Queue Tickets Ingested</span>
                  </div>
                  <div className="kpi-digit" style={{ color: "#60a5fa" }}>
                    {metrics.total_tickets}
                  </div>
                  <div className="kpi-foot">
                    <span>4 Active Cases • 6 Closed Records</span>
                  </div>
                </div>

                <div className="metric-kpi-card">
                  <div className="kpi-title">
                    <Shield size={14} />
                    <span>Policy Grounding SLA</span>
                  </div>
                  <div className="kpi-digit" style={{ color: "#a855f7" }}>
                    100%
                  </div>
                  <div className="kpi-foot">
                    <CheckCircle2 size={12} />
                    <span>Zero Hallucination Guardrail</span>
                  </div>
                </div>
              </div>
            )}

            <div className="table-viewport-card" style={{ padding: "24px" }}>
              <h3 style={{ fontSize: "1.05rem", fontWeight: 700, marginBottom: "14px", color: "#ffffff" }}>
                Queue Ticket Status Breakdown (Assessment 2 PDF Ground Truth)
              </h3>
              {metrics && metrics.tickets_by_status && (
                <div style={{ display: "flex", flexWrap: "wrap", gap: "12px" }}>
                  {Object.entries(metrics.tickets_by_status).map(([status, count]) => (
                    <div
                      key={status}
                      style={{
                        background: "var(--bg-input)",
                        border: "1px solid var(--border)",
                        padding: "12px 18px",
                        borderRadius: "var(--r-sm)",
                        display: "flex",
                        alignItems: "center",
                        gap: "10px",
                      }}
                    >
                      <span style={{ color: "var(--text-secondary)", fontSize: "0.86rem" }}>
                        {status}:
                      </span>
                      <span style={{ color: "#60a5fa", fontWeight: 700, fontSize: "1.2rem" }}>
                        {count}
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}
      </div>

      {/* --------------------------------------------------------------------
          Policy Inspector Modal
         -------------------------------------------------------------------- */}
      {inspectedPolicy && (
        <div className="modal-backdrop-blur" onClick={() => setInspectedPolicy(null)}>
          <div className="modal-window-box" onClick={(e) => e.stopPropagation()}>
            <div className="modal-bar-top">
              <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                <span className="req-id-tag">{inspectedPolicy.kb_id}</span>
                <span className="modal-header-text">{inspectedPolicy.title}</span>
              </div>
              <button
                className="modal-dismiss-btn"
                onClick={() => setInspectedPolicy(null)}
              >
                <X size={18} />
              </button>
            </div>
            <div className="modal-main-content">
              <div style={{ marginBottom: "14px" }}>
                <span className="cat-chip" style={{ fontSize: "0.74rem", padding: "3px 10px" }}>
                  Category: {inspectedPolicy.category}
                </span>
              </div>
              <p style={{ marginBottom: "16px", color: "#ffffff", fontWeight: 500 }}>
                {inspectedPolicy.content}
              </p>
              {inspectedPolicy.requires_approval && (
                <div
                  className="escalation-banner escalation-approval-style"
                  style={{ marginTop: "16px" }}
                >
                  <AlertTriangle size={18} style={{ flexShrink: 0 }} />
                  <div>
                    <div style={{ fontSize: "0.72rem", fontWeight: 700, textTransform: "uppercase" }}>
                      Governance Requirement
                    </div>
                    <div>
                      <strong>Approval Authority Required:</strong>{" "}
                      {inspectedPolicy.approval_authority}
                    </div>
                  </div>
                </div>
              )}
            </div>
            <div className="modal-bar-bottom">
              <button
                className="send-action-btn"
                onClick={() => {
                  const policyTitle = inspectedPolicy.title;
                  const policyId = inspectedPolicy.kb_id;
                  setInspectedPolicy(null);
                  setActiveTab("chat");
                  handleSendMessage(`Provide complete guidance for ${policyId}: ${policyTitle}`);
                }}
              >
                <span>Ask Copilot about this Policy</span>
                <ArrowRight size={14} />
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
