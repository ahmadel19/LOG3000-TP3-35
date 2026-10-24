"""Tests d'intégration de la route Flask ``/`` avec le client de test Flask.

Ils vérifient le cycle complet requête → calcul → page rendue, sans lancer
de vrai serveur.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app  # noqa: E402


class TestRouteIndex(unittest.TestCase):
    """Comportement de la page principale en GET et en POST."""

    def setUp(self):
        """Crée un client de test Flask neuf pour chaque test."""
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_get_affiche_la_calculatrice(self):
        """GET / répond 200 et contient le titre et l'écran."""
        reponse = self.client.get("/")
        self.assertEqual(reponse.status_code, 200)
        html = reponse.get_data(as_text=True)
        self.assertIn("Flask Calculator", html)
        self.assertIn('id="display"', html)

    def test_post_affiche_le_resultat(self):
        """POST d'une addition valide réaffiche la page avec le résultat dans l'écran."""
        reponse = self.client.post("/", data={"display": "2+3"})
        self.assertEqual(reponse.status_code, 200)
        self.assertIn('value="5.0"', reponse.get_data(as_text=True))

    def test_post_expression_invalide(self):
        """Une expression invalide produit un message 'Error:' et non une erreur 500."""
        reponse = self.client.post("/", data={"display": "1+2+3"})
        self.assertEqual(reponse.status_code, 200)
        self.assertIn("Error: only one operator is allowed", reponse.get_data(as_text=True))

    def test_post_division_par_zero(self):
        """La division par zéro est signalée dans l'écran, sans planter le serveur."""
        reponse = self.client.post("/", data={"display": "5/0"})
        self.assertEqual(reponse.status_code, 200)
        self.assertIn("Error:", reponse.get_data(as_text=True))

    def test_post_sans_champ(self):
        """Un POST sans champ 'display' est traité comme une expression vide."""
        reponse = self.client.post("/", data={})
        self.assertEqual(reponse.status_code, 200)
        self.assertIn("Error: empty expression", reponse.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()