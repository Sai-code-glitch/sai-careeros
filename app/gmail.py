"""
Optional Gmail sender.

For safety and to avoid accidental spam, the main product creates outreach drafts and requires
approval. Connect Gmail OAuth credentials before enabling actual send.
"""
import base64
from email.message import EmailMessage
import httpx
from app.config import REQUIRE_APPROVAL_BEFORE_EMAIL

async def send_via_gmail(access_token: str, to_email: str, subject: str, body: str, approved=False):
    if REQUIRE_APPROVAL_BEFORE_EMAIL and not approved:
        return {"status": "APPROVAL_REQUIRED"}
    msg = EmailMessage()
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode().rstrip("=")
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(
            "https://gmail.googleapis.com/gmail/v1/users/me/messages/send",
            headers={"Authorization": f"Bearer {access_token}"},
            json={"raw": raw},
        )
        r.raise_for_status()
        return {"status": "SENT", "id": r.json().get("id")}
