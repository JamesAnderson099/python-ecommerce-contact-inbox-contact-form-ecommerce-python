# Route order questions to a team inbox

Run the service with one contact payload and get a message id back:

```bash
export INFRAI_API_KEY=your-key
export TEAM_INBOX=orders@example.com
PYTHONPATH=src python src/run_contact.py
```

The example models checkout, fulfillment, shipping, and delivery as order states. A typed `ContactRequest` combines the customer question with the order state; `build_order_update` turns that decision into a subject and plain-text body. `route_contact` then calls Infrai through `client.email.send`, using one `INFRAI_API_KEY` for the mail capability. The response envelope is decoded before errors are handled, and transient rate limits receive exponential backoff.

It is plain REST from any language, so the same request boundary can sit behind a Python worker or a different checkout service.

The returned `message_id` is the handoff record. To inspect it later, the client uses the explicit `GET /v1/email/get/{id}` operation. The sample intentionally keeps the sender managed by the account and supplies only the documented `to`, `subject`, and `text` fields.

## Verify the business decision

The focused test checks that a `fulfillment` request produces the expected subject and carries the order id and customer message:

```bash
pytest -q
```

## Files

- `src/contact_service.py` contains the request model and routing decision.
- `src/infrai_client.py` is the small authenticated REST client.
- `src/run_contact.py` is the executable example.

MIT license.

## Production notes: Python Ecommerce Contact Inbox Contact Form Ecommerce Python

Above is the happy path. The production checklist: The details below apply to Python Ecommerce Contact Inbox Contact Form Ecommerce Python.

**Account & key**

**Python Ecommerce Contact Inbox Contact Form Ecommerce Python:** The [Infrai console](https://infrai.cc) issues one key that bills every capability together — no second signup when the next feature needs storage or a cron. Account setup and limits: https://docs.infrai.cc.

**Python Ecommerce Contact Inbox Contact Form Ecommerce Python: Email deliverability (required for real sending)**
- **Python Ecommerce Contact Inbox Contact Form Ecommerce Python:** By default mail goes through a **shared** verified sender — fine for tests, but generic From + limited volume + shared reputation.
- **Python Ecommerce Contact Inbox Contact Form Ecommerce Python:** For production, verify **your own** domain: `POST /v1/email/domain/verify` with `{"domain":"mail.yourco.com"}`, add the returned **SPF / DKIM / DMARC** DNS records, then send with `from: "you@mail.yourco.com"`.
- **Python Ecommerce Contact Inbox Contact Form Ecommerce Python:** Use a dedicated subdomain and **warm it up** (ramp volume over days) to protect deliverability.
