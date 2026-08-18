import json
from types import SimpleNamespace

from shipment_event import ShipmentRequest, decide_shipment


class FakeCompletions:
    def create(self, **kwargs):
        assert kwargs["model"] == "auto"
        assert "signed the delivery sheet" in kwargs["messages"][0]["content"]
        return SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content=json.dumps({
                "status": "delivered",
                "action": "Archive proof of delivery",
                "exception": None,
            })))]
        )


class FakeClient:
    chat = SimpleNamespace(completions=FakeCompletions())


def test_signed_delivery_moves_shipment_to_delivered():
    result = decide_shipment(
        ShipmentRequest("SHP-1042", "Driver left the pallet at dock 3; receiver signed the delivery sheet.", "pod.pdf"),
        FakeClient(),
    )
    assert result.status == "delivered"
    assert result.action == "Archive proof of delivery"
    assert result.exception is None
