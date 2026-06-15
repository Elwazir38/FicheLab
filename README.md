# FicheLab

Composeur **visuel** de fiches d'exercices de maths, prêtes à imprimer en PDF.
Il pilote le moteur public **MathALEA** (CoopMaths) : tu choisis des exercices
dans un catalogue par niveau / thème, tu règles chaque exercice, et tu obtiens
une fiche complète avec corrigé — sans réinventer le générateur.

> **Principe / licence.** FicheLab **n'embarque aucun code de MathALEA** (AGPL-3.0).
> Il se contente de **composer des URLs** vers `coopmaths.fr/alea/`, comme un
> signet intelligent. Le PDF est produit côté MathALEA.

## Ce que ça fait (v1)

- Catalogue navigable **6e / 5e / 4e / 3e** (référentiels officiels MathALEA, thèmes + intitulés).
- Constructeur de fiche : ajout, réordonnancement (glisser-déposer), nombre de
  questions, réglages avancés (`s`, `s2`, `s3`), corrigé on/off, colonnes.
- **Aperçu live** intégré (vue élève / diaporama / LaTeX).
- **Génération PDF** en un clic (ouvre la page d'export de MathALEA).
- Chaque fiche est un **fichier `.json` reproductible** (`fiches/`) : la graine
  `alea` est figée, donc régénérer redonne exactement les mêmes énoncés/corrigés.
- **CLI** pour régénérer une fiche sans ouvrir l'interface.

## Installation

Prérequis : Python 3.11+ (testé sur 3.14).

```powershell
cd "C:\Users\rachi\OneDrive\Documents\FicheLab"
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Lancer l'application

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.app:app --reload
```

Puis ouvrir **http://localhost:8000**.

## CLI (régénération)

```powershell
# Construit l'URL d'une fiche et l'ouvre dans le navigateur
.\.venv\Scripts\python.exe -m backend.cli build fiches\ma-fiche.json

# Affiche juste l'URL (sans ouvrir)
.\.venv\Scripts\python.exe -m backend.cli url fiches\ma-fiche.json

# Régénère tout un dossier de fiches
.\.venv\Scripts\python.exe -m backend.cli build-all fiches\
```

## Tests

```powershell
.\.venv\Scripts\python.exe -m pip install pytest
.\.venv\Scripts\python.exe -m pytest backend\tests -q
```

## Structure

```
FicheLab/
├── backend/
│   ├── app.py          API FastAPI + service de l'UI
│   ├── mathalea.py     manifeste -> URL MathALEA (cœur, testé)
│   ├── catalogue.py    chargement des référentiels par niveau/thème
│   ├── fiches.py       sauvegarde des manifestes .json
│   ├── cli.py          régénération en ligne de commande
│   └── tests/
├── data/mathalea_raw/  référentiels officiels MathALEA (source du catalogue)
├── fiches/             tes fiches enregistrées (.json, versionnables)
├── web/                interface (index.html, app.js, style.css)
└── requirements.txt
```

## Format d'une fiche (`fiches/*.json`)

```json
{
  "version": 1,
  "titre": "4ème — Fractions — Fiche 1",
  "entete": { "classe": "4ème B", "date": "2026-06-15" },
  "mise_en_page": { "colonnes": 2, "corrige": true, "vue": "eleve" },
  "exercices": [
    { "id": "4C21", "titre": "Additionner...", "source": "mathalea",
      "n": 4, "sup": {}, "cd": null, "uuid": "ab12c", "alea": "VAQ7" }
  ]
}
```

`id` = code de l'exercice MathALEA · `n` = nombre de questions ·
`sup` = réglages avancés · `alea`/`uuid` = graines figées (reproductibilité).

## Pyromaths (génération 100 % locale, ton style)

Phase 2 : un second moteur, **Pyromaths** (vendorisé dans `engines/pyromaths`,
GPLv3), qui génère les fiches **en local** avec corrigés très détaillés, **sans
passer par aucun site**, rendues avec **ton template** (`styles/`).

Prérequis : une chaîne LaTeX (**MiKTeX** ou TeX Live) avec `lualatex` + `latexmk`.

**Ton style** se règle à deux endroits :
- `styles/style.json` : couleur principale, établissement, en-tête élève, police.
- `fonts/` : dépose ton fichier `.ttf`/`.otf`, puis renseigne son nom dans
  `style.json` (`"police": "Nom De La Police"`). Sinon, police par défaut propre.
- `styles/fiche.tex.j2` : le gabarit LaTeX complet, si tu veux pousser plus loin.

Depuis l'interface : onglet **Pyromaths** dans le catalogue → ajoute des
exercices → **« PDF Pyromaths (local) »**.

Depuis **Claude Code / la CLI** :

```powershell
# Lister les exercices Pyromaths (filtres possibles)
.\.venv\Scripts\python.exe -m backend.cli pyromaths-list --niveau Quatrième --search fraction

# Générer le PDF stylé d'une fiche
.\.venv\Scripts\python.exe -m backend.cli pyromaths-gen fiches\exemple-pyromaths-4e.json -o ma-fiche.pdf --open
```

Format d'une fiche Pyromaths (`exercices[].source = "pyromaths"`) :

```json
{ "titre": "4ème — Calcul littéral", "niveau": "Quatrième",
  "entete": { "classe": "4ème B", "date": "16/06/2026" },
  "mise_en_page": { "corrige": true },
  "exercices": [ { "source": "pyromaths", "name": "distributivite", "seed": 11, "nb": 1 } ] }
```

`name` = identifiant Pyromaths (cf. `pyromaths-list`) · `seed` = graine figée
(reproductible) · `nb` = nombre de copies de l'exercice.

> Note de portage : Pyromaths est gelé (2023) ; trois patchs Python 3.14 sont
> appliqués dans `engines/pyromaths` (voir `engines/README.md`).

## Feuille de route

- **Fusion MathALEA + Pyromaths en un seul PDF** (prochaine étape) : capturer le
  LaTeX MathALEA en local et le compiler avec Pyromaths sous le template maison.
- Ajout des niveaux lycée MathALEA (déposer le référentiel dans `data/mathalea_raw/`).
