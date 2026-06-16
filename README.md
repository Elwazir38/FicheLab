# FicheLab

[![CI](https://github.com/Elwazir38/FicheLab/actions/workflows/ci.yml/badge.svg)](https://github.com/Elwazir38/FicheLab/actions/workflows/ci.yml)

Composeur **visuel** de fiches d'exercices de maths, prêtes à imprimer en PDF.
Catalogue navigable par niveau, exercices ajoutés à la souris, mise en page
réglable, **PDF généré en local** avec ton style maison — sans dépendre
d'aucun service en ligne.

Le moteur de génération est **Pyromaths** (vendorisé sous GPLv3 dans
`engines/pyromaths/`) : énoncés et corrigés détaillés produits par Python,
compilés en PDF via une chaîne LaTeX locale.

## Ce que ça fait

- Catalogue navigable par niveau (Sixième → Troisième aujourd'hui ; CM1/CM2 et
  Seconde en cours d'ajout).
- Constructeur de fiche : ajout, réordonnancement (glisser-déposer), nombre
  d'occurrences de chaque exercice, corrigé on/off.
- **Génération PDF locale** en un clic, avec ton style (couleur, établissement,
  police, en-tête élève).
- Chaque fiche est un **fichier `.json` reproductible** (`fiches/`) : la `seed`
  de chaque exercice est figée, donc régénérer redonne exactement les mêmes
  énoncés et corrigés.
- **CLI** pour régénérer une fiche sans ouvrir l'interface.

## Installation

Prérequis : Python 3.11+ (testé sur 3.14) + une chaîne LaTeX (**MiKTeX** ou
**TeX Live**) exposant `lualatex` et `latexmk` sur le `PATH`.

```powershell
cd "C:\Users\rachi\OneDrive\Documents\FicheLab"
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip install -e engines\pyromaths
```

## Lancer l'application

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.app:app --reload
```

Puis ouvrir **http://localhost:8000**.

## CLI

```powershell
# Lister les exercices Pyromaths disponibles (filtres possibles)
.\.venv\Scripts\python.exe -m backend.cli pyromaths-list --niveau Quatrième --search fraction

# Générer le PDF d'une fiche
.\.venv\Scripts\python.exe -m backend.cli pyromaths-gen fiches\exemple-pyromaths-4e.json -o ma-fiche.pdf --open
```

## Tests

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest backend\tests -q
```

## Structure

```
FicheLab/
├── backend/
│   ├── app.py               API FastAPI + service de l'UI
│   ├── pyromaths_engine.py  catalogue + génération via Pyromaths
│   ├── render.py            blocs -> LaTeX (template maison) -> PDF lualatex
│   ├── style.py             chargement du style maison (styles/style.json)
│   ├── fiches.py            sauvegarde des manifestes .json
│   ├── cli.py               régénération en ligne de commande
│   └── tests/
├── engines/pyromaths/  moteur Pyromaths vendorisé (GPLv3, gelé 2023 + 3 patchs Py3.14)
├── fiches/             tes fiches enregistrées (.json, versionnables)
├── styles/             style.json + fiche.tex.j2 (gabarit LaTeX)
├── fonts/              tes polices personnelles (facultatif)
├── web/                interface (index.html, app.js, style.css, onboarding.js)
└── requirements.txt
```

## Format d'une fiche (`fiches/*.json`)

```json
{
  "version": 1,
  "titre": "4ème — Calcul littéral — Pyromaths",
  "niveau": "Quatrième",
  "entete": { "classe": "4ème B", "date": "16/06/2026" },
  "mise_en_page": { "corrige": true },
  "exercices": [
    { "source": "pyromaths", "name": "distributivite", "seed": 11, "nb": 1 },
    { "source": "pyromaths", "name": "double_distributivite", "seed": 5, "nb": 1 }
  ]
}
```

`name` = identifiant Pyromaths (cf. `pyromaths-list`) · `seed` = graine figée
(reproductible) · `nb` = nombre de copies de l'exercice · `source` reste
explicite pour anticiper l'arrivée de moteurs complémentaires.

## Style maison

Le style se règle à deux endroits :

- `styles/style.json` : couleur principale, établissement, police, en-tête élève.
- `fonts/` : dépose ton `.ttf`/`.otf`, puis renseigne son nom dans
  `style.json` (`"police": "Nom De La Police"`). Sinon, police par défaut propre.
- `styles/fiche.tex.j2` : le gabarit LaTeX complet, si tu veux pousser plus loin.

> Note de portage : Pyromaths est gelé (2023) ; trois patchs Python 3.14 sont
> appliqués dans `engines/pyromaths` (voir `engines/README.md`).

## Feuille de route

- **Ajouter CM1 / CM2** alignés sur le programme officiel cycle 3 (BO du
  17 avril 2025, applicable rentrée 2025).
- **Brancher Seconde** à partir des générateurs `engines/pyromaths/pyromaths/ex/lycee/`
  réellement programme Seconde (tri à faire avec un sous-agent).
- **Pipeline LLM local** (LM Studio + Gemma / Qwen-Coder) ciblé sur la taxonomie
  BOEN, les contextes d'énoncés textuels et le boilerplate Python — pas sur la
  génération mathématique elle-même, que la `seed` Pyromaths gère déjà.
