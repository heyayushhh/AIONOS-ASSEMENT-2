const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function sendChat({ user_id = 1, user_name = "Aditi Sharma", question }) {
  const res = await fetch(`${API_BASE}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_id, user_name, question }),
  });
  if (!res.ok) {
    throw new Error(`Chat request failed with status ${res.status}`);
  }
  return res.json();
}

export async function getTickets(activeOnly = null) {
  let url = `${API_BASE}/api/tickets`;
  if (activeOnly !== null) {
    url += `?active_only=${activeOnly}`;
  }
  const res = await fetch(url);
  if (!res.ok) throw new Error("Failed to fetch tickets");
  return res.json();
}

export async function getRequests() {
  const res = await fetch(`${API_BASE}/api/requests`);
  if (!res.ok) throw new Error("Failed to fetch requests");
  return res.json();
}

export async function getKnowledgeBase() {
  const res = await fetch(`${API_BASE}/api/kb`);
  if (!res.ok) throw new Error("Failed to fetch knowledge base");
  return res.json();
}

export async function getScenarios() {
  const res = await fetch(`${API_BASE}/api/scenarios`);
  if (!res.ok) throw new Error("Failed to fetch scenarios");
  return res.json();
}

export async function getMetrics() {
  const res = await fetch(`${API_BASE}/api/metrics`);
  if (!res.ok) throw new Error("Failed to fetch metrics");
  return res.json();
}
