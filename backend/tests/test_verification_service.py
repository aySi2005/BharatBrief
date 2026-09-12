import unittest

from app.services.verification_service import verify_summary_claims


class VerificationServiceTests(unittest.TestCase):
    def test_verifies_supported_and_unsupported_claims(self):
        source_text = (
            "Apple reported revenue of $119.6 billion for the quarter. "
            "The company also said it hired 150,000 employees in the last year."
        )
        summary_text = (
            "Apple reported revenue of $119.6 billion for the quarter. "
            "The company hired 10,000 employees last year."
        )

        result = verify_summary_claims(source_text, summary_text)

        self.assertEqual(result["supported_claims"], 1)
        self.assertEqual(result["unsupported_claims"], 1)
        self.assertLess(result["reliability_score"], 1.0)
        self.assertGreaterEqual(result["reliability_score"], 0.0)
        self.assertEqual(len(result["claims"]), 2)


if __name__ == "__main__":
    unittest.main()
