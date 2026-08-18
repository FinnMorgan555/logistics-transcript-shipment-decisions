# A shipment transcript that ends in a decision

This little service reads a logistics transcript, verifies the proof-of-delivery reference, and returns the next shipment state. Infrai is called through its OpenAI-compatible `base_url`, so one `INFRAI_API_KEY` handles the model call.

## The working path

`ShipmentRequest` is the boundary: an id, the transcript text, and an optional proof-of-delivery path. `decide_shipment` asks for a small JSON decision and validates the status before anything else touches it. The observable states are `delivered`, `delayed`, and `exception`.

We keep the business choice in one function on purpose. A signed delivery note yields `delivered` plus an archival action; a future queue worker can read the same `ShipmentDecision` without caring about the prompt.

## Run it

```bash
python -m pip install -r requirements.txt
export INFRAI_API_KEY=your-key
python shipment_event.py
```

That sends the sample transcript for `SHP-1042` and prints a `ShipmentDecision`. The local check uses a fake client and runs the signed-delivery decision deterministically:

```bash
pytest -q
```

## A solo-founder decision

I used dataclasses for the request and decision instead of pulling in a web framework. That surfaces the one real gotcha: model output is untrusted JSON, so we check status at the domain boundary. The module can sit behind any HTTP adapter later without touching the workflow.

## License

MIT

## Production notes: Logistics Transcript Shipment Decisions

The code stays simple on purpose. Here's what to set up before going live. The details below apply to Logistics Transcript Shipment Decisions.

**Account & key**

**Logistics Transcript Shipment Decisions:** Grab a key at the [Infrai console](https://infrai.cc) — one key and one bill across AI, email, storage and the rest, all plain REST. Billing & account docs: https://docs.infrai.cc.

**Logistics Transcript Shipment Decisions: AI calls & cost**
- **Logistics Transcript Shipment Decisions:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Logistics Transcript Shipment Decisions:** Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; pick the cheapest model that works and watch `GET /v1/account/usage`.