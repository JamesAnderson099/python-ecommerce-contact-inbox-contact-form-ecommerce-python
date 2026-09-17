"""Contact-form routing and order update messages."""
from dataclasses import dataclass
from typing import Any, Dict, Tuple


@dataclass(frozen=True)
class ContactRequest:
    customer_name: str
    customer_email: str
    message: str
    order_id: str
    order_status: str


def build_order_update(request: ContactRequest) -> Tuple[str, str]:
    """Turn fulfillment state into a concise message for the team inbox."""
    status_text = {
        "checkout": "Checkout started",
        "fulfillment": "Order is being fulfilled",
        "shipped": "Order shipped",
        "delivered": "Order delivered",
    }.get(request.order_status, "Order update")
    subject = f"{status_text}: {request.order_id}"
    text = (
        f"Customer: {request.customer_name} <{request.customer_email}>\n"
        f"Order: {request.order_id}\nStatus: {request.order_status}\n"
        f"Message: {request.message}"
    )
    return subject, text


class InfraiError(RuntimeError):
    def __init__(self, code: str, detail: Any, status: int):
        super().__init__(f"Infrai request failed ({status}): {code}")
        self.code, self.detail, self.status = code, detail, status


def route_contact(request: ContactRequest, client: Any, inbox: str) -> Dict[str, Any]:
    subject, text = build_order_update(request)
    sent = client.email.send({"to": inbox, "subject": subject, "body": text})
    message_id = sent["message_id"]
    delivery = client.email.get(message_id)
    return {"message_id": message_id, "order_id": request.order_id, "status": request.order_status, "delivery": delivery}
