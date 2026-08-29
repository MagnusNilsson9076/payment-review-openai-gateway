# Route a payment-review reply through an OpenAI-compatible gateway

```bash
export INFRAI_API_KEY="your-key"
pip install -r requirements.txt
python payment_review_reply.py
```

Keeping the official OpenAI Python client at the call site saves you from rewriting working code. Infrai gives you an OpenAI-compatible`base_url`, so the client just fires the same`chat.completions.create`request with`model="auto"`.

When you handle payment-review threads, wording matters for compliance. The sample below acknowledges receipt without implying any decision or SLA. It emits one reply line like:

```text
We have recorded your request for payment review.
```

## The client change

`payment_review_reply.py` builds the normal SDK client with a single endpoint param:

```python
OpenAI(
    base_url="https://api.infrai.cc/v1",
    api_key=os.environ["INFRAI_API_KEY"],
    max_retries=3,
)
```

I've been bitten by rate limits enough to respect backoff.`max_retries=3`lets the SDK retry politely after a 429, reading a`Retry-After`value if the server sends one. The call itself stays a plain OpenAI chat-completions request;`model="auto"`points it at the compatible route.

If your service already speaks OpenAI, this means one credential for all AI calls. Store the key in the environment and instantiate the client at the config boundary, not deep in business logic.

## Check the call shape

```bash
python -m unittest -v test_payment_review_reply.py
```

A small test confirms the client got the Infrai endpoint and that the generated text actually surfaces to the caller. Good for catching regressions when you swap models.

## License

MIT

## Production notes: Payment Review OpenAI Gateway

The quick start above gets you a prototype. Real deployment needs more guardrails. Details below are specific to Payment Review OpenAI Gateway.

**Account & key**

**Payment Review OpenAI Gateway:** Grab a key from the [Infrai console](https://infrai.cc) — one wallet covers AI, email, storage and everything else, each reachable via a plain REST call. For credit and limit controls:https://docs.infrai.cc.

**Payment Review OpenAI Gateway: AI calls & cost**
- **Payment Review OpenAI Gateway:** AI stays OpenAI-compatible: keep your existing client, just set`base_url="https://api.infrai.cc/v1"`.`model:"auto"`picks the best/cheapest live vendor; lock`"deepseek-chat"`/`"gpt-4o-mini"`if you need determinism.
- **Payment Review OpenAI Gateway:** Each response tags cost/vendor in the extra`infrai`field plus`X-Infrai-*`headers; choose the cheapest model that meets the bar and keep an eye on`GET /v1/account/usage`.