# RUNBOOK — FicheLab

Composeur visuel de fiches d'exercices de maths qui **génère les PDF en local**
via le moteur **Pyromaths** (vendorisé sous GPLv3 dans `engines/pyromaths`).
Aucun appel sortant à un service tiers : énoncés, corrigés et compilation LaTeX
se passent intégralement sur la machine.

## Prérequis

- **Python 3.11+** (testé sur 3.14 ; le `.venv` du dépôt tourne sur 3.14.5).
- **Windows / PowerShell** (les commandes ci-dessous utilisent `.\.venv\Scripts\python.exe`).
- **Une chaîne LaTeX installée** : **MiKTeX** ou **TeX Live**, exposant
  `lualatex` et `latexmk` sur le `PATH`. Indispensable pour la génération PDF.

### Installation

```powershell
cd "C:\Users\rachi\OneDrive\Documents\FicheLab"
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip install -e engines\pyromaths
```

> `backend/pyromaths_engine.py` insère `engines/pyromaths` dans `sys.path` au
> chargement, donc l'import fonctionne aussi sans `pip install -e`. La commande
> editable reste recommandée — elle rend `pyromaths` discoverable hors du contexte
> FicheLab (tests isolés, scripts ad hoc).

## Démarrer

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.app:app --reload
```

Puis ouvrir **http://localhost:8000**.

- Port : **8000** (port par défaut d'uvicorn). En cas de conflit : `--port 8001`.
- L'interface `web/` n'a **pas** besoin d'un serveur séparé : `backend/app.py` monte
  `web/` en statique sur `/`. Ouvrir la racine sert directement `web/index.html`,
  sur le même port que l'API (`/api/...`).

### CLI (régénérer une fiche sans l'interface)

```powershell
# Lister les exercices Pyromaths (filtres possibles)
.\.venv\Scripts\python.exe -m backend.cli pyromaths-list --niveau Quatrième --search fraction

# Générer le PDF d'une fiche
.\.venv\Scripts\python.exe -m backend.cli pyromaths-gen fiches\exemple-pyromaths-4e.json -o ma-fiche.pdf --open
```

## Tester

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest backend\tests -q
```

Ce que ça vérifie :
- **`backend\tests\test_pyromaths_engine.py`** — catalogue Pyromaths,
  reproductibilité des blocs par graine, injection du style maison dans
  la source LaTeX (sans compilation PDF).
- **`backend\tests\test_bibliotheque.py`** — chaque fiche `.json` livrée
  dans `fiches/` a une structure minimale valide (titre, exercices avec
  `name`).

> Attention : `test_pyromaths_engine.py` débute par
> `pytest.importorskip("backend.pyromaths_engine")`. **Sans le moteur Pyromaths
> installé, ces tests sont silencieusement SAUTÉS (skipped), pas échoués.**

**Vérification de fumée** (sans tests) : lancer le backend, ouvrir
http://localhost:8000, composer une fiche, cliquer « Générer le PDF » dans la
colonne de droite — le PDF doit se télécharger.

## Maintenir

Où vivent les données :
- **`fiches/`** — tes fiches enregistrées, un fichier `.json` par fiche
  (`backend/fiches.py`). Versionnables (OneDrive / git), reproductibles : la
  `seed` de chaque exercice est figée, donc régénérer redonne exactement la
  même fiche/PDF. Exemple livré : `exemple-pyromaths-4e.json`.
- **`styles/`** — `style.json` (couleur principale, établissement, en-tête,
  police) et `fiche.tex.j2` (gabarit LaTeX complet).
- **`fonts/`** — tes polices `.ttf`/`.otf` perso. Le nom à utiliser dans
  `style.json` est le nom fontspec de la police.
- **`engines/pyromaths/`** — moteur Pyromaths vendorisé (GPLv3, gelé 2023,
  3 patchs Python 3.14 ; cf. `engines/README.md`). Ne pas modifier les exercices.

Ajouter / régénérer une fiche :
- **Via l'UI** : composer puis enregistrer (POST `/api/fiche` → écrit
  `fiches/<slug>.json`, slug dérivé du titre).
- **À la main** : copier un `.json` existant dans `fiches/`, l'éditer, puis
  régénérer avec `pyromaths-gen`.

Autres opérations :
- **Changer le style** : éditer `styles/style.json` (rapide) ou
  `styles/fiche.tex.j2` (gabarit complet). Pour une police perso : la déposer
  dans `fonts/` et renseigner son nom dans `style.json`.

## Dépanner

| Symptôme | Cause probable | Solution |
|---|---|---|
| `ModuleNotFoundError: No module named 'uvicorn'` (ou `fastapi`) | Dépendances non installées dans le venv | `.\.venv\Scripts\python.exe -m pip install -r requirements.txt` |
| `'.venv' n'est pas reconnu` / mauvais Python utilisé | venv absent ou commande lancée avec un Python global | Recréer (`python -m venv .venv`) et toujours préfixer par `.\.venv\Scripts\python.exe` |
| `[Errno 10048] address already in use` au lancement d'uvicorn | Port **8000** déjà occupé (instance déjà lancée) | Fermer l'autre instance, ou changer de port : `--port 8001` |
| `No module named 'backend'` | Commande lancée hors de la racine du projet | Se replacer dans `C:\Users\rachi\OneDrive\Documents\FicheLab` avant de lancer |
| `No module named pytest` | `pytest` non installé | `.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt` |
| `ModuleNotFoundError: pyromaths` (catalogue vide ou échec génération) | Moteur Pyromaths non installé editable | `.\.venv\Scripts\python.exe -m pip install -e engines\pyromaths` |
| HTTP 500 « Génération échouée » avec trace `latexmk` introuvable | Chaîne LaTeX absente | Installer **MiKTeX** ou **TeX Live** ; vérifier `latexmk` et `lualatex` sur le `PATH` (rouvrir le terminal) |
| `RuntimeError: Compilation LaTeX échouée. Dossier conservé pour diagnostic : <tmp>` | latexmk présent mais aucun PDF produit (paquet manquant, erreur de gabarit) | Relancer en `--verbose`, inspecter `.tex`/`.log` dans le dossier temporaire conservé ; vérifier MiKTeX/lualatex |

> Rédigé le 2026-06-14, mis à jour le 2026-06-16 (excision MathALEA, moteur unique Pyromaths).
