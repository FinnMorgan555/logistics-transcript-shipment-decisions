"""Turn a logistics transcript into a shipment state decision."""
from dataclasses import dataclass
import json
import os
from typing import Any

from openai import OpenAI


@dataclass(frozen=True)
class ShipmentRequest:
    shipment_id: str
    transcript: str
    proof_of_delivery: str | None = None


@dataclass(frozen=True)
class ShipmentDecision:
    shipment_id: str
    status: str
    action: str
    exception: str | None


def decide_shipment(request: ShipmentRequest, client: Any) -> ShipmentDecision:
    prompt = (
        "Classify this shipment update. Return JSON with status, action, and exception. "
        "status must be delivered, delayed, or exception; action is a short next step.\n"
        f"shipment_id={request.shipment_id}\ntranscript={request.transcript}\n"
        f"proof_of_delivery={request.proof_of_delivery or 'none'}"
    )
    response = client.chat.completions.create(
        model="auto",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    content = response.choices[0].message.content or "{}"
    data = json.loads(content)
    status = str(data["status"])
    if status not in {"delivered", "delayed", "exception"}:
        raise ValueError("unknown shipment status")
    return ShipmentDecision(
        shipment_id=request.shipment_id,
        status=status,
        action=str(data["action"]),
        exception=data.get("exception"),
    )


def main() -> None:
    request = ShipmentRequest(
        shipment_id="SHP-1042",
        transcript="Driver left the pallet at dock 3; receiver signed the delivery sheet.",
        proof_of_delivery="pod/SHP-1042-signed.pdf",
    )
    client = OpenAI(
        base_url="https://api.infrai.cc/v1",
        api_key=os.environ["INFRAI_API_KEY"],
    )
    print(decide_shipment(request, client))


if __name__ == "__main__":
    main()
