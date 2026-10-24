"""Tests unitaires des fonctions arithmétiques de ``operators.py``.

Chaque fonction est vérifiée isolément, sans passer par Flask ni par
``calculate``, pour qu'un échec pointe directement vers la fonction fautive.
"""

import os
import sys
import unittest

# Rend les modules de la racine (app.py, operators.py) importables, que les tests
# soient lancés avec unittest ou pytest, depuis n'importe quel dossier.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from operators import add, subtract, multiply, divide  # noqa: E402


class TestAdd(unittest.TestCase):
    """Vérifie que ``add(a, b)`` retourne ``a + b``."""

    def test_entiers_positifs(self):
        """2 + 3 doit donner 5."""
        self.assertEqual(add(2, 3), 5)

    def test_negatif_et_zero(self):
        """L'addition avec un négatif ou avec zéro suit l'arithmétique usuelle."""
        self.assertEqual(add(-4, 1), -3)
        self.assertEqual(add(7, 0), 7)

    def test_decimaux(self):
        """Les flottants sont additionnés (comparaison approchée)."""
        self.assertAlmostEqual(add(0.1, 0.2), 0.3)


class TestSubtract(unittest.TestCase):
    """Vérifie que ``subtract(a, b)`` retourne ``a - b`` (ordre des opérandes)."""

    def test_ordre_des_operandes(self):
        """5 - 3 doit donner 2 et non -2 : l'opérande de gauche est le diminuende."""
        self.assertEqual(subtract(5, 3), 2)

    def test_resultat_negatif(self):
        """3 - 5 doit donner -2."""
        self.assertEqual(subtract(3, 5), -2)

    def test_soustraire_zero(self):
        """Soustraire 0 laisse le nombre inchangé."""
        self.assertEqual(subtract(9, 0), 9)


class TestMultiply(unittest.TestCase):
    """Vérifie que ``multiply(a, b)`` retourne le produit ``a * b``."""

    def test_entiers(self):
        """2 * 3 doit donner 6 (et non 2 ** 3 = 8)."""
        self.assertEqual(multiply(2, 3), 6)

    def test_par_zero(self):
        """Tout nombre multiplié par 0 donne 0."""
        self.assertEqual(multiply(5, 0), 0)

    def test_signe(self):
        """Le produit d'un négatif et d'un positif est négatif."""
        self.assertEqual(multiply(-4, 2), -8)


class TestDivide(unittest.TestCase):
    """Vérifie que ``divide(a, b)`` fait une division réelle ``a / b``."""

    def test_division_exacte(self):
        """8 / 2 doit donner 4."""
        self.assertEqual(divide(8, 2), 4)

    def test_conserve_la_partie_decimale(self):
        """7 / 2 doit donner 3.5 : une division entière (3) serait incorrecte."""
        self.assertEqual(divide(7, 2), 3.5)

    def test_negatif(self):
        """-7 / 2 doit donner -3.5 (la division entière arrondirait à -4)."""
        self.assertEqual(divide(-7, 2), -3.5)

    def test_division_par_zero(self):
        """Diviser par zéro lève ZeroDivisionError, affichée ensuite par la route."""
        with self.assertRaises(ZeroDivisionError):
            divide(1, 0)


if __name__ == "__main__":
    unittest.main()