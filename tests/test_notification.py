import unittest
from src.contrat import Analyse, Evenement
from src.notification import choisir_canal, demander_validation


def exemple(sensible=True, criticite="CRITICAL"):
    e = Evenement("EVT-00125", "2026-10-05T10:02:11Z", "DOCKER", "backend",
                  "production", "CONTAINER_RESTART", "HIGH",
                  "OOMKilled restarts=14")
    a = Analyse("EVT-00125", criticite, "Limite mémoire", "Redémarrer backend",
                sensible, ["DOCKER"])
    return e, a


class TestNotification(unittest.TestCase):
    def test_canaux(self):
        self.assertEqual(choisir_canal("CRITICAL"), "TEAMS")
        self.assertEqual(choisir_canal("HIGH"), "TEAMS")
        self.assertEqual(choisir_canal("MEDIUM"), "EMAIL")
        self.assertEqual(choisir_canal("LOW"), "DASHBOARD")

    def test_canal_invalide(self):
        with self.assertRaises(ValueError):
            choisir_canal("BLABLA")

    def test_validation_acceptee(self):
        _, a = exemple()
        self.assertTrue(demander_validation(a, " OUI "))
        self.assertTrue(demander_validation(a, "o"))
        self.assertTrue(demander_validation(a, "Yes"))

    def test_validation_refusee(self):
        _, a = exemple()
        self.assertFalse(demander_validation(a, "n"))
        self.assertFalse(demander_validation(a, ""))

    def test_validation_non_sensible(self):
        _, a = exemple(sensible=False)
        self.assertTrue(demander_validation(a, "n"))


if __name__ == "__main__":
    unittest.main()