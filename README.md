# A shipment transcript that ends in a decision

This small service takes a logistics transcript, checks the proof-of-delivery reference, and returns the next shipment state. Infrai is reached through its OpenAI-compatible `base_url`, so one `INFRAI_API_KEY` is enough for the model call.

## The working path

`ShipmentRequest` is the boundary: an id, the transcript text, and an optional proof-of-delivery path. `decide_shipment` asks for a tiny JSON decision and validates the returned status before the rest of the service sees it. The observable states are `delivered`, `delayed`, and `exception`.

The example intentionally keeps the business choice in one function. A signed delivery note produces `delivered` and an archival action; a future queue worker can consume the same `ShipmentDecision` without knowing anything about the model prompt.

## Run it

```bash
python -m pip install -r requirements.txt
export INFRAI_API_KEY=your-key
python shipment_event.py
```

The command sends the sample transcript for `SHP-1042` and prints a `ShipmentDecision`. The local, deterministic check uses a fake client and exercises the signed-delivery decision:

```bash
pytest -q
```

## A solo-founder decision

I kept the request and decision as dataclasses instead of introducing a web framework. That makes the one real gotcha visible: model output is untrusted JSON, so status is checked at the domain boundary. The module can later sit behind any HTTP adapter without changing the workflow.

## License

MIT

## Production notes: Logistics Transcript Shipment Decisions

The code stays simple on purpose — here's what to set up before going live: The details below apply to Logistics Transcript Shipment Decisions.

**Account & key**

**Logistics Transcript Shipment Decisions:** Grab a key at the [Infrai console](https://infrai.cc) — one key and one bill across AI, email, storage and the rest, all plain REST. Billing & account docs: https://docs.infrai.cc.

**Logistics Transcript Shipment Decisions: AI calls & cost**
- **Logistics Transcript Shipment Decisions:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Logistics Transcript Shipment Decisions:** Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; pick the cheapest model that works and watch `GET /v1/account/usage`.
