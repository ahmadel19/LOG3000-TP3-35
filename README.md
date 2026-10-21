# LOG3000 - TP3 - ÉQUIPE 35

## Description 
Application web de calculatrice simple développée avec Flask.

## Objectif 
L'objectif est de configurer le projet sur GitHub afin de mieux collaborer, documenter le dépôt et la base de code, puis réaliser des tests et des corrections de bogues. 

## Prérequis 
- Un compte GitHub
- Git installé localement
- Python installé
- pip installé

## Installation
1. Cloner le dépôt :
  ```bash
  git clone https://github.com/ahmadel19/LOG3000-TP3-35.git
  ```
2. Se déplacer dans le dossier du projet :
   ```bash
   cd LOG3000-TP3-35
   ```
3. Installer Flask :
   ```bash
   pip install flask
   ```
4. Lancer l'application :
   ```bash
   python app.py
   ```
5. Ouvrir l'adresse affichée dans le terminal dans un navigateur afin d'accéder à l'application.

## Utilisation
1. Ouvrir l'application dans un navigateur.
2. Utiliser les boutons de la calculatrice pour entrer une expression mathématique.
3. Cliquer sur `=` pour envoyer l'expression au serveur.
4. Le résultat du calcul est affiché dans la zone d'affichage.
5. Utiliser le bouton `C` pour effacer l'expression.

## Structure du projet

```text
LOG3000-TP3-35/
├── app.py
├── operators.py
├── README.md
├── static/
│   ├── README.md
│   └── style.css
└── templates/
   ├── README.md
   └── index.html
```

## Tests

Les tests automatisés seront ajoutés dans un répertoire `tests/`.

Pour exécuter les tests, il faut faire la commande suivante : 
```bash
pytest
```

## Flux de contribution
Le projet utilise Git et GitHub pour gérer les modifications.
1. Une issue GitHub est créée lorsqu'un bogue est identifié.
2. Une branche séparée est créée pour chaque issue.
3. Les modifications sont effectuées et testées sur cette branche.
4. Les changements sont validés avec des messages de commit clairs. 
5. Une Pull Request est ouverte pour faire réviser les changements. 
6. Après validation, la branche est fusionnée dans `main`.
