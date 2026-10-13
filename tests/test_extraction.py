import unittest

from src.extraction import masquer_secrets, normaliser_docker

LIGNE = "2026-10-05 10:02:11 ERROR backend OOMKilled restarts=14 node=db-02"

class TestExtraction(unittest.TestCase):
    def test_masquer_secrets(self):
        self.assertEqual(masquer_secrets("login ok password=abc123 user=bob"),
                                "login ok password=[SECRET] user=bob")

    def test_normaliser_docker(self):
        evt = normaliser_docker(LIGNE, 125)
        self.assertEqual(evt.id, "EVT-00125")
        self.assertEqual(evt.timestamp, "2026-10-05T10:02:11Z")
        self.assertEqual(evt.severity, "HIGH")

if __name__ == "__main__":
    unittest.main()