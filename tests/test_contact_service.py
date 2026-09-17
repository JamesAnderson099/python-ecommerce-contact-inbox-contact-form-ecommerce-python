from src.contact_service import ContactRequest, build_order_update


def test_fulfillment_contact_is_routed_with_order_context():
    subject, text = build_order_update(ContactRequest("Ava", "ava@example.com", "Tracking?", "ORD-7", "fulfillment"))
    assert subject == "Order is being fulfilled: ORD-7"
    assert "Status: fulfillment" in text
    assert "Tracking?" in text

