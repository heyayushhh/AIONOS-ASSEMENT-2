// Veridian Corp API Client
// Priority: import.meta.env.VITE_API_URL -> fallback to http://localhost:8000
const rawBase = (import.meta.env.VITE_API_URL || "").trim();
export const API_BASE = rawBase ? rawBase.replace(/\/+$/, "") : "http://localhost:8000";

export async function checkHealth() {
  const res = await fetch(`${API_BASE}/health`);
  if (!res.ok) {
    throw new Error(`Health check failed with status ${res.status}`);
  }
  return res.json();
}

export async function sendChat({ user_id = 1, user_name = "Aditi Sharma", question }) {
  const res = await fetch(`${API_BASE}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_id, user_name, question }),
  });
  if (!res.ok) {
    const detail = await res.text().catch(() => "");
    throw new Error(`Chat request failed (${res.status}): ${detail || res.statusText}`);
  }
  return res.json();
}

export async function getTickets(activeOnly = null) {
  let url = `${API_BASE}/api/tickets`;
  if (activeOnly !== null) {
    url += `?active_only=${activeOnly}`;
  }
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Failed to fetch tickets (${res.status})`);
  return res.json();
}

export async function getRequests() {
  const res = await fetch(`${API_BASE}/api/requests`);
  if (!res.ok) throw new Error(`Failed to fetch requests (${res.status})`);
  return res.json();
}

export async function getKnowledgeBase() {
  const res = await fetch(`${API_BASE}/api/kb`);
  if (!res.ok) throw new Error(`Failed to fetch knowledge base (${res.status})`);
  return res.json();
}

export async function getScenarios() {
  const res = await fetch(`${API_BASE}/api/scenarios`);
  if (!res.ok) throw new Error(`Failed to fetch scenarios (${res.status})`);
  return res.json();
}

export async function getMetrics() {
  const res = await fetch(`${API_BASE}/api/metrics`);
  if (!res.ok) throw new Error(`Failed to fetch metrics (${res.status})`);
  return res.json();
}
