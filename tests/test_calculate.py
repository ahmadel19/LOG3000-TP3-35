"""Tests de ``app.calculate`` : analyse d'une expression texte et calcul.

Ces tests vérifient le contrat de ``calculate`` tel que décrit dans sa
docstring : une seule opération binaire, espaces ignorés, opérandes réels,
et des erreurs explicites pour les expressions invalides.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import calculate  # noqa: E402


class TestCalculateOperations(unittest.TestCase):
    """Une expression valide par opérateur donne le bon résultat."""

    def test_addition(self):
        """'2+3' vaut 5."""
        self.assertEqual(calculate("2+3"), 5)

    def test_soustraction(self):
        """'9-4' vaut 5 (opérande de gauche moins opérande de droite)."""
        self.assertEqual(calculate("9-4"), 5)

    def test_multiplication(self):
        """'6*7' vaut 42."""
        self.assertEqual(calculate("6*7"), 42)

    def test_division(self):
        """'7/2' vaut 3.5."""
        self.assertEqual(calculate("7/2"), 3.5)


class TestCalculateFormat(unittest.TestCase):
    """Tolérance aux variations de format permises par le contrat."""

    def test_espaces_ignores(self):
        """Les espaces autour et entre les opérandes sont ignorés."""
        self.assertEqual(calculate("  12 +  30 "), 42)

    def test_decimaux(self):
        """Les opérandes décimaux sont acceptés."""
        self.assertAlmostEqual(calculate("1.5+2.25"), 3.75)

    def test_resultat_est_un_float(self):
        """Les opérandes sont convertis en float, donc le résultat aussi."""
        self.assertIsInstance(calculate("2+3"), float)


class TestCalculateNombresNegatifs(unittest.TestCase):
    """Un signe '-' en tête d'opérande est un signe, pas un opérateur.

    Les cas utilisent l'addition pour isoler l'analyse de l'expression du
    comportement des autres opérateurs.
    """

    def test_premier_operande_negatif(self):
        """'-3+2' vaut -1 : le '-' initial est le signe de 3."""
        self.assertEqual(calculate("-3+2"), -1)

    def test_second_operande_negatif(self):
        """'3+-2' vaut 1 : le '-' qui suit l'opérateur est le signe de 2."""
        self.assertEqual(calculate("3+-2"), 1)

    def test_deux_operandes_negatifs(self):
        """'-3+-2' vaut -5."""
        self.assertEqual(calculate("-3+-2"), -5)


class TestCalculateErreurs(unittest.TestCase):
    """Les expressions invalides lèvent une erreur explicite."""

    def test_expression_vide(self):
        """Une chaîne vide est refusée."""
        with self.assertRaises(ValueError):
            calculate("")

    def test_plusieurs_operateurs(self):
        """'1+2+3' est refusé : une seule opération est permise."""
        with self.assertRaisesRegex(ValueError, "only one operator"):
            calculate("1+2+3")

    def test_sans_operateur(self):
        """'42' est refusé : il faut un opérateur."""
        with self.assertRaises(ValueError):
            calculate("42")

    def test_operateur_en_fin(self):
        """'5*' est refusé : il manque l'opérande de droite."""
        with self.assertRaises(ValueError):
            calculate("5*")

    def test_operande_non_numerique(self):
        """'a+1' est refusé avec un message sur les opérandes."""
        with self.assertRaisesRegex(ValueError, "operands must be numbers"):
            calculate("a+1")

    def test_division_par_zero(self):
        """'5/0' lève ZeroDivisionError."""
        with self.assertRaises(ZeroDivisionError):
            calculate("5/0")


if __name__ == "__main__":
    unittest.main()