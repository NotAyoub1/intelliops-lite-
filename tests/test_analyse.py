import unittest
from src.analyse import analyser, classer, est_doublon, rechercher_runbook
from src.contrat import RUNBOOKS, Evenement


def evt(event_type="LOG", severity="LOW", message="ok", component="backend",
        source="DOCKER"):
    return Evenement("EVT-00001", "2026-10-05T10:00:00Z", source, component,
                     "production", event_type, severity, message)


class TestAnalyse(unittest.TestCase):
    def test_doublon(self):
        vus = set()
        self.assertFalse(est_doublon(evt(message="a"), vus))
        self.assertTrue(est_doublon(evt(message="a"), vus))

    def test_pas_doublon_si_message_different(self):
        vus = set()
        est_doublon(evt(message="a"), vus)
        self.assertFalse(est_doublon(evt(message="b"), vus))


    def test_runbook_trouve_sans_casse(self):
        e = evt(message="Container oomkilled restarts=3")
        self.assertEqual(rechercher_runbook(e, RUNBOOKS), RUNBOOKS["OOMKilled"])

    def test_runbook_absent(self):
        self.assertIsNone(rechercher_runbook(evt(message="health check ok"),
                                             RUNBOOKS))
    def test_classer_redemarrages(self):
        e = evt("CONTAINER_RESTART", "HIGH", "OOMKilled restarts=14")
        self.assertEqual(classer(e), "CRITICAL")

    def test_classer_seuil_10(self):
        e = evt("CONTAINER_RESTART", "HIGH", "OOMKilled restarts=10")
        self.assertEqual(classer(e), "CRITICAL")

    def test_classer_peu_de_redemarrages(self):
        e = evt("CONTAINER_RESTART", "HIGH", "OOMKilled restarts=3")
        self.assertEqual(classer(e), "MEDIUM")

    def test_classer_vulnerabilite_critique(self):
        e = evt("VULNERABILITY", "CRITICAL", "CVE-2026-1234", source="TRIVY")
        self.assertEqual(classer(e), "HIGH")

    def test_classer_par_defaut(self):
        self.assertEqual(classer(evt("LOG", "MEDIUM")), "MEDIUM")

if __name__ == "__main__":
    unittest.main()