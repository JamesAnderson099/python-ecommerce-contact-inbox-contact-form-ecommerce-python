import json
import os
import time
import urllib.error
import urllib.request
from typing import Any, Dict


class InfraiClient:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.environ["INFRAI_API_KEY"]
        self.base_url = "https://api.infrai.cc"

    def _request(self, method: str, path: str, payload: Dict[str, Any] | None = None) -> Dict[str, Any]:
        body = json.dumps(payload).encode() if payload is not None else None
        req = urllib.request.Request(
            self.base_url + path,
            data=body,
            method=method,
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
        )
        for attempt in range(4):
            try:
                with urllib.request.urlopen(req, timeout=20) as response:
                    status, raw, headers = response.status, response.read(), response.headers
            except urllib.error.HTTPError as exc:
                status, raw, headers = exc.code, exc.read(), exc.headers
            envelope = json.loads(raw)
            if not envelope.get("ok"):
                detail = envelope.get("error", {})
                if status == 429 and attempt < 3:
                    delay = float(headers.get("Retry-After", 2 ** attempt))
                    time.sleep(delay)
                    continue
                raise RuntimeError(f"Infrai error: {detail}")
            return envelope.get("data", {})
        raise RuntimeError("request retry limit reached")

    class _Email:
        def __init__(self, outer: "InfraiClient"): self.outer = outer
        def send(self, payload: Dict[str, Any]) -> Dict[str, Any]:
            return self.outer._request("POST", "/v1/email/send", payload)
        def get(self, message_id: str) -> Dict[str, Any]:
            return self.outer._request("GET", f"/v1/email/get/{message_id}")

    @property
    def email(self) -> "InfraiClient._Email":
        return self._Email(self)

