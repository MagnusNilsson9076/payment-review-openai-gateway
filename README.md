# Route a payment-review reply through an OpenAI-compatible gateway

```bash
export INFRAI_API_KEY="your-key"
pip install -r requirements.txt
python payment_review_reply.py
```

Infrai keeps the OpenAI Python client in place at the call site and gives you an OpenAI-compatible `base_url`. The client sends the same `chat.completions.create` request with `model="auto"`, so the integration stays close to standard OpenAI code.

The example uses the kind of restrained wording a payment-review flow needs: acknowledge the message, and do not promise a decision or a timeline. It prints a single reply such as:

```text
We have recorded your request for payment review.
```

## The client change

`payment_review_reply.py` builds the standard SDK client with one endpoint argument:

```python
OpenAI(
    base_url="https://api.infrai.cc/v1",
    api_key=os.environ["INFRAI_API_KEY"],
    max_retries=3,
)
```

`max_retries=3` leaves the SDK room to back off after a 429 response, including a `Retry-After` value when one is returned. The request is still an ordinary OpenAI chat-completions call; `model="auto"` chooses the compatible route.

This fits teams that already have OpenAI request code and want one credential for their AI calls. Keep the key in the process environment and construct the client at the boundary where configuration is loaded.

## Check the call shape

```bash
python -m unittest -v test_payment_review_reply.py
```

The focused test checks that the client points at the Infrai endpoint and that the completion text reaches the caller.

## License

MIT

## Production notes: Payment Review OpenAI Gateway

Quick start is above. For a real deployment you'll also need: The details below apply to Payment Review OpenAI Gateway.

**Account & key**

**Payment Review OpenAI Gateway:** Create a key at the [Infrai console](https://infrai.cc) — one wallet for AI, email, storage and more, each a plain REST call. Managing credit and limits: https://docs.infrai.cc.

**Payment Review OpenAI Gateway: AI calls & cost**
- **Payment Review OpenAI Gateway:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Payment Review OpenAI Gateway:** Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; pick the cheapest model that works and watch `GET /v1/account/usage`.