# JOURNAL — FicheLab

Notes datées des passes de travail. Une entrée par session significative,
focus sur ce qui a changé et **pourquoi**, pas sur "comment". Un changement
de code est dans `git` (le futur) ; ici on capture le contexte décisionnel.

---

## 2026-06-15 — Mise sous contrôle de version + armature de projet

**Levier.** L'outil était fonctionnel (32 tests verts) mais vivait **hors
Git**, dans OneDrive — alors que toute la doctrine le présuppose : le JOURNAL
parle de « git (le futur) », le CLAUDE.md exige que « toute règle durable
s'écrive dans le dépôt », le README qualifie les fiches de « versionnables ».
Sans dépôt : aucune historisation, aucun rollback, et un risque réel de
corruption via la synchro OneDrive. C'était le manque n°1, en amont de tout
le reste. Choix : poser l'armature manquante d'un coup plutôt que du code
fonctionnel — la valeur ici est la traçabilité, pas une feature de plus.

**Ce qui a été ajouté / corrigé.**
- `git init` + commit initial (`95b836f`, 449 fichiers suivis).
- `LICENSE` — **GPLv3**, texte officiel verbatim (réutilisé depuis
  `engines/pyromaths/COPYING`). Choix dicté par la vendorisation de Pyromaths
  (GPLv3) dans `engines/` : distribuer l'ensemble sous GPLv3 est le seul choix
  juridiquement sûr. FicheLab déclarait scrupuleusement la licence *des autres*
  (MathALEA AGPL non embarqué) mais n'avait pas la sienne.
- `.gitignore` — `.venv`, caches Python, PDF temporaires, artefacts OneDrive.
- `.gitattributes` — normalisation LF dans le dépôt.
- **Pyromaths réellement vendorisé** : le `.git` imbriqué a été supprimé.
  Avant, `git add` le voyait comme un *gitlink* (`Am engines/pyromaths`) — un
  simple pointeur de sous-module, sans les fichiers. Après suppression :
  **390 fichiers source tracés**. C'est ce qui rend le choix GPLv3 cohérent
  (le code GPL est présent et tracé, pas juste référencé).
- Nettoyage des sauvegardes manuelles `web/*.AVANT-design-web.*` (rôle rendu
  obsolète par Git).
- Dépendance de test déclarée : `requirements-dev.txt` (`pytest>=9.0`,
  installé via `-r requirements.txt`) ; `requirements.txt` et la section
  « Tests » du README pointent désormais dessus, au lieu du `pip install
  pytest` en commentaire.

**Vérification.**
- `pytest backend\tests` : **32 passed** — inchangé avant/après la
  vendorisation (le moteur Pyromaths s'importe et tourne toujours).
- `git ls-files engines/pyromaths` : 390 fichiers (vendorisation réelle, pas
  un gitlink). `git status` : arbre propre.
- `pip install -r requirements-dev.txt --dry-run` : résolu sans conflit.

**Frontière de licence — respectée.** Aucun code MathALEA (AGPL) embarqué.
Pyromaths (GPLv3) est vendorisé *et* la distribution est désormais sous GPLv3,
ce qui lève l'ambiguïté précédente (code GPL présent sans licence déclarée).

**Reste à faire (non bloquant).** Dossier `fonts/` documenté mais absent
(doc ≠ réalité) ; pas de CI (possible maintenant que Git existe, utile si
push distant) ; envisager `pyproject.toml` si la config se densifie.

---

## 2026-06-14 — Bibliothèque d'amorce 6e–3e (16 fiches)

**Levier.** Avant ce passage, FicheLab livrait 2 fiches d'exemple
(`demo-4eme-fractions.json`, `exemple-pyromaths-4e.json`) — l'outil était
techniquement complet mais "vide" d'usage. Choix : pousser le contenu, pas
la robustesse (la chaîne `mathalea.py` est déjà couverte et `latexmk` n'a
pas changé). 1 prof qui ouvre FicheLab après ce passage a 16 fiches prêtes
à imprimer ; c'est de la valeur immédiate.

**Ce qui a été ajouté.**
- `scripts/build_library.py` — scaffold qui décrit la bibliothèque
  ([id, n, uuid, alea] par fiche) et l'écrit dans `fiches/`. Une seule
  source de vérité, ids vérifiés contre `index_titres()` avant écriture,
  garde anti-doublon `uuid` intra-fiche.
- `fiches/` — 16 nouvelles fiches `.json` reproductibles : 4 par niveau
  (6e/5e/4e/3e), 2–4 exercices, 2 colonnes, corrigé activé, vue élève.
  Couvre les chapitres centraux du collège (nombres, calcul littéral,
  fractions, géo, Pythagore, trigo, fonctions, arithmétique, stats).
- `backend/tests/test_bibliotheque.py` — garde-fou qui parcourt
  `fiches/*.json` et vérifie pour chaque fiche : structure minimale, vue
  MathALEA valide, ids présents dans le catalogue, URL d'export se compose
  et contient un bloc `id=` par exercice **dans l'ordre** (`parse_qsl`,
  pas `count`, pour ne pas confondre `id` et `uuid`). Reste valide quand
  une fiche n'a que des exercices Pyromaths.

**Vérification.**
- `pytest backend\tests` : **32 passed in 0.20s** (13 avant, 19 nouveaux
  via paramétrisation sur les fiches livrées).
- `python -m backend.cli build-all fiches\ --no-open` : URL composée pour
  chacune des 18 fiches (16 nouvelles + 2 anciennes), pas d'erreur.

**Suivi de revue (code-reviewer, armoire globale).**
- Collisions `uuid` inter-fiches signalées (`60101`, `60111`) : renommées en
  `6N101`/`6M101`/`6N111`/`6M111` — plus mnémoniques (préfixe = code-thème),
  plus aucune collision.
- Ordre incohérent dans `6eme-perimetres-et-aires` (aires avant
  périmètres alors que le titre dit l'inverse) : inversé.
- Titre `6eme-nombres-entiers-et-decimaux` jugé trompeur (`6N11` est du
  repérage, pas du calcul décimal) : retitré "Nombres entiers, décimaux
  et repérage" (l'ancien fichier orphelin a été supprimé).
- Suggestion non-suivie : splitter la fiche stats 5e en deux niveaux. La
  variété d'un seul fichier (lecture + calcul) reste utile pour une fiche
  de révision ; à revoir si retour terrain négatif.

**Frontière de licence — respectée.** Le scaffold importe uniquement
`backend.catalogue` (lecture du référentiel local) et `backend.mathalea`
(composition d'URLs). Aucun code MathALEA (AGPL) n'a été embarqué.

**Comment ajouter une fiche.**
- Via l'UI : composer → "Enregistrer" → fichier écrit dans `fiches/`.
- À la main : copier un `.json` existant, éditer.
- Reproductible en lot : ajouter une entrée à `LIBRARY` dans
  `scripts/build_library.py` puis relancer `python -m scripts.build_library`.
