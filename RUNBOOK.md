# RUNBOOK — FicheLab

Composeur visuel de fiches d'exercices de maths qui **pilote le moteur public MathALEA**
(CoopMaths) en composant des URLs. FicheLab **n'embarque aucun code MathALEA** (AGPL-3.0) :
le PDF est produit côté `coopmaths.fr/alea/`. Un second moteur local **Pyromaths** (vendorisé,
GPLv3) génère des fiches hors-ligne avec un template maison.

## Prérequis

- **Python 3.11+** (testé sur 3.14 ; le `.venv` du dépôt tourne sur 3.14.5).
  > À CONFIRMER : pas de fichier `.python-version` dans le dépôt ; la version vient du `README.md`.
- **Windows / PowerShell** (les commandes ci-dessous utilisent `.\.venv\Scripts\python.exe`).
- Pour Pyromaths uniquement : une chaîne LaTeX (**MiKTeX** ou TeX Live) exposant `lualatex` + `latexmk` sur le `PATH`. Inutile pour le moteur MathALEA.

> **Installation à deux niveaux.** `pip install -r requirements.txt` n'installe que `fastapi` + `uvicorn[standard]` — soit le moteur **MathALEA** (composition d'URLs), l'UI et les tests du cœur. Il **n'installe ni `pytest`, ni le moteur Pyromaths, ni LaTeX**. Pour générer des PDF Pyromaths en local, faire aussi l'installation complète ci-dessous.

### Installation minimale (moteur MathALEA + UI)

```powershell
cd "C:\Users\rachi\OneDrive\Documents\FicheLab"
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### Installation complète (ajoute le moteur Pyromaths local)

À faire **en plus**, pour générer des PDF Pyromaths stylés (nécessite aussi LaTeX) :

```powershell
.\.venv\Scripts\python.exe -m pip install -e engines\pyromaths
```

> À CONFIRMER : nécessité réelle de `pip install -e engines\pyromaths`. `backend/pyromaths_engine.py` insère `engines/pyromaths` dans `sys.path` au chargement, donc `import pyromaths` pourrait fonctionner **sans** install editable. `engines/README.md` documente quand même cette commande — la conserver par sécurité tant que ce point n'est pas tranché.

## Démarrer

Installation faite (§ Prérequis), depuis la racine du projet :

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.app:app --reload
```

Puis ouvrir **http://localhost:8000**.

- Port : **8000** (port par défaut d'uvicorn ; `backend/app.py` ne le surcharge pas). En cas de conflit : ajouter `--port 8001` et ouvrir `http://localhost:8001`.
- L'interface `web/` n'a **pas** besoin d'un serveur séparé : `backend/app.py` monte
  `web/` en statique sur `/` (`app.mount("/", StaticFiles(directory=WEB_DIR, html=True))`).
  Ouvrir la racine sert directement `web/index.html`, sur le même port que l'API (`/api/...`).

### CLI (régénérer une fiche sans l'interface)

```powershell
# Composer l'URL MathALEA d'une fiche et l'ouvrir dans le navigateur
.\.venv\Scripts\python.exe -m backend.cli build fiches\ma-fiche.json

# Afficher seulement l'URL (sans ouvrir)
.\.venv\Scripts\python.exe -m backend.cli url fiches\ma-fiche.json

# Régénérer tout un dossier de fiches
.\.venv\Scripts\python.exe -m backend.cli build-all fiches\

# Pyromaths (génération PDF 100 % locale, nécessite LaTeX)
.\.venv\Scripts\python.exe -m backend.cli pyromaths-list --niveau Quatrième --search fraction
.\.venv\Scripts\python.exe -m backend.cli pyromaths-gen fiches\exemple-pyromaths-4e.json -o ma-fiche.pdf --open
```

## Tester

`pytest` n'est **pas** dans `requirements.txt` (juste une note) : l'installer d'abord.
Lancer depuis la **racine** `FicheLab` (sinon `No module named 'backend'`).

```powershell
.\.venv\Scripts\python.exe -m pip install pytest
.\.venv\Scripts\python.exe -m pytest backend\tests -q
```

Ce que ça vérifie :
- **`backend\tests\test_mathalea.py`** — le cœur : manifeste → URL MathALEA (ordre des
  paramètres, chaînage multi-exercices, réglages `sup`, `cd` corrigé, vue invalide,
  reproductibilité, idempotence du gel `uuid`/`alea`). **Tourne sur l'installation minimale.**
- **`backend\tests\test_pyromaths_engine.py`** — catalogue Pyromaths, reproductibilité des
  blocs par graine, injection du style maison dans le LaTeX (sans compilation PDF).

> Attention : `test_pyromaths_engine.py` débute par `pytest.importorskip("backend.pyromaths_engine")`.
> **Sans le moteur Pyromaths installé, ces tests sont silencieusement SAUTÉS (skipped), pas
> échoués.** Un « tout passe » sur l'installation minimale ne couvre donc que le moteur MathALEA ;
> pour valider Pyromaths, faire d'abord l'installation complète.

**Vérification de fumée** (sans tests) : lancer le backend, ouvrir http://localhost:8000,
composer une fiche, et vérifier que le bouton de génération PDF ouvre bien une URL
`coopmaths.fr/alea/...` — c'est la frontière de licence : FicheLab compose l'URL, MathALEA
produit le PDF.

## Maintenir

Où vivent les données :
- **`fiches/`** — tes fiches enregistrées, **un fichier `.json` par fiche** (`backend/fiches.py`).
  Versionnables (OneDrive / git), reproductibles : les graines (`uuid`/`alea` pour MathALEA,
  `seed` pour Pyromaths) sont figées, donc régénérer redonne exactement la même fiche/PDF.
  Exemples livrés : `demo-4eme-fractions.json`, `exemple-pyromaths-4e.json`.
- **`data/mathalea_raw/`** — référentiels officiels MathALEA (source du catalogue). Source
  faisant autorité : `allExercice.json`. Les `*AvecSousThemes.json` ne servent qu'aux
  **libellés** de thèmes (`backend/catalogue.py`).
- **`styles/`** — `style.json` (couleur principale, établissement, en-tête, police) et
  `fiche.tex.j2` (gabarit LaTeX Pyromaths).
- **`engines/pyromaths/`** — moteur Pyromaths vendorisé (GPLv3, gelé 2023, 3 patchs Python 3.14 ;
  cf. `engines/README.md`). Ne pas modifier les exercices.

Ajouter / régénérer une fiche :
- **Via l'UI** : composer puis enregistrer (POST `/api/fiche` → écrit `fiches/<slug>.json`,
  slug dérivé du titre).
- **À la main** : copier un `.json` existant dans `fiches/`, l'éditer, puis régénérer avec la CLI
  (`build` pour MathALEA, `pyromaths-gen` pour Pyromaths).
- **En lot** : `.\.venv\Scripts\python.exe -m backend.cli build-all fiches\`.

Autres opérations :
- **Ajouter un niveau MathALEA** (ex. lycée) : déposer le référentiel dans `data/mathalea_raw/`
  puis l'exposer dans `LEVELS` de `backend/catalogue.py`. Le catalogue est mis en cache
  (`lru_cache`) → **redémarrer le serveur** après modification des données.
- **Changer le style des PDF Pyromaths** : éditer `styles/style.json` (rapide) ou
  `styles/fiche.tex.j2` (gabarit complet). Pour une police perso : la déposer dans `fonts/` et
  renseigner son nom dans `style.json`.

## Dépanner

| Symptôme | Cause probable | Solution |
|---|---|---|
| `ModuleNotFoundError: No module named 'uvicorn'` (ou `fastapi`) | Dépendances non installées dans le venv | `.\.venv\Scripts\python.exe -m pip install -r requirements.txt` |
| `'.venv' n'est pas reconnu` / mauvais Python utilisé | venv absent ou commande lancée avec un Python global | Recréer (`python -m venv .venv`) et toujours préfixer par `.\.venv\Scripts\python.exe` |
| `[Errno 10048] address already in use` au lancement d'uvicorn | Port **8000** déjà occupé (instance déjà lancée) | Fermer l'autre instance, ou changer de port : `... -m uvicorn backend.app:app --reload --port 8001` puis ouvrir `http://localhost:8001` |
| `No module named 'backend'` | Commande lancée hors de la racine du projet | Se replacer dans `C:\Users\rachi\OneDrive\Documents\FicheLab` avant de lancer |
| `pytest : commande introuvable` / `No module named pytest` | `pytest` non installé (volontairement hors `requirements.txt`) | `.\.venv\Scripts\python.exe -m pip install pytest` |
| Tests Pyromaths « skipped » ; ou `ModuleNotFoundError: pyromaths` (CLI/onglet Pyromaths) | Moteur non installé : `test_pyromaths_engine.py` fait `pytest.importorskip(...)` et saute, et `backend.pyromaths_engine` est chargé paresseusement | Faire l'installation complète (`pip install -e engines\pyromaths`) |
| `pyromaths-gen` : traceback `latexmk` introuvable ; via l'API **HTTP 500 « Génération échouée »** | `render.py` appelle `subprocess.run(["latexmk", ...])` **sans garde `FileNotFoundError`** | Installer **MiKTeX** ou TeX Live ; vérifier `latexmk` **et** `lualatex` sur le `PATH` (rouvrir le terminal). Les commandes MathALEA (`build`/`url`) marchent sans LaTeX |
| `RuntimeError: Compilation LaTeX échouée. Dossier conservé pour diagnostic : <tmp>` | latexmk présent mais aucun PDF produit (paquet manquant, erreur de gabarit) | Relancer en `--verbose` et inspecter `.tex`/`.log` dans le dossier temporaire conservé ; vérifier MiKTeX/lualatex |
| Aperçu / export PDF qui n'ouvre rien dans le navigateur | `coopmaths.fr` indisponible. FicheLab **ne fait que composer une URL** (`backend/mathalea.py`) : l'app et la CLI n'échouent pas, seul l'export côté MathALEA échoue | Ne pas chercher de bug dans FicheLab : vérifier l'accès à `https://coopmaths.fr/alea/` et réessayer. L'URL reste valide et reproductible (graines figées) |

> Rédigé le 2026-06-14 par sous-agent docs (lecture du code).
