import json
import os
from contact_service import ContactRequest, route_contact
from infrai_client import InfraiClient


def main() -> None:
    request = ContactRequest("Ava Chen", "ava@example.com", "When will it arrive?", "ORD-1042", "fulfillment")
    result = route_contact(request, InfraiClient(), os.environ["TEAM_INBOX"])
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

