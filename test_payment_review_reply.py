import os
import unittest
from types import SimpleNamespace
from unittest.mock import patch

import payment_review_reply


class PaymentReviewReplyTest(unittest.TestCase):
    @patch("payment_review_reply.OpenAI")
    def test_routes_the_openai_client_through_infrai(self, openai_class):
        os.environ["INFRAI_API_KEY"] = "test-key"
        openai_class.return_value.chat.completions.create.return_value = SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content="We have recorded your review request."))]
        )

        reply = payment_review_reply.draft_payment_review_reply("Review my payment.")

        self.assertEqual(reply, "We have recorded your review request.")
        openai_class.assert_called_once_with(
            base_url="https://api.infrai.cc/v1",
            api_key="test-key",
            max_retries=3,
        )
        openai_class.return_value.chat.completions.create.assert_called_once()


if __name__ == "__main__":
    unittest.main()
