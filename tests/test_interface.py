"""Tests de l'interface HTML rendue par ``templates/index.html``.

La page est obtenue via le client de test Flask, puis analysée avec
``html.parser`` (bibliothèque standard) pour retrouver chaque bouton, le
caractère qu'il ajoute à l'écran et le libellé que voit l'utilisateur.
"""

import os
import re
import sys
import unittest
from html.parser import HTMLParser

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app  # noqa: E402

# Libellés acceptés pour les opérateurs : le symbole ASCII ou son équivalent
# typographique usuel sur une calculatrice.
LIBELLES_ACCEPTES = {
    "*": {"*", "×"},
    "/": {"/", "÷"},
}


class _ExtracteurBoutons(HTMLParser):
    """Collecte les boutons de la page sous forme de (onclick, type, libellé)."""

    def __init__(self):
        super().__init__()
        self.boutons = []
        self._courant = None

    def handle_starttag(self, tag, attrs):
        """Démarre la capture d'un bouton et mémorise ses attributs utiles."""
        if tag == "button":
            attributs = dict(attrs)
            self._courant = {
                "onclick": attributs.get("onclick", ""),
                "type": attributs.get("type", ""),
                "libelle": "",
            }

    def handle_data(self, data):
        """Accumule le texte visible du bouton en cours de capture."""
        if self._courant is not None:
            self._courant["libelle"] += data

    def handle_endtag(self, tag):
        """Termine la capture du bouton courant."""
        if tag == "button" and self._courant is not None:
            self._courant["libelle"] = self._courant["libelle"].strip()
            self.boutons.append(self._courant)
            self._courant = None


class TestInterface(unittest.TestCase):
    """Cohérence entre les boutons affichés et ce qu'ils envoient."""

    @classmethod
    def setUpClass(cls):
        """Rend la page une seule fois et extrait la liste des boutons."""
        app.config["TESTING"] = True
        html = app.test_client().get("/").get_data(as_text=True)
        extracteur = _ExtracteurBoutons()
        extracteur.feed(html)
        cls.boutons = extracteur.boutons
        # Associe le caractère ajouté par appendToDisplay('x') au libellé affiché.
        cls.saisie_vers_libelle = {}
        for bouton in cls.boutons:
            m = re.search(r"appendToDisplay\('(.)'\)", bouton["onclick"])
            if m:
                cls.saisie_vers_libelle[m.group(1)] = bouton["libelle"]

    def test_tous_les_chiffres_ont_un_bouton(self):
        """Les dix chiffres 0 à 9 peuvent être saisis."""
        for chiffre in "0123456789":
            self.assertIn(chiffre, self.saisie_vers_libelle, f"aucun bouton pour {chiffre}")

    def test_libelle_des_chiffres(self):
        """Chaque bouton de chiffre affiche exactement le chiffre qu'il ajoute."""
        for chiffre in "0123456789":
            with self.subTest(chiffre=chiffre):
                self.assertEqual(self.saisie_vers_libelle.get(chiffre), chiffre)

    def test_libelle_des_operateurs(self):
        """Chaque bouton d'opérateur affiche son symbole (jamais un bouton vide)."""
        for operateur in "+-*/":
            with self.subTest(operateur=operateur):
                acceptes = LIBELLES_ACCEPTES.get(operateur, {operateur})
                self.assertIn(self.saisie_vers_libelle.get(operateur), acceptes)

    def test_boutons_egal_et_effacer(self):
        """Il existe un bouton '=' qui soumet le formulaire et un bouton 'C' qui efface."""
        egal = [b for b in self.boutons if b["libelle"] == "="]
        self.assertEqual(len(egal), 1)
        self.assertEqual(egal[0]["type"], "submit")
        effacer = [b for b in self.boutons if b["libelle"] == "C"]
        self.assertEqual(len(effacer), 1)
        self.assertIn("clearDisplay", effacer[0]["onclick"])


if __name__ == "__main__":
    unittest.main()