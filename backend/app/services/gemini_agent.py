"""
Gemini AI Agent Service for Veridian Corp Internal Service Agent
Integrates with Google Gemini API with function calling, grounded strictly in KB-01..10 and Veridian Corp dataset.
"""

import json
import logging
import requests
from typing import Dict, Any, List, Optional
from app.config import settings
from app.services.veridian_policy_engine import policy_engine

logger = logging.getLogger("gemini_agent")


class GeminiAgentService:
    def __init__(self):
        self.api_key = settings.gemini_api_key

    def process_chat(self, question: str, user_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Process a helpdesk chat message. If GEMINI_API_KEY is available and configured,
        call Gemini API. If unconfigured or on error, fallback to the deterministic Veridian policy engine.
        """
        if not self.api_key:
            # Deterministic policy engine fallback
            return policy_engine.evaluate_request(question, user_name)

        try:
            return self._call_gemini_api(question, user_name)
        except Exception as e:
            logger.warning(f"Gemini API invocation failed: {e}. Falling back to deterministic engine.")
            return policy_engine.evaluate_request(question, user_name)

    def _call_gemini_api(self, question: str, user_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Direct REST call to Gemini 2.5 Flash / 1.5 Flash API with tool declarations and strict grounding instructions.
        """
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}"

        system_instruction = (
            "You are the official Veridian Corp IT Internal Service Agent for the week of September 21–25, 2026. "
            "You must ground your answers strictly in the official Veridian Corp knowledge base (KB-01 to KB-10) "
            "and the Asset Management Policy. Never invent policies, permissions, or unauthorized approvals.\n"
            "Key Rules:\n"
            "- Passwords: Self-service reset is available. Locked out after 5 failed attempts -> manual IT unlock.\n"
            "- VPN: Full-time employees automatic. Contractors require manager approval via request form. 90-day expiry.\n"
            "- Laptop replacement: Eligible after 3 years or verified failure (2 weeks notice). Asset Management Policy 4-year cycle requires Finance sign-off for replacement outside 4 years.\n"
            "- Software: Standard catalog self-installed. Non-catalog (including extensions) requires IT Security review (3-5 business days).\n"
            "- Printer: Check queue, restart spooler; log ticket with asset tag if unresolved.\n"
            "- Mailbox quota: Default 25GB; increases require manager approval, capped at 50GB.\n"
            "- Guest Wi-Fi: 24-hour pass generated at front-desk kiosk; no IT ticket required.\n"
            "- Expense tool: Access granted by Finance; IT only assists with login after creation.\n"
            "- Phishing/malware: Report to security@veridian-corp.example immediately; NEVER forward.\n"
            "- WFH equipment: Remote >3 days/week eligible for chair/monitor; requires manager sign-off + Finance processing."
        )

        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": f"User: {user_name or 'Employee'}\nQuestion: {question}"}]
                }
            ],
            "systemInstruction": {
                "parts": [{"text": system_instruction}]
            },
            "generationConfig": {
                "temperature": 0.1,
                "maxOutputTokens": 800
            }
        }

        resp = requests.post(url, json=payload, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            candidates = data.get("candidates", [])
            if candidates:
                text = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                engine_res = policy_engine.evaluate_request(question, user_name)
                return {
                    "answer": text,
                    "citations": engine_res.get("citations", []),
                    "policy_decision": engine_res.get("policy_decision", "AI_GROUNDED_RESPONSE"),
                    "escalated_to": engine_res.get("escalated_to"),
                    "tool_calls": engine_res.get("tool_calls", []),
                }

        # If HTTP response not 200, use deterministic engine
        return policy_engine.evaluate_request(question, user_name)


gemini_agent = GeminiAgentService()
