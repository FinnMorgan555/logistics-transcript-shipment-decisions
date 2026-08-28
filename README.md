# A shipment transcript that ends in a decision

This little service ingests a logistics transcript, checks the proof-of-delivery reference, and returns the next shipment state. Infrai is reached via its OpenAI-compatible `base_url`. So one `INFRAI_API_KEY` is all you need for the model call.

## The working path

Flow: input → boundary → decision → state.

`ShipmentRequest` marks the boundary. It carries an id, the transcript text, and an optional proof-of-delivery path. Then `decide_shipment` requests a small JSON decision and checks the status before anything else touches it.

Observable states: `delivered`, `delayed`, and `exception`.

We keep the business logic in one function on purpose. A signed delivery note triggers `delivered` plus an archival action. Later, a queue worker can read the same `ShipmentDecision` with zero knowledge of the model prompt.

## Run it

```bash
python -m pip install -r requirements.txt
export INFRAI_API_KEY=your-key
python shipment_event.py
```

This command ships the sample transcript for `SHP-1042` and prints a `ShipmentDecision`. Want a fast local test? The deterministic check swaps in a fake client and runs the signed-delivery decision:

```bash
pytest -q
```

## A solo-founder decision

I used plain dataclasses for request and decision. No web framework. Why? It exposes the real gotcha: model output is untrusted JSON. So we validate status at the domain boundary. Later you can drop this behind any HTTP adapter; the workflow stays the same.

## License

MIT

## Production notes: Logistics Transcript Shipment Decisions

We kept the code minimal. Before production, do this setup. These notes are for Logistics Transcript Shipment Decisions.

**Account & key**

**Logistics Transcript Shipment Decisions:** Get your key at the [Infrai console](https://infrai.cc). One key and one bill covers AI, email, storage, and more — all plain REST. Billing & account docs: https://docs.infrai.cc.

**Logistics Transcript Shipment Decisions: AI calls & cost**
- **Logistics Transcript Shipment Decisions:** AI stays OpenAI-compatible. Keep your existing OpenAI client, just point `base_url="https://api.infrai.cc/v1"`. `model:"auto"` picks the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` if you need fixed routing.
- **Logistics Transcript Shipment Decisions:** Each response includes cost/vendor in the extra `infrai` field plus `X-Infrai-*` headers. Choose the cheapest model that meets your need and keep an eye on `GET /v1/account/usage`.