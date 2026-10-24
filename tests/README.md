# `tests/` — Suite de tests

## Raison d'être

Vérifier automatiquement que la calculatrice respecte le comportement documenté
(docstrings de `app.py` et `operators.py`, README principal). Chaque bogue corrigé
dans le projet est couvert par au moins un test qui échouait avant le correctif.

## Exécuter les tests

Depuis la **racine du dépôt**, après avoir installé les dépendances (`pip install -r requirements.txt`) :

```bash
python -m unittest discover -s tests -v
```

Exécuter un seul fichier ou une seule classe :

```bash
python -m unittest discover -s tests -p "test_operators.py" -v
python -m unittest tests.test_calculate.TestCalculateNombresNegatifs -v
```

Les tests sont écrits avec `unittest` (bibliothèque standard) et sont aussi
exécutés par pytest : `pytest -v` depuis la racine du dépôt.

Résultat attendu sur `main` après la fusion des correctifs : `38 passed` (pytest) ou `Ran 38 tests … OK` (unittest).

## Ce que couvrent les tests

| Fichier | Niveau | Couverture |
|---|---|---|
| `test_operators.py` | Unitaire | `add`, `subtract`, `multiply`, `divide` : entiers, négatifs, zéro, décimaux, ordre des opérandes, division réelle, division par zéro. |
| `test_calculate.py` | Unitaire | `app.calculate` : une opération par opérateur, espaces, décimaux, nombres négatifs, erreurs (vide, plusieurs opérateurs, sans opérateur, opérateur en fin, opérande non numérique, division par zéro). |
| `test_routes.py` | Intégration | Route `/` via le client de test Flask : GET, POST valide, POST invalide, division par zéro, POST sans champ. |
| `test_interface.py` | Interface | Page rendue analysée avec `html.parser` : chaque chiffre a un bouton, le libellé de chaque bouton correspond au caractère qu'il ajoute, les opérateurs ne sont pas vides, présence de `=` (submit) et `C`. |

## Correspondance avec les issues

| Issue | Tests qui échouaient avant le correctif |
|---|---|
| #1 Soustraction inversée | `TestSubtract.*`, `TestCalculateOperations.test_soustraction` |
| #2 Libellés erronés des boutons 2 et 8 | `TestInterface.test_libelle_des_chiffres` |
| #3 Boutons `*` et `/` sans libellé | `TestInterface.test_libelle_des_operateurs` |
| #4 Nombres négatifs refusés | `TestCalculateNombresNegatifs.*` |

Les tests de `multiply()` et `divide()` passent dès leur ajout : ces deux fonctions
avaient été corrigées lors de la phase de documentation (commit `ce52470`).

## Dépendances et hypothèses

- Flask doit être installé (`pip install -r requirements.txt`).
- Chaque fichier ajoute la racine du dépôt à `sys.path` pour importer `app` et
  `operators` ; les tests peuvent donc être lancés depuis la racine sans
  configuration supplémentaire.
- Aucun serveur n'est lancé : les tests de route et d'interface utilisent
  `app.test_client()`.