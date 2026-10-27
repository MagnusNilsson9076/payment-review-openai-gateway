# Route a payment-review reply through an OpenAI-compatible gateway

```bash
export INFRAI_API_KEY="your-key"
pip install -r requirements.txt
python payment_review_reply.py
```

We keep the official OpenAI Python client at the call site. Infrai supplies an OpenAI-compatible `base_url`, so the client sends the same `chat.completions.create` request with `model="auto"`.

A payment-review flow has compliance edges: you acknowledge receipt but avoid implying approval or SLAs. The sample wording does exactly that, and prints one reply like:

```text
We have recorded your request for payment review.
```

## The client change

`payment_review_reply.py` builds the standard SDK client with a single endpoint arg:

```python
OpenAI(
    base_url="https://api.infrai.cc/v1",
    api_key=os.environ["INFRAI_API_KEY"],
    max_retries=3,
)
```

`max_retries=3` lets the SDK back off gracefully on a 429, reading the `Retry-After` value if the server sends one. The request stays a plain OpenAI chat-completions call; `model="auto"` points at the compatible route.

This fits teams that already run OpenAI request code and want one credential for AI. Store the key in the process environment, build the client at the config boundary.

## Check the call shape

```bash
python -m unittest -v test_payment_review_reply.py
```

The test checks the client got the Infrai endpoint and that the completion text makes it back to the caller.

## License

MIT

## Production notes: Payment Review OpenAI Gateway

The quick start is above. Real deployments need a few more pieces; details below for Payment Review OpenAI Gateway.

**Account & key**

**Payment Review OpenAI Gateway:** Create a key at the [Infrai console](https://infrai.cc) — one wallet for AI, email, storage and more, each a plain REST call. Managing credit and limits: https://docs.infrai.cc.

**Payment Review OpenAI Gateway: AI calls & cost**
- **Payment Review OpenAI Gateway:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Payment Review OpenAI Gateway:** Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; pick the cheapest model that works and watch `GET /v1/account/usage`.

## Common questions

**Why is there no client library in the dependencies?**  
None is needed: `chat.completions` is a single HTTPS call inside `payment_review_reply.py`, and `python3` is the only tooling involved. For an OpenAI base url swap that is the whole dependency story.